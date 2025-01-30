import re

from .utilities import (
    has_meaningful_when_blank,
    has_void,
    is_block,
    is_meaningful_when_blank,
    is_void,
)


def enhance_node(node, options):
    """
    Augments the node with:
    - node.is_block: True if node is block-like
    - node.is_code: True if node is <code> or has a code parent
    - node.is_blank: True if node is considered blank (no text or only whitespace)
    - node.flanking_whitespace: dict(leading, trailing)
    """
    node.is_block = is_block(node)
    node.is_code = (node.node_name == "CODE") or (
        node.parent and getattr(node.parent, "is_code", False)
    )
    node.is_blank = _is_blank(node)
    node.flanking_whitespace = _compute_flanking_whitespace(node, options)
    return node


def _is_blank(node):
    """
    Returns True if node is blank: either text-like with only whitespace or
    all children are blank (and node not void/meaningful).
    """
    if is_void(node) or is_meaningful_when_blank(node):
        return False

    if node.node_type in [3, 4]:  # text or cdata
        return bool(re.match(r"^\s*$", node.data))

    if has_void(node) or has_meaningful_when_blank(node):
        return False

    return all(_is_blank(child) for child in node.children)


def _compute_flanking_whitespace(node, options):
    """
    For inline nodes, figure out if there's whitespace leading or trailing that might
    need to be trimmed or replaced.
    """
    # If it's a block or if code blocks are preformatted, we skip
    if node.is_block or (options.get("preformattedCode") and node.is_code):
        return {"leading": "", "trailing": ""}

    text = node.text_content()
    leading_ws, trailing_ws = _extract_edge_whitespace(text)

    if leading_ws and _flanked_by_whitespace("left", node, options):
        leading_ws = ""
    if trailing_ws and _flanked_by_whitespace("right", node, options):
        trailing_ws = ""

    return {"leading": leading_ws, "trailing": trailing_ws}


def _extract_edge_whitespace(text):
    if match := re.match(r"^(\s*)(.*?)(\s*)$", text, flags=re.DOTALL):
        return match[1], match[3]
    return "", ""


def _flanked_by_whitespace(side, node, options):
    """
    Checks neighbors to see if there's whitespace that would make
    the leading/trailing space redundant.
    """
    sibling = node.previous_sibling if side == "left" else node.next_sibling
    if sibling:
        if sibling.node_type == 3 and sibling.data:
            if side == "left" and sibling.data.endswith(" "):
                return True
            if side == "right" and sibling.data.startswith(" "):
                return True

        if options.get("preformattedCode") and sibling.node_name == "CODE":
            return False

        # For inline siblings, check if the text content has leading/trailing spaces
        if sibling.node_type == 1 and not is_block(sibling):
            sibling_text = sibling.text_content()
            if side == "left" and sibling_text.endswith(" "):
                return True
            if side == "right" and sibling_text.startswith(" "):
                return True
    return False
