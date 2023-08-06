import os
import logging
import sys
import importlib
import inspect
from pathlib import Path
import argparse
from collections.abc import Mapping
import warnings

import yaml

from ploomber.spec.DAGSpec import DAGSpec
from ploomber.env.EnvDict import EnvDict
from ploomber.util.util import load_dotted_path


def process_arg(s):
    clean = None

    if s.startswith('--'):
        clean = s[2:]
    elif s.startswith('-'):
        clean = s[1:]
    else:
        clean = s

    return clean.replace('-', '_')


class CustomParser(argparse.ArgumentParser):
    """
    Most of our CLI commands operate on entry points, the CLI signature is
    defined by a few static arguments (they always appear when doing
    ploomber {cmd} --entry-point {entry} --help) and dynamic arguments
    (they are generated depending on the entry point). To support this, we
    have this CustomParser that distinguishes between static and dynamic args

    Once initialized, static args must be added using this as a context
    manager, only after this has happened, other arguments can be added using
    parser.add_argument.
    """
    def __init__(self, *args, **kwargs):
        self.DEFAULT_ENTRY_POINT = os.environ.get(
            'ENTRY_POINT') or 'pipeline.yaml'

        self.static_args = []
        self.finished_static_api = False
        self.in_context = False
        self.finished_init = False
        super().__init__(*args, **kwargs)

        self.add_argument('--log',
                          '-l',
                          help='Enables logging to stdout at the '
                          'specified level',
                          default=None)

        self.add_argument('--entry-point',
                          '-e',
                          help='Entry point(DAG), defaults to pipeline.yaml. '
                          'Replaced if there is an ENTRY_POINT env '
                          'variable defined',
                          default=self.DEFAULT_ENTRY_POINT)

        self.finished_init = True

    def parse_entry_point_value(self):
        """
        Returns the entry_point value pased without calling parse_args(),
        this is required to find env params to show, if we call parse_args()
        the CLI stops there and shows available params
        """
        index = None

        try:
            index = sys.argv.index('--entry-point')
        except ValueError:
            pass

        try:
            index = sys.argv.index('-e')
        except ValueError:
            pass

        return self.DEFAULT_ENTRY_POINT if index is None else sys.argv[index +
                                                                       1]

    def add_argument(self, *args, **kwargs):
        if not self.finished_static_api:
            if not self.in_context and self.finished_init:
                raise RuntimeError('Cannot add arguments until the static '
                                   'API has been declared')
            else:
                self.static_args.extend([process_arg(arg) for arg in args])
        return super().add_argument(*args, **kwargs)

    def __enter__(self):
        self.in_context = True
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.in_context = False
        self.finished_static_api = True

    def process_factory_dotted_path(self, dotted_path):
        """Parse a factory entry point, returns initialized dag and parsed args
        """
        entry = load_dotted_path(dotted_path, raise_=True)

        # add args using the function's signature
        required, _ = _add_args_from_callable(self, entry)

        # if entry point was decorated with @with_env, add arguments
        # to replace declared variables in env.yaml
        if hasattr(entry, '_env_dict'):
            _add_args_from_env_dict(self, entry._env_dict)

        args = self.parse_args()

        if hasattr(args, 'log'):
            if args.log is not None:
                logging.basicConfig(level=args.log.upper())

        # extract required (by using function signature) params from the cli
        # args
        kwargs = {key: getattr(args, key) for key in required}

        # env and function defaults replaced
        replaced = _args_to_replace_in_env(args, self.static_args)

        # TODO: add a way of test this by the parameters it will use to
        # call the function, have an aux function to get those then another
        # to execute, test using the first one
        dag = entry(**{**kwargs, **replaced})

        return dag, args


def _first_non_empty_line(doc):
    for line in doc.split('\n'):
        if line:
            return line.strip()


def _parse_doc(callable_):
    """
    Convert numpydoc docstring to a list of dictionaries
    """
    doc = callable_.__doc__

    # no docstring
    if doc is None:
        return {'params': {}, 'summary': None}

    # try to import numpydoc, if can't find it, just returnt the first line
    try:
        docscrape = importlib.import_module('numpydoc.docscrape')
    except ModuleNotFoundError:
        return {'params': {}, 'summary': _first_non_empty_line(doc)}

    doc_parsed = docscrape.NumpyDocString(doc)

    parameters = {
        p.name: {
            'desc': ' '.join(p.desc),
            'type': p.type
        }
        for p in doc_parsed['Parameters']
    }

    # docscrape returns one element per line
    summary = 'Docstring: {}'.format('\n'.join(doc_parsed['Summary']))

    return {'params': parameters, 'summary': summary}


def _args_to_replace_in_env(args, static_args):
    """
    Returns a dictionary with all extra cli parameters passed, all these must
    be parameters that part of the env or params (with no defaults) if
    entry point is a factory function
    """
    return {
        name: getattr(args, name)
        for name in dir(args) if not name.startswith('_')
        if getattr(args, name) is not None if name not in static_args
    }


def _add_args_from_env_dict(parser, env_dict):
    """
    Add one parameter to the args parser by taking a look at all values
    defined in an env dict object
    """
    # flatten keys from the env dictionary. e.g. from {'a': {'b': 1}} is
    # converted to {'a--b': 1}. This allows us to add cli args such as --a--b
    # to modify any key in the env. Note that we use double hyphens to have
    # an unambious section separator. Environments are commonly loaded from
    # YAML files. Keys in such files might contain hyphens/underscores, we
    # allow users to have those characters but double hyphens/underscores are
    # not permitted as they'd conflict with the CLI generation logic
    flat_env_dict = _flatten_dict(env_dict._data)

    for arg, val in flat_env_dict.items():
        parser.add_argument('--env--' + arg, help='Default: {}'.format(val))


def _parse_signature_from_callable(callable_):
    """
    Parse a callable signature, return a dictionary with
    {param_key: default_value} and a list of required parameters
    """
    sig = inspect.signature(callable_)

    required = [
        k for k, v in sig.parameters.items() if v.default == inspect._empty
    ]

    defaults = {
        k: v.default
        for k, v in sig.parameters.items() if v.default != inspect._empty
    }

    return required, defaults, sig.parameters


def get_desc(doc, arg):
    arg_data = doc['params'].get(arg)
    return None if arg_data is None else arg_data['desc']


def add_argument_kwargs(params, arg):
    """
    Build kwargs for parser.add_argument function
    """
    valid_hints = [int, float, str, bool]

    fn_default = params[arg].default
    fn_annotation = params[arg].annotation

    # special case, bool with default value becomes a flag
    if fn_annotation is bool and fn_default is not inspect._empty:
        kwargs = {'action': 'store_true' if not fn_default else 'store_false'}
    elif fn_annotation in valid_hints:
        kwargs = {'type': fn_annotation, 'default': fn_default}
    else:
        kwargs = {'default': fn_default}

    return kwargs


def _add_args_from_callable(parser, callable_):
    """
    Modifies an args parser to include parameters from a callable, adding
    parameters with default values as optional and parameters with no defaults
    as mandatory. Adds descriptions from parsing the callable's docstring

    It also adds the description from the docstring, if any

    Returns parsed args: required (list) and defaults (dict)
    """
    doc = _parse_doc(callable_)
    required, defaults, params = _parse_signature_from_callable(callable_)

    for arg, default in defaults.items():
        parser.add_argument('--' + arg,
                            help=get_desc(doc, arg),
                            **add_argument_kwargs(params, arg))

    for arg in required:
        parser.add_argument(arg,
                            help=get_desc(doc, arg),
                            **add_argument_kwargs(params, arg))

    if doc['summary']:
        desc = parser.description
        parser.description = '{}. {}'.format(desc, doc['summary'])

    return required, defaults


def _process_file_or_entry_point(parser):
    """
    Process a file entry point file or directory), returns the initialized dag
    and parsed args

    Parameters
    ----------
    parser : CustomParser
        CLI arg parser
    """
    if Path('env.yaml').exists():
        env_dict = EnvDict('env.yaml')
        _add_args_from_env_dict(parser, env_dict)

    args = parser.parse_args()

    if hasattr(args, 'log'):
        if args.log is not None:
            logging.basicConfig(level=args.log.upper())

    if Path(args.entry_point).is_dir():
        dag = DAGSpec.from_directory(args.entry_point).to_dag()
    else:
        with open(args.entry_point) as f:
            dag_dict = yaml.load(f, Loader=yaml.SafeLoader)

        # load env.yaml if there is one
        if Path('env.yaml').exists():
            env = EnvDict('env.yaml')
            # and replace keys depending on passed cli args
            replaced = _args_to_replace_in_env(args, parser.static_args)
            env = env._replace_flatten_keys(replaced)
            dag = DAGSpec(dag_dict, env=env).to_dag()
        else:
            dag = DAGSpec(dag_dict).to_dag()

    return dag, args


def _process_entry_point(parser, entry_point, static_args):
    """Process an entry point from the user

    Parameters
    ----------
    parser : CustomParser
        The cli parser object

    entry_point : str
        An entry point string, this can be either path to a file or a dotted
        path to a function that returns a DAG
    """
    help_cmd = '--help' in sys.argv or '-h' in sys.argv

    path = Path(entry_point)
    entry_file_exists = path.exists()
    entry_obj = load_dotted_path(entry_point, raise_=False)

    # if the file does not exist but the value has sufix yaml/yml, show a
    # warning because the last thing to try is to interpret it as a dotted
    # path and that's probably not what the user wants
    if not entry_file_exists and path.suffix in {'.yaml', '.yml'}:
        warnings.warn('Entry point value "{}" has extension "{}", which '
                      'suggests a spec file, but the file doesn\'t '
                      'exist'.format(entry_point, path.suffix))

    # even if the entry file is not a file nor a valid module, show the help
    # menu, but show a warning
    if (help_cmd and not entry_file_exists and not entry_obj):
        warnings.warn('Failed to load entry point "{}". It is not a file '
                      'nor a valid dotted path'.format(entry_point))

        args = parser.parse_args()

    # first check if the entry point is an existing file
    elif path.exists():
        dag, args = _process_file_or_entry_point(parser)
    # assume it's a dotted path to a factory
    else:
        dag, args = parser.process_factory_dotted_path(entry_point)

    return dag, args


# TODO: the next two functions are only used to override default behavior
# when using the jupyter extension, but they have to be integrated with the CLI
# to provide consistent behavior. The problem is that logic implemented
# in _process_file_or_entry_point and _process_factory_dotted_path
# also contains some CLI specific parts that we don't require here
def find_entry_point_type(entry_point):
    """

    Step 1: If not ENTRY_POINT is defined nor a value is passed, a default
    value is used (pipeline.yaml for CLI, recursive lookup for Jupyter client).
    If ENTRY_POINT is defined, this simply overrides the default value, but
    passing a value overrides the default value. Once the value is determined.

    Step 2: If value is a valid directory, DAG is loaded from such directory,
    if it's a file, it's loaded from that file (spec), finally, it's
    interpreted as a dotted path
    """
    if Path(entry_point).exists():
        if Path(entry_point).is_dir():
            return 'directory'
        else:
            return 'file'
    else:
        return 'dotted-path'


def load_entry_point(entry_point):
    type_ = find_entry_point_type(entry_point)

    if type_ == 'directory':
        spec = DAGSpec.from_directory(entry_point)
        path = Path(entry_point)
    elif type_ == 'file':
        spec = DAGSpec(entry_point)
        path = Path(entry_point).parent
    elif type_ == 'dotted-path':
        raise ValueError('dotted paths are currently unsupported')
        # fn = load_dotted_path(entry_point, raise_=True)
        # dag = fn()
    else:
        raise ValueError('Unknown entry point type {}'.format(type_))

    return spec, spec.to_dag(), path


def _custom_command(parser):
    """
    Parses an entry point, adding arguments by extracting them from the env.
    Returns a dag and the parsed args
    """
    entry_point = parser.parse_entry_point_value()
    dag, args = _process_entry_point(parser, entry_point, parser.static_args)
    return dag, args


def _flatten_dict(d, prefix=''):
    """
    Convert a nested dict: {'a': {'b': 1}} -> {'a--b': 1}
    """
    out = {}

    for k, v in d.items():
        if isinstance(v, Mapping):
            out = {**out, **_flatten_dict(v, prefix=prefix + k + '--')}
        else:
            out[prefix + k] = v

    return out
