from . import graphqElements
from elements.utils import StringUtils

def queryAll(table, columns):
    camelCase = StringUtils.generate_camel_case(table)
    FirstCaps = StringUtils.pluralize("".join((camelCase[0].upper(), camelCase[1:])))
    atomicElements = generate_graphqElements(columns)
    nodes = graphqElements.nodes(*atomicElements)
    firstClassElement = firstClassElementFactory(f'all{FirstCaps}', nodes)
    query = graphqElements.query(f'all{FirstCaps}', firstClassElement)
    return query()

def queryTableByIdFunc(table, columns):
    camelCase = StringUtils.generate_camel_case(table)
    FirstCaps = "".join((camelCase[0].upper(), camelCase[1:]))

    def queryTableById(_id):
        arg = graphqElements.argument(f'{camelCase}Id', _id)
        atomicElements = generate_graphqElements(columns)
        firstClassElement = firstClassElementFactory(f'{camelCase}By{FirstCaps}Id', *atomicElements, argument=arg)
        query = graphqElements.query(f'get{FirstCaps}By{FirstCaps}Id', firstClassElement)
        return query()

    return queryTableById

def queryTableWithColumnFilterFunc(table, columns, column, filter_type='like'):
    camelCase = StringUtils.generate_camel_case(table)
    FirstCaps = StringUtils.pluralize("".join((camelCase[0].upper(), camelCase[1:])))

    def queryTableWithColumnFilter(identifier):
        if isinstance(column, dict):
            subfilters = []
            for i, c in enumerate(column.keys()):
                columnCamelCase = StringUtils.generate_camel_case(c)
                val = graphqElements.var(column[c], identifier[columnCamelCase])
                subfilters.append(graphqElements.var(columnCamelCase, val))
            fltr = graphqElements.filter(*subfilters)
        else:
            columnCamelCase = StringUtils.generate_camel_case(column)
            fltr = graphqElements.filter(graphqElements.var(f'{columnCamelCase}', graphqElements.var(filter_type, identifier)))
        atomicElements = generate_graphqElements(columns)
        nodes = graphqElements.nodes(*atomicElements)
        firstClassElement = firstClassElementFactory(f'all{FirstCaps}', nodes, filter=fltr)
        query = graphqElements.query(f'all{FirstCaps}', firstClassElement)
        return query()

    return queryTableWithColumnFilter


def queryTableById(table, columns, _id):
    camelCase = StringUtils.generate_camel_case(table)
    FirstCaps = "".join((camelCase[0].upper(), camelCase[1:]))
    arg = graphqElements.argument(f'{camelCase}Id', _id)
    atomicElements = generate_graphqElements(columns)
    firstClassElement = firstClassElementFactory(f'{camelCase}By{FirstCaps}Id', *atomicElements, argument=arg)
    query = graphqElements.query(f'get{FirstCaps}By{FirstCaps}Id', firstClassElement)
    return query()

def queryTableWithColumnFilter(table, columns, column, identifier, filter_type='like'):
    camelCase = StringUtils.generate_camel_case(table)
    FirstCaps = StringUtils.pluralize("".join((camelCase[0].upper(), camelCase[1:])))
    if isinstance(column, dict):
        subfilters = []
        for i, c in enumerate(column.keys()):
            columnCamelCase = StringUtils.generate_camel_case(c)
            val = graphqElements.var(column[c], identifier[columnCamelCase])
            subfilters.append(graphqElements.var(columnCamelCase, val))
        fltr = graphqElements.filter(*subfilters)
    else:
        columnCamelCase = StringUtils.generate_camel_case(column)
        fltr = graphqElements.filter(graphqElements.var(f'{columnCamelCase}', graphqElements.var(filter_type, identifier)))
    atomicElements = generate_graphqElements(columns)
    nodes = graphqElements.nodes(*atomicElements)
    firstClassElement = firstClassElementFactory(f'all{FirstCaps}', nodes, filter=fltr)
    query = graphqElements.query(f'all{FirstCaps}', firstClassElement)
    return query()

def atomicElementFactory(name):
    return graphqElements.queryElement(name)

def generate_graphqElements(columns):
    if isinstance(columns, str):
        return atomicElementFactory(StringUtils.generate_camel_case(columns))
    elif isinstance(columns, dict):
        return firstClassElementFactory(next(c for c in columns.keys()), generate_graphqElements(columns.get(next(c for c in columns.keys()))))
    elif isinstance(columns, list):
        return [generate_graphqElements(column) for column in columns]

def firstClassElementFactory(name, *elements, **kwargs):
    return graphqElements.queryElement(name, *elements, condition=kwargs.get('condition', None), argument=kwargs.get('argument', None), filter=kwargs.get('filter', None))
