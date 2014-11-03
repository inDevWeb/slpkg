#!/usr/bin/python
# -*- coding: utf-8 -*-

# greps.py file is part of slpkg.

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

# https://github.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os

from toolbar import status
from __metadata__ import lib_path
from splitting import split_package

from slack.slack_version import slack_ver


def repo_data(PACKAGES_TXT, step, repo):
    '''
    Grap data packages
    '''
    (name, location, size, unsize,
     rname, rlocation, rsize, runsize) = ([] for i in range(8))
    index, toolbar_width = 0, 700
    for line in PACKAGES_TXT.splitlines():
        index += 1
        toolbar_width = status(index, toolbar_width, step)
        if line.startswith("PACKAGE NAME"):
            name.append(line[15:].strip())
        if line.startswith("PACKAGE LOCATION"):
            location.append(line[21:].strip())
        if line.startswith("PACKAGE SIZE (compressed):  "):
            size.append(line[28:-2].strip())
        if line.startswith("PACKAGE SIZE (uncompressed):  "):
            unsize.append(line[30:-2].strip())
    if repo == "rlw":
        (rname,
         rlocation,
         rsize,
         runsize
         ) = rlw_filter(name, location, size, unsize)
    elif repo == "alien":
        (rname,
         rlocation,
         rsize,
         runsize
         ) = alien_filter(name, location, size, unsize)
    elif repo == "slacky":
        (rname,
         rlocation,
         rsize,
         runsize
         ) = slacky_filter(name, location, size, unsize)
    return [rname, rlocation, rsize, runsize]


def rlw_filter(name, location, size, unsize):
    '''
    Filter rlw repository data
    '''
    arch = os.uname()[4]
    if arch.startswith("i") and arch.endswith("86"):
        arch = "i486"
    (fname, flocation, fsize, funsize) = ([] for i in range(4))
    for n, l, s, u in zip(name, location, size, unsize):
        if arch in n:
            fname.append(n)
            flocation.append(l)
            fsize.append(s)
            funsize.append(u)
    return [fname, flocation, fsize, funsize]


def alien_filter(name, location, size, unsize):
    '''
    Filter alien repository data
    '''
    arch = os.uname()[4]
    path_pkg = "pkg64"
    if arch.startswith("i") and arch.endswith("86"):
        arch, path_pkg = "i486", "pkg"
    (fname, flocation, fsize, funsize) = ([] for i in range(4))
    for n, l, s, u in zip(name, location, size, unsize):
        loc = l.split("/")
        if arch in n and loc[-1] == slack_ver():
            fname.append(n)
            flocation.append(l)
            fsize.append(s)
            funsize.append(u)
        elif "noarch" in n and loc[-1] == slack_ver() and loc[-2] == path_pkg:
            fname.append(n)
            flocation.append(l)
            fsize.append(s)
            funsize.append(u)
    return [fname, flocation, fsize, funsize]


def slacky_filter(name, location, size, unsize):
    '''
    Filter slacky repository data
    but nothing to filter yet
    '''
    return name, location, size, unsize


def repo_requires(name, repo):
    '''
    Grap package requirements from alien repository
    '''
    if repo == "alien":
        lib = lib_path + "alien_repo/PACKAGES.TXT"
    elif repo == "slacky":
        lib = lib_path + "slacky_repo/PACKAGES.TXT"
    f = open(lib, "r")
    PACKAGES_TXT = f.read()
    f.close()
    for line in PACKAGES_TXT.splitlines():
        if line.startswith("PACKAGE NAME: "):
            pkg = line[14:].strip()
            alien_name = split_package(pkg)[0]
        if line.startswith("PACKAGE REQUIRED: "):
            if alien_name == name:
                return line[18:].strip().split(",")