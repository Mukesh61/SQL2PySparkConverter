class ASTNode:
    pass

class SelectNode(ASTNode):
    def __init__(self, columns, table, joins=None, where=None, group_by=None, order_by=None, cte=None, window=None):
        self.columns = columns
        self.table = table
        self.joins = joins
        self.where = where
        self.group_by = group_by
        self.order_by = order_by
        self.cte = cte
        self.window = window


class PySparkGenerator:

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visitNode)
        return visitor(node)


    def generic_visitNode(self, node):
        return "under construction"

    def visit_SelectNode(self, node):
        code = "df = " + node.table + "_df"
        if node.joins:
            for join in node.joins:
                code += f"df = df.join({join['table']}, on='{join['on']}', how='{join['type']}')\n"
        if node.where:
            code += f".filter({node.where})"
        if node.group_by:
            group_column = {', '.join([f'col("{col}")' for col in node.group_by])}
            code += f"df = df.groupBy({group_column})\n"
        if node.window:
            code += "# Window functions logic here\n"

        select_column = ', '.join([f'col("{col}")' for col in node.columns])
        code += f".select({select_column})\n"
        code += "df.show()"
        return code
