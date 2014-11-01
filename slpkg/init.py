#!/usr/bin/python
# -*- coding: utf-8 -*-

# init.py file is part of slpkg.

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
import sys

from url_read import URL
from file_size import FileSize
from __metadata__ import log_path, lib_path

from slack.slack_version import slack_ver


class Initialization(object):

    def __init__(self):
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        if not os.path.exists(lib_path):
            os.mkdir(lib_path)

    def sbo(self):
        '''
        Creating sbo local library
        '''
        log = log_path + "sbo/"
        lib = lib_path + "sbo_repo/"
        lib_file = "SLACKBUILDS.TXT"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        packages_txt = ("http://slackbuilds.org/slackbuilds/{0}/{1}".format(
            slack_ver(), lib_file))
        changelog_txt = ("http://slackbuilds.org/slackbuilds/{0}/{1}".format(
            slack_ver(), log_file))
        self.write(lib, lib_file, packages_txt)
        self.write(log, log_file, changelog_txt)
        self.remote(log, log_file, changelog_txt, lib, lib_file, packages_txt)

    def rlw(self):
        '''
        Creating rlw local library
        '''
        log = log_path + "rlw/"
        lib = lib_path + "rlw_repo/"
        lib_file = "PACKAGES.TXT"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        packages_txt = ("http://rlworkman.net/pkgs/{0}/{1}".format(
            slack_ver(), lib_file))
        changelog_txt = ("http://rlworkman.net/pkgs/{0}/{1}".format(
            slack_ver(), log_file))
        self.write(lib, lib_file, packages_txt)
        self.write(log, log_file, changelog_txt)
        self.remote(log, log_file, changelog_txt, lib, lib_file, packages_txt)

    def alien(self):
        '''
        Creating alien local library
        '''
        log = log_path + "alien/"
        lib = lib_path + "alien_repo/"
        lib_file = "PACKAGES.TXT"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        packages_txt = ("http://www.slackware.com/~alien/slackbuilds/"
                        "{0}".format(lib_file))
        changelog_txt = ("http://www.slackware.com/~alien/slackbuilds/"
                         "{0}".format(log_file))
        self.write(lib, lib_file, packages_txt)
        self.write(log, log_file, changelog_txt)
        self.remote(log, log_file, changelog_txt, lib, lib_file, packages_txt)

    @staticmethod
    def write(path, files, file_url):
        '''
        Read SLACKBUILDS.TXT from slackbuilds.org and write in
        /var/lib/slpkg/sbo_repo directory if not exist
        '''
        if not os.path.isfile(path + files):
            print("\nslpkg ...initialization")
            sys.stdout.write(files + " read ...")
            sys.stdout.flush()
            PACKAGES_TXT = URL(file_url).reading()
            sys.stdout.write("Done\n")
            with open("{0}{1}".format(path, files), "w") as f:
                f.write(PACKAGES_TXT)
                f.close()
                print("File {0} created in {1}".format(files, path))

    @staticmethod
    def remote(*args):
        '''
        args[0]=log, args[1]=log_file, arg[2]=changelog_txt
        args[3]=lib, args[4]=lib_file, arg[5]=packages_txt

        If the two files differ in size delete and replaced with new
        We take the size of ChangeLog.txt from the server and locally
        '''
        server = FileSize(args[2]).server()
        local = FileSize(args[0] + args[1]).local()
        if server != local:
            os.remove("{0}{1}".format(args[3], args[4]))
            os.remove("{0}{1}".format(args[0], args[1]))
            print("\nNEWS in " + args[1])
            print("slpkg ...initialization")
            sys.stdout.write("Files re-created ...")
            sys.stdout.flush()
            PACKAGES_TXT = URL(args[5]).reading()
            CHANGELOG_TXT = URL(args[2]).reading()
            with open("{0}{1}".format(args[3], args[4]), "w") as f:
                f.write(PACKAGES_TXT)
                f.close()
            with open("{0}{1}".format(args[0], args[1]), "w") as f:
                f.write(CHANGELOG_TXT)
                f.close()
            sys.stdout.write("Done\n")
