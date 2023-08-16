from argparse import ArgumentParser, Namespace
from contextlib import contextmanager
from pathlib import Path
from subprocess import check_call
from typing import Generator


def _args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--collection", required=True, type=str, help="Name of collection"
    )
    parser.add_argument(
        "--warc-file-directory",
        required=True,
        type=Path,
        help="Directory containing WARC files belonging to a collection",
    )
    parser.add_argument(
        "--number-of-threads",
        required=True,
        type=int,
        help="Number of threads to use for indexing",
    )
    return parser.parse_args()


def _main() -> None:
    args = _args()
    solr_version = "7.7.3"
    apache_tomcat_version = "8.5.60"
    solrwayback_version = "4.4.2"

    with _solr(
        solr_version=solr_version, solrwayback_version=solrwayback_version
    ), _tomcat(
        apache_tomcat_version=apache_tomcat_version,
        solrwayback_version=solrwayback_version,
    ):
        _index(
            args.collection,
            number_of_threads=args.number_of_threads,
            warc_file_directory=args.warc_file_directory,
            solrwayback_version=solrwayback_version,
        )


@contextmanager
def _solr(solr_version: str, solrwayback_version: str) -> Generator[None, None, None]:
    _start_solr(solr_version=solr_version, solrwayback_version=solrwayback_version)
    yield
    _stop_solr(solr_version=solr_version, solrwayback_version=solrwayback_version)


@contextmanager
def _tomcat(
    apache_tomcat_version: str, solrwayback_version: str
) -> Generator[None, None, None]:
    _start_tomcat(
        apache_tomcat_version=apache_tomcat_version,
        solrwayback_version=solrwayback_version,
    )
    yield
    _stop_tomcat(
        apache_tomcat_version=apache_tomcat_version,
        solrwayback_version=solrwayback_version,
    )


def _stop_tomcat(apache_tomcat_version: str, solrwayback_version: str) -> None:
    home_dir = Path().resolve()
    apache_tomcat_path = (
        home_dir
        / "unpacked-bundle"
        / f"solrwayback_package_{solrwayback_version}"
        / f"apache-tomcat-{apache_tomcat_version}"
        / "bin"
        / "shutdown.sh"
    )
    check_call(
        [str(apache_tomcat_path)],
    )


def _stop_solr(solr_version: str, solrwayback_version: str) -> None:
    home_dir = Path().resolve()
    solr_path = (
        home_dir
        / "unpacked-bundle"
        / f"solrwayback_package_{solrwayback_version}"
        / f"solr-{solr_version}"
        / "bin"
        / "solr"
    )
    check_call(
        [str(solr_path), "stop", "-all"],
    )


def _start_solr(solr_version: str, solrwayback_version: str) -> None:
    home_dir = Path().resolve()
    solr_path = (
        home_dir
        / "unpacked-bundle"
        / f"solrwayback_package_{solrwayback_version}"
        / f"solr-{solr_version}"
        / "bin"
        / "solr"
    )
    check_call(
        [str(solr_path), "start"],
    )


def _start_tomcat(apache_tomcat_version: str, solrwayback_version: str) -> None:
    home_dir = Path().resolve()

    apache_tomcat_path = (
        home_dir
        / "unpacked-bundle"
        / f"solrwayback_package_{solrwayback_version}"
        / f"apache-tomcat-{apache_tomcat_version}"
        / "bin"
        / "startup.sh"
    )
    check_call(
        [str(apache_tomcat_path)],
    )


def _index(
    collection: str,
    number_of_threads: int,
    warc_file_directory: Path,
    solrwayback_version: str,
) -> None:
    home_dir = Path().resolve()

    all_warc_files = list(warc_file_directory.rglob("*.warc.gz"))
    warc_indexer_path = (
        home_dir
        / "unpacked-bundle"
        / f"solrwayback_package_{solrwayback_version}"
        / "indexing"
        / "warc-indexer.sh"
    )

    check_call(
        [str(warc_indexer_path), *map(str, all_warc_files)],
        env={
            "THREADS": str(number_of_threads),
            "INDEXER_CUSTOM": f"--collection={collection}",
            "JAVA_TOOL_OPTIONS": "-Dfile.encoding=UTF8",  # Remove when `solrwayback` version greater than 4.4.2 is out.
        },
    )


if __name__ == "__main__":
    _main()
