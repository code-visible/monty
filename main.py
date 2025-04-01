import argparse
import json
import os

from monty import DEFAULT_EXCLUDE_DIRECTORIES, DEFAULT_INCLUDE_FILE_TYPES
from project import Project  # type: ignore

parser = argparse.ArgumentParser()
parser.add_argument("--project", type=str, help="project path", default=".")
parser.add_argument("--directory", type=str, help="directory path", default=".")
parser.add_argument("--minify", type=str, help="minify=1/0", default="0")
parser.add_argument("--dump", type=str, help="JSON dump path", default="parsed.json")
parser.add_argument(
    "--excludes",
    type=str,
    help="directory to exclude; exclude=tests,examples",
    default=DEFAULT_EXCLUDE_DIRECTORIES,
)
parser.add_argument(
    "--types",
    type=str,
    help="allowed file types; types=*.json,README.md",
    default=DEFAULT_INCLUDE_FILE_TYPES,
)
parser.add_argument("--name", type=str, help="name of the project", default="project")
args = parser.parse_args()

dist_path = os.path.join(os.getcwd(), args.dump)

p = Project(args.name, args.project, args.directory, args.excludes, args.types)

p.scan()
p.parse_files()
p.build_dependencies()
p.complete_fields()

with open(dist_path, "w") as f:
    json.dump(p.dump(), f)
