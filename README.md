# Cargo Upgrade Service Project
NC State CSC517: Object-Oriented Design and Development

Chris Brown (dcbrow10@ncsu.edu)  
Bradford Ingersoll (bingers@ncsu.edu)  
Qiufeng Yu (qyu4@ncsu.edu)

The **Servo Dependency Tool** is a set of python scripts that automatically upgrades [Cargo](http://doc.crates.io/index.html) dependencies for the Servo web browser engine (Github page: https://github.com/servo/servo).

## Video:
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
In order to run the tool, first make a local clone of the [Servo](https://github.com/servo/servo) repository
```
     git clone https://github.com/servo/servo.git
```
and then run the main driver file: **servo_dependency_tool.py**.
```
     python3 servo_dependency_tool.py
`````
The tool will first do a git pull command to get the latest fork of the Servo repository, then it wil create a new branch on the local clone and update all the dependencies. Finaly, it will open a new pull request against Servo's github repository from our local fork.

**For more detailed instructions on how to use this tool, please click on the video on the top.**

[Issue Tracker](https://github.com/servo/servo/issues/15600)

[Servo Wiki page](https://github.com/servo/servo/wiki/Cargo-upgrade-service-project)
