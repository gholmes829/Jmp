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
Add line to terminal configuration file (.zshrc, .bashrc, etc):
```
source <path to repo>/jmp_wrapper.sh
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
