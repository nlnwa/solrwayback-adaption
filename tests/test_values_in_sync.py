from pathlib import Path
from tempfile import TemporaryDirectory

from pytest import raises

from ensure_arguments_in_sync import _ensure_arguments_in_sync


def test_valid() -> None:
    dockerfile = """ARG SOLR_VERSION=8.8.2"""
    workflow = """SOLR_VERSION=8.8.2"""

    with TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        dockerfile_path = temp_dir / "Dockerfile"
        workflow_path = temp_dir / "workflow.yml"
        dockerfile_path.write_text(dockerfile, encoding="utf-8")
        workflow_path.write_text(workflow, encoding="utf-8")

        _ensure_arguments_in_sync([dockerfile_path], [workflow_path])


def test_invalid() -> None:
    dockerfile = """ARG SOLR_VERSION=8.8.2"""
    workflow = """SOLR_VERSION=8.8.3"""

    with TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        dockerfile_path = temp_dir / "Dockerfile"
        workflow_path = temp_dir / "workflow.yml"
        dockerfile_path.write_text(dockerfile, encoding="utf-8")
        workflow_path.write_text(workflow, encoding="utf-8")

        with raises(RuntimeError):
            _ensure_arguments_in_sync([dockerfile_path], [workflow_path])
