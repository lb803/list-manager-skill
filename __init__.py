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

from mycroft import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder

import json
from os.path import dirname, join


class ListManager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        try:
            # Loads data from data.json
            self.JSON_PATH = join(dirname(__file__), 'data.json')
            self.json_data = self.read_data()
        except FileNotFoundError:
            # If not found, creates an empty data.json file 
            # (i.e. first skill run)
            self.json_data = {}
            self.write_data()

    def read_data(self):
        with open(self.JSON_PATH, 'r') as json_file:
            return json.load(json_file)

    def write_data(self):
        with open(self.JSON_PATH, 'w') as json_file:
            json.dump(self.json_data, json_file)

    @intent_handler(IntentBuilder('read')
        .require('what')
        .require('list')
        .optionally('list_name'))
    def handle_read(self, message):
        """ Read list names or item names from a list """
            
        list_name = message.data.get('list_name')

        if list_name:
            try:
                items = self.json_data.get(list_name)
                assert items
                assert len(items) > 0
            except AssertionError:
                self.speak_dialog('no.items', {'list_name': list_name})
            else:
                items_str = self.list_to_str(items)

                self.speak_dialog('items.in.list', {'list': list_name,
                                                    'items': items})
        else:
            lists = list(self.json_data.keys())
            try:
                assert len(lists) > 0
            except AssertionError:
                self.speak_dialog('no.lists')
            else:
                lists_str = self.list_to_str(lists)
                list_or_lists = self.plural_singular_form(lists)

                self.speak_dialog('list.lists', 
                                  {'list_names': lists_str,
                                   'list': list_or_lists})

    @intent_handler(IntentBuilder('add')
        .require('add')
        .require('list')
        .require('list_name')
        .optionally('item_name'))
    def handle_add(self, message):
        """ Adds a new list or append a new item to an existing list """

        item_name = message.data.get('item_name')
        list_name = message.data.get('list_name')

        if item_name:
            try:
                assert list_name in self.json_data.keys()
            except AssertionError:
                self.speak_dialog('list.not.found', 
                                  {'list_name': list_name})
            else:
                items = self.json_data.get(list_name)
                items.append(item_name)
                self.json_data.update({list_name: items})
                self.write_data()

                self.speak_dialog('item.added', 
                                  {'item_name': item_name,
                                   'list_name': list_name})
        else:
            try:
                assert list_name not in self.json_data.keys()
            except AssertionError:
                self.speak_dialog('list.found', 
                                  {'list_name': list_name})
            else:
                self.json_data.update({list_name: []})
                self.write_data()

                self.speak_dialog('list.added', {'list_name': list_name})

    @intent_handler(IntentBuilder('del')
        .require('del')
        .require('list')
        .require('list_name')
        .optionally('item_name'))
    def handle_del(self, message):
        """ Removes a list or an item from an existing list """

        item_name = message.data.get('item_name')
        list_name = message.data.get('list_name')

        if item_name:
            try:
                assert list_name in self.json_data.keys()
                assert item_name in self.json_data[list_name]
            except AssertionError:
                self.speak_dialog('item.not.found', 
                                  {'item_name': item_name,
                                   'list_name': list_name})
            else:
                if self.confirm_deletion(item_name):
                    updated_list = [x for x in self.json_data[list_name] \
                                    if x != item_name]
                    self.json_data[list_name] = {list_name: updated_list}
                    self.write_data()

                    self.speak_dialog('item.removed', 
                                      {'item_name': item_name,
                                       'list_name': list_name})
        else:
            try:
                assert list_name in self.json_data.keys()
            except AssertionError:
                self.speak_dialog('list.not.found', 
                                  {'list_name': list_name})
            else:
                if self.confirm_deletion(list_name):
                    del self.json_data[list_name]
                    self.write_data()

                    self.speak_dialog('list.removed', 
                                      {'list_name': list_name})

    def list_to_str(self, lists):
        """ Converts items of a python list into a neat string """

        conj = self.translate_namedvalues('conj', delim=',')
        conj_spaced = ' {} '.format(conj.get('conj'))
        return ', '.join(lists[:-2] + [conj_spaced.join(lists[-2:])])

    def plural_singular_form(self, lists):
        """ Returns singular or plural form as necessary """
        
        value = self.translate_namedvalues('list.or.lists', delim=',')
        return value.get('singular') if len(lists) == 1 else value.get('plural')

    def confirm_deletion(self, item):
        """ Makes sure the user really wants to delete an item """

        resp = self.ask_yesno('confirm.deletion', data={'item': item})
        if resp == 'yes':
            return True
        else:
            self.speak_dialog('cancelled')
        return False


def create_skill():
    return ListManager()
