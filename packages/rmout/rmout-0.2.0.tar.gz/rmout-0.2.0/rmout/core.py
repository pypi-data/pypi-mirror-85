import os
import click

from rmout.files import (
    get_extensions_set,
    extract_files_by_extlist,
)
from rmout.trash import (
    extract_target_from_userinput,
    get_extensiondir_for_sendtotrash,
    send_to_trash,
)


@click.command(help='\
rmout is a tool that throws files with the extension written \
in the .rmoutrc file into the trash.')
def run():
    debug = False
    rmout(debug)
    click.echo('finished.')


def rmout(debug=True):
    current_dir = os.getcwd()
    target_ext_set = get_extensions_set(current_dir)
    if not target_ext_set:
        return
    trash_candidate = extract_files_by_extlist(target_ext_set, current_dir)
    if not trash_candidate:
        return
    codelist = extract_target_from_userinput()
    throwaway = get_extensiondir_for_sendtotrash(codelist, trash_candidate)
    send_to_trash(throwaway, debug)
