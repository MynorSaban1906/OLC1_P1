# aqui estan todos los tipos de datos que se pueden usar dentro del compilador

from enum import Enum

class Type(Enum):
    ENTERO = 1
    DECIMAL = 2
    BOOLEANO = 3
    CHARACTER = 4
    CADENA = 5
    NULO = 6
    ARREGLO = 7
    ID=8

class ArithmeticOperator(Enum):
    MAS = 1
    MENOS = 2
    POR = 3
    DIV = 4
    POT = 5
    MOD = 6
    UMENOS = 7
    AUMENTO= 8
    DECREMENTO=9

class RelationalOperator(Enum):
    MENORQUE = 1
    MAYORQUE = 2
    IGUALIGUAL = 3
    DIFERENTE = 4
    MENORIGUAL = 5
    MAYORIGUAL = 6

class LogicOperator(Enum):
    NOT = 1
    AND = 2
    OR = 3

class OperationsMath(Enum):
    LOG10=1
    LOG=2
    SEN=3
    COS=4
    TAN=5
    SQRT=6