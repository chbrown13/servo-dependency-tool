# Cargo Upgrade Service Project
NC State CSC517: Object-Oriented Design and Development

Chris Brown (dcbrow10@ncsu.edu)  
Bradford Ingersoll (bingers@ncsu.edu)  
Qiufeng Yu (qyu4@ncsu.edu)

The **Servo Dependency Tool** is a set of python scripts that automatically upgrades [Cargo](http://doc.crates.io/index.html) dependencies for the Servo web browser engine (Github page: https://github.com/servo/servo).

## Background Information
[Servo](https://github.com/servo/servo) is a prototype web browser engine written in the Rust language. It is currently developed on 64bit OS X, 64bit Linux, and Android. Servo depends on numerous other Rust libraries that are published on [the package manager crates.io](https://crates.io/). There are no notifications for when packages are updated; it's up to developers to keep track of when they need to upgrade their dependencies. The goal of the Servo Dependency Tool is to automatically upgrade Servo's dependencies whenever new versions are released.










Issue Tracker: https://github.com/servo/servo/issues/15600

Dependency Tool Wiki: https://github.com/servo/servo/wiki/Cargo-upgrade-service-project
