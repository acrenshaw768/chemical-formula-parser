lexer grammar ExprLexer;

WS: [ \t\n\r\f]+ -> skip ;

INT : [0-9]+ ;
ID: [A-Z][a-z]? ;

LPAREN : '(' ;
RPAREN : ')' ;
LBRACK : '[';
RBRACK : ']';

DOT : '.';

SOLID: '(s)'; 
LIQUID: '(l)';
GAS: '(g)';
AQUEOUS: '(aq)';

PLUS : '+';
REACTION : '->';
