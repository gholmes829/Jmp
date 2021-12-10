# Jmp

## Description
Navigate your filesystem with speeds never seen before. Given a set of regular expressions, `jmp` will intelligently search through your files and `cd` you into your intended directory. Instead of `cd Users/gholmes/Projects/Diviner/core/` (what a waste of time and energy), just input `jmp Diviner core` to achieve the same results. Arguments can be regular expressions and can "guide" the search to a final prediction.

## Intallation
Have a working installation of `Python 3`

\
Clone this repo:
```
$ git clone https://github.com/gholmes829/Jmp.git
```
\
Set proper path for wrappar and add line to terminal configuration file (.zshrc, .bashrc, etc):
```
$ echo -e "SCRIPT_DIR=\"$(pwd)/Jmp\"\n\n$(cat Jmp/jmp_wrapper.sh)" > Jmp/jmp_wrapper.sh; \
  echo "\nsource \"$(pwd)/Jmp/jmp_wrapper.sh\"" >> <YOUR TERMINAL CONFIG PATH>
```

## Usage
Basic usage is as follows
```
$ jmp <filename>
$ jmp <dirname>
```
\
Run the following to learn more about flags
```
$ jmp -h
```

Flags enable you to specify type of file to search, set search root path, silence output, and more.

Lastly, take note of function variations `jmpa` for absolute jump, `jmpf` for file jump, and `jmpd` for dir jump.
