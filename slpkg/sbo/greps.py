#!/usr/bin/python
# -*- coding: utf-8 -*-

# greps.py

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

# https://github.com/dslackw/slpkg

# This program is free software: you can redistribute it and/or modify
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

from url_read import url_read
from __metadata__ import arch, lib_path

def sbo_source_dwn(name):
    '''
    Grep sources downloads links
    '''
    if arch == "x86_64":
        for line in open(lib_path + "sbo_repo/SLACKBUILDS.TXT", "r"):
            if arch == "x86_64":
                if line.startswith("SLACKBUILD NAME: "):
                    sbo_name = line[17:].strip()
                if line.startswith("SLACKBUILD DOWNLOAD_x86_64: "):
                    if sbo_name == name:
                        if line[28:].strip():
                            return line[28:].strip()
    for line in open(lib_path + "sbo_repo/SLACKBUILDS.TXT", "r"):
        if line.startswith("SLACKBUILD NAME: "):
            sbo_name = line[17:].strip()
        if line.startswith("SLACKBUILD DOWNLOAD: "):
            if sbo_name == name:
                return line[21:].strip() 
        
def sbo_requires_pkg(sbo_url, name):
    '''
    Grep package requirements
    '''
    read_info = url_read(sbo_url + name + ".info")
    for line in read_info.splitlines():
        if line.startswith("REQUIRES=\""):
            return line[10:-1].strip().split()

def sbo_version_pkg(name):
    '''
    Grep package verion
    '''
    for line in open(lib_path + "sbo_repo/SLACKBUILDS.TXT", "r"):
        if line.startswith("SLACKBUILD NAME: "):
            sbo_name = line[17:].strip()
        if line.startswith("SLACKBUILD VERSION: "):
            if sbo_name == name:
                return line[20:].strip()