from pathlib import Path
from stat import S_IXGRP, S_IXOTH, S_IXUSR
from tempfile import TemporaryDirectory

from fetch_solrwayback_bundle import _fetch_bundle


def test_executable_bits_are_set() -> None:
    with TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        destination = temp_dir / "bundle"
        solrwayback_version = "4.4.2"

        _fetch_bundle(solrwayback_version=solrwayback_version, destination=destination)

        sh_files = list(destination.rglob("*.sh"))
        for sh_file in sh_files:
            assert (
                sh_file.stat().st_mode & S_IXUSR != 0
            ), f"File '{sh_file}' has does not have user executable bit set"
            assert (
                sh_file.stat().st_mode & S_IXGRP != 0
            ), f"File '{sh_file}' has does not have group executable bit set"
            assert (
                sh_file.stat().st_mode & S_IXOTH != 0
            ), f"File '{sh_file}' has does not have other executable bit set"
