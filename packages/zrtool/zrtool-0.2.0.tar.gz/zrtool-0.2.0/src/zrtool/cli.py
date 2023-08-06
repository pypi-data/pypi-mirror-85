# Copyright 2020 Rémy Taymans <remytms@tsmail.eu>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""CLI commands"""

import json
import os
import re
import shutil
import string
import tempfile
from fnmatch import fnmatch
from pathlib import Path

import click
import invoke
import yaml

import zrtool
from zrtool import tool, zrpa

# Context settings
CONTEXT_SETTINGS = {"auto_envvar_prefix": zrtool.PGRNAME.upper()}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=zrtool.__version__)
def main():
    """
    Manage ZoomR project and zrpa achive.

    To get help on a particular command run:

        zrtool COMMAND --help
    """
    invc = invoke.Context()
    result = invc.run(
        "{flacbin} --version".format(flacbin=zrtool.FLACBIN),
        hide=True,
        warn=True,
    )
    if not result.ok:
        click.echo(
            "Warning: {flacbin} cannot be used some functionality will not "
            "work properly.".format(flacbin=zrtool.FLACBIN),
            err=True,
        )


@main.command("archive", short_help="Create zrpa archive")
@click.option(
    "ask_pjtag",
    "--ask-project-tag/--no-project-tag",
    is_flag=True,
    default=False,
    help="Ask tags for the project.",
)
@click.option(
    "ask_ftag",
    "--ask-file-tag/--no-file-tag",
    is_flag=True,
    default=False,
    help="Ask tags for each audio file.",
)
@click.option(
    "compress",
    "--no-compress/--compress",
    is_flag=True,
    default=True,
    help=(
        "Compress means that wav file will be converted into flac file. "
        "By default it's compressed."
    ),
)
@click.option("--keep", "-k", is_flag=True, default=False)
@click.option(
    "metadataname",
    "--metadata",
    type=click.Path(exists=True),
    metavar="METADATAFILE",
    help="Path to a json or yaml file that will be used to read metadata.",
)
@click.argument("pjdir", type=click.Path(exists=True, file_okay=False))
@click.argument("zrpaname", metavar="ZRPA", type=click.Path(dir_okay=False))
@click.pass_context
def archive_cmd(
    ctx, ask_pjtag, ask_ftag, compress, keep, metadataname, pjdir, zrpaname
):
    """
    Create archive named ZRPA from project directory PJDIR.
    """
    pjdirpath = Path(pjdir).expanduser().resolve()
    arcpath = Path(zrpaname).expanduser().resolve()
    # Ensure thate zrpa does not exist
    if arcpath.exists():
        click.confirm(
            "The file '{zrpa}' already exist. "
            "Do you want to overwrite it?".format(zrpa=zrpaname),
            default=False,
            abort=True,
        )
    # Read metadata or create it
    metadata = {"project": {}, "audio": {}}
    if metadataname:
        metadatapath = Path(metadataname).expanduser().resolve()
        if metadatapath.suffix in (".yml", ".yaml"):
            with metadatapath.open("r") as yamlfile:
                metadata = yaml.safe_load(yamlfile.read())
        elif metadatapath.suffix == ".json":
            with metadatapath.open("r") as jsonfile:
                metadata = json.load(jsonfile)
        else:
            ctx.fail("Error: metadata file should be JSON or YAML.")
    # YAML file instruction
    instruction = (
        "# This is a regular yaml file.\n"
        "# Enter one tag per line as follow:\n"
        "# key: value\n"
        "# Example:\n"
        "# name: Name of this song\n"
        "# author: Me\n"
    )
    # Ask for project metadata
    if not metadataname and ask_pjtag:
        pjtag = "# Enter tags for the project\n#\n" + instruction
        pjtag_dict = tool.editmetadata(pjtag)
        metadata["project"] = tool.secure_usertag(pjtag_dict)
    # Ask for each file metadata
    if not metadataname and ask_ftag:
        for file in sorted((pjdirpath / "AUDIO").iterdir()):
            filetag = (
                "# Enter tags for file '{fname}'\n#\n".format(fname=file.name)
                + instruction
            )
            filetag_dict = tool.editmetadata(filetag)
            metadata["audio"][file.name] = tool.secure_usertag(filetag_dict)
    # Create zrpa file
    with zrpa.open(arcpath, mode="w", flac_compression=compress) as zrpafile:
        zrpafile.create(pjdir=pjdirpath)
        zrpafile.metadata = metadata
    # Keep or delete the original file
    if not keep:
        shutil.rmtree(pjdirpath)


@main.command("export", short_help="Export zrpa archive to ZoomR format")
@click.option(
    "--number",
    metavar="N",
    nargs=1,
    type=int,
    help="The number of the project, if not specified it will be "
    "guessed looking at other project in the target directory.",
)
@click.option(
    "--with-tags/--without-tags",
    is_flag=True,
    default=False,
    help="Choose if metadata.json file should be exported or not.",
)
@click.argument("zrpaname", metavar="ZRPA", type=click.Path(dir_okay=False))
@click.argument(
    "targetdir",
    type=click.Path(exists=True, file_okay=False),
    required=False,
    default=".",
)
@click.pass_context
def export_cmd(ctx, number, with_tags, targetdir, zrpaname):
    """
    Export archive named ZRPA to a PROJNNN directory located in the
    current directory or if specified in target directory TARGETDIR.
    """
    # Define target directory
    targetdirpath = Path(targetdir).expanduser().resolve()
    # Define project name
    if not number:
        # Guess project name from taget directory
        number = 0
        for file in targetdirpath.iterdir():
            match = re.match(r"PROJ(?P<nb>\d{3})", file.name.upper())
            if match and int(match.group("nb")) >= number:
                number = int(match.group("nb")) + 1
    pjname = "PROJ{:03d}".format(number)
    pjdirpath = targetdirpath / pjname
    # Extract zrpa file
    try:
        with zrpa.open(zrpaname, mode="r") as zrpafile:
            zrpafile.export(pjdir=pjdirpath, with_tags=with_tags)
    except FileExistsError as err:
        ctx.fail(err)


@main.command("extract", short_help="Extract files from the archive.")
@click.option(
    "directory",
    "--directory",
    "-d",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, writable=True
    ),
    metavar="DIRECTORY",
    default=".",
    help="Directory to extract file in.",
)
@click.argument(
    "zrpaname",
    metavar="ZRPA",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument("patterns", nargs=-1)
def extract_cmd(zrpaname, directory, patterns):
    """
    Extract files that match PATTERNS if any. The files are extracted to
    the current directory or to DIRECTORY if specified.
    """
    if not patterns:
        patterns = ("*",)
    with zrpa.open(zrpaname, mode="r") as zrpafile:
        for name in zrpafile.names():
            for pattern in patterns:
                if fnmatch(name, pattern):
                    zrpafile.extract(name, path=directory)
                    break


@main.command("file", short_help="Add or update files to the archive.")
@click.option(
    "update",
    "--update",
    is_flag=True,
    default=False,
    help="Update the file if it already exists.",
)
@click.option(
    "dest",
    "--dest",
    metavar="DEST",
    default="",
    help="Destination directory in the archive.",
)
@click.argument(
    "zrpaname",
    metavar="ZRPA",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "files",
    nargs=-1,
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
)
@click.pass_context
def file_cmd(ctx, zrpaname, update, dest, files):
    """
    Add FILES to the ZRPA archive or update FILES in the ZRPA archive.
    """
    paths = [Path(file) for file in files]
    if not paths:
        ctx.exit()
    destpath = Path(dest)
    audiopath = Path("AUDIO")
    # Check that files does not already exist if --update not given
    if not update:
        with zrpa.open(zrpaname, mode="r") as zrpafile:
            for path in paths:
                if path.suffix.lower() == ".wav" and not dest:
                    if str(audiopath / path.name) in zrpafile.names():
                        ctx.fail(
                            "File '{}' already exists in archive.".format(
                                audiopath / path.name
                            )
                        )
                else:
                    if str(destpath / path.name) in zrpafile.names():
                        ctx.fail(
                            "File '{}' already exists in archive.".format(
                                destpath / path.name
                            )
                        )
    # Add or update files
    with zrpa.open(zrpaname, mode="a") as zrpafile:
        for path in paths:
            if path.suffix.lower() == ".wav" and not dest:
                zrpafile.add(path, arcname=audiopath / path.name)
            else:
                zrpafile.add(path, arcname=destpath / path.name)


@main.command("files", short_help="List content of a zrpa archive")
@click.argument(
    "zrpaname",
    metavar="ZRPA",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument("patterns", nargs=-1)
def files_cmd(zrpaname, patterns):
    """
    List content of the archive named ZRPA. If PATTERNS is given, list
    only content of the archive that matches at least one of the
    PATTERNS.
    """
    if not patterns:
        patterns = ("*",)
    with zrpa.open(zrpaname, mode="r") as zrpafile:
        for name in zrpafile.names():
            for pattern in patterns:
                if fnmatch(name, pattern):
                    click.echo(
                        name + os.sep
                        if zrpafile.member(name).isdir()
                        else name
                    )
                    break


@main.command("get", short_help="Extract audio files from the archive.")
@click.option(
    "directory",
    "--directory",
    "-d",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, writable=True
    ),
    metavar="DIRECTORY",
    default=".",
    help="Directory to extract file in.",
)
@click.option(
    "fmt",
    "--format",
    type=click.Choice(["wav", "flac"]),
    default="flac",
    show_default=True,
    help="Format of the extracted file.",
)
@click.option(
    "name",
    "--name",
    help="""Pattern for the name of the output file. Tags of the file
    should be used with brackets.
    E.g. '$title - $author.flac'""",
)
@click.argument(
    "zrpaname",
    metavar="ZRPA",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument("audiofiles", required=True, nargs=-1)
@click.pass_context
def get_cmd(ctx, zrpaname, directory, fmt, name, audiofiles):
    """
    Extract AUDIOFILES to the current directory or to DIRECTORY if
    specified. AUDIOFILES can be converted with the --format option.

    The name of the output files can be controlled with the --name
    option that read archive metadata.
    By default, the name of the file will be based on the '_filename'
    tag for the file in the archive.
    """
    directory = Path(directory)
    # Check that audiofiles exists in the archive
    audiofileinfos = []
    for audiofile in audiofiles:
        with zrpa.open(zrpaname, mode="r") as zrpafile:
            zrpa_audiofile = [
                name for name in zrpafile.names() if name.startswith("AUDIO/")
            ]
            if audiofile in zrpa_audiofile:
                audiofileinfos.append({"arcname": Path(audiofile)})
            elif "AUDIO/" + audiofile in zrpa_audiofile:
                audiofileinfos.append({"arcname": Path("AUDIO/" + audiofile)})
            else:
                ctx.fail(
                    "File '{}' not found in AUDIO directory of the "
                    "archive.".format(audiofile)
                )
    # Get new names
    with zrpa.open(zrpaname, mode="r") as zrpafile:
        audiotags = zrpafile.metadata["audio"]
        for audiofileinfo in audiofileinfos:
            if name:
                if audiofileinfo["arcname"].name not in audiotags:
                    ctx.fail(
                        "No tags for file '{}'.".format(
                            audiofileinfo["arcname"].name
                        )
                    )
                try:
                    audiofileinfo["name"] = Path(
                        string.Template(name).substitute(
                            zrpafile.metadata["audio"][
                                audiofileinfo["arcname"].name
                            ]
                        )
                    )
                except ValueError as err:
                    ctx.fail("Invalid --name value: {}.".format(err))
                except KeyError as err:
                    ctx.fail(
                        "Tag {} not found for file '{}'.".format(
                            str(err), audiofileinfo["arcname"].name
                        )
                    )
            elif (
                audiofileinfo["arcname"].name in audiotags
                and "_filename" in audiotags[audiofileinfo["arcname"].name]
            ):
                audiofileinfo["name"] = Path(
                    audiotags[audiofileinfo["arcname"].name]["_filename"]
                )
            else:
                audiofileinfo["name"] = Path(audiofileinfo["arcname"].name)
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdirpath = Path(tmpdirname)
        for audiofileinfo in audiofileinfos:
            if fmt == "wav":
                extractedpath = tmpdirpath / audiofileinfo["arcname"]
            else:
                extractedpath = (
                    tmpdirpath
                    / audiofileinfo["arcname"].parent
                    / (audiofileinfo["arcname"].name + ".flac")
                )
            with zrpa.open(zrpaname, mode="r") as zrpafile:
                zrpafile.extract(
                    str(audiofileinfo["arcname"]),
                    path=tmpdirpath,
                    decompress=fmt == "wav",
                )
            extractedpath.rename(directory / audiofileinfo["name"])


@main.command("tags", short_help="Show metadata of an archive.")
@click.option(
    "project",
    "--project",
    is_flag=True,
    default=False,
    help="Show only metadata of the project. Can be combined with "
    "--file to also show some file metadata.",
)
@click.option(
    "files",
    "--file",
    metavar="FILE",
    multiple=True,
    help="Show only metadata of FILE. Can be combined with --project.",
)
@click.option(
    "keyarg",
    "--key",
    metavar="KEY",
    help="Show the value for a given KEY. --project or --file must be "
    "used with this option.",
)
@click.argument(
    "zrpaname",
    metavar="ZRPA",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.pass_context
def tags_cmd(ctx, zrpaname, project, files, keyarg):
    """
    Show metadata of the archive ZRPA.
    """
    # Check files
    if files:
        with zrpa.open(zrpaname, mode="r") as zrpafile:
            for file in files:
                if file not in zrpafile.metadata["audio"]:
                    ctx.fail(
                        "file '{}' does not exist in metadata.".format(file)
                    )
    # Checks for key
    if keyarg and not project and not files:
        ctx.fail(
            "--key can not be used without using --project or --file opitons."
        )
    if keyarg and len(files) > 1:
        ctx.fail("--key can not be used with multiple --file options.")
    if keyarg and project:
        with zrpa.open(zrpaname, mode="r") as zrpafile:
            if keyarg in zrpafile.metadata["project"]:
                click.echo(zrpafile.metadata["project"][keyarg])
                ctx.exit()
            else:
                ctx.fail(
                    "key '{}' does not exist in project metadata.".format(
                        keyarg
                    )
                )
    if keyarg and files:
        with zrpa.open(zrpaname, mode="r") as zrpafile:
            if keyarg in zrpafile.metadata["audio"][files[0]]:
                click.echo(zrpafile.metadata["audio"][files[0]][keyarg])
                ctx.exit()
            else:
                ctx.fail(
                    "key '{key}' does not exist in '{file}' metadata.".format(
                        key=keyarg, file=files[0]
                    )
                )
    # Show if key not specified
    print_project = project or (not project and not files)
    print_files = files or (not project and not files)
    with zrpa.open(zrpaname, mode="r") as zrpafile:
        if print_project:
            for key, val in zrpafile.metadata["project"].items():
                click.echo("{key}: {val}".format(key=key, val=val))
        if print_files:
            for file, tags in zrpafile.metadata["audio"].items():
                if file in files or not files:
                    if print_project:
                        click.echo("  ", nl=False)
                    click.echo("{file}:".format(file=file))
                    for key, val in tags.items():
                        if print_project:
                            click.echo("    ", nl=False)
                        else:
                            click.echo("  ", nl=False)
                        click.echo("{key}: {val}".format(key=key, val=val))
