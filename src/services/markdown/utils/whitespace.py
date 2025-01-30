# flake8: noqa: F841
"""
The collapse_whitespace function is adapted from collapse-whitespace by Luc Thevenard.
The MIT License (MIT)
Copyright (c) 2014 Luc Thevenard
"""

import re


def collapse_whitespace(element, is_block_fn, is_void_fn, is_pre_fn):
    """
    Collapses consecutive whitespace characters in `element`'s text nodes into a single space.
    Preserves whitespace in preformatted text and void elements.

    Args:
        element (Node): The root element to process.
        is_block_fn (callable): A function(node) -> bool indicating whether the node is block-level.
        is_void_fn (callable): A function(node) -> bool indicating whether the node is a void element.
        is_pre_fn (callable): A function(node) -> bool indicating whether the node is a pre/code element.

    Returns:
        None. Modifies the node-tree in-place.
    """
    if not element.first_child or is_pre_fn(element):
        return

    prev_text_node = None
    keep_leading_space = False

    # We iterate through the tree manually, looking ahead for the "next node".
    # We'll use `current_node` and get the next node by checking children/siblings/parents:
    current_node = element.first_child
    prev_node = element  # We'll track the previously processed node to know where to continue from

    while current_node != element:
        if current_node.node_type in (3, 4):  # TEXT_NODE or CDATA_SECTION_NODE
            new_data, keep_leading_space = _process_text_node(
                current_node, prev_text_node, keep_leading_space
            )
            if new_data is None:
                next_in_line = _determine_next_node(prev_node, current_node, is_pre_fn)
                current_node.remove_self()
                current_node = next_in_line
                continue
            current_node.data = new_data
            prev_text_node = current_node

        elif current_node.node_type == 1:  # ELEMENT_NODE
            _process_element_node(
                current_node,
                is_block_fn,
                is_void_fn,
                is_pre_fn,
                prev_text_node,
                keep_leading_space,
            )
        else:
            # For comment or unknown node types, remove them
            next_in_line = _determine_next_node(prev_node, current_node, is_pre_fn)
            current_node.remove_self()
            current_node = next_in_line
            continue

        next_in_line = _determine_next_node(prev_node, current_node, is_pre_fn)
        prev_node = current_node
        current_node = next_in_line

    # Final trimming if there's a trailing space in the last text node
    if prev_text_node:
        prev_text_node.data = prev_text_node.data.rstrip()
        if not prev_text_node.data:
            prev_text_node.remove_self()


def _determine_next_node(previous_node, current_node, is_pre_fn):
    """
    Determines which node is "next" in the depth-first traversal sequence.

    Args:
        previous_node (Node): The last processed node.
        current_node (Node): The current node.
        is_pre_fn (callable): A function(node) -> bool that checks if a node is <pre> or <code>.

    Returns:
        Node: The next node in the traversal, or the parent if we are at the end of siblings.
    """
    # If the `previous_node` is the parent of the `current_node` or the node is <pre>/<code>,
    # we move to the next sibling or up to the parent.
    if (previous_node and previous_node.parent == current_node) or is_pre_fn(
        current_node
    ):
        return current_node.next_sibling or current_node.parent

    # Otherwise, we go down into children first, else siblings, else up
    if current_node.first_child:
        return current_node.first_child
    if current_node.next_sibling:
        return current_node.next_sibling
    return current_node.parent


def _process_text_node(current_node, prev_text_node, keep_leading_space):
    new_data = re.sub(r"[ \r\n\t]+", " ", current_node.data)
    if (
        (not prev_text_node or prev_text_node.data.endswith(" "))
        and (not keep_leading_space)
        and new_data.startswith(" ")
    ):
        new_data = new_data[1:]
    if not new_data:
        return None, keep_leading_space
    return new_data, keep_leading_space


def _process_element_node(
    current_node,
    is_block_fn,
    is_void_fn,
    is_pre_fn,
    prev_text_node,
    keep_leading_space,
):
    if is_block_fn(current_node) or current_node.node_name == "BR":
        if prev_text_node:
            prev_text_node.data = prev_text_node.data.rstrip()
        prev_text_node = None
        keep_leading_space = False
    elif is_void_fn(current_node) or is_pre_fn(current_node):
        prev_text_node = None
        keep_leading_space = True
    else:
        keep_leading_space = False
