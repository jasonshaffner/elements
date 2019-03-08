class query:
    def __init__(self, elementName, *elements, **kwargs):
        self.elementName = elementName
        self.operation = kwargs.get('operation', 'query')
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
        self.filter = kwargs.get('filter', None)

    def __call__(self, indent=0):
        return self.construct(indent)

    def construct(self, indent=0):
        query = self.elementName
        if self.condition:
            query += " " + self.condition()
        if self.input:
            query += " " + self.input()
        if self.argument:
            query += " " + self.argument()
        if self.filter:
            query += " " + self.filter()
        if not self.elements:
            return query + "\n"
        if isinstance(self.elements, type(self)):
            query += " {\n" + ((indent + 1) * '\t') + self.elements.construct(indent + 1)
        else:
            query += " {\n"
            for element in self.elements:
                if element:
                    query += ((indent + 1) * '\t') + element.construct(indent + 1) + '\n'
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
        if isinstance(self.var_value, int):
            return self.var_name + ": " + str(self.var_value)
        elif isinstance(self.var_value, str):
            return self.var_name + ': "' + self.var_value + '"'
        elif isinstance(self.var_value, type(self)):
            return self.var_name + ': {'  + self.var_value.construct() + '}\n'
        elif isinstance(self.var_value, list):
            return self.var_name + ': {' + ", ".join(val.construct() for val in self.var_value) + '}\n'


class argument(queryElement):
    def __init__(self, *args):
       self.vars = args

    def construct(self, *args):
        if isinstance(self.vars, var):
            return '(' + self.var() + ' )'
        elif isinstance(self.vars[0], var):
            return "".join(('(', ", ".join([var() for var in self.vars]), ')'))
        elif len(self.vars) == 2 and isinstance(self.vars[0], str) and isinstance(self.vars[1], (str,int)):
            return '(' + var(self.vars[0], self.vars[1])() + ')'


class condition(queryElement):
    def __init__(self, var_name, var_value):
        self.var = var(var_name, var_value)

    def construct(self, *args):
        return '(condition: { ' + self.var() + ' })'

class filter(queryElement):
    def __init__(self, *args):
        self.vars = args

    def construct(self, *args):
        if isinstance(self.vars, var):
            return "".join(('(filter: { ', self.vars(), ' })'))
        elif isinstance(self.vars[0], var):
            return "".join(('(filter: { ', ", ".join([arg() for arg in self.vars]), ' })'))
        elif len(args) == 2 and isinstance(self.vars[0], str) and isinstance(self.vars[1], (str,int)):
            return "".join(('(filter: { ', var(self.vars[0], self.vars[1])(), ' })'))

class input(queryElement):
    def __init__(self, *variables):
        super().__init__('input:', variables)

    def construct(self, indent=0):
        if not self.elements:
            return
        return '(' + super().construct(indent=indent + 1) + ((indent + 1) * '\t') + ')'
