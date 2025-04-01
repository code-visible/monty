PARSER_NAME = "monty"
VESION = "v0.0.1"
LANG = "Python"
TYPE_NORMAL = "normal"
TYPE_MINIFY = "minify"

# default value
DEFAULT_EXCLUDE_DIRECTORIES = ".*,testdata,tests,changelogs,scripts,docs"
DEFAULT_INCLUDE_FILE_TYPES = (
    "README.md,LICENSE,go.mod,go.sum,*.json,*.yaml,*.yml,Makefile"
)
DEFAULT_SHOULD_PARSE_TEST = False

__version__ = VESION


def version():
    return __version__
