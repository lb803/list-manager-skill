from unittest.mock import MagicMock
from test.integrationtests.skills.skill_tester import SkillTest

def test_runner(skill, example, emitter, loader):

    # Get the skill object from the skill path
    s = [s for s in loader.skills if s and s.root_dir == skill]

    # replace the db with a mock
    s[0].db = MagicMock()

    # Read lists
    if example.endswith('handle_read.0.intent.json'):
        s[0].db.no_lists.return_value = False
        s[0].db.read_lists.return_value = ['films', 'readings']

    # Read items on list
    if example.endswith('handle_read.1.intent.json'):
        s[0].db.list_empty.return_value = False
        s[0].db.list_exists.return_value = True
        s[0].db.read_items.return_value = ['office space', 'snowden']

    # Read list, but there are no lists yet
    if example.endswith('handle_read.2.intent.json'):
        s[0].db.no_lists.return_value = True

    # Read items on list, but the list is empty
    if example.endswith('handle_read.3.intent.json'):
        s[0].db.list_empty.return_value = True
        s[0].db.list_exists.return_value = True

    # Read items on list, but the list doesn't exists
    if example.endswith('handle_read.4.intent.json'):
        s[0].db.list_exists.return_value = False

    # Add list
    if example.endswith('handle_add.0.intent.json'):
        s[0].db.list_exists.return_value = False

    # Add item to list
    if example.endswith('handle_add.1.intent.json'):
        s[0].db.item_exists.return_value = False
        s[0].db.list_exists.return_value = True

    # Add list, but list already exists
    if example.endswith('handle_add.2.intent.json'):
        s[0].db.list_exists.return_value = True

    # Add item to list, but list not found
    if example.endswith('handle_add.3.intent.json'):
        s[0].db.list_exists.return_value = False

    # Add item to list, but item already present
    if example.endswith('handle_add.4.intent.json'):
        s[0].db.list_exists.return_value = True
        s[0].db.item_exists.return_value = True

    # Del list
    if example.endswith('handle_del.0.intent.json'):
        s[0].db.list_exists.return_value = True

    # Del item from list
    if example.endswith('handle_del.1.intent.json'):
        s[0].db.list_exists.return_value = True
        s[0].db.item_exists.return_value = True

    # Del list, but the list doesn't exists
    if example.endswith('handle_del.2.intent.json'):
        s[0].db.list_exists.return_value = False

    # Del list, but the user cancels the operation
    if example.endswith('handle_del.3.intent.json'):
        s[0].db.list_exists.return_value = True

    # Del item from list, but list doesn't exists
    if example.endswith('handle_del.4.0.intent.json'):
        s[0].db.list_exists.return_value = False
        s[0].db.item_exists.return_value = True

    # Del item from list, but item doesn't exists
    if example.endswith('handle_del.4.1.intent.json'):
        s[0].db.list_exists.return_value = True
        s[0].db.item_exists.return_value = False

    # Del item from list, but both list and item don't exist
    if example.endswith('handle_del.4.2.intent.json'):
        s[0].db.list_exists.return_value = False
        s[0].db.item_exists.return_value = False

    # Del item from list, but the user cancels the operation
    if example.endswith('handle_del.5.intent.json'):
        s[0].db.list_exists.return_value = True
        s[0].db.item_exists.return_value = True

    return SkillTest(skill, example, emitter).run(loader)
