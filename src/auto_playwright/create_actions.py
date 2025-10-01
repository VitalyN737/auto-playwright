import json
import uuid
from typing import Any, Dict, Callable
from playwright.sync_api import Page, Locator

def create_actions(page: Page) -> Dict[str, Dict[str, Any]]:
    """
    Creates a dictionary of actions that can be performed on the page.
    """

    def get_locator(element_id: str) -> Locator:
        return page.locator(f"[data-element-id='{element_id}']")

    def locator_press_key(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        get_locator(parsed_args["elementId"]).press(parsed_args["key"])
        return {"success": True}

    def page_press_key(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        page.keyboard.press(parsed_args["key"])
        return {"success": True}

    def locate_element(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        locator = page.locator(parsed_args["cssSelector"])
        element_id = str(uuid.uuid4())
        locator.first.evaluate("(node, id) => node.setAttribute('data-element-id', id)", element_id)
        return {"elementId": element_id}

    def locator_evaluate(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        result = get_locator(parsed_args["elementId"]).evaluate(parsed_args["pageFunction"])
        return {"result": result}

    def locator_get_attribute(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        value = get_locator(parsed_args["elementId"]).get_attribute(parsed_args["attributeName"])
        return {"attributeValue": value}

    def locator_inner_html(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        html = get_locator(parsed_args["elementId"]).inner_html()
        return {"innerHTML": html}

    def locator_inner_text(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        text = get_locator(parsed_args["elementId"]).inner_text()
        return {"innerText": text}

    def locator_text_content(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        text = get_locator(parsed_args["elementId"]).text_content()
        return {"textContent": text}

    def locator_input_value(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        value = get_locator(parsed_args["elementId"]).input_value()
        return {"inputValue": value}

    def locator_blur(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        get_locator(parsed_args["elementId"]).blur()
        return {"success": True}

    def locator_bounding_box(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        box = get_locator(parsed_args["elementId"]).bounding_box()
        return box

    def locator_check(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        get_locator(parsed_args["elementId"]).check()
        return {"success": True}

    def locator_uncheck(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        get_locator(parsed_args["elementId"]).uncheck()
        return {"success": True}

    def locator_is_checked(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        is_checked = get_locator(parsed_args["elementId"]).is_checked()
        return {"isChecked": is_checked}

    def locator_is_editable(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        is_editable = get_locator(parsed_args["elementId"]).is_editable()
        return {"isEditable": is_editable}

    def locator_is_enabled(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        is_enabled = get_locator(parsed_args["elementId"]).is_enabled()
        return {"isEnabled": is_enabled}

    def locator_is_visible(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        is_visible = get_locator(parsed_args["elementId"]).is_visible()
        return {"isVisible": is_visible}

    def locator_clear(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        get_locator(parsed_args["elementId"]).clear()
        return {"success": True}

    def locator_click(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        get_locator(parsed_args["elementId"]).click()
        return {"success": True}

    def locator_count(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        count = get_locator(parsed_args["elementId"]).count()
        return {"elementCount": count}

    def locator_fill(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        get_locator(parsed_args["elementId"]).fill(parsed_args["value"])
        return {"success": True}

    def page_goto(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        response = page.goto(parsed_args["url"])
        return {"url": response.url if response else None}

    def locator_select_option(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        element_id = parsed_args.get("elementId")
        css_selector = parsed_args.get("cssSelector")

        if element_id:
            locator = get_locator(element_id)
        elif css_selector:
            locator = page.locator(css_selector)
        else:
            raise ValueError("Either elementId or cssSelector must be provided.")

        value = parsed_args.get("value")
        label = parsed_args.get("label")
        index = parsed_args.get("index")

        if value is not None:
            locator.select_option(value)
        elif label is not None:
            locator.select_option(label=label)
        elif index is not None:
            locator.select_option(index=index)
        else:
            raise ValueError("You must provide at least one of the parameters: value, label, or index.")

        return {"success": True}

    def expect_to_be(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        actual = parsed_args["actual"]
        expected = parsed_args["expected"]
        return {"actual": actual, "expected": expected, "success": actual == expected}

    def expect_not_to_be(args: str) -> Dict[str, Any]:
        parsed_args = json.loads(args)
        actual = parsed_args["actual"]
        expected = parsed_args["expected"]
        return {"actual": actual, "expected": expected, "success": actual != expected}

    def result_assertion(args: str) -> Dict[str, Any]:
        return json.loads(args)

    def result_query(args: str) -> Dict[str, Any]:
        return json.loads(args)

    def result_action(args: str) -> Dict[str, Any]:
        return {"success": True}

    def result_error(args: str) -> Dict[str, Any]:
        return json.loads(args)

    actions = {
        "locator_pressKey": {
            "function": locator_press_key,
            "name": "locator_pressKey",
            "description": "Presses a key while focused on the specified element.",
            "parameters": {
                "type": "object",
                "properties": {
                    "elementId": {"type": "string"},
                    "key": {"type": "string", "description": "The name of the key to press, e.g., 'Enter', 'ArrowUp', 'a'."},
                },
            },
        },
        "page_pressKey": {
            "function": page_press_key,
            "name": "page_pressKey",
            "description": "Presses a key globally on the page.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "The name of the key to press, e.g., 'Enter', 'ArrowDown', 'b'."},
                },
            },
        },
        "locateElement": {
            "function": locate_element,
            "name": "locateElement",
            "description": "Locates element using a CSS selector and returns elementId. This element ID can be used with other functions to perform actions on the element.",
            "parameters": {
                "type": "object",
                "properties": {"cssSelector": {"type": "string"}},
            },
        },
        "locator_evaluate": {
            "function": locator_evaluate,
            "description": "Execute JavaScript code in the page, taking the matching element as an argument.",
            "name": "locator_evaluate",
            "parameters": {
                "type": "object",
                "properties": {
                    "elementId": {"type": "string"},
                    "pageFunction": {"type": "string", "description": "Function to be evaluated in the page context, e.g. node => node.innerText"},
                },
            },
        },
        "locator_getAttribute": {
            "function": locator_get_attribute,
            "name": "locator_getAttribute",
            "description": "Returns the matching element's attribute value.",
            "parameters": {
                "type": "object",
                "properties": {
                    "attributeName": {"type": "string"},
                    "elementId": {"type": "string"},
                },
            },
        },
        "locator_innerHTML": {
            "function": locator_inner_html,
            "name": "locator_innerHTML",
            "description": "Returns the element.innerHTML.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_innerText": {
            "function": locator_inner_text,
            "name": "locator_innerText",
            "description": "Returns the element.innerText.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_textContent": {
            "function": locator_text_content,
            "name": "locator_textContent",
            "description": "Returns the node.textContent.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_inputValue": {
            "function": locator_input_value,
            "name": "locator_inputValue",
            "description": "Returns input.value for the selected <input> or <textarea> or <select> element.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_blur": {
            "function": locator_blur,
            "name": "locator_blur",
            "description": "Removes keyboard focus from the current element.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_boundingBox": {
            "function": locator_bounding_box,
            "name": "locator_boundingBox",
            "description": "This method returns the bounding box of the element matching the locator, or null if the element is not visible.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_check": {
            "function": locator_check,
            "name": "locator_check",
            "description": "Ensure that checkbox or radio element is checked.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_uncheck": {
            "function": locator_uncheck,
            "name": "locator_uncheck",
            "description": "Ensure that checkbox or radio element is unchecked.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_isChecked": {
            "function": locator_is_checked,
            "name": "locator_isChecked",
            "description": "Returns whether the element is checked.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_isEditable": {
            "function": locator_is_editable,
            "name": "locator_isEditable",
            "description": "Returns whether the element is editable.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_isEnabled": {
            "function": locator_is_enabled,
            "name": "locator_isEnabled",
            "description": "Returns whether the element is enabled.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_isVisible": {
            "function": locator_is_visible,
            "name": "locator_isVisible",
            "description": "Returns whether the element is visible.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_clear": {
            "function": locator_clear,
            "name": "locator_clear",
            "description": "Clear the input field.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_click": {
            "function": locator_click,
            "name": "locator_click",
            "description": "Click an element.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_count": {
            "function": locator_count,
            "name": "locator_count",
            "description": "Returns the number of elements matching the locator.",
            "parameters": {
                "type": "object",
                "properties": {"elementId": {"type": "string"}},
            },
        },
        "locator_fill": {
            "function": locator_fill,
            "name": "locator_fill",
            "description": "Set a value to the input field.",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {"type": "string"},
                    "elementId": {"type": "string"},
                },
            },
        },
        "page_goto": {
            "function": page_goto,
            "name": "page_goto",
            "description": "Navigate to the specified URL.",
            "parameters": {
                "type": "object",
                "properties": {"url": {"type": "string", "description": "The URL to navigate to"}},
                "required": ["url"],
            },
        },
        "locator_selectOption": {
            "function": locator_select_option,
            "name": "locator_selectOption",
            "description": "Selects option(s) in a <select> element. Requires either an elementId (obtained via locateElement) or a direct cssSelector.",
            "parameters": {
                "type": "object",
                "properties": {
                    "elementId": {"type": "string", "description": "The ID of the <select> element, obtained via locateElement."},
                    "cssSelector": {"type": "string", "description": "CSS selector to locate the <select> element directly, e.g., '#my-select' or 'form select'."},
                    "value": {"type": ["string", "array"], "description": "Select options with matching value attribute. Can be a string or an array for multi-select.", "items": {"type": "string"}},
                    "label": {"type": ["string", "array"], "description": "Select options with matching visible text. Can be a string or an array for multi-select.", "items": {"type": "string"}},
                    "index": {"type": ["number", "array"], "description": "Select options by their index (zero-based). Can be a number or an array for multi-select.", "items": {"type": "number"}},
                },
            },
        },
        "expect_toBe": {
            "function": expect_to_be,
            "name": "expect_toBe",
            "description": "Asserts that the actual value is equal to the expected value.",
            "parameters": {
                "type": "object",
                "properties": {
                    "actual": {"type": "string"},
                    "expected": {"type": "string"},
                },
            },
        },
        "expect_notToBe": {
            "function": expect_not_to_be,
            "name": "expect_notToBe",
            "description": "Asserts that the actual value is not equal to the expected value.",
            "parameters": {
                "type": "object",
                "properties": {
                    "actual": {"type": "string"},
                    "expected": {"type": "string"},
                },
            },
        },
        "resultAssertion": {
            "function": result_assertion,
            "description": "This function is called when the initial instructions asked to assert something; then 'assertion' is either true or false (boolean) depending on whether the assertion succeeded.",
            "name": "resultAssertion",
            "parameters": {
                "type": "object",
                "properties": {"assertion": {"type": "boolean"}},
            },
        },
        "resultQuery": {
            "function": result_query,
            "description": "This function is called at the end when the initial instructions asked to extract data; then 'query' property is set to a text value of the extracted data.",
            "name": "resultQuery",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
            },
        },
        "resultAction": {
            "function": result_action,
            "description": "This function is called at the end when the initial instructions asked to perform an action.",
            "name": "resultAction",
            "parameters": {"type": "object", "properties": {}},
        },
        "resultError": {
            "function": result_error,
            "description": "If user instructions cannot be completed, then this function is used to produce the final response.",
            "name": "resultError",
            "parameters": {
                "type": "object",
                "properties": {"errorMessage": {"type": "string"}},
            },
        },
    }
    return actions