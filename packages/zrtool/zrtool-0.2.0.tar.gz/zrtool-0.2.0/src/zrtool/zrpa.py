# Copyright 2020 Rémy Taymans <remytms@tsmail.eu>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""ZRPA lib"""

import io
import json
import lzma
import tarfile
import time
from pathlib import Path
from tempfile import TemporaryDirectory

import invoke

from zrtool import FLACBIN


# pylint: disable=redefined-builtin
def open(filename, mode="r", flac_compression=True):
    """Open a ZRPA archive and return an ZRPAFile object."""
    return ZRPAFile(filename, mode=mode, flac_compression=flac_compression)


class ZRPAFile:
    """A ZRPA archive"""

    def __init__(self, filename, mode="r", flac_compression=True):
        """
        Create a ZRPA archive. If filename already exists it open the
        archive. If filename does not exists it opens an empty file.
        """
        self._mode = mode
        self._filename = Path(filename)
        self._flac_compression = flac_compression
        self.metadata = self._readmetadata()
        self.tarfile = tarfile.open(filename, mode)

    def close(self):
        """Close the ZRPA archive"""
        if self._mode in "wax":
            self._writemetadata()
        self.tarfile.close()

    def member(self, name):
        """
        Return a TarInfo file of the corresponding name. name should
        be listed by names(). Raise KeyError in name is not found in the
        archive.
        """
        name = str(name)
        rawnames = self.tarfile.getnames()
        flacname = name + ".flac"
        xzname = name + ".xz"
        if flacname in rawnames:
            return self.tarfile.getmember(flacname)
        if xzname in rawnames:
            return self.tarfile.getmember(xzname)
        return self.tarfile.getmember(name)

    def names(self):
        """
        Return a list of the filenames of file in the archive.
        Names are sorted, and duplicates are removed. Also the
        compression extension is removed.
        """
        rawnames = set(self.tarfile.getnames())
        names = set()
        for name in rawnames:
            if name.endswith(".flac"):
                names.add(name[:-5])
            elif name.endswith(".xz"):
                names.add(name[:-3])
            else:
                names.add(name)
        return list(sorted(names))

    def extract(self, member, path=".", decompress=True):
        """
        Extract member from the archive to path. member should be a
        element of names() or an TarInfo object.
        """
        if not isinstance(member, tarfile.TarInfo):
            member = self.member(member)
        self.tarfile.extract(member, path=path)
        if decompress:
            invc = invoke.Context()
            file = Path(path) / Path(member.name)
            if file.suffix.lower() == ".flac":
                newfile = file.with_suffix("")
                invc.run(
                    (
                        "{flacbin} "
                        "--decode "
                        "--totally-silent "
                        "--keep-foreign-metadata "
                        "--output-name {output} "
                        "{input}"
                    ).format(flacbin=FLACBIN, input=file, output=newfile)
                )
                file.unlink()
            elif file.suffix.lower() == ".xz":
                newfile = file.with_suffix("")
                with newfile.open("wb") as dest:
                    with lzma.open(file, "rb") as xzfile:
                        while True:
                            block = xzfile.read(16)
                            if not block:
                                break
                            dest.write(block)
                file.unlink()

    def extractall(self, path=".", members=None, decompress=True):
        """
        Extract all members from the archive to path. members should be
        a subset of names() or a list of TarInfo object from
        self.tarfile.getmembers()
        """
        zrpamembers = set()
        if members:
            for member in members:
                if isinstance(member, tarfile.TarInfo):
                    zrpamembers.add(member)
                else:
                    zrpamembers.add(self.member(member))
        else:
            for name in self.names():
                zrpamembers.add(self.member(name))
        for member in zrpamembers:
            self.extract(member, path=path, decompress=decompress)

    def add(self, filename, arcname=None):
        """
        Add filename to the archive. filename is compressed before being
        added. If filename is a directory its content is added
        recursively.
        """
        filepath = Path(filename)
        if not arcname:
            arcname = Path(filename)
        else:
            arcname = Path(arcname)
        invc = invoke.Context()
        if filepath.is_file():
            with TemporaryDirectory() as tmpdirname:
                tmpdirpath = Path(tmpdirname)
                if (
                    filepath.suffix.lower() == ".wav"
                    and self._flac_compression
                ):
                    newfilepath = tmpdirpath / (filepath.name + ".flac")
                    arcname = arcname.with_name(arcname.name + ".flac")
                    invc.run(
                        (
                            "{flacbin} "
                            "--best "
                            "--totally-silent "
                            "--keep-foreign-metadata "
                            "--output-name {output} "
                            "{input}"
                        ).format(
                            flacbin=FLACBIN,
                            input=filepath,
                            output=newfilepath,
                        )
                    )
                else:
                    newfilepath = tmpdirpath / (filepath.name + ".xz")
                    arcname = arcname.with_name(arcname.name + ".xz")
                    with lzma.open(newfilepath, "wb") as xzfile:
                        with filepath.open("rb") as source:
                            while True:
                                block = source.read(16)
                                if not block:
                                    break
                                xzfile.write(block)
                self.tarfile.add(
                    newfilepath, arcname=arcname, filter=self._reset_uidgid
                )
        elif filepath.is_dir():
            self.tarfile.add(filepath, arcname=arcname, recursive=False)
            for file in sorted(filepath.iterdir()):
                self.add(file, arcname=arcname / file.name)

    def create(self, pjdir):
        """
        Read a project directory (the original format for ZoomR
        devices) and fill in the current zrpa file accordingly.
        """
        for file in sorted(pjdir.iterdir()):
            self.add(file, arcname=file.name)

    def export(self, pjdir, with_tags=True):
        """
        Export the current archive to it's original format in pjdir.
        """
        # Create project directory
        pjdir.mkdir()
        self.extractall(path=pjdir)
        if not with_tags:
            (pjdir / "metadata.json").unlink()

    def _readmetadata(self):
        """Read metadata from the archive and store it as a dictionary."""
        # Archive must be opened in read mode to read existing metadata.
        # Opening it in other mode does not allow to read data from it.
        metadata = {"project": {}, "audio": {}}
        if self._filename.exists():
            with tarfile.open(self._filename, mode="r") as rawzrpa:
                try:
                    metadatainfo = rawzrpa.getmember("metadata.json.xz")
                    with lzma.open(
                        rawzrpa.extractfile(metadatainfo), mode="r"
                    ) as metadatafile:
                        metadata = json.load(metadatafile)
                except KeyError:
                    pass
        return metadata

    def _writemetadata(self):
        """Write metadata from self.metadata to the archive."""
        file = io.BytesIO()
        with lzma.open(file, mode="wt") as xzfile:
            json.dump(self.metadata, xzfile, indent=4)
        # Create empty TarInfo
        tarinfo = tarfile.TarInfo(name="metadata.json.xz")
        # Set size for TarInfo
        tarinfo.size = len(file.getvalue())
        tarinfo.mtime = round(time.time())
        tarinfo = self._reset_uidgid(tarinfo)
        # Has the buffer file has been read, we need to rewind to the
        # beginning of the buffer before giving it to tarfile.
        file.seek(0)
        self.tarfile.addfile(tarinfo, fileobj=file)

    def __enter__(self):
        self.tarfile.__enter__()
        return self

    def __exit__(self, errtype, value, traceback):
        if errtype is None:
            # No errors occurred, file can be closed normally.
            self.close()
        self.tarfile.__exit__(errtype, value, traceback)

    @staticmethod
    def _reset_uidgid(tarinfo):
        """
        This is a filter function for tarfile.add() function.
        Reset gid and uid to root.
        """
        tarinfo.uid = tarinfo.gid = 0
        tarinfo.uname = tarinfo.gname = "root"
        return tarinfo
