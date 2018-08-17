class query:
	def __init__(self, elementName, operation='query', *elements):
		self.elementName = elementName
		self.operation = operation
		if elements and not isinstance(elements, type(self)) and not isinstance(elements[0], type(self)):
			self.elements = [e for element in elements for e in element]
		else: self.elements = elements

	def __call__(self):
		return self.construct()

	def addElement(self, element):
		self.elements.append(element)

	def construct(self, indent=0):
		query = " ".join([self.operation, self.elementName])
		if not self.elements: return query + "\n"
		if isinstance(self.elements, type(self)):
			query += " {\n\t" + self.elements.construct(indent + 1)
		else:
			for element in self.elements:
				query += " {\n\t" + element.construct(indent + 1)
		query += "\n}"
		return query


class queryElement(query):
	def __init__(self, elementName, *elements, **kwargs):
		self.elementName = elementName
		if elements and not isinstance(elements, type(self)) and not isinstance(elements[0], type(self)):
			self.elements = [e for element in elements for e in element]
		else: self.elements = elements
		self.condition = kwargs.get('condition', None)
		self.input = kwargs.get('input', None)
		self.argument = kwargs.get('argument', None)

	def __call__(self, indent=0):
		return self.construct(indent)

	def construct(self, indent=0):
		query = self.elementName
		if self.condition: query += " " + self.condition()
		if self.input: query += " " + self.input()
		if self.argument: query += " " + self.argument()
		if not self.elements: return query + "\n"
		print(type(self.elements), type(self))
		if isinstance(self.elements, type(self)):
			query += " {\n" + ((indent + 1) * '\t') + self.elements.construct(indent + 1)
		else:
			query += " {\n"
			for element in self.elements:
				query += ((indent + 1) * '\t') + element.construct(indent + 1)
		query += '\n' + (indent * '\t') + '}\n'
		return query


class nodes(queryElement):
	def __init__(self, *elements):
		super().__init__('nodes', elements)


class var(queryElement):
	def __init__(self, var_name, var_value):
		self.var_name = var_name
		self.var_value = var_value

	def construct(self, *args):
		if isinstance(self.var_value, int): return self.var_name + ": " + str(self.var_value)
		return self.var_name + ': "' + self.var_value + '"'


class argument(queryElement):
	def __init__(self, var_name, var_value):
		self.var = var(var_name, var_value)

	def construct(self, *args):
		return '(' + self.var() + ' )'


class condition(queryElement):
	def __init__(self, var_name, var_value):
		self.var = var(var_name, var_value)

	def construct(self, *args):
		return '(condition: { ' + self.var() + '" })'


class input(queryElement):
	def __init__(self, *variables):
		super().__init__('input:', variables)

	def construct(self, indent=0):
		if not self.elements: return
		return '(' + super().construct(indent=0) + (indent * '\t') + ')'
