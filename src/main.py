from src.common import constants
from src.parser.parser_handler import SQLParser
from src.converter.converter_handler import PySparkGenerator, SelectNode

if __name__ == '__main__':
    print(constants.tool_logo)

    sql_query = '''SELECT Name, Age 
                   FROM emp 
                   WHERE Subject='Physics' AND (Age =28 OR Age=24)
                   '''

    sql_parser = SQLParser(sql_query)
    ast = sql_parser.parse_select()
    ast_node = SelectNode(**ast)

    generator = PySparkGenerator()
    code = generator.visit(ast_node)
    print(code)
