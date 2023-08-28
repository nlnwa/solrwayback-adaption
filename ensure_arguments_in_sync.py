from pathlib import Path
from re import findall
from typing import Sequence, TypeAlias

ArgumentStruct: TypeAlias = dict[str, dict[str, list[Path]]]


def _main() -> None:
    all_docker_files = list(Path().rglob("Dockerfile*"))
    all_workflow_files = list((Path() / ".github" / "workflows").rglob("*.yml"))
    print("Checking that the following paths contain the same arguments")
    print(*list(map(str, all_docker_files + all_workflow_files)))
    _ensure_arguments_in_sync(all_docker_files, all_workflow_files)


def _ensure_arguments_in_sync(
    dockerfiles: Sequence[Path], workflows: Sequence[Path]
) -> None:
    argument_struct: ArgumentStruct = {}

    for docker_file in dockerfiles:
        _dockerfile(docker_file, argument_struct)

    for workflow_file in workflows:
        _workflow(workflow_file, argument_struct)

    _validate_argument_struct(argument_struct)


def _flatten(non_flat: list):
    return [item for sublist in non_flat for item in sublist]


def _validate_argument_struct(argument_struct: ArgumentStruct) -> None:
    for argument, versions in argument_struct.items():
        if len(versions) > 1:
            relevant_files = list(map(str, _flatten(versions.values())))
            raise RuntimeError(
                f"Argument: '{argument}' has has inconsistent values for the versions: '{', '.join(versions)}' in the paths '{', '.join(relevant_files)}'"
            )


def _dockerfile(dockerfile: Path, argument_struct: ArgumentStruct) -> None:
    pattern = r"(ARG\s+)(\S+)(=)(\S*)"  # https://regex101.com/r/6tqpqz/1
    _insert_arguments(path=dockerfile, argument_struct=argument_struct, pattern=pattern)


def _workflow(workflow_file: Path, argument_struct: ArgumentStruct) -> None:
    pattern = r"(\s*)(\S+)(=)(\S*)"  # https://regex101.com/r/w3xhV9/1
    ignore_arguments = [
        "type=ref,event",  # is not a argument shared between workflows and dockerfiles
    ]
    _insert_arguments(
        path=workflow_file,
        argument_struct=argument_struct,
        pattern=pattern,
        ignore_arguments=ignore_arguments,
    )


def _insert_arguments(
    path: Path, argument_struct: ArgumentStruct, pattern: str, ignore_arguments=None
) -> None:
    content = path.read_text(encoding="utf-8")
    if matched := findall(pattern, content):
        for match in matched:
            argument_name = match[1]
            argument_version = match[3]
            if ignore_arguments and argument_name in ignore_arguments:
                continue
            if argument_name not in argument_struct:
                argument_struct[argument_name] = {
                    argument_version: [
                        path,
                    ]
                }
            else:
                if argument_version not in argument_struct[argument_name]:
                    argument_struct[argument_name][argument_version] = [
                        path,
                    ]
                else:
                    argument_struct[argument_name][argument_version] = argument_struct[
                        argument_name
                    ][argument_version] + [
                        path,
                    ]


if __name__ == "__main__":
    _main()
