"""
BOMIST Utilities (bomist.com)
"""

import json
import shutil
import tarfile
import re
from os import path, getcwd, listdir, makedirs

from .crypto import decode
from .v2 import (create_doc, create_tree_node, create_tree,
                 create_safe_id, generate_random_id, safe_id_str)


def dump1(wspath, outpath=None):
    print(f"Dumping {wspath}")
    if not _check_if_ws_exits(wspath):
        print("ERROR", f"workspace not found at {wspath}",)
        return

    datapath = path.join(wspath, "data")

    all_docs = []

    storage_mapper = {}
    labels_mapper = {}
    category_mapper = {}
    docs_mapper = {}  # ref -> id
    files_mapper = {}  # file_main -> id

    with open(path.join(datapath, ".labels"), "rb") as f:
        d = json.loads(decode(f.read()))
        plabels = d.get("labels", [])
        nodes = []
        for plabel in plabels:
            pname = plabel.get("name")
            pnode = create_tree_node("label", pname)
            k = pname
            labels_mapper[k] = pnode['id']
            child_nodes = []
            for slabel in plabel.get("sub", []):
                sname = slabel.get('name')
                snode = create_tree_node(
                    "label", sname, pnode['id'])
                child_nodes.append(snode)
                k = "\t".join([pname, sname])
                labels_mapper[k] = snode['id']
            pnode['childNodes'] = child_nodes
            nodes.append(pnode)

        labels_tree_doc = create_doc("tree", create_tree("labels", nodes))
        all_docs += [labels_tree_doc]

    with open(path.join(datapath, ".storage"), "rb") as f:
        d = json.loads(decode(f.read()))
        [tree_doc, storage_docs, mapper] = _create_storage(d)
        storage_mapper = mapper
        all_docs += [tree_doc] + storage_docs

    with open(path.join(datapath, ".categories"), "rb") as f:
        category_docs = []
        d = json.loads(decode(f.read()))
        categories = d["categories"]
        for c in categories:
            doc = create_doc("category", {
                'name': c
            })
            category_mapper[c] = doc['_id']
            category_docs.append(doc)
        all_docs += category_docs

    docpaths = listdir(path.join(datapath, "files"))
    for docpath in docpaths:
        doc_docs = []
        with open(path.join(datapath, "files", docpath, ".doc"), "rb") as f:
            d = json.loads(decode(f.read()))
            doc = create_doc("document", {})
            ext = path.splitext(d['file_main'])[1]
            fpath = f"{safe_id_str(doc['_id'])}{ext}"
            doc.update({
                'document': {
                    'name': d['title'],
                    'notes': d['notes'],
                    'category': category_mapper.get(d['category'], "") if d['category'] else "",
                    'path': {
                        'local': fpath
                    }
                }
            })
            k = d['ref']
            docs_mapper[k] = doc['_id']
            k = d['file_main']
            files_mapper[k] = fpath
            doc_docs.append(doc)
        all_docs += doc_docs

    partpaths = listdir(path.join(datapath, "parts"))
    for partpath in partpaths:
        part_docs = []
        with open(path.join(datapath, "parts", partpath, ".part"), "rb") as f:
            d = json.loads(decode(f.read()))

            label_k = "\t".join([d['plabel'], d['slabel']])
            label = labels_mapper.get(label_k, "") if label_k else ""

            storage_k = d['storage']
            storage = storage_mapper.get(storage_k) if storage_k else ""

            re_tolerance = re.compile(
                "([0-9.,]+)\s*(?=%|ppm)").findall(d['value'] or "")
            tolerance = int(re_tolerance[0]) if len(re_tolerance) > 0 else None

            part = {
                'id': create_safe_id("part", f"{d['mpn']}_{d['brand']}"),
                'type': "outsourced",
                'mpn': d['mpn'],
                'manufacturer': d['brand'],
                'description': d['desc'],
                'value': d['value'],
                'package': d['package'],
                'tolerance': tolerance,
                'label': label,
                'stock': int(d['stock']),
                'stockInHouse': int(d['stock']),
                'lowStock': int(d['stock_low']),
                'notes': d['notes'],
                'hidden': bool(d.get('obsolete', False) or d['stock_ignore'])
            }
            doc = create_doc("part", part)

            inventory_doc = create_doc("inventory", {
                'id': f"r/{part['id']}:{generate_random_id('inventory')}",
                'status': 'in_house',
                'storage': storage,
                'qty': int(d['stock'])
            })

            if d['docs']:
                for ref in d['docs']:
                    doc_id = docs_mapper.get(ref)
                    ref_doc = create_doc("ref", {
                        'id': f"r/{part['id']}:{doc_id}",
                        'refId': doc_id
                    })
                    part_docs += [ref_doc]

            part_docs += [doc, inventory_doc]

        all_docs += part_docs

    outpath = outpath or getcwd()

    tmp_dir = path.join(outpath, ".tmp")
    dump_dir = path.join(tmp_dir, "dump-data")
    files_dir = path.join(dump_dir, "files")

    makedirs(files_dir, exist_ok=True)
    makedirs(outpath, exist_ok=True)

    with open(path.join(dump_dir, "allDocs.json"), "w") as f:
        rows = list(map(lambda d: dict({
            'doc': d
        }), all_docs))
        all_docs = {
            'total_rows': len(all_docs),
            'rows': rows
        }
        f.write(json.dumps(all_docs, indent=2))

    docpaths = listdir(path.join(datapath, "files"))
    for docpath in docpaths:
        filepaths = listdir(path.join(datapath, "files", docpath))
        for filepath in filepaths:
            if filepath in files_mapper.keys():
                fsrc = path.join(datapath, "files", docpath, filepath)
                fdst = path.join(files_dir, files_mapper.get(filepath))
                shutil.copy2(fsrc, fdst)

    tarfilename = "legacy.bomist_dump"
    tarpath = path.join(outpath, tarfilename)
    with tarfile.open(tarpath, "w:gz") as tar:
        tar.add(dump_dir, arcname="dump-data")

    shutil.rmtree(tmp_dir)

    print(f"{tarfilename} created")


def _create_storage(storage):
    mapper = {}
    storage_docs = []

    def _for_each_storage(storage, parent=None, parent_path=None):
        nodes = []
        for s in storage:
            values = s.get('data', [])
            name = values[0]
            spath = (parent_path or []) + [name]
            node = create_tree_node("storage", name, parent)
            k = "\t".join(spath)
            mapper[k] = node['id']
            sdoc = create_doc("storage", {'name': name})
            storage_docs.append(sdoc)
            node['childNodes'] = _for_each_storage(
                s.get('children', []), node['id'], spath)
            nodes.append(node)
        return nodes

    tree_nodes = _for_each_storage(storage, None)
    storage_tree_doc = create_doc("tree", create_tree("storage", tree_nodes))
    return [storage_tree_doc, storage_docs, mapper]


def _check_if_ws_exits(wspath):
    wsfile = ".ws"
    wspath = path.join(wspath, wsfile)
    return path.isfile(wspath)
