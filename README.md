# Auto Playwright

Run Playwright tests using AI.

## Setup

1. Install the `auto-playwright` dependency:

```bash
pip install auto-playwright
```

2. This package relies on talking with OpenAI (https://openai.com/). You must export the API token as an environment variable or add it to your `.env` file:

```bash
export OPENAI_API_KEY='sk-...'
```

3. Import and use the `auto` function in your Playwright tests:

```python
from playwright.sync_api import Page, expect
from src.auto_playwright import auto

def test_auto_playwright_example(page: Page):
    page.goto("/")

    # `auto` can query data
    # In this case, the result is the plain-text content of the header
    header_text = auto("get the header text", {"page": page})

    # `auto` can perform actions
    # In this case, auto will find and fill in the search text input
    auto(f'Type "{header_text}" in the search box', {"page": page})

    # `auto` can assert the state of the website
    # In this case, the result is a boolean outcome
    search_input_has_header_text = auto(
        f'Is the contents of the search box equal to "{header_text}"?',
        {"page": page}
    )

    assert search_input_has_header_text is True
```

### Setup with Azure OpenAI

Pass the required connection details for Azure OpenAI in the `options` dictionary.

```python
from playwright.sync_api import Page, expect
from src.auto_playwright import auto
from src.auto_playwright.types import StepOptions

api_key = "your-api-key"
resource = "your-azure-resource-name"
model = "your-model-deployment-name"

options: StepOptions = {
    "model": model,
    "openai_api_key": api_key,
    "openai_base_url": f"https://{resource}.openai.azure.com/openai/deployments/{model}",
    "openai_default_query": {"api-version": "2023-07-01-preview"},
    "openai_default_headers": {"api-key": api_key},
}

def test_auto_playwright_azure_example(page: Page):
    page.goto("/")

    header_text = auto("get the header text", {"page": page}, options)

    auto(f'Type "{header_text}" in the search box', {"page": page}, options)

    search_input_has_header_text = auto(
        f'Is the contents of the search box equal to "{header_text}"?',
        {"page": page},
        options
    )

    assert search_input_has_header_text is True
```

## Usage

At a minimum, the `auto` function requires a plain text prompt and a configuration dictionary containing your `page` object.

```python
auto("<your prompt>", {"page": page})
```

### Browser automation

Running without a test runner like `pytest`:

```python
from playwright.sync_api import sync_playwright
from src.auto_playwright import auto

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.example.com")

    # `auto` can query data
    res = auto("get the header text", {"page": page})

    # res['query'] contains the result
    print(res)
    browser.close()
```

### Debug

You may pass a `debug` attribute in the `options` dictionary to the `auto` function. This will print the prompt and the commands executed by OpenAI.

```python
auto("get the header text", {"page": page}, {"debug": True})
```

You may also set the environment variable `AUTO_PLAYWRIGHT_DEBUG=true`, which will enable debugging for all `auto` calls.

```bash
export AUTO_PLAYWRIGHT_DEBUG=true
```

## Supported Browsers

Every browser that Playwright supports.

## Additional Options

There are additional options you can pass in the `options` dictionary:

```python
options = {
  # If true, debugging information is printed in the console.
  "debug": False,
  # The OpenAI model (https://platform.openai.com/docs/models/overview)
  "model": "gpt-4o",
  # The OpenAI API key
  "openai_api_key": "sk-...",
}

auto("<your prompt>", {"page": page}, options)
```

## Supported Actions & Return Values

Depending on the type of action inferred by the `auto` function, there are different behaviors and return types.

### Action

An action (e.g., "click") is a simulated user interaction with the page. Actions return `None` if they were successful and will raise an error if they failed.

```python
try:
  auto("click the link", {"page": page})
except Exception as e:
  print(f"Failed to click the link: {e}")
```

### Query

A query will return the requested data from the page as a string.

```python
link_text = auto("Get the text of the first link", {"page": page})

print(f"The link text is: {link_text}")
```

### Assert

An assertion is a question that will return `True` or `False`.

```python
there_are_three_links = auto("Are there 3 links on the page?", {"page": page})

print(f'"There are 3 links" is a {there_are_three_links} statement')
```

## Why use Auto Playwright?

| Aspect                         | Conventional Approach                                                               | Testing with Auto Playwright                                                                                                 |
| ------------------------------ | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Coupling with Markup**       | Strongly linked to the application's markup.                                        | Eliminates the use of selectors; actions are determined by the AI assistant at runtime.                                      |
| **Speed of Implementation**    | Slower implementation due to the need for precise code translation for each action. | Rapid test creation using simple, plain text instructions for actions and assertions.                                        |
| **Handling Complex Scenarios** | Automating complex scenarios is challenging and prone to frequent failures.         | Facilitates testing of complex scenarios by focusing on the intended test outcomes.                                          |
| **Test Writing Timing**        | Can only write tests after the complete development of the functionality.           | Enables a Test-Driven Development (TDD) approach, allowing test writing concurrent with or before functionality development. |

## Supported Playwright Actions

- `locator.blur`
- `locator.boundingBox`
- `locator.check`
- `locator.clear`
- `locator.click`
- `locator.count`
- `locator.fill`
- `locator.get_attribute`
- `locator.inner_html`
- `locator.inner_text`
- `locator.input_value`
- `locator.is_checked`
- `locator.is_editable`
- `locator.is_enabled`
- `locator.is_visible`
- `locator.press`
- `locator.select_option`
- `locator.text_content`
- `locator.uncheck`
- `page.goto`
- `page.keyboard.press`

Adding new actions is easy: just update the `actions` dictionary in [`src/auto_playwright/create_actions.py`](src/auto_playwright/create_actions.py).

## Pricing

This library is free. However, there are costs associated with using OpenAI. You can find more information about pricing here: https://openai.com/pricing/.

## Implementation

### HTML Sanitization

The `auto` function uses [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) to sanitize the HTML of the page before sending it to OpenAI. This is done to reduce cost and improve the quality of the generated text.

## ZeroStep

This project draws its inspiration from [ZeroStep](https://zerostep.com/). ZeroStep offers a similar API but with a more robust implementation through its proprietary backend. Auto Playwright was created with the aim of exploring the underlying technology of ZeroStep and establishing a basis for an open-source version of their software. For production environments, I suggest opting for ZeroStep.

Here's a side-by-side comparison of Auto Playwright and ZeroStep:

| Criteria                                                                              | Auto Playwright | ZeroStep |
| ------------------------------------------------------------------------------------- | --------------- | -------- |
| Uses OpenAI API                                                                       | Yes             | No[^3]   |
| Uses plain-text prompts                                                               | Yes             | No       |
| Uses [`functions`](https://platform.openai.com/docs/guides/function-calling) SDK | Yes             | No       |
| Uses HTML sanitization                                                                | Yes             | No       |
| Uses Playwright API                                                                   | Yes             | No[^4]   |
| Uses screenshots                                                                      | No              | Yes      |
| Uses queue                                                                            | No              | Yes      |
| Uses WebSockets                                                                       | No              | Yes      |
| Snapshots                                                                             | HTML            | DOM      |
| Implements parallelism                                                                | No              | Yes      |
| Allows scrolling                                                                      | No              | Yes      |
| Provides fixtures                                                                     | No              | Yes      |
| License                                                                               | MIT             | MIT      |

[^3]: Uses ZeroStep proprietary API.

[^4]: Uses _some_ Playwright API, but predominantly relies on Chrome DevTools Protocol (CDP).