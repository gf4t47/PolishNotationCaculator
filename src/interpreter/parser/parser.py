from src.interpreter.lexer.token import TokenType, Token
from src.interpreter.parser.node.binary import BinaryOp
from src.interpreter.parser.node.factory import FactorNode, Num
from src.interpreter.parser.node.node import AstNode
from src.interpreter.parser.token_stream import TokenStream


class PeekableException(SyntaxError):
    pass


def _construct_binary_node(op: Token, operands: [AstNode]):
    length = len(operands)

    if length == 0:
        raise ValueError("Can't construct binary node with zero operands")
    elif length == 1:
        return operands[0]
    else:
        return BinaryOp(op, operands[0], _construct_binary_node(op, operands[1::]))


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

    def _syntax_error_wrapper(self, action, *argv, **kwargs):
        record = self._token_streams.current()
        try:
            return True, action(*argv, **kwargs)
        except PeekableException as e:
            self._vomit(record)
            return False, e

    def _vomit(self, index: int):
        self._token_streams.reset(index)

    def _eat(self, token_type: TokenType) -> Token:
        if self.current_token.type == token_type:
            eaten = self.current_token
            self.current_token = self._token_streams.next_token()
            return eaten

        raise PeekableException(f"can't eat token type {self.current_token.type}, expecting {type}")

    def number(self) -> Num:
        """
        number:
            Token.TokenType == NUMBER
        :return: Num
        """
        if self.current_token.type != TokenType.NUMBER:
            raise PeekableException(f'Unexpected number token {self.current_token}')

        return Num(self._eat(TokenType.NUMBER))

    def factor(self) -> FactorNode:
        """
        factor:
            number
        :return: FactoryNode
        """
        if self.current_token.type == TokenType.NUMBER:
            return self.number()

        raise PeekableException(f'Unexpected factor token {self.current_token}')

    def factor_list(self) -> [FactorNode]:
        """
        factor_list:
            factor factor             #if self.binary_op is True
            | factor factor (factor)* #if self.binary_op is False
        :return: [FactorNode]
        """
        factors = [self.factor(), self.factor()]  # at least have two operands
        if not self.binary_op:
            is_factor, node = self._syntax_error_wrapper(self.factor)
            while is_factor:
                factors.append(node)
                is_factor, node = self._syntax_error_wrapper(self.factor)
        return factors

    def formula(self) -> BinaryOp:
        """
        formula:
            OP factor_list
        :return: BinaryOp
        """
        if self.current_token.type == TokenType.OPERATOR:
            op = self._eat(TokenType.OPERATOR)
            nodes = self.factor_list()
            return _construct_binary_node(op, nodes)

        raise PeekableException(f'Unexpected formula token {self.current_token}')

    def operand(self) -> (FactorNode, BinaryOp):
        """
        operand:
            factor
            | formula                #if self.binary_op is True
            | LPAREN factor RPAREN
            | LPAREN formula RPAREN
        :return: factor node or formula node
        """
        if self.current_token.type == TokenType.BRACKET and self.current_token.value is True:
            self._eat(TokenType.BRACKET)
            is_formula, formula_node = self._syntax_error_wrapper(self.formula)
            if is_formula:
                assert self.current_token.type == TokenType.BRACKET
                assert self.current_token.value is False
                self._eat(TokenType.BRACKET)
                return formula_node

            is_factor, factor_node = self._syntax_error_wrapper(self.factor)
            if is_factor:
                assert self.current_token.type == TokenType.BRACKET
                assert self.current_token.value is False
                self._eat(TokenType.BRACKET)
                return factor_node
        else:
            if self.binary_op:
                is_formula, formula_node = self._syntax_error_wrapper(self.formula)
                if is_formula:
                    return formula_node

            is_factor, factor_node = self._syntax_error_wrapper(self.factor)
            if is_factor:
                return factor_node

    def term(self) -> AstNode:
        """
        term:
            operand
            | OP operand term         #if self.binary_op is True
            | OP operand term (term)* #if self.binary_op is False
        :return AstNode:
        """
        if self.current_token.type == TokenType.OPERATOR:
            nodes = []
            op = self._eat(TokenType.OPERATOR)
            nodes.append(self.operand())
            nodes.append(self.term())
            if not self.binary_op:
                is_term, term_node = self._syntax_error_wrapper(self.term)
                while is_term:
                    nodes.append(term_node)
                    is_term, term_node = self._syntax_error_wrapper(self.term)
            return _construct_binary_node(op, nodes)

        return self.operand()

    def parse(self):
        node = self.term()

        if self.current_token.type != TokenType.EOF:
            raise TypeError(f'the token stream is not finished after parsing, token left = {self.current_token}')

        return node
