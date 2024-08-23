from typing import Literal


Operator = Literal["=", "!=", ">", "<", ">=", "<=", "in"]

class 

class Expression:
    condition: str
    operator: Operator
    value: str

    def __init__(self, condition: str, operator: Operator, value: str):
        self.condition = condition
        self.operator = operator
        self.value = value

    def __str__(self):
        return f"{self.condition} {self.operator} {self.value}"

    def to_query(self):
        return str(self)
