import functools

from .rules.commonmark import COMMONMARK_RULES
from .rules.manager import RuleManager
from .utils.node import enhance_node
from .utils.root_node import build_root_node
from .utils.utilities import extend, trim_leading_newlines, trim_trailing_newlines


class MarkdownConverter:
    """
    A refactored version of TurndownService. Converts HTML -> Markdown.

    Methods:
        to_markdown(input_obj):  Main method to convert HTML or Node to MD.
        use(plugin):             Apply a plugin (function or list of functions).
        add_rule(key, rule):     Manually add a rule.
        keep(filter_func):       Keep some elements unconverted (as-is).
        remove(filter_func):     Remove some elements entirely (empty output).
        escape(text):            Escape special Markdown characters.
    """

    def __init__(self, options=None):
        if options is None:
            options = {}

        defaults = {
            "rules": COMMONMARK_RULES,
            "headingStyle": "setext",
            "hr": "* * *",
            "bulletListMarker": "*",
            "codeBlockStyle": "indented",
            "fence": "```",
            "emDelimiter": "_",
            "strongDelimiter": "**",
            "linkStyle": "inlined",
            "linkReferenceStyle": "full",
            "br": "  ",
            "preformattedCode": False,
            "blankReplacement": lambda content, node, opts: (
                "\n\n" if getattr(node, "is_block", False) else ""
            ),
            "keepReplacement": lambda content, node, opts: (
                "\n\n" + node.outer_html + "\n\n"
                if getattr(node, "is_block", False)
                else node.outer_html
            ),
            "defaultReplacement": lambda content, node, opts: (
                "\n\n" + content + "\n\n"
                if getattr(node, "is_block", False)
                else content
            ),
        }
        # Merge user options with defaults
        self.options = extend({}, defaults, options)
        self.rules = RuleManager(self.options)

    def to_markdown(self, input_obj):
        """
        Convert the given HTML or node to a Markdown string.
        """
        if not _can_convert(input_obj):
            raise TypeError(f"Cannot convert object: {input_obj}")

        text_input = input_obj.strip() if isinstance(input_obj, str) else ""
        if isinstance(input_obj, str) and not text_input:
            return ""

        root = build_root_node(input_obj, self.options)
        result = self._process_children(root)
        return self._post_process(result).strip("\r\n ")

    def use(self, plugin):
        """
        Register one or more plugin(s). A plugin is a function(turndown_service).
        """
        if isinstance(plugin, list):
            for p in plugin:
                self.use(p)
        elif callable(plugin):
            plugin(self)
        else:
            raise TypeError("Plugin must be callable or list of callables.")
        return self

    def add_rule(self, key, rule):
        self.rules.add(key, rule)
        return self

    def keep(self, filter_func):
        self.rules.keep(filter_func)
        return self

    def remove(self, filter_func):
        self.rules.remove(filter_func)
        return self

    def escape(self, text):
        """
        Escapes certain characters so that they are not parsed as MD.
        """
        import re

        escapes = [
            (r"\\", r"\\\\"),
            (r"\*", r"\\*"),
            (r"^-", r"\\-"),
            (r"^\+ ", r"\\+ "),
            (r"^(=+)", r"\\\1"),
            (r"^(#{1,6}) ", r"\\\1 "),
            (r"`", r"\\`"),
            (r"^~~~", r"\\~~~"),
            (r"\[", r"\\["),
            (r"\]", r"\\]"),
            (r"^>", r"\\>"),
            (r"_", r"\\_"),
            (r"^(\d+)\. ", r"\1\\. "),
        ]
        for pat, repl in escapes:
            text = re.sub(pat, repl, text, flags=re.MULTILINE)
        return text

    # --- Internals ---

    def _process_children(self, parent_node):
        """
        Recursively processes the child nodes of parent_node, building a single string.
        """

        def reducer(acc, child):
            # Enhance the node with metadata
            child = enhance_node(child, self.options)
            if child.node_type == 3:  # TEXT
                # If it's code, preserve; otherwise do .escape
                piece = (
                    child.node_value if child.is_code else self.escape(child.node_value)
                )
            elif child.node_type == 1:  # ELEMENT
                piece = self._replacement_for_node(child)
            else:
                piece = ""
            return _join_markdown(acc, piece)

        return functools.reduce(reducer, parent_node.children, "")

    def _replacement_for_node(self, node):
        """
        Retrieves the rule for this node, and calls it with (content, node, options).
        Content is the result of processing children. We then handle flanking whitespace.
        """
        rule = self.rules.for_node(node)
        inner_content = self._process_children(node)
        ws = node.flanking_whitespace
        if ws["leading"] or ws["trailing"]:
            inner_content = inner_content.strip()
        return (
            ws["leading"]
            + rule["replacement"](inner_content, node, self.options)
            + ws["trailing"]
        )

    def _post_process(self, text):
        """
        After collecting all text, let each rule append references or other data to the end.
        """
        results = [text]

        def try_append(rule_obj, _):
            appended = ""
            if "append" in rule_obj and callable(rule_obj["append"]):
                appended = rule_obj["append"](self.options)
            if appended:
                results[0] = _join_markdown(results[0], appended)

        self.rules.for_each_rule(try_append)
        return results[0]


def _join_markdown(first, second):
    """
    Joins two Markdown segments with minimal extra newlines.
    """
    s1 = trim_trailing_newlines(first)
    s2 = trim_leading_newlines(second)
    # Figure out how many newlines we had at the boundary
    newlines_count = (len(first) - len(s1)) + (len(second) - len(s2))
    # Cap at 2
    sep = "\n\n"[:newlines_count]
    return s1 + sep + s2


def _can_convert(x):
    """
    Determine if x is either a non-empty string or a valid node with .node_type in [1,9,11].
    """
    if x is None:
        return False
    if isinstance(x, str):
        return True
    return x.node_type in [1, 9, 11] if hasattr(x, "node_type") else False
