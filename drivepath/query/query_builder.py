class QueryBuilder:
    def __init__(self):
        self.query = ""

    def add(self, condition):
        if self.query:
            self.query += " and "
        self.query += condition

    def build(self):
        return self.query
