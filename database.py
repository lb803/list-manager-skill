#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Luca Baffa - lb803@mailbox.org

import json
from os.path import dirname, join

class Database:
    """
    This module manages the data.json file where items and lists 
    are stored.

    Sections:
        File handling   take care of read / write operations
        Checks          methods to assert specific conditions
        Read            methods to read from data.json
        Add             methods to write to data.json
        Del             methods to remove data from data.json
    """

    def __init__(self):
        self.JSON_PATH = join(dirname(__file__), 'data.json')
        try:
            # Load list data from data.json
            self.json_data = self.read_data()
        except FileNotFoundError:
            # If file not found, create an empty data.json
            self.json_data = {}
            self.write_data()

    ## FILE HANDLING
    def read_data(self):
        with open(self.JSON_PATH, 'r') as json_file:
            return json.load(json_file)

    def write_data(self):
        with open(self.JSON_PATH, 'w') as json_file:
            json.dump(self.json_data, json_file)

    ## CHECKS
    def item_exists(self, list, item):
        return True if item in self.json_data[list] else False

    def no_lists(self):
        return True if len(list(self.json_data.keys())) == 0 else False

    def list_empty(self, list):
        if len(self.json_data.get(list)) == 0:
            return True
        else:
            return False

    def list_exists(self, list):
        return True if list in self.json_data.keys() else False

    ## READ
    def read_items(self, list):
        return self.json_data.get(list)

    def read_lists(self):
        return list(self.json_data.keys())

    ## ADD
    def add_item(self, list, item):
        self.json_data[list].append(item)
        self.write_data()

    def add_list(self, list):
        self.json_data[list] = []
        self.write_data()

    ## DEL
    def del_item(self, list, item):
        item_index = self.json_data[list].index(item)
        del self.json_data[list][item_index]
        self.write_data()

    def del_list(self, list):
        del self.json_data[list]
        self.write_data()
