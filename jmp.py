"""
Author: Grant Holmes
Email: g.holmes429@gmail.com
"""

import sys
import os.path as osp, os
from pathlib import Path
import re
import argparse
from typing import AnyStr, Callable, Dict, List, Tuple, MutableSet, Pattern, Union
from functools import reduce
from enum import IntEnum
from json import load


ROOT_DIR = osp.dirname(osp.realpath(__file__))

def search(
        queue: List[Tuple[str, List[str], int]],
        search_cond: Callable[[str], bool],
        match_cond: Callable[[str, str], bool],
        blacklist: List[str],
    ) -> str:
    """Breadth first search traversal of file system, attempts to find a match given constraints."""

    def process_file(path: str, targets: List[str], depth: int) -> str:
        """Determine whether a file is a match, should be searched, both, or neither."""
        if match_cond(path, targets[0]):
            if len(targets) - 1:  # if we are yet to reach the final target expr
                if search_cond(path):  # lets add this path to be expanded and searched
                    queue.append((path, targets[1:], depth - 1))
            elif not osp.isdir(path):  # lets return parent dir of file as the match
                return osp.dirname(path)
            else:  # lets return the path which we know to be a directory
                return path
        elif search_cond(path):  # path is not a match but should be expanded and searched
            queue.append((path, targets, depth - 1))

    # main search loop
    while queue:
        origin, targets, depth = queue.pop(0)
        if not depth: return  # we exhausted allocated depth, give up
        try: files = [f for f in os.listdir(origin) if not any(b.match(f) for b in blacklist)]
        except (PermissionError, FileNotFoundError): continue  # might not be able or allowed to access certain files, skip
        for f in files:
            match = process_file(osp.join(origin, f), targets, depth)
            if match: return match  # if a match is found, we are done
        

def load_aliases() -> Dict[str, str]:
    try:
        with open(osp.join(ROOT_DIR, 'aliases.json'), 'r') as f:
            return load(f)
    except FileNotFoundError: return {}


def load_blacklist() -> MutableSet[Pattern[AnyStr]]:
    try:
        with open(osp.join(ROOT_DIR, 'blacklist.json'), 'r') as f:
            return {re.compile(b) for b in load(f)}
    except FileNotFoundError: return set()


def depth(arg: str) -> int:
    """Initializer for -l argparser argument."""
    try:
        d = int(arg)
        assert d > 0 or d == -1
        return d
    except (TypeError, AssertionError):
        raise argparse.ArgumentTypeError('Depth must be greater than 0 or -1')

def get_safe_cwd() -> Union[str, Exception]:
    """Handles edge case where users run jmp from deleted directory"""
    try:
        return os.getcwd()
    except PermissionError as err:
        return err

Types = IntEnum('Types', 'Unspecified File Dir All', start=0)

def make_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Super powered cd!')
    parser.add_argument('--level', '-l', type=depth, default=-1, help='limit search depth')
    parser.add_argument('--begin', '-b', default=get_safe_cwd(), help='select root of search path')
    parser.add_argument('--silent', '-s', action='store_const', const=True, help='prevent normal stdout to console')
    parser.add_argument('--partial', '-p', action='store_const', const=True, help='modify match condition to allow for mid string regex match')
    parser.add_argument('--file', '-f', dest='flags', action='append_const', const=Types.File, help='specify to add file types to search')
    parser.add_argument('--dir', '-d', dest='flags', action='append_const', const=Types.Dir, help='specify to add dir types to search')
    parser.add_argument('regexes', nargs='*', help='arbitrary number of regexes to match against')
    return parser


def main() -> None:
    parser = make_argparser()
    try: args = parser.parse_args()
    except: sys.exit(1)
    if not args.regexes:
        print(str(Path.home()), flush=True)
        sys.exit(0)

    aliases = load_aliases()
    blacklist = load_blacklist()
    regexes = [regex if regex not in aliases else aliases[regex] for regex in args.regexes]
    begin = args.begin
    if isinstance(begin, Exception):
        raise begin

    backwards_ptn = re.compile(r'[.][.]([/][.][.])*[/]?')

    # initial parsing
    backwards_ptn_match = re.fullmatch(backwards_ptn, regexes[0])
    if len(regexes) == 1 and regexes[0] == '/':
        print('/', flush=True)
        sys.exit(0)
    elif regexes[0] == '/':
        begin = '/'
        regexes = regexes[1:]
    elif len(regexes) == 1 and regexes[0] == str(Path.home()):
        print(str(Path.home()), flush=True)
        sys.exit(0)
    elif regexes[0] == str(Path.home()):  # implies > 1 arg
        begin = osp.abspath(str(Path.home()))
        regexes = regexes[1:]
    elif len(regexes) == 1 and backwards_ptn_match:
        print(regexes[0], flush=True)
        sys.exit(0)
    elif backwards_ptn_match:
        num_back = regexes[0].count('..')
        for _ in range(num_back): begin = osp.dirname(begin)
        regexes = regexes[1:]

    search_match_fn = re.search if args.partial else re.match

    # splits on / to add support for tab completion
    regexes = [checkpoint for regex in regexes for checkpoint in regex.split('/')]

    valid_type = {
        Types.Unspecified: lambda p: osp.exists(p),
        Types.File: lambda p: osp.isfile(p) and not osp.isdir(p),
        Types.Dir: lambda p: osp.isdir(p),
        Types.All: lambda p: osp.exists(p)
    }[reduce(lambda a, b: a | b, args.flags or [], 0)]

    # specify which files should be explored
    def search_cond(path: str) -> bool:
        return osp.isdir(path) 

    # specify how a match should be determined
    def match_cond(path: str, target: str) -> bool:
        try:
            return search_match_fn(target, osp.basename(path)) and valid_type(path)
        except re.error as re_err:
            print(f'Invalid pattern for "{re_err.pattern}": {re_err.args[0]}.', flush=True)
            sys.exit(1)

    # run the search
    match = search([(begin, regexes, args.level)], search_cond, match_cond, blacklist)

    if match:
        print(match, flush=True)
        sys.exit(0)
    elif not args.silent:
        print('Failed to find path.', flush=True)
    
    sys.exit(1)  # a successful search would have already exited prior to this


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
