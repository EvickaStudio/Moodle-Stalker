class RuleManager:
    """
    Manages rules for converting nodes to Markdown. Supports:
    - keep-rules (bypass normal conversion)
    - remove-rules (omit output)
    - normal rules (with a 'filter' and 'replacement')

    Also handles a 'blankRule' and 'defaultRule'.
    """

    def __init__(self, options):
        self.options = options
        self._keep_rules = []
        self._remove_rules = []

        self.blankRule = {"replacement": options["blankReplacement"]}
        self.keepReplacement = options["keepReplacement"]
        self.defaultRule = {"replacement": options["defaultReplacement"]}

        self.rule_list = []
        self.rule_list.extend(iter(options["rules"].values()))

    def add(self, key, rule):
        """
        Insert a custom rule at the front of the list. This has priority.
        """
        self.rule_list.insert(0, rule)

    def keep(self, filter_func):
        """
        Keep a node "as-is" if filter_func(node) is True.
        """
        self._keep_rules.insert(
            0, {"filter": filter_func, "replacement": self.keepReplacement}
        )

    def remove(self, filter_func):
        """
        Remove a node if filter_func(node) is True (emits empty string).
        """
        self._remove_rules.insert(
            0, {"filter": filter_func, "replacement": lambda c, n, o: ""}
        )

    def for_node(self, node):
        """
        Returns the first matching rule for the node, or a blankRule/defaultRule otherwise.
        """
        if getattr(node, "is_blank", False):
            return self.blankRule

        # normal custom rules
        rule = (
            self._match_rule(self.rule_list, node)
            or self._match_rule(self._keep_rules, node)
            or self._match_rule(self._remove_rules, node)
        )
        return rule or self.defaultRule

    def for_each_rule(self, fn):
        """
        Allows iterating over all rules in the main rule list (e.g., for post-processing).
        """
        for i, r in enumerate(self.rule_list):
            fn(r, i)

    def _match_rule(self, rules_list, node):
        return next(
            (
                rule_def
                for rule_def in rules_list
                if _rule_filter_matches(rule_def["filter"], node, self.options)
            ),
            None,
        )


def _rule_filter_matches(filt, node, options):
    """
    Return True if a node matches the filter 'filt' in a rule:
      - str => node.node_name.lower() == filt
      - list => node.node_name.lower() in filt
      - callable => filt(node, options) => bool
    """
    if isinstance(filt, str):
        return node.node_name.lower() == filt
    elif isinstance(filt, list):
        return node.node_name.lower() in filt
    elif callable(filt):
        return filt(node, options)
    else:
        raise TypeError("Rule filters must be str, list, or callable.")
