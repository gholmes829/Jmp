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

def search(queue: List[Tuple[str, List[str], int]],
            search_cond: Callable[[str, str], bool],
            match_cond: Callable[[str, str], bool],
            blacklist: List[str],
        ) -> None:
    """
    Breadth first search through files.
    search_cond determines what gets added to search queue
    match_cond determines whether a file should be considered as a final match
    """
    while queue:
        origin, targets, depth = queue.pop(0)
        if not depth: return  # ran out of depth
        # gen files and filter out those that match blacklist patterns
        try: files = [f for f in os.listdir(origin) if not any(b.match(f) for b in blacklist)]
        except PermissionError: continue  # not allowed to access certain files
        for f in files:
            path = osp.join(origin, f)
            if match_cond(targets[0], path):
                if len(targets) - 1:  # there are more targets to search
                    if search_cond(origin, f):
                        queue.append((path, targets[1:], depth - 1))
                else:  # matched last target!
                    if not osp.isdir(path):
                        path = osp.dirname(path)
                    print(path, flush=True)
                    sys.exit(0)
            elif search_cond(origin, f): queue.append((path, targets, depth -1))


def depth(arg: str) -> int:
    """Initializer for -l argparser argument."""
    try:
        d = int(arg)
        assert d > 0 or d == -1
        return d
    except (TypeError, AssertionError):
        raise argparse.ArgumentTypeError('Depth must be greater than 0 or -1')


Types = IntEnum('Types', 'Unspecified File Dir All', start=0)

def main() -> None:
    parser = argparse.ArgumentParser(description='Super powered cd!')
    parser.add_argument('--level', '-l', type=depth, default=-1, help='limit search depth')
    parser.add_argument('--begin', '-b', default=os.getcwd(), help='select root of search path')
    parser.add_argument('--silent', '-s', action='store_const', const=True, help='prevent normal stdout to console')
    parser.add_argument('--file', '-f', dest='flags', action='append_const', const=Types.File, help='specify to add file types to search')
    parser.add_argument('--dir', '-d', dest='flags', action='append_const', const=Types.Dir, help='specify to add dir types to search')
    parser.add_argument('regexes', nargs='+', help='arbitrary number of regexes to match against')

    try: args = parser.parse_args()
    except: sys.exit(1)

    try:
        with open(osp.join(ROOT_DIR, 'aliases.json'), 'r') as f:
            aliases = load(f)
    except FileNotFoundError: aliases = {}
    regexes = [regex if regex not in aliases else aliases[regex] for regex in args.regexes]

    try:
        with open(osp.join(ROOT_DIR, 'blacklist.json'), 'r') as f:
            blacklist = {re.compile(b) for b in load(f)}
    except FileNotFoundError: blacklist = []

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

    # start the search
    search([(args.begin, regexes, args.level)], search_cond, match_cond, blacklist)

    if not args.silent:  # a successful search would have already exited by this point
        print('Failed to find path.', flush=True)

    sys.exit(1)

if __name__ == '__main__':
    main()
