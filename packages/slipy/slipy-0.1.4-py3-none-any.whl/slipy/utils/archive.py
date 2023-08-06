import os
import pathlib
import shutil

# Higher level utilities


def compress(archive_name, root_dir=None, verbose=1, skip_report=None):
    """
    Fix the format

    Parameters
    ----------
    """
    if root_dir is None:
        root_dir = archive_name
    root_dir = pathlib.Path(root_dir).absolute()

    if isinstance(archive_name, pathlib.Path):
        archive_path = archive_name
        archive_path = archive_path.parent / (archive_name.name + ".zip")
    else:
        archive_path = pathlib.Path(archive_name + ".zip")

    if archive_path.exists():
        ans = input(f"'{archive_path.name}' exists, do you want to overwrite? [y/N]")
        if ans.lower() not in ["y", "yes"]:
            print("nothing done")
            return
        else:
            archive_path.unlink()

    if skip_report is None:
        skip_report = []

    if verbose >= 1:
        print(f"Archiving following files in '{archive_name}.zip':")

    for node, node_dir, node_files in os.walk(root_dir):
        node = (pathlib.Path(root_dir) / node).absolute().relative_to(root_dir)
        if verbose >= 2 or (verbose == 1 and node not in skip_report):
            print(f"\t{node}")
            for f in node_files:
                f = node / f
                print(f"\t{f}")
    return shutil.make_archive(archive_name, "zip", root_dir)


def uncompress(archive_name, dest_dir=".", folder="."):
    # make it working also without extension
    archive_path = None
    for el in pathlib.Path(folder).iterdir():
        if el.stem == archive_name:
            archive_path = el.absolute()

    if archive_path is None:
        archive_path = pathlib.Path(archive_name).absolute()

    dest_path = pathlib.Path(dest_dir).absolute()

    shutil.unpack_archive(str(archive_path), str(dest_dir))
