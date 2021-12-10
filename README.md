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
Modify wrapper to set path:
```
echo -e "SCRIPT_DIR=\"$(pwd)/Jmp\"\n\n$(cat Jmp/jmp_wrapper.sh)" > Jmp/jmp_wrapper.sh
```
\
Add line to terminal configuration file (.zshrc, .bashrc, etc):
```
$ echo "\nsource \"$(pwd)/Jmp/jmp_wrapper.sh\"" >> <path to your config>
```

## Usage
Basic usage is as follows
```
$ jmp <file name>
$ jmp <dirname>
```
\
Run the following to learn more about flags
```
$ jmp -h
```
\
Also take note of variations `jmpa` for absolute jump, `jmpf` for file jump, and `jmpd` for dir jump.
