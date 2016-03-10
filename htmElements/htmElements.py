class HTMElement(object):

	def __init__(self, tagname, **kwargs):
		self.tagname = tagname
		self.attributes = kwargs.get('attributes', [])
		self.content = kwargs.get('content', [])
		self.prebreak = kwargs.get("prebreak", False)
		self.postbreak = kwargs.get("postbreak", False)

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
				if isinstance(element, HTMElement): markup += element.construct(indent=indent+1)
				else: markup += "\t" * (indent+1) + element
		markup += "\t" * indent + "</" + self.tagname + ">\n"
		if self.prebreak: markup = HTMBreak.construct(HTMBreak()) + markup
		if self.postbreak: markup += HTMBreak.construct(HTMBreak())
		return markup

class HTMPage(HTMElement):
	def __init__(self, **kwargs):
		self.tagname = "html"
		HTMElement.__init__(self, self.tagname)
		self.preamble = kwargs.get('preamble', 'Content-type: text/html\n\n<!doctype html>\n')
		self.head = kwargs.get('head', HTMElement("head"))
		self.body = kwargs.get('body', HTMElement("body"))
		
	def construct(self):
		markup = self.preamble
		self.add_content(self.head)
		self.add_content(self.body)
		markup += HTMElement.construct(self)
		return markup
		

class HTMAttribute(object):
	def __init__(self, name, value):
		self.name = name
		self.value = value

	def construct(self):
		return " " + self.name + '="' + str(self.value) + '"'


class HTMEnclosed_element(HTMElement):
	def __init__(self, tagname, **kwargs):
		self.tagname = tagname
		HTMElement.__init__(self, self.tagname, **kwargs)

	def construct(self, indent=0):
		markup = "\t" * indent + "<" +  self.tagname
		if self.attributes:
			for attribute in self.attributes:
				markup += attribute.construct()
		markup += ">\n"
		if self.prebreak: markup = HTMBreak.construct(HTMBreak()) + markup
		if self.postbreak: markup += HTMBreak.construct(HTMBreak())
		return markup


class HTMEmpty_element(HTMElement):

	def __init__(self, tagname):
		self.tagname = tagname

	def construct(self, indent=0):
		return "\t" * indent + "<" + self.tagname + ">\n"


class HTMBreak(HTMEmpty_element):

	def __init__(self):
		self.tagname = "br"

class HTMA(HTMElement):

	def __init__(self, href, **kwargs):
		self.tagname = "a"
		HTMElement.__init__(self, self.tagname, **kwargs)
		self.href = HTMAttribute("href", href)
		self.attributes.insert(0, self.href)
		self.content = [kwargs.get('text', None)]

class HTMStylesheet(HTMEnclosed_element):

	def __init__(self, href):
		self.tagname = "link"
		HTMEnclosed_element.__init__(self, self.tagname)
		self.href = HTMAttribute("href", href)
		self.rel = HTMAttribute("rel", "stylesheet")
		self.attributes = [self.rel, self.href]

class HTMIcon(HTMEnclosed_element):

	def __init__(self, href):
		self.tagname = "link"
		HTMEnclosed_element.__init__(self, self.tagname)
		self.href = HTMAttribute("href", href)
		self.rel = HTMAttribute("rel", "shortcut icon")
		self.attributes = [self.rel, self.href]

class HTMTitle(HTMElement):

	def __init__(self, title):
		self.tagname = "title"
		HTMElement.__init__(self, self.tagname)
		self.content = [title + '\n']

class HTMBody(HTMElement):

	def __init__(self, **kwargs):
		self.tagname = "body"
		HTMElement.__init__(self, self.tagname, **kwargs)

class HTMDiv(HTMElement):

	def __init__(self, id, **kwargs):
		self.tagname = "div"
		HTMElement.__init__(self, self.tagname, **kwargs)
		self.id = HTMAttribute("id", id)
		self.attributes.insert(0, self.id)

class HTMInput(HTMEnclosed_element):

	def __init__(self, name, type, **kwargs):
		self.tagname = "input"
		HTMEnclosed_element.__init__(self, self.tagname, **kwargs)
		self.name = HTMAttribute("name", name)
		self.type = HTMAttribute("type", type)
		self.value = kwargs.get("value", None)
		self.size = kwargs.get("size", None)
		self.attributes = [self.type, self.name]
		if self.value: self.attributes.append(HTMAttribute("value", self.value))
		if self.size: self.attributes.append(HTMAttribute("size", self.size))

class HTMSubmitbutton(HTMEnclosed_element):
	
	def __init__(self):
		self.tagname = "input"
		HTMEnclosed_element.__init__(self, self.tagname)
		self.attributes = [HTMAttribute("type", "submit"), HTMAttribute("value", "Submit")]

class HTMResetbutton(HTMEnclosed_element):
	
	def __init__(self):
		self.tagname = "input"
		HTMEnclosed_element.__init__(self, self.tagname)
		self.attributes = [HTMAttribute("type", "reset"), HTMAttribute("value", "Reset")]

class HTMForm(HTMElement):

	def __init__(self, method, action, **kwargs):
		self.tagname = "form"
		HTMElement.__init__(self, self.tagname, **kwargs)
		self.method = HTMAttribute("method", method)
		self.action = HTMAttribute("action", action)
		self.attributes.insert(0, self.action)
		self.attributes.insert(0, self.method)

class HTMTextarea(HTMElement):

	def __init__(self, name, rows, cols, **kwargs):
		self.tagname = "textarea"
		HTMElement.__init__(self, self.tagname, **kwargs)
		self.name = HTMAttribute("name", name)
		self.rows = HTMAttribute("rows", rows)
		self.cols = HTMAttribute("cols", cols)
		self.attributes.insert(0, self.cols)
		self.attributes.insert(0, self.rows)
		self.attributes.insert(0, self.name)
