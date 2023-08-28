from argparse import ArgumentParser, Namespace
from pathlib import Path
from urllib.request import urlopen
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from http import HTTPStatus


def _args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--solrwayback-version",
        required=True,
        type=str,
        help="solrwayback bundle version",
    )
    parser.add_argument(
        "--destination",
        required=True,
        type=Path,
        help="Directory to download solrwayback bundle to",
    )
    return parser.parse_args()


def _main() -> None:
    args = _args()
    url = f"https://github.com/netarchivesuite/solrwayback/releases/download/{args.solrwayback_version}/solrwayback_package_{args.solrwayback_version}.zip"
    print(f"Downloading {url} to {args.destination}", flush=True)

    with urlopen(url) as response:
        if response.getcode() != HTTPStatus.OK:
            raise RuntimeError(
                f"Failed to download '{url}', got response code '{response.getcode()}'"
            )
        with TemporaryDirectory() as temp_dir_name:
            zip_path = Path(temp_dir_name) / "solrwayback.zip"
            with zip_path.open("wb") as zip_file:
                zip_file.write(response.read())
            with ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(args.destination)


if __name__ == "__main__":
    _main()
