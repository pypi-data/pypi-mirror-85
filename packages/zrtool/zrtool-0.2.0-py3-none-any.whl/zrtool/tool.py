# Copyright 2020 Rémy Taymans <remytms@tsmail.eu>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""Tools for CLI commands"""

import click
import yaml


def reset_uidgid(tarinfo):
    """
    This is a filter function for tarfile.add() function.
    Reset gid and uid to root.
    """
    tarinfo.uid = tarinfo.gid = 0
    tarinfo.uname = tarinfo.gname = "root"
    return tarinfo


def secure_userkey(key):
    """
    Conform a key entered by a user to the format standard.
    :param key: A key entered by a user.
    """
    key = key.lower().strip()
    key = key.replace(" ", "_")
    if key[:2] == "__":
        key = key.lstrip("_")
    return key


def secure_usertag(data):
    """
    Tags should be represented by a dict with keys and value. This
    function ensure that tags entered by a user conform to this.
    :param data: a dict of tags entered by a user.
    """
    if not isinstance(data, dict):
        data = {}
    new_data = {}
    for key, value in data.items():
        new_key = secure_userkey(key)
        new_data[new_key] = str(value)
    return new_data


def editmetadata(header="# This is a regular yaml file.\n"):
    """Ask user to enter metadata in a yaml file."""
    yamlfile = header
    dataok = False
    while not dataok:
        user_yaml = click.edit(yamlfile, extension=".yaml")
        try:
            if user_yaml:
                yaml_dict = yaml.safe_load(user_yaml)
            else:
                yaml_dict = yaml.safe_load(yamlfile)
            dataok = True
        except yaml.YAMLError as err:
            if click.confirm(
                "An error occur during parsing. Do you want to try again?",
                default=True,
            ):
                if user_yaml:
                    yamlfile = user_yaml
                user_yaml += (
                    "#\n# An error occur during parsing of this file\n"
                )
                for line in str(err).split("\n"):
                    user_yaml += "# {err}\n".format(err=line)
            else:
                yaml_dict = {}
                dataok = True
    return yaml_dict
