<h1 align="center">
  py-ftparchive
</h1>

<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/made%20with-blood,%20sweat,%20&amp%20tears-E760A4.svg" alt="Made with blood, sweat and tears">
  </a>
  <a href="https://github.com/LuzProject/py-ftparchive/graphs/contributors" target="_blank">
    <img src="https://img.shields.io/github/contributors/LuzProject/py-ftparchive.svg" alt="Contributors">
  </a>
  <a href="https://github.com/LuzProject/py-ftparchive/commits/main" target="_blank">
    <img src="https://img.shields.io/github/commit-activity/w/LuzProject/py-ftparchive.svg" alt="Commits">
  </a>
</p>

<p align="center">
    (Mostly) drop in replacement for `apt-ftparchive`, a tool for building Packages and Release files for APT repos written in pure Python.
</p>

## Features
1. Create a `Packages` file from a directory full of .debs
2. Create a `Release` file from a repo directory

## py-ftparchive -h output 

    usage: py-ftparchive [-h] [-v] {packages,release} ...

    positional arguments:
    {packages,release}  sub-command help
        packages          compile all deb files in a directory into a Packages file
        release           compile a release file

    options:
    -h, --help          show this help message and exit
    -v, --version       show current version and exit