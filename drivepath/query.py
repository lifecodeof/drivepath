from abc import ABC
from typing import TYPE_CHECKING, Literal, Self, overload

if TYPE_CHECKING:
    from drivepath.drive import Drive

ComparisonOperator = Literal["=", "!=", ">", "<", ">=", "<=", "in"]


class Expression(ABC):
    def __str__(self) -> str:
        return self.to_query()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_query()})"

    def to_query(self) -> str:
        raise NotImplementedError

    def _escape(self, value: str) -> str:
        return value.replace("\\", "\\\\").replace("'", "\\'")

    def _quote(self, value: str) -> str:
        return f"'{self._escape(value)}'"

    def __and__(self, other: "Expression"):
        return LogicalExpression(self, "and", other)

    def __or__(self, other: "Expression"):
        return LogicalExpression(self, "or", other)

    def __invert__(self):
        return NotExpression(self)

    def execute(self, drive: "Drive"):
        return drive.query(self)


class ComparisonExpression(Expression):
    term: str
    operator: ComparisonOperator
    value: str

    def __init__(self, term: str, operator: ComparisonOperator, value: str):
        self.term = term
        self.operator = operator
        self.value = value

    def to_query(self) -> str:
        term = self.term
        value = self.value

        if self.operator == "in":
            term = self._quote(term)
        else:
            value = self._quote(value)

        return f"{term} {self.operator} {value}"


LogicalOperator = Literal["and", "or"]


class LogicalExpression(Expression):
    left: Expression
    operator: LogicalOperator
    right: Expression

    def __init__(self, left: Expression, operator: LogicalOperator, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def to_query(self) -> str:
        return f"({self.left}) {self.operator} ({self.right})"


class NotExpression(Expression):
    expression: Expression

    def __init__(self, expression: Expression):
        self.expression = expression

    def to_query(self) -> str:
        return f"not {self.expression}"


class HasExpression(Expression):
    term: str
    properties: dict[str, str]

    def __init__(self, term: str, properties: dict[str, str]):
        self.term = term
        self.properties = properties

    def to_query(self) -> str:
        properties = " and ".join([f"{k}='{self._escape(v)}'" for k, v in self.properties.items()])
        return f"{self.term} has {{ {properties} }}"


@overload
def q(left: str, operator: ComparisonOperator, right: str) -> ComparisonExpression: ...


@overload
def q(left: Expression, operator: LogicalOperator, right: Expression) -> LogicalExpression: ...


def q(left, operator, right) -> Expression:
    """Create a query expression."""

    if isinstance(left, str) and isinstance(right, str):
        return ComparisonExpression(left, operator, right)
    elif isinstance(left, Expression) and isinstance(right, Expression):
        return LogicalExpression(left, operator, right)
    else:
        raise ValueError(f"Invalid expression types {left=} and {right=}")


def not_(expression: Expression) -> NotExpression:
    """Negate an expression."""

    return NotExpression(expression)
