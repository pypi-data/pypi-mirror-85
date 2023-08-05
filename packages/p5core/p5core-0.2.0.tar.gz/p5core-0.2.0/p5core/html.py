from typing import Final, List, Optional

_inline_tags: Final[List[str]] = [
    "a",
    "abbr",
    "acronym",
    "b",
    "bdo",
    "big",
    "br",
    "button",
    "cite",
    "code",
    "dfn",
    "em",
    "i",
    "img",
    "input",
    "kbd",
    "label",
    "map",
    "object",
    "output",
    "q",
    "samp",
    "script",
    "select",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
    "textarea",
    "time",
    "tt",
    "var",
]


class Tag:
    _push_levels = []

    def __init__(self, tag: str, *, parent=None, text: Optional[str] = None, **kwargs):
        self.tag = tag
        self.attribs = {}
        self.children = []  # text or Tag
        if text is not None:
            self.append(text)
        self.parent = parent
        if parent is None and Tag._push_levels:
            self.parent = Tag._push_levels[-1]
        if self.parent:
            self.parent.children.append(self)
        for attrib, attrib_value in kwargs.items():
            if attrib == "class_":
                attrib = "class"
            self.attribs[attrib] = attrib_value

    def __str__(self):
        # TODO ça va pas pour les \n
        ret = ""
        if self.inline:
            indent = ""
            line_break = ""
            tag_terminator = ""
        else:
            indent = self.indent_level * "    "
            line_break = "\n"
            if any(isinstance(child, str) for child in self.children):
                line_break = ""
            tag_terminator = "\n"

        ret += f"{indent}<{self.tag}"
        ret += "".join(
            f' {attrib}="{attrib_value}"'
            for attrib, attrib_value in self.attribs.items()
        )
        if not self.children:
            ret += f"/>{tag_terminator}"
        else:
            ret += f">{line_break}"
            ret += "".join(str(child) for child in self.children)
            if line_break:
                ret += f"{indent}"
            ret += f"</{self.tag}>{tag_terminator}"
        return ret

    def __enter__(self):
        Tag._push_levels.append(self)
        return self

    def __exit__(self, type, value, traceback):
        Tag._push_levels.pop()

    def __getattr__(self, name):
        return Tag(tag=name, parent=self)

    def append(self, element):
        self.children.append(element)
        if isinstance(element, Tag):
            element.parent = self

    @property
    def indent_level(self):
        # TODO mécanisme de cache ?
        if self.inline:
            return 0
        parent = self.parent
        level = 0
        while parent:
            level += 1
            parent = parent.parent
        return level

    @property
    def inline(self):
        return self.tag in _inline_tags
