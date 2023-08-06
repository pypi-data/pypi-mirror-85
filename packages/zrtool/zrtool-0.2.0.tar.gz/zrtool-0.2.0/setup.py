# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zrtool']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3,<6.0', 'click>=7.0,<8.0', 'invoke>=1.3,<2.0']

entry_points = \
{'console_scripts': ['zrtool = zrtool.cli:main']}

setup_kwargs = {
    'name': 'zrtool',
    'version': '0.2.0',
    'description': 'CLI tool to deal with ZoomR16 project',
    'long_description': '[![pipeline status](https://gitlab.com/remytms/zrtool/badges/master/pipeline.svg)](https://gitlab.com/remytms/zrtool/pipelines)\n[![coverage report](https://gitlab.com/remytms/zrtool/badges/master/coverage.svg)](https://gitlab.com/remytms/zrtool/pipelines)\n\nzrtool\n======\n\nzrtool is a little cli tool that let you do some actions on a ZoomR16\nproject. For now, you can backup a project in a compressed format, and\nextract any data you need from it. You can also get the original\nuncompressed project if you want to restore a backuped project into you\nZoomR16 device.\n\n\nInstallation\n------------\n\nzrtool need a proper installation of `flac`\n(https://www.xiph.org/flac/) to work. The flac encoder and decoder is\navailable on most platform, e.g. `apt install flac` for debian based OS.\n\nzrtool will try to use the `flac` command line. If the `flac` binary is\nnot accessible from your PATH, it can be specified with the\n`ZRTOOL_FLAC_BIN` environnement.\n\nThe recommended way to install zrtool is by using `pipx`:\n\n```sh\npipx install zrtool\n```\n\nIf you don\'t want to install `pipx` to manage python cli tools\ninstallation, zrtool can also be installed with pip:\n\n```sh\npip install zrtool\n```\n\n\nUsage example\n-------------\n\n**All this options are not yet available. They will be included in\nversion 1.0.0. To see what\'s already implemented refer to the CHANGES\ndocument.**\n\nBackup a project under the zrpa format.\n```sh\n$ zrtool archive [--compress|--no-compress] PRJ000/ project-000.zrpa\n```\n\nConvert back to the original format.\n```sh\n$ zrtool export [--number N] project-000.zrpa [foo/]\n```\nIt will create a directory `PROJ000` in the foo directory. If foo is not\nspecified, create `PROJ000` in the current directory. Number is\noptional, if not given the number of the project is determined by the\nproject that can be found in the target directory. If specified this\nnumber is used to define the name of the project directory.\n\n\n### Search\n\nSearch based on metadata.\n```sh\n$ zrtool filter \\\n    [--not] \\\n    --zprop "name" "Test" \\\n    --zprop-track "fader" 80 1 \\\n    --tag "title" ".*song" \\\n    --tag-file "title" ".*song" "MONO-000" \\\n    [--recursive] \\\n    [directory/...]\npath/to/archive.zrpa\npath/to/other-archive.zrpa\n```\nReturn the path of zrpa archive that match at least one of the given tag\nor zprop. It get archive from directory if given, else it reads path\nfrom stdin.\nFilter can be piped to each other to perform "and" filter and more\ncomplex search.\n\n\n### Metadata\n\nShow metadata of a zrpa archive.\n```sh\n$ zrtool tags project-000.zrpa\ntitle: Song title\nauthor: Band name\ndate: 2020-02-29\n  MONO-000.WAV:\n    author: Someone\n    instrument: Guitar\n    comment: Recorded with simple microphone\n  MASTR000.WAV:\n    comment: First mix done. Needs to be improved\n$ zrtool tags --project project-000.zrpa\ntitle: Song title\nauthor: Band name\ndate: 2020-02-29\n$ zrtool tags --file MONO-000.WAV project-000.zrpa\nMONO-000.WAV:\n  author: Someone\n  instrument: Guitar\n  comment: Recorded with simple microphone\n$ zrtool tags --project --key title project-000.zrpa\nSong title\n$ zrtool tags --file MONO-000.WAV --key instrument project-000.zrpa\nguitar\n```\n\nAdd a new key and value to a project.\n```sh\n$ zrtool tag [--update] --key-value Take 0 project-000.zrpa\n$ zrtool tag [--update] --key-value Author Someone --file MONO-000 project-000.zrpa\n```\n\nEdit an existing metadata of a project.\n```sh\n$ zrtool tag --key Title project-000.zrpa\n$ zrtool tag --key Instrument --file MONO-000 project-000.zrpa\n$ zrtool project-000.zrpa metadata rename-key Author Artist\n```\n\nRename an existing key.\n```sh\n$ zrtool tag --rename-key Author Artist project-000.zrpa\n$ zrtool tag --rename-key Author Artist --file MONO-000 project-000.zrpa\n```\n\nDelete an existing tag.\n```sh\n$ zrtool rmtag --key Title project-000.zrpa\n$ zrtool rmtag --key Title --file MONO-000 project-000.zrpa\n```\n\n\n### Files\n\nList archive content.\n```sh\n$ zrtool files project-000.zrpa\nAUDIO/\nAUDIO/MASTR000.WAV\nAUDIO/MONO-000.WAV\nAUDIO/MONO-001.WAV\nAUDIO/MONO-002.WAV\nAUDIO/MONO-003.WAV\nAUDIO/MONO-004.WAV\nAUDIO/MONO-005.WAV\nEFXDATA.ZDT\nmetadata.json\nPRJDATA.ZDT\n$ zrtool files project-000.zrpa AUDIO\nAUDIO/\nAUDIO/MASTR000.WAV\nAUDIO/MONO-000.WAV\nAUDIO/MONO-001.WAV\nAUDIO/MONO-002.WAV\nAUDIO/MONO-003.WAV\nAUDIO/MONO-004.WAV\nAUDIO/MONO-005.WAV\n$ zrtool files project-000.zrpa AUDIO/*\nAUDIO/MASTR000.WAV\nAUDIO/MONO-000.WAV\nAUDIO/MONO-001.WAV\nAUDIO/MONO-002.WAV\nAUDIO/MONO-003.WAV\nAUDIO/MONO-004.WAV\nAUDIO/MONO-005.WAV\n$ zrtool files project-000.zrpa AUDIO/* *.ZDT\nAUDIO/MASTR000.WAV\nAUDIO/MONO-000.WAV\nAUDIO/MONO-001.WAV\nAUDIO/MONO-002.WAV\nAUDIO/MONO-003.WAV\nAUDIO/MONO-004.WAV\nAUDIO/MONO-005.WAV\nEFXDATA.ZDT\nPRJDATA.ZDT\n```\n\nExtract a file from an archive.\n```sh\n$ zrtool extract [--directory foo/] project-000.zrpa AUDIO/* *.ZDT\n```\n\nExtract **audio** files from an archive.\n```sh\n$ zrtool get \\\n    --format {flac|vorbis|mp3|wav} \\\n    [--directory foo/]\n    [--name \'${title} - ${author}.ogg\'] \\\n    project-000.zrpa MASTR000...\n```\n\nAdd audio file to an archive. File are added to the root of the archive,\nexcept audio file that are added to the audio directory. If `--dest\nDEST` option is given, `DEST` is created in the archive starting from\nthe root and files are added in this directory. It prevent from\noverwriting metadata file with a non-conform metadata file.\n```sh\n$ zrtool file [--update] [--dest AUDIO] project-000.zrpa music.wav\n$ zrtool file [--update] project-000.zrpa note.txt\n```\n\nRemove a file from an archive. Some integrity checks needs to be done.\n```sh\n$ zrtool rmfile project-000.zrpa AUDIO/MONO-000.WAV...\n```\n\n\n### Project data\n\nRead project data in the `PRJDATA.ZDT` file.\n```sh\n$ zrtool zprops project-000.zrpa\nname: PROJ000\n...\n$ zrtool zprops --track 1 project-000.zrpa\nfile: MONO-000.WAV\nfader: 80\n...\n$ zrtool zprops --key name project-000.zrpa\nPROJ000\n```\n\nEdit project data.\n```sh\n$ zrtool zprop --key-value name "MYPROJ" project-000.zrpa\n$ zrtool zprop --key-value file MASTR000.WAV --track 1 project-000.zrpa\n$ zrtool zprop --key File --track 1 project-000.zrpa\n```\n',
    'author': 'Rémy Taymans',
    'author_email': 'remytms@tsmail.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/remytms/zrtool',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
