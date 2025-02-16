import re

token_specification = [
    ('KEYWORD', r'\b(SELECT|FROM|WHERE|AND|OR|GROUP BY|ORDER BY|JOIN|ON|AS|IN|NOT IN|INNER|LEFT|RIGHT|OUTER|UNION|ALL|DISTINCT|CASE|WHEN|THEN|ELSE|END|LIKE|IS|NULL)\b'),
    ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('OPERATOR', r'[=<>!]+|[\+\-\*/]'),
    ('NUMBER', r'\b\d+(\.\d*)?\b'),
    ('STRING', r"'[^']*'"),
    ('COMMA', r','),
    ('DOT', r'\.'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('WHITESPACE', r'\s+'),
    ('OTHER', r'.'),
]

def tokenize(sql):
    token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    tokens = []
    for match in re.finditer(token_regex, sql, re.IGNORECASE):
        kind = match.lastgroup
        value = match.group()
        if kind != 'WHITESPACE':
            tokens.append((kind, value))
    return tokens

if __name__ == "__main__":
    sql_query = "SELECT Name, Age FROM emp where Subject='Physics' and Age =28"
    tokens = tokenize(sql_query)
    print(tokens)
