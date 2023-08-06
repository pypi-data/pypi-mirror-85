import cgi
import magic
import os
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm
import typer

from .config import URL
from .exceptions import handleNetworkError
from .utils import check_bhej_version, compress, decompress

app = typer.Typer()


@app.command()
def up(filename: str):
    check_bhej_version()

    try:
        typer.echo(f"Compressing {filename}")
        compressed_filename = compress(filename)
        file = open(compressed_filename, "rb").read()

        if len(file) > 1048576:
            typer.echo(
                "Compressed file size too large. Compressed files must be smaller than 1GB. Aborting."
            )
            raise typer.Exit(code=8)

        mime = magic.Magic(mime=True)
        files = {"upload_file": (filename, file, mime.from_file(filename))}
    except FileNotFoundError:
        typer.echo(f"No such file: '{filename}'. Aborting.")
        raise typer.Exit(code=3)
    except IsADirectoryError:
        files = {"upload_file": (filename, file, "application/x-gzip")}
    except Exception as err:
        typer.echo(f"Unexpected Error: {str(err)}")
        raise (err)

    typer.echo(f"Uploading {filename}")

    e = MultipartEncoder(fields=files)

    with tqdm(total=e.len, dynamic_ncols=True, unit="B", unit_scale=True) as bar:
        m = MultipartEncoderMonitor(
            e, lambda monitor: bar.update(monitor.bytes_read - bar.n)
        )
        try:
            req = requests.post(
                URL + "/upload", data=m, headers={"Content-Type": m.content_type}
            )
        except Exception:
            handleNetworkError()

    if req.status_code == 500:
        typer.echo("There was an unexpected server error. Please try again later.")
        raise typer.Exit(code=7)

    code = req.text
    link = f"{URL}/file/{code}"

    typer.echo(f"Upload successful! Your code is -> {code}")
    typer.echo(f"You can also download the file directly at {link}")
    os.unlink(compressed_filename)

    return


@app.command()
def down(filecode: str, dest: str = "."):
    check_bhej_version()
    # TODO: Add an option to change the file name?

    if not os.path.exists(dest):
        typer.echo(f"No such location: {dest}. Aborting.")
        return

    if not os.path.isdir(dest):
        typer.echo(f"{dest} is not a directory. Aborting.")
        # TODO: Add a prompt to ask whether you'd like to create the dir.
        return

    dest = os.path.join(dest, "")  # Adds trailing slash if missing.

    typer.echo(f"Downloading {filecode}")
    req = requests.get(URL + "/download/" + filecode, stream=True)

    total_size_in_bytes = int(req.headers.get("Content-Length", 0))

    block_size = 1024
    progress_bar = tqdm(
        total=total_size_in_bytes, dynamic_ncols=True, unit="B", unit_scale=True
    )

    try:
        _, params = cgi.parse_header(req.headers["Content-Disposition"])
    except KeyError:
        print(f"File associated with {filecode} not found. Please check code.")
        raise typer.Exit(code=10)
    except Exception as err:
        print("An unexpected error occurred")
        print(err)
        raise typer.Exit(code=11)

    filename = params["filename"]

    fname = dest + filename

    with open(fname, "wb") as file:
        for data in req.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print(progress_bar.n, total_size_in_bytes)
        print("ERROR, something went wrong")

    typer.echo(f"Downloaded {fname}. Starting decompression.")

    decompress(fname)

    os.remove(fname)

    typer.echo("Done!")
