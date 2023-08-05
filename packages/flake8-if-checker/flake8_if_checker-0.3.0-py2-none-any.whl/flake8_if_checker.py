import ast
import collections
import enum
from optparse import OptionConflictError

try:
    # pylint:disable=unused-import
    from argparse import Namespace
    from flake8.options.manager import OptionManager
    from typing import Dict, Iterator, List, Optional, Tuple, Union

    # pylint:enable=unused-import

    IfCheckerReportItem = Tuple[int, int, str, type]  # pylint:disable=invalid-name
except ImportError:  # pragma: no cover
    pass


DEFAULT_MAX_IF_CONDITIONS = 2

Result = collections.namedtuple("Result", "type kind line col condition_count")


class IfCheckerErrors(enum.Enum):
    IF01 = "IF01 Too many conditions ({condition_count}) in {type} {kind}"


class IfKind(enum.Enum):
    IfExp = "Expression"
    If = "Statement"


class IfType(enum.Enum):
    IF = "IF"
    ELIF = "ELIF"


class AstVisitor(object):
    def __init__(self):
        # type: () -> None
        self._result_store = {}  # type: Dict[Tuple[str, int, int], Result]

    @property
    def results(self):
        # type: () -> Tuple[Result]
        return tuple(  # type:ignore
            sorted(
                self._result_store.values(),
                key=lambda result: (result.line, result.col, result.kind),
            )
        )

    def lookup(self, tree):
        # type: (ast.Module) -> None
        assert hasattr(tree, "body"), "tree must have `body` property"
        self._visit_node(tree)

    def _get_type(self, node):
        # type: (ast.AST) -> str
        return type(node).__name__

    def _visit_node(self, node):
        # type: (ast.AST) -> None
        self.__visit_subtree(node, "body")
        self.__visit_subtree(node, "orelse")
        self.__visit_subtree(node, "test")
        self.__visit_subtree(node, "value")
        self.__visit_subtree(node, "values")

        # Visiting: If statements & expression
        if isinstance(node, (ast.If, ast.IfExp)):
            self.__visit_if(node)

    def __count_if(self, node):
        # type: (ast.stmt) -> int
        counter = 0
        values = getattr(node, "values", [])

        if isinstance(values, collections.Iterable):
            for node_value in values:
                node_type = self._get_type(node_value)
                if node_type == "BoolOp":
                    counter += self.__count_if(node_value)
                else:
                    counter += 1

        return counter

    def __visit_if(self, node):
        # type: (Union[ast.If, ast.IfExp]) -> None
        node_type = self._get_type(node)
        node_line = node.lineno
        node_col = node.col_offset
        node_kind = IfKind[node_type].value
        result_key = (node_kind, node_line, node_col)

        node_test = getattr(node, "test")
        test_values = getattr(node_test, "values", [])
        if not test_values:
            counter = 1
        else:
            counter = self.__count_if(node_test)

        self._result_store[result_key] = Result(
            type=None,
            kind=node_kind,
            line=node_line,
            col=node_col,
            condition_count=counter,
        )

    def __visit_subtree(self, node, subtree_name):
        # type: (ast.AST, str) -> None
        subtree = getattr(node, subtree_name, [])
        if isinstance(subtree, collections.Iterable):
            for subtree_item in subtree:
                self._visit_node(subtree_item)
        elif isinstance(subtree, ast.AST):
            self._visit_node(subtree)


class IfChecker(object):
    name = "flake8_if_checker"
    version = "0.3.0"

    IF_LEN = len("if ")
    ELIF_LEN = len("elif ")

    def __init__(self, tree, lines, options):
        # type: (ast.Module, List[str], Namespace) -> None
        self.tree = tree
        self.lines = lines
        self.options = options

    @classmethod
    def add_options(cls, parser):  # pragma: no cover
        # type: (OptionManager) -> None
        flag = "--max-if-conditions"
        kwargs = {
            "default": DEFAULT_MAX_IF_CONDITIONS,
            "metavar": "n",
            "parse_from_config": "True",
            "type": "int",
        }

        config_opts = getattr(parser, "config_options", None)
        if isinstance(config_opts, list):
            # Flake8 2.x
            kwargs.pop("parse_from_config")
            if flag[2:] not in parser.config_options:
                parser.config_options.append(flag[2:])

        try:
            parser.add_option(flag, **kwargs)
        except OptionConflictError:
            pass

    def run(self):
        # type: () -> Iterator[IfCheckerReportItem]
        tree = ast.fix_missing_locations(self.tree)

        visitor = AstVisitor()
        visitor.lookup(tree)

        for result in visitor.results:
            fixed_result = self._fix_result_item(result)
            if self._has_if01_error(fixed_result):
                yield self._format_report(
                    IfCheckerErrors.IF01, fixed_result  # type:ignore
                )

    def _fix_result_item(self, result):
        # type: (Result) -> Optional[Result]
        # Add default IF type
        kwargs = result._asdict()

        try:
            _type, _col = self._find_type_and_column(  # type:ignore
                self.lines[kwargs["line"] - 1], kwargs["col"]
            )
        except TypeError:  # pragma: no cover
            return None

        kwargs["type"] = _type.value
        kwargs["col"] = _col
        return Result(**kwargs)

    def _find_type_and_column(self, code_line, column):  # noqa:C901
        # type: (str, int) -> Optional[Tuple[IfType, int]]

        def _find_result(value):
            # type: (str) -> Optional[Tuple[IfType, int]]
            if value.strip().startswith("elif"):
                return IfType.ELIF, value.index("elif")
            if value.strip().startswith("if"):
                return IfType.IF, value.index("if")
            if "if " in value and " else " in value:
                return IfType.IF, value.index("if")
            return None  # pragma: no cover

        if column == 0:
            _maybe_result = _find_result(code_line)
            if _maybe_result:
                return _maybe_result

        for substr_from in (column - self.ELIF_LEN, column - self.IF_LEN):
            if substr_from < 0:
                continue

            _maybe_result = _find_result(code_line[substr_from:])
            if _maybe_result:
                _type, _col = _maybe_result
                return _type, _col + substr_from

        return None  # pragma: no cover

    def _has_if01_error(self, result):
        # type: (Optional[Result]) -> bool
        return (
            result
            and result.condition_count > self.options.max_if_conditions  # type:ignore
        )

    def _format_report(self, error, result):
        # type: (IfCheckerErrors, Result) -> IfCheckerReportItem
        return (
            result.line,
            result.col,
            error.value.format(**result._asdict()),
            type(self),
        )
