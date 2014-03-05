import json
import re

class InvalidExpressionError(Exception):
    """ Expression Syntax Error """

class Expression(object):
    """ Query Expression

        Support operands: =, <=, <, >, >=, in, like (SQL-like string pattern), rlike (Regular-expression pattern), indexed with (only for Riak)
    """

    IS_PARAMETER     = 'param'
    IS_PROPERTY_PATH = 'path'
    IS_DATA          = 'data'

    def __init__(self):
        self._sub_expressions  = []
        self._re_statement     = re.compile('^\s*(?P<left>.+)\s+(?P<operand>=|<=|<|>=|>|in|like|rlike|indexed with)\s+(?P<right>.+)\s*$')
        self._re_parameter     = re.compile('^:[a-zA-Z0-9_]+$')
        self._re_property_path = re.compile('^[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]*)+$')

    @property
    def sub_expressions(self):
        return self._sub_expressions

    def expect(self, statement):
        # parse the statement
        pass

    def _compile(self, statement):
        fixed_syntax_operands = ('in', 'like', 'rlike', 'indexed with')

        expr = self._parse(statement)

        try:
            expr['left']  = self._parse_side(expr['left'])
        except InvalidExpressionError as exception:
            raise InvalidExpressionError('The left side of the expression cannot be parsed.')

        try:
            expr['right']  = self._parse_side(expr['right'])
        except InvalidExpressionError as exception:
            raise InvalidExpressionError('The left side of the expression cannot be parsed.')

        # Validate the syntax
        if expr['left']['type'] != Expression.IS_PROPERTY_PATH and expr['operand'] in fixed_syntax_operands:
            raise InvalidExpressionError('The property path must be on the left of the operand.')

        if expr['right']['type'] == Expression.IS_PROPERTY_PATH and expr['operand'] in fixed_syntax_operands:
            raise InvalidExpressionError('The property path cannot be on the right of the operand.')

        return expr

    def _parse_side(self, sub_statement):
        kind = Expression.IS_DATA

        if self._re_parameter.match(sub_statement):
            kind = Expression.IS_PARAMETER

        elif self._re_property_path.match(sub_statement):
            kind = Expression.IS_PROPERTY_PATH

        if kind != Expression.IS_DATA:
            return {
                'original': sub_statement,
                'type':     kind,
                'value':    None
            }

        decoded_data = None

        try:
            decoded_data = json.loads(sub_statement)
        except ValueError as exception:
            raise InvalidExpressionError('Unable to decode the data.')

        return {
            'original': sub_statement,
            'type':     kind,
            'value':    decoded_data
        }

    def _parse(self, statement):
        matches = self._re_statement.match(statement)

        if not matches:
            raise InvalidExpressionError('Incomplete statement: {}'.format(statement))

        expr = matches.groupdict()

        return expr