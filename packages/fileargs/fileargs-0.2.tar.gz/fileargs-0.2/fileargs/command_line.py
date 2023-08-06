from jinja2 import Environment
import json
import os
import yaml
import argparse
import sys
from configparser import ConfigParser
import logging

def is_valid_file(parser, arg):
    """check if file exists"""
    if not os.path.exists(arg):
        parser.error("The given parameter file %s does not exist!" % arg)
    else:
        return arg


def read_json(filename):
    """reads file and returns dict"""
    with open(filename, 'r') as fp:
        vars = json.load(fp)
    return vars

def read_yaml(filename):
    """reads file and returns dict"""
    with open(filename, 'r') as fp:
        vars = yaml.load(fp, Loader=yaml.SafeLoader)        
    return vars

def read_ini(filename):
    """reads file and returns dict"""
    parser = ConfigParser()
    parser.read(filename)
    vars = {section: dict(parser.items(section)) for section in parser.sections()}
    return vars

def load_param_files(params):
    """read variables from all config files"""
    combined_vars = {}
    readers = {
        "json": read_json, 
        "yaml": read_yaml,
        "ini": read_ini
    }
    for filename in params:
        vars = None
        for format, reader in readers.items():
            try:
                vars = reader(filename)
                logging.debug("loaded file '%s' using '%s' format." % (filename, format))
            except:
                pass        
        if vars:
            combined_vars.update(vars)
        else:
            logging.error("could not find suitable reader for file '%s'" % filename)
            return None

    return combined_vars


def render_command(command, vars):
    env = Environment()
    template = env.from_string(" ".join(command))
    command = template.render(**vars)
    logging.debug("executing command '%s'" % command)
    return command


def main():
    """fileargs - read config file and executes command after template substitution"""

    parser = argparse.ArgumentParser()
    parser.add_argument('command', metavar="COMMAND", nargs='*')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')    
    parser.add_argument("-p", '--params', dest="params", default="params.yaml",
                    nargs='+', metavar="PARAMS",
                    type=lambda x: is_valid_file(parser, x))    
    args = parser.parse_args()
    
    logging.basicConfig(level={True: logging.DEBUG, False: logging.INFO}[args.verbose])

    # load all config vars
    vars = load_param_files(args.params)
    if not vars:
        sys.exit(1)
    
    # render command
    command = render_command(args.command, vars)

    # run command
    sys.exit(os.system(command))






if __name__ == "__main__":
    main()
