from src.interpreter.lexer.token import TokenType, Token
from src.interpreter.parser.node.binary import BinaryOp
from src.interpreter.parser.node.factory import FactorNode, Num
from src.interpreter.parser.node.node import AstNode
from src.interpreter.parser.token_stream import TokenStream


def syntax_error_wrapper(action, *argv):
    try:
        return True, action(argv)
    except SyntaxError as e:
        return False, e


class Parser:
    def __init__(self, tokens: TokenStream):
        self._token_streams = tokens
        self.current_token = self._token_streams.next_token()

    @property
    def current_token(self) -> Token:
        return self._current_token

    @current_token.setter
    def current_token(self, value: Token):
        self._current_token = value

    def eat(self, token_type: TokenType) -> bool:
        if self.current_token.type == token_type:
            self.current_token = self._token_streams.next_token()
            return True

        raise SyntaxError(f'unexpected token type {self.current_token.type}, expecting {type}')

    def number(self) -> Num:
        """
        number:
            Token.TokenType == NUMBER
        :return: Num
        """
        node = Num(self.current_token)
        self.eat(TokenType.NUMBER)
        return node

    def factor(self) -> FactorNode:
        """
        factor:
            number
            | LPAREN number RPAREN
        :return: FactoryNode
        """
        if self.current_token.type == TokenType.NUMBER:
            return self.number()
        elif self.current_token.type == TokenType.BRACKET and self.current_token.value is True:
            self.eat(TokenType.BRACKET)
            node = self.number()
            assert self.current_token.type == TokenType.BRACKET and self.current_token.value is False
            self.eat(TokenType.BRACKET)
            return node

        raise SyntaxError(f'Unexpected factor token {self.current_token}')

    def factor_list(self) -> [FactorNode]:
        """
        factor_list:
            factor factor (factor)*
        :return: [FactorNode]
        """
        factors = [self.factor(), self.factor()]
        return factors

    def formula(self) -> BinaryOp:
        """
        formula:
            OP factor_list
            | LPAREN OP factor_list RPAREN
        :return: BinaryOp
        """
        pass

    def term(self) -> AstNode:
        """
        term: factor
            | formula
            | OP factor (term)+
            | OP formula (term)+
        :return AstNode:
        """
        pass

    def parse(self):
        node = self.term()

        if self.current_token.type != TokenType.EOF:
            raise TypeError(f'the token stream is not finished after parsing, last token = {self.current_token}')

        return node
