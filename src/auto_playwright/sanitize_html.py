import re
from bs4 import BeautifulSoup

# Based on sanitize-html defaults and the extra tags from the TS file.
ALLOWED_TAGS = [
    "a", "abbr", "b", "blockquote", "br", "cite", "code", "dd", "dl", "dt",
    "em", "i", "li", "ol", "p", "pre", "q", "small", "strike", "strong", "sub",
    "sup", "u", "ul", "button", "input", "textarea", "select", "h1", "h2", "h3", "h4", "h5", "h6",
    "div", "span", "img", "header", "footer", "main", "section", "article",
    "aside", "nav", "details", "summary", "kbd"
]

ALLOWED_ATTRIBUTES = {
    "*": ["class", "id", "style"],
    "a": ["href", "name", "target"],
    "img": ["src", "srcset", "alt", "title", "width", "height", "loading"],
    "input": ["type", "value", "placeholder", "name", "id", "disabled"],
    "select": ["name", "id", "disabled"],
    "textarea": ["placeholder", "name", "id", "disabled"],
}

def sanitize(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.find_all(True):
        if tag.name not in ALLOWED_TAGS:
            tag.unwrap()
            continue

        if 'class' in tag.attrs:
            original_classes = tag.attrs['class']
            sanitized_classes = []
            for c in original_classes:
                sanitized_class = f"A{re.sub('[^a-zA-Z0-9_-]', '', c)}"
                sanitized_classes.append(sanitized_class)
            tag.attrs['class'] = sanitized_classes

        attrs = dict(tag.attrs)
        for attr in list(attrs.keys()):
            allowed = ALLOWED_ATTRIBUTES.get(tag.name, []) + ALLOWED_ATTRIBUTES.get("*", [])

            is_allowed = attr in allowed
            is_data_attr = attr.startswith("data-")

            if not is_allowed and not is_data_attr:
                 del tag[attr]

    return str(soup)