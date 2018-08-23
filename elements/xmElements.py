class xmElement(object):
    def __init__(self, tagname, **kwargs):
        self.tagname = tagname
        self.attributes = kwargs.get('attributes', [])
        self.content = kwargs.get('content', [])
        self.prebreak = kwargs.get("prebreak", 0)
        self.postbreak = kwargs.get("postbreak", 0)

    def add_attribute(self, attribute):
        self.attributes.append(attribute)

    def add_content(self, content):
        self.content.append(content)

    def construct(self, indent=0):
        markup = "\t" * indent + "<" +  self.tagname 
        if self.attributes:
            for attribute in self.attributes:
                markup += attribute.construct()
        markup += ">\n"
        if self.content:
            for element in self.content:
                if isinstance(element, xmElement): markup += element.construct(indent=indent+1)
                else: markup += "\t" * (indent+1) + element + "\n"
        endtag = "</" + self.tagname + ">"
        if self.prebreak: markup = Break.construct(Break()) * self.prebreak + markup
        if self.postbreak: endtag += Break.construct(Break()) * self.postbreak
        endtag = "\t" * indent + endtag + '\n'
        markup += endtag
        return markup


class Document(xmElement):
    def __init__(self, **kwargs):
        self.tagname = "xml"
        xmElement.__init__(self, self.tagname)
        self.preamble = kwargs.get('preamble', '<?xml version="1.0" encoding="UTF-8"?>')
        self.content = kwargs.get('content', None)

    def construct(self):
        markup = self.preamble
        markup += xmElement.construct(self)
        return markup


class Attribute(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def construct(self):
        return ' ' + self.name + '="' + str(self.value) + '"'


class EnclosedElement(xmElement):
    def __init__(self, tagname, **kwargs):
        self.tagname = tagname
        xmElement.__init__(self, self.tagname, **kwargs)

    def construct(self, indent=0):
        markup = "<" +  self.tagname
        if self.attributes:
            for attribute in self.attributes:
                markup += attribute.construct()
        markup += ">"
        if self.prebreak: markup = Break.construct(Break()) * self.prebreak + markup
        if self.postbreak: markup += Break.construct(Break()) * self.postbreak
        markup = "\t" * indent + markup + '\n'
        return markup


class EmptyElement(xmElement):
    def __init__(self, tagname):
        self.tagname = tagname

    def construct(self, indent=0):
        return "\t" * indent + "<" + self.tagname + ">"
