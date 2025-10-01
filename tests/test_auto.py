import os
import pytest
from playwright.sync_api import Page, expect
from auto_playwright import auto

# To run these tests, you must have an OPENAI_API_KEY environment variable set.
# You can get a key from https://platform.openai.com/

# Skip all tests in this file if the OPENAI_API_KEY is not set.
pytestmark = pytest.mark.skipif(not os.environ.get("OPENAI_API_KEY"), reason="OPENAI_API_KEY is not set")

def test_executes_query(page: Page, test_server):
    page.goto(test_server)
    header_text = auto("get the header text", {"page": page, "test": None})
    assert header_text == "Hello, Rayrun!"

def test_executes_action(page: Page, test_server):
    page.goto(test_server)
    auto('Type "foo" in the search box', {"page": page, "test": None})
    expect(page.get_by_test_id("search-input")).to_have_value("foo")

def test_executes_click(page: Page, test_server):
    page.goto(test_server)
    auto("Click the button until the counter value is equal to 2", {"page": page, "test": None})
    expect(page.get_by_test_id("current-count")).to_have_text("2")

def test_asserts_to_be(page: Page, test_server):
    page.goto(test_server)
    is_equal = auto('Is the contents of the header equal to "Hello, Rayrun!"?', {"page": page, "test": None})
    assert is_equal is True

def test_asserts_not_to_be(page: Page, test_server):
    page.goto(test_server)
    is_equal = auto('Is the contents of the header equal to "Flying Donkeys"?', {"page": page, "test": None})
    assert is_equal is False

def test_executes_query_action_and_assertion(page: Page, test_server):
    page.goto(test_server)

    header_text = auto("get the header text", {"page": page, "test": None})

    auto(f'type "{header_text}" in the search box', {"page": page, "test": None})

    is_equal = auto(f'is the contents of the search box equal to "{header_text}"?', {"page": page, "test": None})

    assert is_equal is True

def test_runs_without_test_parameter(page: Page, test_server):
    page.goto(test_server)
    result = auto("get the header text", {"page": page})
    assert result["query"] == "Hello, Rayrun!"

def test_selects_an_option_from_dropdown(page: Page, test_server):
    page.goto(test_server)
    auto("Select the 'Banana' option from the fruit dropdown", {"page": page, "test": None})
    expect(page.get_by_test_id("selected-fruit")).to_have_text("Banana")

def test_selects_option_by_value_from_dropdown(page: Page, test_server):
    page.goto(test_server)
    auto("Select the option with value 'cherry' from the fruit dropdown", {"page": page, "test": None})
    expect(page.get_by_test_id("selected-fruit")).to_have_text("Cherry")

def test_selects_multiple_options_from_multi_select(page: Page, test_server):
    page.goto(test_server)
    auto("Select the 'Red' and 'Blue' options from the colors multi-select", {"page": page, "test": None})
    expect(page.get_by_test_id("selected-colors")).to_have_text("Red, Blue")