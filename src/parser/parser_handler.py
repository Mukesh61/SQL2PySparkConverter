from src.common.sql_tokenizer import tokenize

class SQLParser:
    def __init__(self, sql_query):
        self.tokens = tokenize(sql_query)
        self.current_token_index = 0

    def check(self, token_type, value=None):
        if self.current_token_index >= len(self.tokens):
            return False
        token = self.tokens[self.current_token_index]
        if value:
            return token[0] == token_type and token[1].upper() == value.upper()
        return token[0] == token_type

    def match_and_advance_cursor(self, token_type, value):
        if not self.check(token_type, value):
            raise SyntaxError(f"Expected {value} but got {self.tokens[self.current_token_index]}")
        self.current_token_index += 1

    def parse_select(self):
        self.match_and_advance_cursor('KEYWORD', 'SELECT')
        columns = self.parse_columns()
        self.match_and_advance_cursor('KEYWORD', 'FROM')
        table = self.consume('IDENTIFIER')[1]
        where_clause = None
        if self.check('KEYWORD', 'WHERE'):
            where_clause = self.parse_where()
        return {'columns': columns, 'table': table, 'where': where_clause}

    def parse_columns(self):
        columns = []

        columns.append(self.consume('IDENTIFIER')[1])
        while self.check('COMMA'):
            self.current_token_index += 1
            columns.append(self.consume('IDENTIFIER')[1])
        return columns

    def parse_where_condition(self):
        where_cond:str = "(col('"
        left = self.consume('IDENTIFIER')[1]
        where_cond += left + "')"
        operator = self.consume('OPERATOR')[1]
        if operator == "=":
            where_cond += "=="
        else:
            where_cond += operator + " "
        right = self.consume_any(['NUMBER', 'STRING', 'IDENTIFIER'])[1]
        where_cond += right + ")"

        return where_cond

    def parse_where(self):
        self.match_and_advance_cursor('KEYWORD', 'WHERE')
        where_cond = ""
        where_cond += self.parse_where_condition()
        while (self.check('KEYWORD', 'AND') or
               self.check('KEYWORD', 'OR') or self.check('RPAREN')):
            token_value_pyspark = ''
            # print(f"processing: {self.tokens[self.current_token_index][0]}")
            token_value = self.tokens[self.current_token_index][1]
            if token_value.upper() == "AND":
                token_value_pyspark = '&'
            elif token_value.upper() == "OR":
                token_value_pyspark = '|'

            where_cond += token_value_pyspark + " "

            if self.check('RPAREN'):
                where_cond += self.consume('RPAREN')[1]
                continue

            self.current_token_index += 1

            if self.check('LPAREN'):
                where_cond += self.consume('LPAREN')[1]

            where_cond += self.parse_where_condition()

        return where_cond

    def consume(self, token_type):
        token = self.tokens[self.current_token_index]
        if token[0] == token_type:
            self.current_token_index += 1
            return token
        raise SyntaxError(f"Expected {token_type} but got {token}")

    def consume_any(self, token_types):
        token = self.tokens[self.current_token_index]
        if token[0] in token_types:
            self.current_token_index += 1
            return token
        raise SyntaxError(f"Expected one of {token_types} but got {token}")
