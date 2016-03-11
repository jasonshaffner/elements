class htmElement(object):
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
				if isinstance(element, htmElement): markup += element.construct(indent=indent+1)
				else: markup += "\t" * (indent+1) + element + "\n"
		endtag = "</" + self.tagname + ">"
		if self.prebreak: markup = Break.construct(Break()) * self.prebreak + markup
		if self.postbreak: endtag += Break.construct(Break()) * self.postbreak
		endtag = "\t" * indent + endtag + '\n'
		markup += endtag
		return markup


class Page(htmElement):
	def __init__(self, **kwargs):
		self.tagname = "html"
		htmElement.__init__(self, self.tagname)
		self.preamble = kwargs.get('preamble', 'Content-type: text/html\n\n<!doctype html>\n')
		self.head = kwargs.get('head', htmElement("head"))
		self.body = kwargs.get('body', htmElement("body"))
		
	def construct(self):
		markup = self.preamble
		self.add_content(self.head)
		self.add_content(self.body)
		markup += htmElement.construct(self)
		return markup
		

class Attribute(object):
	def __init__(self, name, value):
		self.name = name
		self.value = value

	def construct(self):
		return " " + self.name + '=' + str(self.value)


class Enclosed_element(htmElement):
	def __init__(self, tagname, **kwargs):
		self.tagname = tagname
		htmElement.__init__(self, self.tagname, **kwargs)

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


class Empty_element(htmElement):
	def __init__(self, tagname):
		self.tagname = tagname

	def construct(self, indent=0):
		return "\t" * indent + "<" + self.tagname + ">"


class Break(Empty_element):
	def __init__(self):
		self.tagname = "br"


class A(htmElement):
	def __init__(self, href, **kwargs):
		self.tagname = "a"
		htmElement.__init__(self, self.tagname, **kwargs)
		self.href = Attribute("href", href)
		self.attributes.insert(0, self.href)
		self.content = [kwargs.get('text', None)]

	def construct(self, indent=0):
		markup = "\t" * indent + "<" +  self.tagname 
		for attribute in self.attributes:
			markup += attribute.construct()
		markup += ">"
		if self.content: markup += self.content[0]
		markup += "</" + self.tagname + ">"
		if self.prebreak: markup = Break.construct(Break()) * self.prebreak + markup
		if self.postbreak: markup += Break.construct(Break()) * self.postbreak
		return markup + '\n'


class Stylesheet(Enclosed_element):
	def __init__(self, href):
		self.tagname = "link"
		Enclosed_element.__init__(self, self.tagname)
		self.href = Attribute("href", href)
		self.rel = Attribute("rel", "stylesheet")
		self.attributes = [self.rel, self.href]


class Icon(Enclosed_element):
	def __init__(self, href):
		self.tagname = "link"
		Enclosed_element.__init__(self, self.tagname)
		self.href = Attribute("href", href)
		self.rel = Attribute("rel", "shortcut icon")
		self.attributes = [self.rel, self.href]


class Title(htmElement):
	def __init__(self, title):
		self.tagname = "title"
		htmElement.__init__(self, self.tagname)
		self.content = [title]


class Body(htmElement):
	def __init__(self, **kwargs):
		self.tagname = "body"
		htmElement.__init__(self, self.tagname, **kwargs)


class Div(htmElement):
	def __init__(self, id, **kwargs):
		self.tagname = "div"
		htmElement.__init__(self, self.tagname, **kwargs)
		self.id = Attribute("id", id)
		self.attributes.insert(0, self.id)


class Input(Enclosed_element):
	def __init__(self, name, type, **kwargs):
		self.tagname = "input"
		Enclosed_element.__init__(self, self.tagname, **kwargs)
		self.name = Attribute("name", name)
		self.type = Attribute("type", type)
		self.value = kwargs.get("value", None)
		self.size = kwargs.get("size", None)
		self.attributes = [self.type, self.name]
		if self.value: self.attributes.append(Attribute("value", self.value))
		if self.size: self.attributes.append(Attribute("size", self.size))


class Submitbutton(Enclosed_element):
	def __init__(self):
		self.tagname = "input"
		Enclosed_element.__init__(self, self.tagname)
		self.attributes = [Attribute("type", "submit"), Attribute("value", "Submit")]


class Resetbutton(Enclosed_element):
	def __init__(self):
		self.tagname = "input"
		Enclosed_element.__init__(self, self.tagname)
		self.attributes = [Attribute("type", "reset"), Attribute("value", "Reset")]


class Form(htmElement):
	def __init__(self, method, action, **kwargs):
		self.tagname = "form"
		htmElement.__init__(self, self.tagname, **kwargs)
		self.method = Attribute("method", method)
		self.action = Attribute("action", action)
		self.attributes.insert(0, self.action)
		self.attributes.insert(0, self.method)


class Textarea(htmElement):
	def __init__(self, name, rows, cols, **kwargs):
		self.tagname = "textarea"
		htmElement.__init__(self, self.tagname, **kwargs)
		self.name = Attribute("name", name)
		self.rows = Attribute("rows", rows)
		self.cols = Attribute("cols", cols)
		self.attributes.insert(0, self.name)
		self.attributes.insert(0, self.cols)
		self.attributes.insert(0, self.rows)

	def construct(self, indent=0):
		markup = "\t" * indent + "<" +  self.tagname 
		for attribute in self.attributes:
			markup += attribute.construct()
		markup += ">"
		if self.content: markup += self.content[0]
		markup += "</" + self.tagname + ">"
		if self.prebreak: markup = Break.construct(Break()) * self.prebreak + markup
		if self.postbreak: markup += Break.construct(Break()) * self.postbreak
		return markup + '\n'
