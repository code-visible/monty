PARSER_NAME = "monty"
PARSER_VESION = "v0.0.2"
PROTOL_VESION = "v0.2.1"
LANG = "Python"
TYPE_NORMAL = "normal"
TYPE_MINIFY = "minify"

# default value
DEFAULT_EXCLUDE_DIRECTORIES = ".*,testdata,tests,changelogs,scripts,docs"
DEFAULT_INCLUDE_FILE_TYPES = (
    "README.md,LICENSE,go.mod,go.sum,*.json,*.yaml,*.yml,Makefile"
)

DEFAULT_SHOULD_PARSE_TEST = False

__version__ = PARSER_VESION


def version():
    return __version__
