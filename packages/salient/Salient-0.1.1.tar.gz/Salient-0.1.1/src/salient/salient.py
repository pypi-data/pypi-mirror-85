import argparse
import asyncio
import sys

from collections import defaultdict
from pathlib import Path
from typing import Callable, List


def do_config():
    parser = setup_arguments()
    values = vars(parser.parse_args())
    values["linters"] = []
    linters = (
        ("redefined_column", lint_redefined_columns),
        ("nullable_true", lint_unnecessary_nullable),
        ("index_false", lint_unnecessary_index_false),
    )
    values["linters"] = [fn for name, fn in linters if values[name]]
    # TODO: add environment variables and config file
    return values


def setup_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--nullable-true",
        action="store_true",
        help="Check for unnecessary nullable=True",
    )
    parser.add_argument(
        "-i",
        "--index-false",
        action="store_true",
        help="Check for unnecessary index=False",
    )
    parser.add_argument(
        "-r",
        "--redefined-column",
        action="store_true",
        help="Check for columns that are redefined.",
    )
    parser.add_argument("--config", type=str, help="Load options from CONFIG FILE.")
    parser.add_argument("files", nargs="+", help="files to lint")
    parser.add_argument(
        "-R",
        "--recursive",
        action="store_true",
        default=False,
        help="If FILES includes directories scan those as well",
    )
    parser.add_argument("-1", "--stop-after-first-error", help="stop after first error")
    return parser


async def find_unnecessary_x_bool(
    contents, str_to_find: str, bool_to_find: str = "False"
):
    errors = []
    for line_no, line in enumerate(contents.splitlines()):
        line_cleaned = line.replace(" ", "")
        if f"{str_to_find}={bool_to_find}" in line_cleaned:
            errors.append(("", [(line_no + 1, line)]))
    return errors


async def lint_unnecessary_index_false(contents):
    results = await find_unnecessary_x_bool(contents, "index")
    if results:
        output = await format_errors("Unnecessary index=False", results)
        return False, output
    return True, ""


async def lint_unnecessary_nullable(contents):
    results = await find_unnecessary_x_bool(contents, "nullable", "True")
    if results:
        output = await format_errors("Unnecessary nullable=True", results)
        return False, output
    return True, ""


class DuplicateFinder:
    def __init__(self):
        self.duplicates = defaultdict(list)
        self.items = {}

    def __setitem__(self, key, value):
        if not key in self.items:
            self.items[key] = value
        else:
            if key in self.duplicates:
                self.duplicates[key].append(value)
            else:
                self.duplicates[key].append(self.items[key])
                self.duplicates[key].append(value)

    def __getitem__(self, key):
        return self.items.__getitem__(key)


async def find_duplicate_definitions(contents):
    df = DuplicateFinder()
    for line_no, line in enumerate(contents.splitlines()):
        if "=" in line and "Column" in line:
            df[line.strip().split("=")[0].strip()] = (
                line_no + 1,
                line.split("=", maxsplit=1)[1].strip(),
            )
    return df.duplicates


async def format_errors(error_name, result_items):
    output = ""
    for result in result_items:
        key, values = result
        details = [f"{ln}: {dfn}" for ln, dfn in values]
        if key:
            output += f"  {error_name} - {key}:"
        else:
            output += f"  {error_name}:"
        for line in details:
            output += "\n    " + line
    return output


async def lint_redefined_columns(contents):
    results = await find_duplicate_definitions(contents)
    if results:
        output = await format_errors("Redefined Columns", list(results.items()))
        return False, output
    return True, ""


async def run_lint_on_file(name, contents, linters):
    file_output = name
    passing = True

    for linter in linters:
        pass_, output = await linter(contents)
        if not pass_:
            passing = False
            file_output += f"\n{output}"

    if passing:
        return True, ""
    return False, file_output


async def read_file(fn):
    # TODO: this is blocking, need aiofiles, I guess
    with open(fn) as f:
        return f.read()


async def get_files(files: str):
    lint_files = []
    for f in files:
        if Path(f).is_dir():
            continue  # TODO: add recursion
        lint_files.append(f)
    return lint_files


async def main(files: list, linters: List[Callable]):
    combined_output = ""
    failures = 0

    for f in await get_files(files):
        pass_, output = await run_lint_on_file(f, await read_file(f), linters)
        if not pass_:
            failures += 1
            combined_output += f"\n{output}"

    if failures:
        print(f"{failures} file(s) with errors were found.\n{combined_output}")
        sys.exit(1)
    else:
        print("Success")


def cmd():
    config = do_config()
    if not config["linters"]:
        print("Nothing to run, please select one or more linters.")
        sys.exit(5)
    asyncio.run(main(config["files"], config["linters"]))


if __name__ == "__main__":
    cmd()
