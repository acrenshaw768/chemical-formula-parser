parser grammar ExprParser;
options { tokenVocab=ExprLexer; }

program : reaction * EOF;

elem : ID;
isotope : LPAREN INT elem RPAREN | LBRACK INT elem RBRACK;
mult : INT;
homonuclear : (elem | isotope) mult?;

wrappable_molecule : homonuclear+ 
    | homonuclear* (
        (LPAREN wrappable_molecule RPAREN mult ?) 
        | (LBRACK wrappable_molecule RBRACK mult ?)
    ) homonuclear*;
    
stoichiometric_coefficient: DOT mult?;
molecule : wrappable_molecule +
    | molecule stoichiometric_coefficient molecule;
    
state: SOLID | LIQUID | GAS | AQUEOUS;
stateful_molecule : molecule state;

summable_molecule : mult? (molecule | stateful_molecule);
molecule_sum : summable_molecule (PLUS summable_molecule)*;
reaction : lhs=molecule_sum REACTION rhs=molecule_sum;
