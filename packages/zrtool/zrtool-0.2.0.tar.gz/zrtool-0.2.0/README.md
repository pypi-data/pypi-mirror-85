[![pipeline status](https://gitlab.com/remytms/zrtool/badges/master/pipeline.svg)](https://gitlab.com/remytms/zrtool/pipelines)
[![coverage report](https://gitlab.com/remytms/zrtool/badges/master/coverage.svg)](https://gitlab.com/remytms/zrtool/pipelines)

zrtool
======

zrtool is a little cli tool that let you do some actions on a ZoomR16
project. For now, you can backup a project in a compressed format, and
extract any data you need from it. You can also get the original
uncompressed project if you want to restore a backuped project into you
ZoomR16 device.


Installation
------------

zrtool need a proper installation of `flac`
(https://www.xiph.org/flac/) to work. The flac encoder and decoder is
available on most platform, e.g. `apt install flac` for debian based OS.

zrtool will try to use the `flac` command line. If the `flac` binary is
not accessible from your PATH, it can be specified with the
`ZRTOOL_FLAC_BIN` environnement.

The recommended way to install zrtool is by using `pipx`:

```sh
pipx install zrtool
```

If you don't want to install `pipx` to manage python cli tools
installation, zrtool can also be installed with pip:

```sh
pip install zrtool
```


Usage example
-------------

**All this options are not yet available. They will be included in
version 1.0.0. To see what's already implemented refer to the CHANGES
document.**

Backup a project under the zrpa format.
```sh
$ zrtool archive [--compress|--no-compress] PRJ000/ project-000.zrpa
```

Convert back to the original format.
```sh
$ zrtool export [--number N] project-000.zrpa [foo/]
```
It will create a directory `PROJ000` in the foo directory. If foo is not
specified, create `PROJ000` in the current directory. Number is
optional, if not given the number of the project is determined by the
project that can be found in the target directory. If specified this
number is used to define the name of the project directory.


### Search

Search based on metadata.
```sh
$ zrtool filter \
    [--not] \
    --zprop "name" "Test" \
    --zprop-track "fader" 80 1 \
    --tag "title" ".*song" \
    --tag-file "title" ".*song" "MONO-000" \
    [--recursive] \
    [directory/...]
path/to/archive.zrpa
path/to/other-archive.zrpa
```
Return the path of zrpa archive that match at least one of the given tag
or zprop. It get archive from directory if given, else it reads path
from stdin.
Filter can be piped to each other to perform "and" filter and more
complex search.


### Metadata

Show metadata of a zrpa archive.
```sh
$ zrtool tags project-000.zrpa
title: Song title
author: Band name
date: 2020-02-29
  MONO-000.WAV:
    author: Someone
    instrument: Guitar
    comment: Recorded with simple microphone
  MASTR000.WAV:
    comment: First mix done. Needs to be improved
$ zrtool tags --project project-000.zrpa
title: Song title
author: Band name
date: 2020-02-29
$ zrtool tags --file MONO-000.WAV project-000.zrpa
MONO-000.WAV:
  author: Someone
  instrument: Guitar
  comment: Recorded with simple microphone
$ zrtool tags --project --key title project-000.zrpa
Song title
$ zrtool tags --file MONO-000.WAV --key instrument project-000.zrpa
guitar
```

Add a new key and value to a project.
```sh
$ zrtool tag [--update] --key-value Take 0 project-000.zrpa
$ zrtool tag [--update] --key-value Author Someone --file MONO-000 project-000.zrpa
```

Edit an existing metadata of a project.
```sh
$ zrtool tag --key Title project-000.zrpa
$ zrtool tag --key Instrument --file MONO-000 project-000.zrpa
$ zrtool project-000.zrpa metadata rename-key Author Artist
```

Rename an existing key.
```sh
$ zrtool tag --rename-key Author Artist project-000.zrpa
$ zrtool tag --rename-key Author Artist --file MONO-000 project-000.zrpa
```

Delete an existing tag.
```sh
$ zrtool rmtag --key Title project-000.zrpa
$ zrtool rmtag --key Title --file MONO-000 project-000.zrpa
```


### Files

List archive content.
```sh
$ zrtool files project-000.zrpa
AUDIO/
AUDIO/MASTR000.WAV
AUDIO/MONO-000.WAV
AUDIO/MONO-001.WAV
AUDIO/MONO-002.WAV
AUDIO/MONO-003.WAV
AUDIO/MONO-004.WAV
AUDIO/MONO-005.WAV
EFXDATA.ZDT
metadata.json
PRJDATA.ZDT
$ zrtool files project-000.zrpa AUDIO
AUDIO/
AUDIO/MASTR000.WAV
AUDIO/MONO-000.WAV
AUDIO/MONO-001.WAV
AUDIO/MONO-002.WAV
AUDIO/MONO-003.WAV
AUDIO/MONO-004.WAV
AUDIO/MONO-005.WAV
$ zrtool files project-000.zrpa AUDIO/*
AUDIO/MASTR000.WAV
AUDIO/MONO-000.WAV
AUDIO/MONO-001.WAV
AUDIO/MONO-002.WAV
AUDIO/MONO-003.WAV
AUDIO/MONO-004.WAV
AUDIO/MONO-005.WAV
$ zrtool files project-000.zrpa AUDIO/* *.ZDT
AUDIO/MASTR000.WAV
AUDIO/MONO-000.WAV
AUDIO/MONO-001.WAV
AUDIO/MONO-002.WAV
AUDIO/MONO-003.WAV
AUDIO/MONO-004.WAV
AUDIO/MONO-005.WAV
EFXDATA.ZDT
PRJDATA.ZDT
```

Extract a file from an archive.
```sh
$ zrtool extract [--directory foo/] project-000.zrpa AUDIO/* *.ZDT
```

Extract **audio** files from an archive.
```sh
$ zrtool get \
    --format {flac|vorbis|mp3|wav} \
    [--directory foo/]
    [--name '${title} - ${author}.ogg'] \
    project-000.zrpa MASTR000...
```

Add audio file to an archive. File are added to the root of the archive,
except audio file that are added to the audio directory. If `--dest
DEST` option is given, `DEST` is created in the archive starting from
the root and files are added in this directory. It prevent from
overwriting metadata file with a non-conform metadata file.
```sh
$ zrtool file [--update] [--dest AUDIO] project-000.zrpa music.wav
$ zrtool file [--update] project-000.zrpa note.txt
```

Remove a file from an archive. Some integrity checks needs to be done.
```sh
$ zrtool rmfile project-000.zrpa AUDIO/MONO-000.WAV...
```


### Project data

Read project data in the `PRJDATA.ZDT` file.
```sh
$ zrtool zprops project-000.zrpa
name: PROJ000
...
$ zrtool zprops --track 1 project-000.zrpa
file: MONO-000.WAV
fader: 80
...
$ zrtool zprops --key name project-000.zrpa
PROJ000
```

Edit project data.
```sh
$ zrtool zprop --key-value name "MYPROJ" project-000.zrpa
$ zrtool zprop --key-value file MASTR000.WAV --track 1 project-000.zrpa
$ zrtool zprop --key File --track 1 project-000.zrpa
```
