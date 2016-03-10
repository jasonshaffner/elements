class HTMElement(object):

	def __init__(self, tagname, **kwargs):
		self.tagname = tagname
		self.attributes = kwargs.get('attributes', [])
		self.content = kwargs.get('content', [])

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
		return markup

class HTMPage(HTMElement):
	def __init__(self):
		self.preamble='Content-type: text/html\n\n<!doctype html>\n'
		self.container = HTMElement("html")
		self.head = HTMElement("head")
		self.body = HTMElement("body")
		
	def construct(self):
		markup = self.preamble
		self.container.add_content(self.head)
		self.container.add_content(self.body)
		markup += self.container.construct()
		return markup
		

class HTMAttribute(object):
	def __init__(self, name, value):
		self.name = name
		self.value = value

	def construct(self):
		return self.name + '="' + str(self.value) + '"'


class HTMEnclosed_element(HTMElement):
	def __init__(self, tagname, **kwargs):
		self.tagname = tagname
		self.attributes = kwargs.get('attributes', [])

	def construct(self, indent=0):
		markup = "\t" * indent + "<" +  self.tagname
		if self.attributes:
			for attribute in self.attributes:
				markup += attribute.construct()
		markup += ">\n"
		return markup


class HTMEmpty_element(HTMElement):

	def __init__(self, tagname):
		self.tagname = tagname

	def construct(self, indent=0):
		return "\t" * indent + "<" + self.tagname + ">\n"


class HTMBreak(HTMEmpty_element):

	def __init__(self):
		self.tagname = "br"
