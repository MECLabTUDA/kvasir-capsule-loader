import os
import hashlib
import shutil

import click
import requests
import tqdm

from .config import KVASIR_CAPSULE_PATH


DOWNLOAD_URLS = {
    "metadata.json": "https://files.osf.io/v1/resources/dv2ag/providers/googledrive/metadata.json?action=download&direct&version",
    "metadata.csv": "https://files.osf.io/v1/resources/dv2ag/providers/googledrive/metadata.csv?action=download&direct&version",
    "labelled_images.zip": "https://files.osf.io/v1/resources/dv2ag/providers/googledrive/labelled_images/?zip=",
}

CHECKSUMS = {
    "metadata.json": "c8f2b076283be42485fdb0d5b486a1f5095ce87b5a69f8c8d394cbf05fc2ab4f",
    "metadata.csv": "480373e840c48d7cad45aede92bdc8fa5a7c0064e6b22470d38af9f2032642f5",
    # Google drive regenerates zip files on every new request.
    # zip has "last modified" time in header, which changes every time the zip is packed.
    # That's my explanation why the checksum changes with each download.
    "labelled_images.zip": None,
}


def validate_checksum(filename):
    """
    Compares the SHA256 checksum of a file to a list of known checksums.
    In case somebody compromises the files inside the Google Drive, this
    mandatory check may prevent the download of malware.

    :param filename: Filename as given in the above declared dictionaries.
    :ptype filename: str
    """
    checksum = CHECKSUMS.get(filename, None)
    if checksum is None:
        click.secho("No checksum available to compare with.", fg="yellow")
        click.secho("The downloaded file might be unsafe.", fg="yellow")
        if not click.confirm("Still want to continue?"):
            return False
        return True
    else:
        click.secho("Validating checksum...", fg="blue")
        sha256 = hashlib.sha256()
        destination = KVASIR_CAPSULE_PATH / filename
        with open(destination, "rb") as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                sha256.update(data)
        file_hash = sha256.hexdigest()
        if checksum != file_hash:
            click.secho(
                "Invalid checksum. This might be a bug, a server error or transmission problem.",
                fg="red",
            )
            click.secho(f"expected: {checksum}")
            click.secho(f"download: {file_hash}")
            return False
        click.secho("Checksum ok.", fg="green")
    return True


def download_file(filename):
    """
    Download a file and validate its checksum.

    :param filename: Filename on disk (not path!)
    :ptype filename: str
    """
    url = DOWNLOAD_URLS[filename]
    destination = KVASIR_CAPSULE_PATH / filename
    click.secho(f"File: {filename}", fg="blue")
    click.secho(f"Downloading file from URL {url}...", fg="blue")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(destination, "wb") as f:
            for chunk in tqdm.tqdm(
                r.iter_content(chunk_size=1024),
                total=int(r.headers.get("content-length", 0)) // 1024,
                unit="KB",
            ):
                f.write(chunk)
    click.secho("Done.", fg="green")
    if not validate_checksum(filename):
        exit()
    click.secho("")


def extract_archive(filename):
    """ """
    click.secho(f"Extracting archive {filename}...", fg="blue")
    shutil.unpack_archive(KVASIR_CAPSULE_PATH / filename, KVASIR_CAPSULE_PATH)
    click.secho("Done.", fg="green")


def extract_images():
    """
    Extract all images and write
    """
    # extract and remove labelled_images.zip
    filename = "labelled_images.zip"
    # TODO error handling if file doesn't exist
    extract_archive(filename)
    os.remove(KVASIR_CAPSULE_PATH / filename)
    # extract tar.gz archives inside of the zip
    for archive in KVASIR_CAPSULE_PATH.glob("*.gz"):
        extract_archive(archive)
        os.remove(archive)



def download_all():
    for filename in DOWNLOAD_URLS:
        download_file(filename)
    extract_images()
