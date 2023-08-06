# BOMIST Utilities

Things you can do with it:

- Convert legacy workspaces into BOMIST v2 workspaces

## How to install

This requires Python 3 and the Python Package Installer (pip3) to be installed.
You can download it here:
https://www.python.org/downloads/

Once you have them installed, run the following command on your terminal:

```
$ pip3 install bomist_utils
```

After installing `bomist_utils` through `pip3` you'll end up with it available on your terminal.

On Windows you might have to re-launch your terminal in order for the `bomist_utils` command to be recognized.

To make sure it was properly installed run the following command:

```
$ bomist_utils --help
```

You should see the available options.

## Usage

## Convert legacy workspaces

```
$ bomist_utils --dump1 --ws <wspath> [--out <outpath>]
```

`wspath` is the path of the workspace you want to dump. A `.ws` file must exist in it.

A `legacy.bomist_dump` file will be created on `outpath` or in the folder the command was called from if the `--out` option is not used. This file can then be imported by BOMIST v2.

### Limitations

At the moment this utility can only convert and keep data connections between:

```
parts, documents, labels, storage, categories
```

Projects, orders and history won't be preserved.

Need help? [Get in touch](https://bomist.com/support/contact/)

---

For more info: [bomist.com](https://bomist.com)
