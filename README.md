Jmp: the better cd
=
![Setup](https://img.shields.io/badge/Setup-easy-blue)
![Cross-Platform](https://img.shields.io/badge/Cross--Platform-true-blue)
![Cross-Platform](https://img.shields.io/badge/Documentation-100%25-brightgreen)
![License](https://img.shields.io/badge/Licence-MIT-green)

Ever used the `cd` command? You'll never touch that outdated thing again when you try `jmp`. Navigate your filesystem with unprecedented speed, agility, and dexterity **NEVER** seen before.

- Given a set of regular expressions, `jmp` will **intelligently** search through your files and `cd` you into your intended directory.
- Supports blacklisting and aliasing for **optimal** search performance.
- Offers entire `jmp` suite for **unmatched** convenience.

We don't live forever, so why waste a **single second** more of your life typing unnecessarily verbose paths on the command line?

<p align="center">
  <img src="https://user-images.githubusercontent.com/60802511/145676384-cf72411e-a00b-44ec-b835-f28681a6ae34.mp4" width="75%">
</p>

## Getting Started
In terms of dependencies, all you need is a working installation of [Python 3](https://www.python.org/downloads/). The scripts only utilizes standard libraries so no package installation needed.

\
Clone this repo:
```
$ git clone https://github.com/gholmes829/Jmp.git
```
\
Without changing folders from the place you ran `git clone`, run the following setup:
```
$ echo -e "SCRIPT_DIR=\"$(pwd)/Jmp\"\n\n$(cat Jmp/jmp_wrapper.sh)" > Jmp/jmp_wrapper.sh; \
  echo -e "\nsource \"$(pwd)/Jmp/jmp_wrapper.sh\"" >> <YOUR TERMINAL CONFIG PATH>; \
  source <YOUR TERMINAL CONFIG PATH>
```
where `<YOUR TERMINAL CONFIG PATH>` is the path to your `~/.bashrc`, `~/.zshrc`, or whatever else you use that gets run upon opening a terminal.

If you ever want to uninstall `jmp`, all you need to do is remove the `source <path to jmp_wrapper.sh>` that gets appended to your terminal config file.

## Basic Usage
Basic usage is as follows:
```
$ jmp expr_1 expr_2 ...expr_n
```
where each `expr_i` is a Python-compatible regex string (which includes basic text strings). The algorithm will perform a [breadth first search](https://en.wikipedia.org/wiki/Breadth-first_search) from the specified search root and perform a `cd` upon finding a match.
Take note of several details:
- By default, expressions are matched relative to the *start* of filenames
  - `jmp a` would match `a` and `ab` but not `ba`
  - You could easily `jmp` to somewhere ending with "a" with `jmp ".*a$"`

- By default, `expr_n` matches files in addition to directories
  - In the case of a non-directory match, it will `cd` you to the directory containing the matched file
  - If you want to **only** match directories, try `jmpd`, a simple alias for `jmp -d`

## Blacklisting
If you don't want to waste compute time on deep directories that you know don't contain anything useful, you can use the blacklist. Any blacklisted term will not be evaluated. For example, adding `"Documents"` into `blacklist.json` prevents us from searching for or inside of the documents folder. This allows for a faster experience.

## Aliasing
If you find yourself not wanting to refer to a directory's name every time, you can use aliases. You can modify `aliases.json` to include a key-value pair that transforms your input. For example, adding `"cc": "EECS 665"` to `aliases.json` would make it so `jmp cc` gets interpreted as `jmp EECS\ 665`. This allows for shorter commands that get you to where you want. 

## Flags and Jmp Suite
Learn more about flags and usage:
```
$ jmp -h
```

Flags include:
* `-b, --begin <str, path>` set root of search
* `-f, --file` specify that files (rather than dirs) should be searched for
* `-d, --dir` specify that dirs (rather than files) should be searched for
* `-l, --level <int, level>` search will now run until match found or until max depth reached
* `-s, --silent` indicate that failure to find path should not print a message


Take note of the function variations/ aliases that come with the `jmp` suite:
- `jmpa` runs `jmp` using root as the search root
- `jmps` runs `jmp` using the first argument as the search root
- `jmpf` allows only files to be matched by `expr_n`
- `jmpd` allows only dirs to be matched by `expr_n`

Since a major point of `jmp` is for convenience and to save time, it would make sense to use `jmpd` rather than `jmp -d`, for example.

## Tips and Tricks
If you excessively shorten your expressions, it is very likely you'll end up in a lexically similiar location that is different from what you intended. Using multiple strategic expressions will conversely speed up the operation by narrowing the search space.

Considering the absolute worst case in terms of convenience, we can see that `jmp` converges to `cd` as each expression could be the next folder that you would need to `cd` to (e.g. `jmp Projects Diviner core` vs `cd Projects/Diviner/core`). In other words, `jmp` is *at least* as convenient as `cd` and has potential to be a lot, lot better. However, if you try to drop too much information, you may lose accuracy. Try to use the minimal number of expressions while still retaining substrings or patterns unique to your target location.

Optionally, you can rename the `jmp` command to something else. Setting `alias dc=jmp` in your terminal config file will now let you run `dc D c` (from the example above), where `dc` is now `cd`'s evil nemesis.

Desperately need a file but don't remember the full name or path? Try `jmpa ".*<snippet of name you remember>.*"`.

## Deeper Customization
All `jmp_wrapper.sh` does is call and handle output from `jmp.py`. `jmp.py` is pretty succinct and modular, so it shouldn't be too hard to modify the constraints for searching, matching, or even the traversal algorithm itself.

## Contributing
Please feel free to reach out if you're interested in contributing or have ideas for features!

## License
This project is licensed under the MIT License - see the LICENSE file for details
