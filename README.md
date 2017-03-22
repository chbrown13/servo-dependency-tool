# Cargo Upgrade Service Project
NC State CSC517: Object-Oriented Design and Development

Chris Brown (dcbrow10@ncsu.edu)  
Bradford Ingersoll (bingers@ncsu.edu)  
Qiufeng Yu (qyu4@ncsu.edu)

The **Servo Dependency Tool** is a set of python scripts that automatically upgrades [Cargo](http://doc.crates.io/index.html) dependencies for the Servo web browser engine (Github page: https://github.com/servo/servo).

### Video:
[![Demo Video](https://img.youtube.com/vi/-xS-6JY2o_o/0.jpg)](https://www.youtube.com/watch?v=-xS-6JY2o_o)

## Background Information
[Servo](https://github.com/servo/servo) is a prototype web browser engine written in the Rust language. It is currently developed on 64bit OS X, 64bit Linux, and Android. Servo depends on numerous other Rust libraries that are published on [the package manager crates.io](https://crates.io/). There are no notifications for when packages are updated; it's up to developers to keep track of when they need to upgrade their dependencies. The goal of the Servo Dependency Tool is to automatically upgrade Servo's dependencies whenever new versions are released.

## Installation
### Prerequisites
- [Servo web engine](https://github.com/servo/servo)
- [Python3](https://www.python.org/download/releases/3.0/)
### Installing GitPython and github3.py
The Servo Dependency Tool requires two external libraries ([GitPython](https://github.com/gitpython-developers/GitPython) and [github3.py](https://github.com/sigmavirus24/github3.py)) in order to interact with the Servo github, push lastest dependencies and open pull requests.
- Install GitPython
```
     python3 -m pip install gitpython
```
- Install github3.py
```
     python3 -m pip install github3.py
```
## Running
In order to run the tool, first make a local clone of the [Servo](https://github.com/servo/servo) repository, and then run the main driver file: **servo_dependency_tool.py**.
```
     python3 servo_dependency_tool.py
`````
The tool will first do a git pull command to get the latest fork of the Servo repository, then it wil create a new branch on the local clone and update all the dependencies. Finaly, it will open a new pull request against Servo's github repository from our local fork. 

The lock file looks something like this:
```
[root]
name = "webvr_traits"
version = "0.0.1"
dependencies = [
 "ipc-channel 0.7.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "msg 0.0.1",
 "rust-webvr 0.2.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "serde 0.9.7 (registry+https://github.com/rust-lang/crates.io-index)",
 "serde_derive 0.9.7 (registry+https://github.com/rust-lang/crates.io-index)",
]

[[package]]
name = "adler32"
version = "0.3.0"
source = "registry+https://github.com/rust-lang/crates.io-index"

[[package]]
name = "aho-corasick"
version = "0.6.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
dependencies = [
 "memchr 1.0.1 (registry+https://github.com/rust-lang/crates.io-index)",
]

[[package]]
name = "alloc-no-stdlib"
version = "1.2.0"
source = "registry+https://github.com/rust-lang/crates.io-index"

[[package]]
name = "android_glue"
version = "0.2.1"
source = "registry+https://github.com/rust-lang/crates.io-index"

[[package]]
name = "android_injected_glue"
version = "0.2.1"
source = "git+https://github.com/mmatyas/android-rs-injected-glue#d3223d1273d0dafcf06d6a6405fedfffbf257300"

[[package]]
name = "angle"
version = "0.1.2"
source = "git+https://github.com/servo/angle?branch=servo#99128001400771ee9c8a74dcf54cf6fe11b1e532"
dependencies = [
 "cmake 0.1.20 (registry+https://github.com/rust-lang/crates.io-index)",
 "libc 0.2.20 (registry+https://github.com/rust-lang/crates.io-index)",
]

[[package]]
name = "ansi_term"
version = "0.9.0"
source = "registry+https://github.com/rust-lang/crates.io-index"

[[package]]
name = "app_units"
version = "0.4.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
dependencies = [
 "heapsize 0.3.8 (registry+https://github.com/rust-lang/crates.io-index)",
 "num-traits 0.1.36 (registry+https://github.com/rust-lang/crates.io-index)",
 "rustc-serialize 0.3.22 (registry+https://github.com/rust-lang/crates.io-index)",
 "serde 0.9.7 (registry+https://github.com/rust-lang/crates.io-index)",
]

[[package]]
name = "arrayvec"
version = "0.3.20"
source = "registry+https://github.com/rust-lang/crates.io-index"
dependencies = [
 "nodrop 0.1.8 (registry+https://github.com/rust-lang/crates.io-index)",
 "odds 0.2.25 (registry+https://github.com/rust-lang/crates.io-index)",
]

[[package]]
name = "aster"
version = "0.38.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
dependencies = [
 "syntex_syntax 0.54.0 (registry+https://github.com/rust-lang/crates.io-index)",
]

[[package]]
name = "atomic_refcell"
version = "0.1.0"
source = "registry+https://github.com/rust-lang/crates.io-index"

[[package]]
name = "audio-video-metadata"
version = "0.1.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
dependencies = [
 "mp3-metadata 0.2.3 (registry+https://github.com/rust-lang/crates.io-index)",
 "mp4parse 0.5.1 (registry+https://github.com/rust-lang/crates.io-index)",
 "ogg_metadata 0.3.0 (registry+https://github.com/rust-lang/crates.io-index)",
]

[[package]]
name = "azure"
version = "0.14.0"
source = "git+https://github.com/servo/rust-azure#07a57c4b32cd111cbc4ee1ff80a98a3f3ec3fbec"
dependencies = [
 "cmake 0.1.20 (registry+https://github.com/rust-lang/crates.io-index)",
 "core-foundation 0.3.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "core-graphics 0.7.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "core-text 4.0.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "euclid 0.11.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "freetype 0.2.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "libc 0.2.20 (registry+https://github.com/rust-lang/crates.io-index)",
 "servo-egl 0.2.1 (registry+https://github.com/rust-lang/crates.io-index)",
 "servo-freetype-sys 4.0.3 (registry+https://github.com/rust-lang/crates.io-index)",
 "servo-skia 0.30000003.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "x11 2.12.1 (registry+https://github.com/rust-lang/crates.io-index)",
]

[[package]]
name = "backtrace"
version = "0.3.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
dependencies = [
 "backtrace-sys 0.1.10 (registry+https://github.com/rust-lang/crates.io-index)",
 "cfg-if 0.1.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "dbghelp-sys 0.2.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "kernel32-sys 0.2.2 (registry+https://github.com/rust-lang/crates.io-index)",
 "libc 0.2.20 (registry+https://github.com/rust-lang/crates.io-index)",
 "rustc-demangle 0.1.3 (registry+https://github.com/rust-lang/crates.io-index)",
 "winapi 0.2.8 (registry+https://github.com/rust-lang/crates.io-index)",
]

[[package]]
name = "backtrace-sys"
version = "0.1.10"
source = "registry+https://github.com/rust-lang/crates.io-index"
dependencies = [
 "gcc 0.3.43 (registry+https://github.com/rust-lang/crates.io-index)",
 "libc 0.2.20 (registry+https://github.com/rust-lang/crates.io-index)",
]

[[package]]
name = "bincode"
version = "1.0.0-alpha2"
source = "registry+https://github.com/rust-lang/crates.io-index"
dependencies = [
 "byteorder 1.0.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "num-traits 0.1.36 (registry+https://github.com/rust-lang/crates.io-index)",
 "serde 0.9.7 (registry+https://github.com/rust-lang/crates.io-index)",
]

[[package]]
name = "bindgen"
version = "0.22.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
dependencies = [
 "aster 0.38.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "cexpr 0.2.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "cfg-if 0.1.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "clang-sys 0.14.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "clap 2.20.5 (registry+https://github.com/rust-lang/crates.io-index)",
 "env_logger 0.4.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "lazy_static 0.2.2 (registry+https://github.com/rust-lang/crates.io-index)",
 "log 0.3.6 (registry+https://github.com/rust-lang/crates.io-index)",
 "quasi 0.29.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "quasi_codegen 0.29.0 (registry+https://github.com/rust-lang/crates.io-index)",
 "regex 0.2.1 (registry+https://github.com/rust-lang/crates.io-index)",
 "rustc-serialize 0.3.22 (registry+https://github.com/rust-lang/crates.io-index)",
 "syntex_syntax 0.54.0 (registry+https://github.com/rust-lang/crates.io-index)",
]

[[package]]
name = "bit-set"
version = "0.4.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
dependencies = [
 "bit-vec 0.4.3 (registry+https://github.com/rust-lang/crates.io-index)",
]

[[package]]
name = "bit-vec"
version = "0.4.3"
source = "registry+https://github.com/rust-lang/crates.io-index"

[[package]]
name = "bitflags"
version = "0.7.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
]
```
The TOML file looks something like this:
```
[package]
name = "cargo-toml"
authors = ["Q",
           "Bradford",
           "Chris"]

version = "2.3"

description = "This is a test cargo.toml file"
readme = "README.md"
keywords = ["cargo", "cargo-subcommand", "cli", "dependencies", "crates"]
license = ""

documentation = "https://github.com/chbrown13/servo-dependency-tool"
homepage = "https://github.com/chbrown13/servo-dependency-tool"
repository = "https://github.com/chbrown13/servo-dependency-tool"

[[bin]]
name = "cargo-list"
path = "path/to/bin"

[dependencies]
servo = "0.0.0"
toml = "0.0"
rustc-serialize = "0"
```
**For more detailed instructions on how to use this tool, please click on the video on the top.**

## Issue Tracker: https://github.com/servo/servo/issues/15600
## Servo Wiki page: https://github.com/servo/servo/wiki/Cargo-upgrade-service-project
