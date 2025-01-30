import re

from ..utils.utilities import clean_attribute, repeat


def paragraph_rule(content, node, options):
    """
    Wraps content in double newlines to represent a paragraph in Markdown.
    """
    return "\n\n" + content + "\n\n"


def line_break_rule(content, node, options):
    """
    Converts an HTML line break into a Markdown line break + newline.
    """
    return options["br"] + "\n"


def heading_rule(content, node, options):
    """
    Converts headings into Markdown.
    - 'setext' style (=== or --- under the text) for levels 1 & 2
    - otherwise '#' style
    """
    level = int(node.node_name[1])  # e.g. 'H2' -> 2
    style = options["headingStyle"]
    if style != "setext" or level >= 3:
        return "\n\n" + repeat("#", level) + " " + content + "\n\n"
    underline_char = "=" if level == 1 else "-"
    underline = repeat(underline_char, len(content))
    return f"\n\n{content}\n{underline}\n\n"


def blockquote_rule(content, node, options):
    """
    Prepend '> ' to each line for blockquotes.
    """
    content = content.strip("\n")
    lines = content.split("\n")
    quoted = "\n".join(f"> {line}" for line in lines)
    return "\n\n" + quoted + "\n\n"


def list_rule(content, node, options):
    """
    Ensures spacing in list contexts. Adds blank lines if needed.
    """
    parent = node.parent
    if parent and parent.node_name == "LI" and parent.last_child == node:
        return "\n" + content
    return "\n\n" + content + "\n\n"


def list_item_rule(content, node, options):
    """
    Creates properly indented list items with either bullets or numbers.
    """
    content = content.lstrip("\n").rstrip("\n") + "\n"
    # indent each line by 4 spaces
    lines = [f"    {line}" for line in content.split("\n")]
    content = "\n".join(lines)
    parent = node.parent
    marker = options["bulletListMarker"] + "   "
    if parent and parent.node_name == "OL":
        start_attr = parent.get_attribute("start")
        # We assume parent has a method to find the index among siblings:
        index = parent.index_in_parent(node)
        start_index = (int(start_attr) + index) if start_attr else (index + 1)
        marker = f"{start_index}.  "

    if node.next_sibling and not content.endswith("\n"):
        content += "\n"
    return marker + content


def indented_code_block_rule(content, node, options):
    """
    For 'indented' style code blocks. Indent every line by 4 spaces.
    """
    code_text = node.first_child.text_content()
    code_indented = "\n    ".join(code_text.split("\n"))
    return "\n\n    " + code_indented + "\n\n"


def fenced_code_block_rule(content, node, options):
    """
    For 'fenced' style code blocks. Use triple backticks.
    """
    class_name = node.first_child.get_attribute("class") or ""
    language = ""
    if match := re.search(r"language-(\S+)", class_name):
        language = match[1]

    code_text = node.first_child.text_content().rstrip("\n")
    fence_char = options["fence"][0]
    fence_size = 3

    # Increase fence size if code contains strings of backticks
    longest_fence = max(re.findall(r"^`{3,}", code_text, re.MULTILINE), default="")
    if len(longest_fence) >= fence_size:
        fence_size = len(longest_fence) + 1

    fence = fence_char * fence_size
    return f"\n\n{fence}{language}\n{code_text}\n{fence}\n\n"


def horizontal_rule_rule(content, node, options):
    """
    Converts an <hr> to its Markdown representation (e.g. `* * *`).
    """
    return f"\n\n{options['hr']}\n\n"


def inline_link_rule(content, node, options):
    """
    Converts an <a href="..."> to an inline Markdown link [text](url "title").
    """
    href = node.get_attribute("href")
    if href:
        href = href.replace("(", r"\(").replace(")", r"\)")
    title = clean_attribute(node.get_attribute("title"))
    if title:
        title = f" \"{title.replace('\"', '\\\\\"')}\""  # noqa: E999

    return f"[{content}]({href}{title})"


class ReferenceLinkStore:
    """
    Stores references for reference-style links, allowing them to be appended later.
    """

    def __init__(self):
        self.references = []

    def add_reference(self, ref):
        self.references.append(ref)

    def append_references(self, options):
        if self.references:
            result = "\n\n" + "\n".join(self.references) + "\n\n"
            self.references.clear()
            return result
        return ""


reference_link_store = ReferenceLinkStore()


def reference_link_rule(content, node, options):
    """
    Converts <a> to a reference-style link: [text][id].
    Actual reference appended at the bottom: [id]: href "title"
    """
    href = node.get_attribute("href") or ""
    title = clean_attribute(node.get_attribute("title")) or ""
    if title:
        title = f' "{title}"'

    style = options["linkReferenceStyle"]
    if style == "collapsed":
        replacement = f"[{content}][]"
        ref = f"[{content}]: {href}{title}"
    elif style == "shortcut":
        replacement = f"[{content}]"
        ref = f"[{content}]: {href}{title}"
    else:
        idx = len(reference_link_store.references) + 1
        replacement = f"[{content}][{idx}]"
        ref = f"[{idx}]: {href}{title}"

    reference_link_store.add_reference(ref)
    return replacement


def emphasis_rule(content, node, options):
    """
    Converts <em>/<i> into _text_ or other user-supplied emphasis delimiter.
    """
    if not content.strip():
        return ""
    return options["emDelimiter"] + content + options["emDelimiter"]


def strong_rule(content, node, options):
    """
    Converts <strong>/<b> into **text** or other user-supplied strong delimiter.
    """
    if not content.strip():
        return ""
    return options["strongDelimiter"] + content + options["strongDelimiter"]


def code_rule(content, node, options):
    """
    Converts an inline <code> into a code span with backticks. For example: `code`.
    """
    if not content:
        return ""

    # Replace newlines with spaces
    content = content.replace("\n", " ").replace("\r", "")

    # Possibly add leading/trailing space to avoid collisions with backticks
    import re

    pattern = r"^`|`$|^ .*?[^ ].* $"
    extra_space = " " if re.search(pattern, content) else ""

    delimiter = "`"
    # If content has backticks, we might need to push delimiter to `` or ``` ...
    matches = re.findall(r"`+", content)
    while delimiter in matches:
        delimiter += "`"

    return delimiter + extra_space + content + extra_space + delimiter


def image_rule(content, node, options):
    """
    Converts <img src="..." alt="..." title="..."> into ![alt](src "title").
    """
    alt = clean_attribute(node.get_attribute("alt") or "")
    src = node.get_attribute("src") or ""
    title = clean_attribute(node.get_attribute("title") or "")
    title_part = f' "{title}"' if title else ""
    return f"![{alt}]({src}{title_part})" if src else ""


COMMONMARK_RULES = {
    "paragraph": {"filter": "p", "replacement": paragraph_rule},
    "lineBreak": {"filter": "br", "replacement": line_break_rule},
    "heading": {
        "filter": ["h1", "h2", "h3", "h4", "h5", "h6"],
        "replacement": heading_rule,
    },
    "blockquote": {"filter": "blockquote", "replacement": blockquote_rule},
    "list": {"filter": ["ul", "ol"], "replacement": list_rule},
    "listItem": {"filter": "li", "replacement": list_item_rule},
    "indentedCodeBlock": {
        "filter": lambda node, opts: (
            opts["codeBlockStyle"] == "indented"
            and node.node_name == "PRE"
            and node.first_child
            and node.first_child.node_name == "CODE"
        ),
        "replacement": indented_code_block_rule,
    },
    "fencedCodeBlock": {
        "filter": lambda node, opts: (
            opts["codeBlockStyle"] == "fenced"
            and node.node_name == "PRE"
            and node.first_child
            and node.first_child.node_name == "CODE"
        ),
        "replacement": fenced_code_block_rule,
    },
    "horizontalRule": {"filter": "hr", "replacement": horizontal_rule_rule},
    "inlineLink": {
        "filter": lambda node, opts: (
            opts["linkStyle"] == "inlined"
            and node.node_name == "A"
            and node.get_attribute("href")
        ),
        "replacement": inline_link_rule,
    },
    "referenceLink": {
        "filter": lambda node, opts: (
            opts["linkStyle"] == "referenced"
            and node.node_name == "A"
            and node.get_attribute("href")
        ),
        "replacement": reference_link_rule,
        "append": reference_link_store.append_references,
    },
    "emphasis": {"filter": ["em", "i"], "replacement": emphasis_rule},
    "strong": {"filter": ["strong", "b"], "replacement": strong_rule},
    "code": {
        "filter": lambda node, opts: (
            node.node_name == "CODE"
            and not (
                node.parent
                and node.parent.node_name == "PRE"
                and (node.previous_sibling or node.next_sibling)
            )
        ),
        "replacement": code_rule,
    },
    "image": {"filter": "img", "replacement": image_rule},
}
