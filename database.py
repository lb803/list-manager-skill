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
    def __init__(self):
        self.JSON_PATH = join(dirname(__file__), 'data.json')
        try:
            # Loads list data from data.json
            json_data = self.read_data()
        except FileNotFoundError:
            # If file not found, creates an empty data.json
            self.json_data = {}
            self.write_data()

    def read_data(self):
        with open(self.JSON_PATH, 'r') as json_file:
            return json.load(json_file)

    def write_data(self):
        with open(self.JSON_PATH, 'w') as json_file:
            json.dump(self.json_data, json_file)
            
    def list_empty(self, list):
        return True if len(list) == 0 else False
            
    def list_exists(self, list):
        return True if list in self.json_data.keys() else False
        
    def item_exists(self, list, item):
        return True if item in self.json_data[list] else False
