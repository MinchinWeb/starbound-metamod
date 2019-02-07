from pathlib import Path
import sys

import colorama
from invoke import task, run
import minchin.text as text
import winshell

SB_STEAM_ID = '211820'

SB_BASE_DIR = Path(r'C:\Program Files (x86)\Steam\steamapps\common\Starbound')
SB_STEAM_MODS_DIR = Path(r'C:\Program Files (x86)\Steam\steamapps\workshop\content\211820')
SB_UNIVERSE_DIR = SB_BASE_DIR / 'storage' / 'universe'
SB_PLAYER_DIR = SB_BASE_DIR / 'storage' / 'player'

SB_ASSETS = SB_BASE_DIR / 'assets' / 'packed.pak'

SB_ASSET_PACKER = SB_BASE_DIR / 'win32' / 'asset_packer.exe'
SB_ASSET_UNPACKER = SB_BASE_DIR / 'win32' / 'asset_unpacker.exe'
SB_DUMP_JSON = SB_BASE_DIR / 'win32' / 'dump_versioned_json.exe'
SB_LOAD_JSON = SB_BASE_DIR / 'win32' / 'make_version_json.exe'

STEAM_SB_MOD_URL = "http://steamcommunity.com/sharedfiles/filedetails/?id={}"


colorama.init()
GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW
RESET_ALL = colorama.Style.RESET_ALL


@task
def hello_world(ctx):
    print("Hello World!")


@task
def unpack_assets(ctx, source=SB_ASSETS, destination = 'unpacked'):
    """Unpack the game assets."""
    text.title("Asset Unpacker")

    source = Path(source)
    destination = Path(destination)

    # check source file
    if source.exists():
        print("Games Assets: {}FOUND{}!".format(GREEN, RESET_ALL))
    else:
        print("Game Assets: {}MISSING{}".format(RED, RESET_ALL))
        print("Exiting...")
        sys.exit(1)
    
    # check destination folder
    if destination.exists():
        # test if folder is empty
        if list(destination.rglob('*')):
            print("Destination Folder: {}Exists, Not Empty{}".format(YELLOW, RESET_ALL))
            print("    {}".format(destination.resolve()))
            if text.query_yes_no("    Empty Folder?"):
                winshell.delete_file(destination.rglob('*'), silent=True)
        else:
            print("Destination Folder: {}Exists, Empty{}!".format(GREEN, RESET_ALL))
    else:
        print("Destination Folder: {}MISSING{}".format(YELLOW, RESET_ALL))
        if text.query_yes_no("    Create?"):
            destination.mkdir(parents=True)
        else:
            print("Exiting...")
            sys.exit(1)

    # the actual unpacking!
    cmd = '"{}" "{}" "{}"'.format(
        SB_ASSET_UNPACKER,
        source,
        destination,
    )
    print("Unpacking...")
    run(cmd)
    print("{}Done!{}".format(GREEN, RESET_ALL))


@task
def unpack_steam_mods(ctx, source=SB_STEAM_MODS_DIR,
                      destination = 'unpacked-mods', override_existing=False):
    """Unpack all steam mods."""
    text.title("Steam Mod Unpacker")

    source = Path(source)
    destination = Path(destination)

    # check source file
    if source.exists():
        print("Steam Mods: {}FOUND{}!".format(GREEN, RESET_ALL))
    else:
        print("Steam Mods: {}MISSING{}".format(RED, RESET_ALL))
        print("Exiting...")
        sys.exit(1)
    
    # check destination folder
    if destination.exists():
        # test if folder is empty
        if list(destination.rglob('*')):
            print("Destination Folder: {}Exists, Not Empty{}".format(YELLOW, RESET_ALL))
            print("    {}".format(destination.resolve()))
            if text.query_yes_no("    Empty Folder?"):
                winshell.delete_file(destination.rglob('*'), silent=True)
        else:
            print("Destination Folder: {}Exists, Empty{}!".format(GREEN, RESET_ALL))
    else:
        print("Destination Folder: {}MISSING{}".format(YELLOW, RESET_ALL))
        if text.query_yes_no("    Create?"):
            destination.mkdir(parents=True)
        else:
            print("Exiting...")
            sys.exit(1)

    print("Unpacking...")
    for fn in source.iterdir():
        if fn.is_dir():
            mod_id = fn.name
            mod_destination = destination / mod_id
            if mod_destination.exists():
                mod_override = text.query_yes_no_all("Destination folder for mod {} exists. Override?".format(mod_id),
                                                    default='no')
                if mod_override == 2:
                    override_existing = True
                
                if override_existing or mod_override:
                    winshell.rmdir(mod_destination)
                else:
                    print("    {}Skipping{} {}...".format(YELLOW, RESET_ALL, mod_id))
                    continue
                
            # the actual unpacking!
            cmd = '"{}" "{}" "{}"'.format(
                SB_ASSET_UNPACKER,
                fn / 'contents.pak',
                mod_destination,
            )
            run(cmd)
    print("{}Done!{}".format(GREEN, RESET_ALL))

