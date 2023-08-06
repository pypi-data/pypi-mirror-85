import re

NEWLINE = "\n"
LINK_LINE_PATTERN = re.compile(r"^=>[ \t]*(\S+)([ \t]+(.+))?$")
HEADING_LINE_PATTERN = re.compile(r"^(#{1,3})\s+(.+)$")


class GeminiNode:
    __slots__ = ("text",)
    text: str

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.text.__repr__()}"


class TextNode(GeminiNode):
    pass


class ListItemNode(GeminiNode):
    pass


class HeadingNode(GeminiNode):
    __slots__ = "heading"
    heading: str

    def __init__(self, text, heading):
        self.text = text
        self.heading = heading


class H1Node(HeadingNode):
    pass


class H2Node(HeadingNode):
    pass


class H3Node(HeadingNode):
    pass


class LinkNode(GeminiNode):
    __slots__ = ("url", "name")
    url: str
    name: str

    def __init__(self, text, url, name):
        self.text = text
        self.url = url
        self.name = name

    def __repr__(self):
        result = f"{self.__class__.__name__}: {self.url.__repr__()}"
        if self.name:
            result += f" {self.name.__repr__()}"
        return result


class PreformattedNode(GeminiNode):
    __slots__ = ("alt",)
    alt: str

    def __init__(self, text, alt):
        self.text = text
        self.alt = alt  # optional alt-text for preformatted text

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.alt.__repr__()}"


def parse(text):
    """
    Naive one-pass parser.
    """
    nodes = []
    preformatted = None
    preformatted_alt = ""

    for line in text.strip().split(NEWLINE):

        if line.startswith("```"):
            if preformatted is None:
                # start preformatted mode
                preformatted = ""
                preformatted_alt = line[3:]
            else:
                nodes.append(PreformattedNode(preformatted, preformatted_alt))
                preformatted = None

        elif preformatted is not None:
            if len(preformatted) > 0:
                preformatted += "\n"
            preformatted += line

        elif line.startswith("=>"):
            match = LINK_LINE_PATTERN.match(line)
            if not match:
                nodes.append(TextNode(line))
                continue
            url = match.group(1)
            name = match.group(3)  # may be None
            nodes.append(LinkNode(text=line, url=url, name=name))

        elif line.startswith("*"):
            nodes.append(ListItemNode(line))

        elif line.startswith("#"):
            match = HEADING_LINE_PATTERN.match(line)
            if not match:
                nodes.append(TextNode(line))
                continue
            heading_text = match.group(2)
            hashes = match.group(1)
            level = len(hashes)
            if level == 1:
                nodes.append(H1Node(line, heading_text))
            elif level == 2:
                nodes.append(H2Node(line, heading_text))
            elif level == 3:
                nodes.append(H3Node(line, heading_text))

        else:
            nodes.append(TextNode(line))

    return nodes


def get_title(model):
    # model: instance of Tab
    # if a title is found it is returned immediately
    # otherwise, None is returned.
    mime = model.mime_type
    if mime.startswith("text/gemini"):
        nodes = model.gemini_nodes
        for nodetype in [H1Node, H2Node, H3Node]:
            for node in nodes:
                if isinstance(node, nodetype):
                    return node.text.lstrip("#").strip()

    if mime.startswith("text/x-picrosserror"):
        return model.plaintext.splitlines()[1]

    if mime.startswith("text/"):
        url = model.url
        return str(url).split("/")[-1]

    return None


def is_title_node(node: GeminiNode):
    return type(node) in [H1Node, H2Node, H3Node]


def get_toc(model):
    mime = model.mime_type
    if mime.startswith("text/gemini"):
        nodes = model.gemini_nodes
        headings = []
        for node in nodes:
            if is_title_node(node):
                headings.append(node.text)
        return headings
    return []
