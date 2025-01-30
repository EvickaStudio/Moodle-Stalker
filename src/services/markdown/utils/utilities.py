import re

BLOCK_ELEMENTS = [
    "ADDRESS",
    "ARTICLE",
    "ASIDE",
    "AUDIO",
    "BLOCKQUOTE",
    "BODY",
    "CANVAS",
    "CENTER",
    "DD",
    "DIR",
    "DIV",
    "DL",
    "DT",
    "FIELDSET",
    "FIGCAPTION",
    "FIGURE",
    "FOOTER",
    "FORM",
    "FRAMESET",
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
    "HEADER",
    "HGROUP",
    "HR",
    "HTML",
    "ISINDEX",
    "LI",
    "MAIN",
    "MENU",
    "NAV",
    "NOFRAMES",
    "NOSCRIPT",
    "OL",
    "OUTPUT",
    "P",
    "PRE",
    "SECTION",
    "TABLE",
    "TBODY",
    "TD",
    "TFOOT",
    "TH",
    "THEAD",
    "TR",
    "UL",
]

VOID_ELEMENTS = [
    "AREA",
    "BASE",
    "BR",
    "COL",
    "COMMAND",
    "EMBED",
    "HR",
    "IMG",
    "INPUT",
    "KEYGEN",
    "LINK",
    "META",
    "PARAM",
    "SOURCE",
    "TRACK",
    "WBR",
]

MEANINGFUL_WHEN_BLANK = [
    "A",
    "TABLE",
    "THEAD",
    "TBODY",
    "TFOOT",
    "TH",
    "TD",
    "IFRAME",
    "SCRIPT",
    "AUDIO",
    "VIDEO",
]


def extend(destination, *sources):
    """
    Copy all key-value pairs from each source dict into 'destination'.
    """
    for source in sources:
        for k, v in source.items():
            destination[k] = v
    return destination


def repeat(char, count):
    return char * count


def trim_leading_newlines(s):
    return re.sub(r"^\n+", "", s)


def trim_trailing_newlines(s):
    return re.sub(r"\n+$", "", s)


def is_block(node):
    return node.node_name in BLOCK_ELEMENTS


def is_void(node):
    return node.node_name in VOID_ELEMENTS


def has_void(node):
    """
    Check if 'node' or any of its descendants is void.
    """
    stack = [node]
    while stack:
        cur = stack.pop()
        for child in cur.children:
            if is_void(child):
                return True
            stack.append(child)
    return False


def is_meaningful_when_blank(node):
    return node.node_name in MEANINGFUL_WHEN_BLANK


def has_meaningful_when_blank(node):
    """
    Recursively checks node + children to see if any is in MEANINGFUL_WHEN_BLANK.
    """
    stack = [node]
    while stack:
        cur = stack.pop()
        for child in cur.children:
            if is_meaningful_when_blank(child):
                return True
            stack.append(child)
    return False


def clean_attribute(attr):
    """
    Reduce multiple newlines or line breaks. Return a 'cleaned' attribute or empty string.
    """
    return re.sub(r"(\n+\s*)+", "\n", attr) if attr else ""
