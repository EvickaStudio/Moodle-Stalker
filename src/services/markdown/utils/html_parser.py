import html.entities
import html.parser


class Node:
    """
    Represents a node in an HTML-like tree structure.

    Attributes:
        node_name (str): Uppercase name of the node (e.g., 'DIV', '#TEXT').
        node_type (int): Numeric type (1=Element, 3=Text, 8=Comment, etc.).
        parent (Node or None): Parent node in the tree.
        children (list[Node]): Child nodes.
        attributes (dict): Node attributes.
        data (str): For text nodes, the actual text content.
        is_self_closing (bool): Whether this node is self-closing.

    Properties:
        first_child: The first child node, or None if none.
        last_child: The last child node, or None if none.
        next_sibling: The next sibling node, or None if none.
        previous_sibling: The previous sibling node, or None if none.
        node_value: The text data if it's a text node, otherwise "".
        is_element: True if node_type==1, else False.

    Methods:
        append_child(child): Adds a child node.
        remove_self(): Detaches self from its parent's children.
        text_content(): Gathers text content from this node and descendants.
        get_attribute(attr): Returns the attribute value or None.
        set_attribute(attr, value): Sets an attribute.
        index_in_parent(node): Returns the 0-based index of 'node' among children.
    """

    def __init__(self, node_name, node_type, parent=None):
        self.node_name = node_name.upper()
        self.node_type = node_type
        self.parent = parent
        self.children = []
        self.attributes = {}
        self.data = ""  # used if it's a text node
        self.is_self_closing = False

    @property
    def first_child(self):
        return self.children[0] if self.children else None

    @property
    def last_child(self):
        return self.children[-1] if self.children else None

    @property
    def next_sibling(self):
        if not self.parent:
            return None
        siblings = self.parent.children
        idx = siblings.index(self)
        return siblings[idx + 1] if idx + 1 < len(siblings) else None

    @property
    def previous_sibling(self):
        if not self.parent:
            return None
        siblings = self.parent.children
        idx = siblings.index(self)
        return siblings[idx - 1] if idx >= 1 else None

    @property
    def node_value(self):
        return self.data

    @property
    def is_element(self):
        return self.node_type == 1

    def append_child(self, child):
        child.parent = self
        self.children.append(child)

    def remove_self(self):
        if self.parent:
            self.parent.children.remove(self)
        self.parent = None

    def text_content(self):
        if self.node_type in [3, 4]:  # text or cdata
            return self.data
        return "".join(child.text_content() for child in self.children)

    def get_attribute(self, attr):
        return self.attributes.get(attr)

    def set_attribute(self, attr, value):
        self.attributes[attr] = value

    def index_in_parent(self, node):
        return self.children.index(node) if self.children else 0


class TurndownHTMLParser(html.parser.HTMLParser):
    """
    A custom HTML parser that generates a tree of Nodes rather than a single DOM object.
    """

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.root = Node("document", 1)
        self.current_node = self.root

    def handle_starttag(self, tag, attrs):
        new_node = Node(tag, 1, parent=self.current_node)
        for k, v in attrs:
            new_node.set_attribute(k, v)
        self.current_node.append_child(new_node)

        # Mark some tags as self-closing by default
        if tag in {"br", "img", "hr", "meta", "input", "link"}:
            new_node.is_self_closing = True
        else:
            # Move into that node
            self.current_node = new_node

    def handle_endtag(self, tag):
        temp = self.current_node
        while temp and temp.node_name.lower() != tag.lower():
            temp = temp.parent
        if temp:
            self.current_node = temp.parent or temp

    def handle_startendtag(self, tag, attrs):
        # Self-closing
        new_node = Node(tag, 1, parent=self.current_node)
        new_node.is_self_closing = True
        for k, v in attrs:
            new_node.set_attribute(k, v)
        self.current_node.append_child(new_node)

    def handle_data(self, data):
        text_node = Node("#text", 3, parent=self.current_node)
        text_node.data = data
        self.current_node.append_child(text_node)

    def handle_entityref(self, name):
        text_node = Node("#text", 3, parent=self.current_node)
        c = html.entities.html5.get(name, f"&{name};")
        text_node.data = c
        self.current_node.append_child(text_node)

    def handle_charref(self, name):
        text_node = Node("#text", 3, parent=self.current_node)
        try:
            codepoint = int(name[1:], 16) if name.startswith("x") else int(name)
            text_node.data = chr(codepoint)
        except ValueError:
            text_node.data = f"&#{name};"
        self.current_node.append_child(text_node)


def parse_from_string(html_str):
    """
    Parses an HTML string into the root Node of the constructed tree.
    """
    parser = TurndownHTMLParser()
    parser.feed(html_str)
    parser.close()
    return parser.root
