Feature: list-manager

  Scenario Outline: Create a new list
    Given an english speaking user
      When the user says "Create a new list called integration test"
      Then "list-manager" should reply with dialog from "add.list.dialog"

  Scenario Outline: Add an item to an existing list
    Given an english speaking user
      When the user says "Add office space to my integration test list"
      Then "list-manager" should reply with dialog from "add.item.dialog"

  Scenario Outline: Do not create list if it already exists
    Given an english speaking user
      When the user says "Create a new list called integration test"
      Then "list-manager" should reply with dialog from "list.found.dialog"

  Scenario Outline: Read out the existing lists
    Given an english speaking user
      When the user says "What lists do I have?"
      Then "list-manager" should reply with dialog from "read.lists.dialog"

  Scenario Outline: Read items on a specific list
    Given an english speaking user
      When the user says "What's on my integration test list?"
      Then "list-manager" should reply with dialog from "read.items.dialog"

  Scenario Outline: Delete a specific item from a list
    Given an english speaking user
      When the user says "Remove office space from my integration test list"
      Then "list-manager" should reply with dialog from "confirm.deletion.dialog"
      And the user replies with "yes"
      Then "list-manager" should reply with dialog from "del.item.dialog"

  Scenario Outline: Delete a list
    Given an english speaking user
      When the user says "Remove my integration test list"
      Then "list-manager" should reply with dialog from "confirm.deletion.dialog"
      And the user replies with "yes"
      Then "list-manager" should reply with dialog from "del.list.dialog"