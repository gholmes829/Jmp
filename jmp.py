"""
Author: Grant Holmes
Email: g.holmes429@gmail.com
Date Created: 12/09/2021
"""

import sys
import os.path as osp, os
import re
import argparse
from typing import Callable, List, Tuple
from functools import reduce
import operator
from enum import IntEnum
from json import load


ROOT_DIR = osp.dirname(osp.realpath(__file__))

def search(
        queue: List[Tuple[str, List[str], int]],
        search_cond: Callable[[str, str], bool],
        match_cond: Callable[[str, str], bool],
        blacklist: List[str],
    ) -> str:

    def process_file(f: str, origin: str, targets: List[str], depth: int) -> str:
        path = osp.join(origin, f)
        if match_cond(targets[0], path):
            if len(targets) - 1:  # there are more targets to search
                if search_cond(origin, f):
                    queue.append((path, targets[1:], depth - 1))
            elif not osp.isdir(path): return osp.dirname(path)  # no more targets and found file
            else: return path  # no more targets and found dir
        elif search_cond(origin, f): queue.append((path, targets, depth -1))

    while queue:
        origin, targets, depth = queue.pop(0)
        if not depth: return  # ran out of depth
        try: files = [f for f in os.listdir(origin) if not any(b.match(f) for b in blacklist)]
        except (PermissionError, FileNotFoundError): continue  # not allowed to access certain files, files like proc behave weird 
        for f in files:
            match = process_file(f, origin, targets, depth)
            if match: return match
        

def load_aliases():
    try:
        with open(osp.join(ROOT_DIR, 'aliases.json'), 'r') as f:
            return load(f)
    except FileNotFoundError: return {}


def load_blacklist():
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


Types = IntEnum('Types', 'Unspecified File Dir All', start=0)

def make_argparser():
    parser = argparse.ArgumentParser(description='Super powered cd!')
    parser.add_argument('--level', '-l', type=depth, default=-1, help='limit search depth')
    parser.add_argument('--begin', '-b', default=os.getcwd(), help='select root of search path')
    parser.add_argument('--silent', '-s', action='store_const', const=True, help='prevent normal stdout to console')
    parser.add_argument('--file', '-f', dest='flags', action='append_const', const=Types.File, help='specify to add file types to search')
    parser.add_argument('--dir', '-d', dest='flags', action='append_const', const=Types.Dir, help='specify to add dir types to search')
    parser.add_argument('regexes', nargs='+', help='arbitrary number of regexes to match against')
    return parser


def main() -> None:
    parser = make_argparser()
    try: args = parser.parse_args()
    except: sys.exit(1)

    aliases = load_aliases()
    blacklist = load_blacklist()
    regexes = [regex if regex not in aliases else aliases[regex] for regex in args.regexes]

    valid_type = {
        Types.Unspecified: lambda p: osp.exists(p),
        Types.File: lambda p: osp.isfile(p) and not osp.isdir(p),
        Types.Dir: lambda p: osp.isdir(p),
        Types.All: lambda p: osp.exists(p)
    }[reduce(operator.or_, args.flags or [], 0)]

    # specify which files should be explored
    def search_cond(origin: str, target: str) -> bool:
        return osp.isdir(osp.join(origin, target)) 

    # specify how a match should be determined
    def match_cond(target: str, f: str) -> bool:
        return re.match(target, osp.basename(f)) and valid_type(f)

    # run the search
    match = search([(args.begin, regexes, args.level)], search_cond, match_cond, blacklist)

    if match:
        print(match, flush=True)
        sys.exit(0)
    else:
        if not args.silent:
            print('Failed to find path.', flush=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
