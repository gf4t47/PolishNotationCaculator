import logging
import sys
from typing import Tuple, Callable, Union

from src.interpreter.lexer.token import TokenType, Token
from src.interpreter.parser.node.binary import CalcOp, AssignOp
from src.interpreter.parser.node.factory import FactorNode, Num, Variable
from src.interpreter.parser.node.node import AstNode
from src.interpreter.parser.node.sequence import Sequence
from src.interpreter.parser.token_stream import TokenStream

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.disable(logging.DEBUG)


class PeekableException(SyntaxError):
    pass


def _construct_calc_node(op: Token, operands: [AstNode]):
    length = len(operands)

    if length == 0:
        raise ValueError("Can't construct binary node with zero operands")
    elif length == 1:
        return operands[0]
    else:
        return CalcOp(op, operands[0], _construct_calc_node(op, operands[1::]))


def _assignment_joiner(assignments: [AssignOp], action: Callable, *argv, **kwargs):
    """
    adding current assignment into variable environment
    :param assignments: a list of assignments
    :param action: real parser action
    :param argv: pre assigment nodes
    """
    actor = action(*argv, **kwargs)
    return Sequence(assignments, actor) if assignments is not None and len(assignments) > 0 else actor


class Parser:
    def __init__(self, tokens: TokenStream, binary_op: bool):
        self._token_streams = tokens
        self.current_token = self._token_streams.next_token()
        self._binary_op = binary_op

    @property
    def current_token(self) -> Token:
        return self._current_token

    @current_token.setter
    def current_token(self, value: Token):
        self._current_token = value

    @property
    def binary_op(self):
        return self._binary_op

    def _bracket_stripper(self, action: Callable, *argv, **kwargs):
        """
        strip the brackets, parse the internal content
        :param action: real parser action
        """
        assert self.current_token.type == TokenType.BRACKET
        assert self.current_token.value is True
        self._eat(TokenType.BRACKET)
        result = action(*argv, **kwargs)
        assert self.current_token.type == TokenType.BRACKET
        assert self.current_token.value is False
        self._eat(TokenType.BRACKET)
        return result

    def _peekable_error_wrapper(self, action: Callable, *argv, **kwargs)->Tuple[bool, Union[AstNode, PeekableException]]:
        """
        play as a try and roll back action wrapper
        :param action: real parser action
        :return: indicating action succeed or not, parsed result
        """
        token = self.current_token
        index = self._token_streams.current()
        try:
            return True, action(*argv, **kwargs)
        except PeekableException as e:
            self._vomit(token, index)
            return False, e

    def _vomit(self, token: Token, index: int):
        self.current_token = token
        self._token_streams.reset(index)

    def _eat(self, token_type: TokenType) -> Token:
        if self.current_token.type == token_type:
            eaten = self.current_token
            self.current_token = self._token_streams.next_token()
            return eaten

        raise TypeError(f"can't eat token type {self.current_token.type}, expecting {type}")

    def variable(self)-> Variable:
        """
        variable:
            Token.TokenType == VARIABLE
        :return:
        """
        logging.debug('entry %s with %s', self.variable.__name__, self.current_token)
        if self.current_token.type != TokenType.VARIABLE:
            raise PeekableException(f'Unexpected number token {self.current_token}')

        return Variable(self._eat(TokenType.VARIABLE))

    def number(self) -> Num:
        """
        number:
            Token.TokenType == NUMBER
        :return: Num
        """
        logging.debug('entry %s with %s', self.number.__name__, self.current_token)
        if self.current_token.type != TokenType.NUMBER:
            raise PeekableException(f'Unexpected number token {self.current_token}')

        return Num(self._eat(TokenType.NUMBER))

    def factor(self) -> FactorNode:
        """
        factor:
            number
            | variable
        :return: FactoryNode
        """
        logging.debug('entry %s with %s', self.factor.__name__, self.current_token)
        if self.current_token.type == TokenType.NUMBER:
            return self.number()

        if self.current_token.type == TokenType.VARIABLE:
            return self.variable()

        raise PeekableException(f'Unexpected factor token {self.current_token}')

    def formula(self) -> CalcOp:
        """
        formula:
            OP operand operand                 # if self.binary_op is True
            | OP operand operand (operand)*    # if self.binary_op is False
        :return: BinaryOp
        """
        logging.debug('entry %s with %s', self.formula.__name__, self.current_token)
        op = self._eat(TokenType.CALCULATOR)
        nodes = [self.operand(), self.operand()]
        if self.binary_op is False:
            is_operand, operand = self._peekable_error_wrapper(self.operand)
            while is_operand:
                nodes.append(operand)
                is_operand, operand = self._peekable_error_wrapper(self.operand)
        return _construct_calc_node(op, nodes)

    def assignment(self)->AssignOp:
        """
        assigment:
            = variable factor
        :return:
        """
        logging.debug('entry %s with %s', self.assignment.__name__, self.current_token)
        if self.current_token.type == TokenType.ASSIGN:
            equal = self._eat(TokenType.ASSIGN)
            var = self.variable()
            factor = self.factor()
            return AssignOp(equal, var, factor)

        raise PeekableException(f'Unexpected assigment token {self.current_token}')

    def operand(self) -> [(FactorNode, AssignOp, CalcOp)]:
        """
        operand:
            LPAREN operand RPAREN
            | (assignment)* operand
            | formula
            | factor
        :return: factor node or formula node
        """
        logging.debug('entry %s with %s', self.operand.__name__, self.current_token)
        if self.current_token.type == TokenType.BRACKET and self.current_token.value is True:
            return self._bracket_stripper(self.operand)
        elif self.current_token.type == TokenType.ASSIGN:
            assigns = []
            while self.current_token.type == TokenType.ASSIGN:
                assigns.append(self.assignment())
            return _assignment_joiner(assigns, self.operand)

        return self.formula() if self.current_token.type == TokenType.CALCULATOR else self.factor()

    def parse(self)->AstNode:
        logging.debug('entry %s with %s', self.parse.__name__, self.current_token)
        node = self.operand()

        if self.current_token.type != TokenType.EOF:
            raise TypeError(f'the token stream is not finished after parsing, token left = {self.current_token}')

        return node
