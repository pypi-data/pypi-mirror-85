# MIT License
#
# Copyright (c) 2020 TheCoder777
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# system modules
import os
import shutil

# internal modules
from ..defines import paths
from ..defines.colors import RESET, BOLD, ERROR, SUCCESS


class User:
    def __init__(self, vals):
        # write all values to object
        self.uid, self.name, self.surname, self.nickname, self.email, self.unit, self.week, self.start_week, self.year, self.beginning_year, self.color_mode = vals

        # check user files everytime
        self.check_user_files()

    def check_user_files(self):
        """
        Create user directories and copy templates
        (Checkup for the user)
        """

        console = BOLD + "[USER CHECKUP] " + RESET
        user_dir = os.path.join(paths.USER_PATH, str(self.uid))
        # check user dir
        tocheck = user_dir
        if not os.path.exists(tocheck):
            print(console + ERROR + f"User diretory {tocheck} doesn't exist..." + RESET, end="")
            os.mkdir(tocheck)
            print(console + SUCCESS + "created!" + RESET)
        else:
            print(console + SUCCESS + "User directory found!" + RESET)

        # check todolist
        tocheck = os.path.join(paths.USER_PATH, str(self.uid), paths.TODOLIST_PATH)
        if not os.path.exists(tocheck):
            print(console + ERROR + "Todolist file doesn't exist..." + RESET, end="")
            print("from", paths.TODOLIST_TEMPLATE_PATH, "to", user_dir)
            shutil.copy2(paths.TODOLIST_TEMPLATE_PATH, os.path.join(user_dir, paths.TODOLIST_PATH))
            print(console + SUCCESS + "copied!" + RESET)
        else:
            print(console + SUCCESS + "User directory found!" + RESET)

    def update_all(self, values):
        self.uid, self.name, self.surname, self.nickname, self.email, self.unit, self.week, self.start_week, self.year, self.beginning_year, self.color_mode = values

    def update_defaults(self, week, start_week, year, unit, color_mode):
        self.week = week
        self.start_week = start_week
        self.year = year
        self.unit = unit
        self.color_mode = color_mode

    def update_color_mode(self, color_mode):
        self.color_mode = color_mode
