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

# Import database.py
import sys
from os.path import dirname, abspath
SKILL_DIR = dirname(abspath(__file__))
sys.path.append(SKILL_DIR)
from database import Database


class ListManager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.db = Database()

    @intent_handler(IntentBuilder('read')
        .require('what')
        .require('list')
        .optionally('list_name'))
    def handle_read(self, message):
        """ Read items on a specific list or read all the lists names"""

        list_name = message.data.get('list_name')

        if list_name:
            # If the user specified a list name, read items on that list
            if self.db.list_empty(list_name):
                self.speak_dialog('no.items', {'list_name': list_name})
            elif not self.db.list_exists(list_name):
                self.speak_dialog('list.not.found', {'list_name': list_name})
            else:
                data = {'list': list_name,
                        'items': self.string(self.db.read_items(list_name))}
    
                self.speak_dialog('items.in.list', data)
        else:
            # Alternatively, simply read lists names
            if self.db.no_lists():
                self.speak_dialog('no.lists')
            else:
                lists = self.db.read_lists()
                data = {'list_names': self.string(lists),
                        'list': self.plural_singular_form(lists)}
    
                self.speak_dialog('list.lists', data)

    @intent_handler(IntentBuilder('add')
        .require('add')
        .require('list')
        .require('list_name')
        .optionally('item_name'))
    def handle_add(self, message):
        """ Adds a new item to an existing list or creates a new one """

        list_name = message.data.get('list_name')
        item_name = message.data.get('item_name')

        if item_name:
            # If the user specified an item_name, adds it to a list
            if not self.db.list_exists(list_name):
                data = {'list_name': list_name}
                
                self.speak_dialog('list.not.found', data)
            else:
                self.db.add_item(list_name, item_name)
                data = {'item_name': item_name, 'list_name': list_name}

                self.speak_dialog('item.added', data)
        else:
            # Alternatively, simply creates a new list
            if self.db.list_exists(list_name):
                self.speak_dialog('list.found', {'list_name': list_name})
            else:
                self.db.add_list(list_name)

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
            # If the user specified an item_name, deletes it from the list
            if not (self.db.list_exists(list_name) and \
                    self.db.item_exists(list_name, item_name)):
                data = {'item_name': item_name, 'list_name': list_name}
                
                self.speak_dialog('item.not.found', data)
                        
            else:
                if self.confirm_deletion(item_name):
                    self.db.del_item(list_name, item_name)
                    data = {'item_name': item_name, 'list_name': list_name}
                    
                    self.speak_dialog('item.removed', data)
                   
        else:
            # Alternatively, simply creates a new list
            if not self.db.list_exists(list_name):
                data = {'item_name': item_name, 'list_name': list_name}
                
                self.speak_dialog('list.not.found', data)
            else:
                if self.confirm_deletion(list_name):
                    self.db.del_list(list_name)
                    data = {'item_name': item_name, 'list_name': list_name}

                    self.speak_dialog('list.removed', data)

    def string(self, lists):
        """ Converts a python list into a string such as 'a, b and c' """

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
