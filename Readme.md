Qiita Utility Programs
==================================================================================

qiita-item.py
----------------------------------------------------------------------------------

```console
./qiita-item.py  --help
usage: qiita-item.py [-h] [-n] [--json] [--post] [--patch PATCH] [--get GET] [-N TITLE] [-T TAGS] [-d DEBUG]
                     [--private | --public] [--with_title | --without_title]
                     [file_name]

Qiita Post/Patch/Get Itme

positional arguments:
  file_name             Markdown File Name

optional arguments:
  -h, --help            show this help message and exit
  -n, --dry_run         Dry Run
  --json                Output result in json
  --post                Post Item
  --patch PATCH         Patch user_id
  --get GET             Get user_id
  -N TITLE, --title TITLE
                        Qiita Title
  -T TAGS, --tags TAGS  Qiita Tags
  -d DEBUG, --debug DEBUG
                        debug mode
  --private             Set private=true
  --public              Set private=false
  --with_title          Title is included the Markdown File. Post text without title.
  --without_title       Title is not included the Markdown File. Post text as is.
```

qiita-image-upload.py
----------------------------------------------------------------------------------

```console
shell$ ./qiita-image-upload.py --help
usage: qiita-image-upload.py [-h] [-N NAME] [-T TYPE] [-d DEBUG] [--json] file_name

Qiita Image Uploader

positional arguments:
  file_name             Image File Name

optional arguments:
  -h, --help            show this help message and exit
  -N NAME, --name NAME  Image Name
  -T TYPE, --type TYPE  Image Type
  -d DEBUG, --debug DEBUG
                        debug mode
  --json                Output result in json
```
