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
            ans = text.query_yes_no("    Empty Folder?")
            if ans == text.Answers.YES:
                winshell.delete_file(destination.rglob('*'), silent=True)
        else:
            print("Destination Folder: {}Exists, Empty{}!".format(GREEN, RESET_ALL))
    else:
        print("Destination Folder: {}MISSING{}".format(YELLOW, RESET_ALL))
        ans = text.query_yes_no("    Create?")
        if ans == text.Answers.YES:
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
                      destination = 'unpacked-mods', override_existing=False,
                      skip_existing=False):
    """Unpack all steam mods."""
    text.title("Steam Mod Unpacker")

    count_skipped = 0
    count_unpacked = 0
    count_errorred = 0
    error_list = []

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
            ans = text.query_yes_no("    Empty Folder?", default="no")
            if ans == text.Answers.YES:
                winshell.delete_file(destination.rglob('*'), silent=True)
        else:
            print("Destination Folder: {}Exists, Empty{}!".format(GREEN, RESET_ALL))
    else:
        print("Destination Folder: {}MISSING{}".format(YELLOW, RESET_ALL))
        ans = text.query_yes_no("    Create?")
        if ans == text.Answers.YES:
            destination.mkdir(parents=True)
        else:
            print("Exiting...")
            sys.exit(1)

    print("Unpacking...")
    for fn in source.iterdir():
        if fn.is_dir():
            mod_id = fn.name
            mod_destination = destination / mod_id
            skip_this = False
            override_this = False
            if mod_destination.exists():
                if not override_existing and not skip_existing:
                    ans = text.query_yes_no_all_none(("Destination folder for "
                                                      "mod {} exists. Override?"
                                                      .format(mod_id)),
                                                     default='none')
                    if ans == text.Answers.YES:
                        override_this = True
                    elif ans == text.Answers.NO:
                        skip_this = True
                    elif ans == text.Answers.ALL:
                        override_existing = True
                        override_this = True
                    elif ans == text.Answers.NONE:
                        skip_existing = True
                        skip_this = True

                if override_this or override_existing:
                    winshell.rmdir(mod_destination)
                else:
                    skip_this = True
                
            # the actual unpacking!
            if skip_this:
                print("    {}Skipping{} {}...".format(YELLOW, RESET_ALL, mod_id))
                count_skipped += 1
            else:
                cmd = '"{}" "{}" "{}"'.format(
                    SB_ASSET_UNPACKER,
                    fn / 'contents.pak',
                    mod_destination,
                )
                try:
                    run(cmd)
                except Exception as e:
                    # print(e)
                    count_errorred += 1
                    error_list.append(mod_id)
                else:
                    count_unpacked += 1

    print()
    print(("{}Done!{} {} mods unpacked, {} skipped, and {} errorred."
           .format(GREEN, RESET_ALL, count_unpacked, count_skipped,
                   count_errorred)))
    print("{}Errors{}: {}".format(YELLOW, RESET_ALL, ", ".join(error_list)))
