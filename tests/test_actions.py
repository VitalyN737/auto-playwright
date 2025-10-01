import json
from playwright.sync_api import Page, expect
from src.auto_playwright.create_actions import create_actions

def test_finds_element_using_css_locator(page: Page, test_server):
    page.goto(test_server)
    actions = create_actions(page)
    args = json.dumps({"cssSelector": "h1"})
    result = actions["locateElement"]["function"](args)
    assert "elementId" in result
    assert isinstance(result["elementId"], str)

def test_selects_option_by_value_using_element_id(page: Page, test_server):
    page.goto(test_server)
    actions = create_actions(page)

    locate_args = json.dumps({"cssSelector": "#fruit-select"})
    locate_result = actions["locateElement"]["function"](locate_args)

    select_args = json.dumps({"elementId": locate_result["elementId"], "value": "banana"})
    select_result = actions["locator_selectOption"]["function"](select_args)

    assert select_result == {"success": True}
    expect(page.locator("#selected-fruit")).to_have_text("Banana")

def test_selects_option_by_value_using_css_selector(page: Page, test_server):
    page.goto(test_server)
    actions = create_actions(page)

    select_args = json.dumps({"cssSelector": "#fruit-select", "value": "cherry"})
    select_result = actions["locator_selectOption"]["function"](select_args)

    assert select_result == {"success": True}
    expect(page.locator("#selected-fruit")).to_have_text("Cherry")

def test_selects_option_by_label_using_css_selector(page: Page, test_server):
    page.goto(test_server)
    actions = create_actions(page)

    select_args = json.dumps({"cssSelector": "#fruit-select", "label": "Orange"})
    select_result = actions["locator_selectOption"]["function"](select_args)

    assert select_result == {"success": True}
    expect(page.locator("#selected-fruit")).to_have_text("Orange")

def test_selects_option_by_index_using_css_selector(page: Page, test_server):
    page.goto(test_server)
    actions = create_actions(page)

    select_args = json.dumps({"cssSelector": "#fruit-select", "index": 1})
    select_result = actions["locator_selectOption"]["function"](select_args)

    assert select_result == {"success": True}
    expect(page.locator("#selected-fruit")).to_have_text("Apple")

def test_selects_multiple_options(page: Page, test_server):
    page.goto(test_server)
    actions = create_actions(page)

    select_args = json.dumps({"cssSelector": "#colors-select", "value": ["red", "blue"]})
    select_result = actions["locator_selectOption"]["function"](select_args)

    assert select_result == {"success": True}
    expect(page.locator("#selected-colors")).to_have_text("Red, Blue")