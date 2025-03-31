from project import Project  # type: ignore
import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--project", type=str, help="project path", default=".")
parser.add_argument("--directory", type=str, help="directory path", default=".")
parser.add_argument("--minify", type=str, help="minify=1/0", default="0")
parser.add_argument("--dump", type=str, help="JSON dump path", default="parsed.json")
parser.add_argument("--excludes", type=str, help="directory to exclude; exclude=tests,examples", default="project")
parser.add_argument("--name", type=str, help="name of the project", default="")
args = parser.parse_args()

dist_path = os.path.join(os.getcwd(), args.dump)

p = Project(args.name, args.project, args.directory, args.excludes)

p.scan()
p.parse_files()
p.build_dependencies()
p.complete_fields()

with open(dist_path, 'w') as f:
    json.dump(p.dump(), f)
