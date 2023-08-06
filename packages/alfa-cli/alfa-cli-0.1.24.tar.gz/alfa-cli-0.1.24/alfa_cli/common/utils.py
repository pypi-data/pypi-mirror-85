from functools import wraps
import json
import zipfile
from pathlib import Path
from pathos.multiprocessing import ProcessingPool
from alfa_sdk.common.exceptions import ValidationError


DEFAULT_EXCLUDES = [".git/*", ".gitignore", ".DS_Store"]


#


def zipdir(source, dest, *, excludes=[], includes=[], conf=None):
    if conf is not None:
        excludes, includes = extract_ignore_rules(conf)
    excludes, includes = parse_ignore_rules(excludes, includes)

    root = Path(source)
    files = set(root.glob("**/*"))

    flatten = lambda l: [item for sublist in l for item in sublist]
    excluded = set(flatten([root.glob(glob) for glob in excludes]))
    included = set(flatten([root.glob(glob) for glob in includes]))

    files = files - excluded | included
    files = [x for x in files if x.is_file()]

    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            zf.write(file, file.relative_to(source))


def extract_ignore_rules(conf):
    excludes = []
    includes = []

    functions = conf.get("functions", [])
    for function in functions:
        if type(function) is dict:
            name = list(function.keys())[0]
            data = function.get(name)
        else:
            name = function
            data = functions.get(name)

        package = data.get("package")
        if package is None:
            continue

        to_exclude = ["{}/{}".format(name, x) for x in package.get("exclude", [])]
        to_include = ["{}/{}".format(name, x) for x in package.get("include", [])]
        excludes.extend(to_exclude)
        includes.extend(to_include)

    return excludes, includes


def parse_ignore_rules(excludes, includes):
    for glob in excludes:
        if glob.startswith("!"):
            excludes.remove(glob)
            includes.append(glob[1:])

    excludes = list(set(excludes + DEFAULT_EXCLUDES))
    includes = list(set(includes))

    # convert dir/** to dir/**/* (adds files instead of dirs)
    excludes = [x + "/*" if x.endswith("*") else x for x in excludes]
    includes = [x + "/*" if x.endswith("*") else x for x in includes]

    return excludes, includes


def get_short_environment_name(environment):
    """
    Returns the short version of the environment name that matches the format that they
    are defined in the alfa sdk.
    """
    if _contains(environment, "dev"):
        return "dev"
    if _contains(environment, "test"):
        return "test"
    if _contains(environment, "acc"):
        return "acc"
    if _contains(environment, "prod"):
        return "prod"

    raise ValidationError(error="Invalid alfa environment.")


def _contains(string, substring, case_sensitive=False):
    if not case_sensitive and string and substring:
        string = string.lower()
        substring = substring.lower()
    return string and substring in string


def load_or_parse(data):
    try:
        data = open(data, "r").read()
    except:
        pass
    return json.loads(data)


#


def processify(func):
    """
    Decorator to run a function as a process. Be sure that every argument and the return value
    is serializable. The created process is joined, so the code does not run in parallel.
    Based on: https://github.com/dgerosa/processify.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        processing_pool = ProcessingPool(1)
        arguments = ([arg] for arg in args)
        result = None
        try:
            result = processing_pool.map(func, *arguments)
        finally:
            processing_pool.close()
            processing_pool.join()
            processing_pool.clear()
        return result[0]

    return wrapper
