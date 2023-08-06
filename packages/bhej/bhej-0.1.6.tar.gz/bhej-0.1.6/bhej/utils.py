import gzip
import os
import tarfile
import typer
import pkg_resources
import requests

from .config import COMPRESSION_TYPE, URL
from .exceptions import handleNetworkError


def check_bhej_version():
    try:
        res = requests.get(URL + "/version")
    except Exception:
        handleNetworkError()

    if res.status_code != 200:
        print(res.status_code)
        typer.echo("bye An unexpected error occurred with the server.")
        raise typer.Exit(code=39)

    backend_version = res.text
    current_version = pkg_resources.get_distribution("bhej").version
    if backend_version > current_version:
        typer.echo(
            f"Your CLI app is running {current_version}, but the bhej backend requires {backend_version}."
        )
        typer.echo("Please upgrade with the command...\n")
        typer.echo("\tpip install -U --user bhej\n")
        typer.echo("... to continue.")
        raise typer.Exit(code=43)


def gz_compress(file):
    """Wrapper for gzip.compress. Returns gzipped bytes of file"""
    return gzip.compress(file)


def gz_decompress(file):
    """Wrapper for gzip.decompress. Returns decompressed bytes of file."""
    return gzip.decompress(file)


def tar_compress(source_dir):
    if not os.path.exists(source_dir):
        raise FileNotFoundError
    dir_name = os.path.basename(source_dir)
    dest_dir = "./" + dir_name + ".tar.gz"
    with tarfile.open(dest_dir, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    return dest_dir


def tar_decompress(filepath):
    filename = os.path.basename(str(filepath)[:-7])
    dest_dir = filename
    dest_dir_prefix = 0
    while os.path.exists(dest_dir):
        dest_dir_prefix += 1
        dest_dir = f"{str(dest_dir_prefix)}/{filename}"

    with tarfile.open(filepath, "r:gz") as tar:
        if dest_dir_prefix != 0:
            tar.extractall(str(dest_dir_prefix))
        else:
            tar.extractall()
    typer.echo(f"Decompression complete. File(s) stored at {dest_dir}")


def check_and_rename(filename, add=0):
    """Returns incremented filename if name already taken."""
    original_file = filename
    if add != 0:
        split = os.path.splitext(filename)
        part_1 = split[0] + "_" + str(add)
        filename = "".join([part_1, split[1]])

    if not os.path.isfile(filename):
        return filename
    else:
        return check_and_rename(original_file, add + 1)


def compress(file):
    if COMPRESSION_TYPE == "GZ":
        return gz_compress(file)
    elif COMPRESSION_TYPE == "TAR_GZ":
        return tar_compress(file)


def decompress(file):
    if COMPRESSION_TYPE == "GZ":
        return gz_decompress(file)
    elif COMPRESSION_TYPE == "TAR_GZ":
        return tar_decompress(file)
