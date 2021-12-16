#  gramatica implementada para analizador de lenguaje julia
from Natives.Local import Local
from Natives.Pop import Pop
from Natives.Push import Push
from Natives.Sqrt import Sqrt
from Instruction.ModfyArray import ModifyArray
from Instruction.AccessArray import AccessArray
from Instruction.StatementArray import StatementArray
from Instruction.For import For
from Natives.MathematicalOperations import MathematicalOperations
from Instruction.Continue import Continue
from Instruction.Break import Break
from Instruction.While import While
from Natives.Parse import Parse
from Natives.Length import Length
from Natives.String import String
from Natives.Float import Float
from Instruction.LlamadaFuncion import LlamadaFuncion
from Natives.Trunc import Trunc
from Natives.Typeof import Typeof
from Natives.Lowercase import Lowercase
from Natives.Uppercase import Uppercase
from Instruction.If import If
from Expressions.Relational import Relational
from Instruction.Print import Print
from SymbolsTable.Type import ArithmeticOperator,LogicOperator, RelationalOperator
from Expressions.Aritmetic import Aritmetic 
from Instruction.Statement import Statement
from Expressions.Logic import Logic 
from Instruction.Return import Return
from Instruction.If import If
from Instruction.Function import Function
from SymbolsTable.Type import OperationsMath
from Instruction.Global import Global

from Natives.Cos import Cos
from Natives.Sin import Sin
from Natives.Tan import Tan

from Abstract.NodoAST import NodoAST



from SymbolsTable.Type import Type

from   SymbolsTable.Tree import Tree
from   SymbolsTable.Table import Table
from   SymbolsTable.Exceptions import Exceptions
from Expressions.Primitive import Primitive
from Expressions.Id import Id

import sys

sys.getrecursionlimit()
sys.setrecursionlimit(4000)


import os
import re

errores = [] # array de errores que se registro en el codigo

reservadas = {
    'pop'       : 'RPOP',
    'push'      : 'RPUSH',
    'print'     : 'PRINT',
    'println'   : 'PRINTLN',
    'true'      : 'RTRUE',
    'false'     : 'RFALSE',
    'null'      : 'NULO',
    'Int64'     : 'RINT',
    'Float64'   : 'RDOUBLE',
    'Bool'      : 'RBOLEANO',
    'Char'      : 'RCHAR',
    'String'    : 'RSTRING',
    'end'       : 'END',
    'if'        : 'RIF',
    'else'      : 'RELSE',
    'elseif'    : 'RELSEIF',
    'function'  : 'RFUNCION',
    'return'    : 'RRETURN',
    'parse'     : 'RPARSE',
    'trunc'     : 'RTRUNC',
    'while'     : 'RWHILE',
    'continue'  : 'RCONTINUE',
    'break'     : 'RBREAK',
    'log10'     : 'RLOG10',
    'log'       : 'RLOG',
    'for'       : 'RFOR',
    'in'        : 'RIN',
    'struct'    : 'RSTRUCT',
    'mutable'   : 'RMUTABLE',
    'global'    : 'RGLOBAL',
    'local'     : 'RLOCAL',
    
}
    # simbolos que se usan en el analizador de julia
tokens  = [
    'PTCOMA',
    'PARIZQ',
    'PARDER',
    'MAS',
    'IGUAL',
    'MENOS',
    'POR',
    'POW',
    'DIVIDIDO',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CHAR',
    'ID',
    'MENQUE',
    'MAYQUE',
    'MODULO',
    'MENIGUAL',
    'MAYIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'NOT',
    'AND',
    'OR',
    'DPUNTOS',
    'COMA',
    'PUNTOS',
    'CORDER',
    'CORIZQ',
    


] + list(reservadas.values())



# Tokens declarados
t_PTCOMA    = r';'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_IGUAL     = r'='
t_POW       =r'\^'
t_MODULO    =r'\%'

t_MENQUE    =r'<'
t_MAYQUE    =r'>'
t_IGUALIGUAL =r'=='
t_MENIGUAL  =r'<='
t_MAYIGUAL  =r'>='
t_DIFERENTE =r'!='
t_OR        =r'\|\|'
t_AND       =r'&&'
t_NOT       =r'!'
t_DPUNTOS   =r'::'
t_COMA      =r','
t_PUNTOS    =r':'
t_CORDER='\]'
t_CORIZQ='\['



 
def t_DECIMAL(t):
    r'\d+\.\d+'  # expresion regualar
    try:
        t.value = float(t.value)

    except ValueError:
        print("float demasiado grande %d", t.value)
        t.value = 0
    return t


def t_CHAR(t):
    r'(\'([a-zA-Z]|\\\'|\\"|\\t|\\n|\\\\|.)\')' # expresion regualar

    t.value = t.value[1:-1] # remuevo las comillas simples
    return t


def t_ENTERO(t): 
    r'\d+'  # expresion regualar

    try:
        t.value = int(t.value)
    except ValueError:
        print("entero demasiado grande %d", t.value)
        t.value = 0
    return t


def t_CADENA(t):
    r'\"(\"|.)*?\"' # expresion regualar
    t.value = t.value[1:-1] # remuevo las comillas dobles
    return t

# Comentario de multiples lineas #=  ............................ =#

def t_COMENTARIO_MULTILINEA(t):
    r'\#\=(.|\n)*?\=\#'
    t.lexer.lineno += t.value.count('\n')


# Comentario simple # ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"
def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t
 
def t_error(t):
    errores.append(Exceptions("Lexico","El caracter \"" + t.value[0]+"\" no pertenece al lenguaje" , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()



#Precedencia   solo estan las basicas
precedence = (

    ('left','OR'),
    ('left','AND'),
    ('right','UNOT'),
    ('left','IGUALIGUAL','DIFERENTE'),
    ('left', 'MENQUE', 'MAYQUE','MENIGUAL', 'MAYIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO','MODULO'),
    ('left','POW'),
    ('right','UMENOS'),
    

)
#Abstract

def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t) :
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    
# INSTRUCCIONES

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

# INSTRUCCION

def p_instruccion(t) :
    '''instruccion      :   imprimir_instr final  
                        |   declaracion final
                        |   if_instr END final
                        |   fun_inst END final
                        |   llamadaFuncion final
                        |   return_instr final
                        |   while_instr END final
                        |   break_instr final
                        |   continue_instr final
                        |   for_instr END final
                        |   definicionArreglo_instr final
                        |   modifyArray_instr  final
                        |   PUSHARR final
                        |   POPARR  final
                        |   VARGLOBAL final
                        |   VARLOCAL final

    '''
    t[0] = t[1]


def p_finins(t) :
    '''final      : PTCOMA
                    | '''
    t[0] = None



def p_instruccion_error(t):
    '''instruccion      : error final'''
    errores.append(Exceptions("Sintactico","Error Sintactico con " + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""

# EXPRESIONES OPERATORIAS


def p_expresiones_operatorias(t):
    '''expresion :      expresion MAS expresion
                    |   expresion MENOS expresion  
                    |   expresion POR expresion  
                    |   expresion DIVIDIDO expresion 
                    |   expresion POW expresion  
                    |   expresion MODULO expresion  
                    |   expresion OR expresion  
                    |   expresion AND expresion  

                    |   expresion MENQUE expresion  
                    |   expresion MAYQUE expresion  
                    |   expresion MENIGUAL expresion  
                    |   expresion MAYIGUAL expresion 
                    |   expresion DIFERENTE expresion  
                    |   expresion IGUALIGUAL expresion  
                      
    '''


    if t[2] == '+':   t[0] = Aritmetic(ArithmeticOperator.MAS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':   t[0] = Aritmetic(ArithmeticOperator.MENOS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':   t[0] = Aritmetic(ArithmeticOperator.POR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/':   t[0] = Aritmetic(ArithmeticOperator.DIV, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '^':   t[0] = Aritmetic(ArithmeticOperator.POT, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':   t[0] = Aritmetic(ArithmeticOperator.MOD, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':   t[0] = Logic(LogicOperator.OR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':   t[0] = Logic(LogicOperator.AND, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<':   t[0] = Relational(RelationalOperator.MENORQUE , t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':   t[0] = Relational(RelationalOperator.MAYORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':   t[0] = Relational(RelationalOperator.MENORIGUAL , t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':   t[0] =Relational(RelationalOperator.MAYORIGUAL , t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '!=':   t[0] =Relational(RelationalOperator.DIFERENTE , t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '==':   t[0] =Relational(RelationalOperator.IGUALIGUAL , t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))

# EXPRESIONES PRIMITIVAS
def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0]=t[2]
        

# EXPRESIONES DE EXPRESIONES
def p_primitivo_decimal(t):
    'expresion : DECIMAL'
    t[0] = Primitive(Type.DECIMAL, t[1], t.lineno(1), find_column(input, t.slice[1]))


def p_expresion_entero(t):
    'expresion : ENTERO'
    t[0] = Primitive(Type.ENTERO ,t[1], t.lineno(1), find_column(input, t.slice[1]))


def p_primitivo_cadena(t):
    'expresion : CADENA'
    t[1]=str(t[1]).replace('\\t','\t')
    t[1]=str(t[1]).replace('\\n','\n')
    t[1]=str(t[1]).replace('\\\\','\\')
    t[1]=str(t[1]).replace("\\'","\'")
    t[1]=str(t[1]).replace('\\"','"')
    t[0] = Primitive(Type.CADENA,str(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_char(t):
    'expresion : CHAR'
    t[1]=str(t[1]).replace('\\t','\t')
    t[1]=str(t[1]).replace('\\n','\n')
    t[1]=str(t[1]).replace('\\\\','\\')
    t[1]=str(t[1]).replace("\\'","\'")
    t[1]=str(t[1]).replace('\\"','"')
    t[0] = Primitive(Type.CHARACTER,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_nulo(t):
    'expresion : NULO'
    t[0] = Primitive(Type.NULO,None, t.lineno(1), find_column(input, t.slice[1]))
def p_primitivo_true(t):
    '''expresion : RTRUE'''
    t[0] = Primitive(Type.BOOLEANO, True, t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_false(t):
    '''expresion : RFALSE'''
    t[0] = Primitive(Type.BOOLEANO, False, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_id(t):
    'expresion : ID'
    t[0] = Id(t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_llamada(t):
    'expresion :    llamadaFuncion    '
    t[0]=t[1]



# FUNCIONES NATIVAS

def p_parseval(t):
    '''expresion  :   RPARSE PARIZQ ID  COMA expresion PARDER '''
    t[0]= Parse(t[3],t[5], t.lineno(1), find_column(input, t.slice[1]))

def p_trunc(t):
    '''expresion  :   RTRUNC PARIZQ expresion PARDER '''
    t[0]= Trunc(t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_log(t):
    '''expresion  :   RLOG PARIZQ expresion COMA expresion PARDER '''
    t[0]= MathematicalOperations(OperationsMath.LOG,t[3],t[5], t.lineno(1), find_column(input, t.slice[1]))

def p_log10(t):
    '''expresion  :   RLOG10 PARIZQ expresion PARDER '''
    t[0]= MathematicalOperations(OperationsMath.LOG10,t[3],None, t.lineno(1), find_column(input, t.slice[1]))

def p_pusharr(t):
    '''PUSHARR :   RPUSH NOT PARIZQ  expresion COMA expresion PARDER 
                |   RPUSH NOT PARIZQ  expresion COMA ex PARDER
    '''
    t[0]=Push(t[4],t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_poparr(t):
    '''POPARR :   RPOP NOT PARIZQ  ID PARDER '''
    t[0]=Pop(t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_saber(t):
    '''expresion : POPARR 
                | PUSHARR '''
    t[0]=t[1]

def p_expresionLista(t):
    '''
        expresionlist : expresionlist COMA expresion
                    |   expresion
    '''
    if len(t)==2:
        t[0]=[t[1]]
    else:
        t[1].append(t[3])
        t[0]= t[1]



def p_expresion_global(t):
    '''VARGLOBAL : RGLOBAL ID IGUAL expresion 
            |   RGLOBAL ID 
    
    '''
    if len(t)==3:
        t[0]=Global(t[2], t.lineno(1), find_column(input, t.slice[1]),None)
    else:
        t[0]=Global(t[2], t.lineno(1), find_column(input, t.slice[1]),t[4])

def p_expresion_local(t):
    '''VARLOCAL : RLOCAL ID IGUAL expresion 
            |   RLOCAL ID 
    
    '''
    if len(t)==3:
        t[0]=Local(t[2], t.lineno(1), find_column(input, t.slice[1]),None)
    else:
        t[0]=Local(t[2], t.lineno(1), find_column(input, t.slice[1]),t[4])
#   IMPRIMIR

def p_imprimir(t) :
    '''imprimir_instr   :   PRINT PARIZQ expresionlist PARDER
                        |   PRINTLN PARIZQ expresionlist PARDER    '''
                        
    if t[1]=="print": t[0] = Print(t[3], t.lineno(1), find_column(input, t.slice[1]))
    if t[1]=="println": t[0] = Print(t[3], t.lineno(1), find_column(input, t.slice[1]),True)

def p_expresion_unaria(t):
    '''
    expresion : MENOS expresion %prec UMENOS 
            | NOT expresion %prec UNOT 
    '''
    if t[1] == '-':
        t[0] = Aritmetic(ArithmeticOperator.UMENOS, t[2],None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == '!':
        t[0] = Logic(LogicOperator.NOT, t[2],None, t.lineno(1), find_column(input, t.slice[1]))

# DECLARACION

def p_declaracion_jocl(t):
    '''
        declaracion :   declaracion1
                    |   declaracion2
    '''
    t[0]=t[1]

def p_declaracion_jocl1(t):
    '''
        declaracion1 :   ID IGUAL expresion
    '''
    t[0]=Statement(t[1], t.lineno(1), find_column(input, t.slice[1]),t[3],None)

def p_declaracion_jocl2(t):
    '''
     declaracion2 :  ID IGUAL expresion DPUNTOS tipo
    '''
    t[0]=Statement(t[1], t.lineno(1), find_column(input, t.slice[1]),t[3],t[5])



# IF 

def p_if1(t) :
    'if_instr     : RIF expresion instrucciones '
    t[0] = If(t[2], t[3], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_if2(t) :
    'if_instr     : RIF expresion instrucciones RELSE instrucciones'
    t[0] = If(t[2], t[3], t[5], None, t.lineno(1), find_column(input, t.slice[1]))

def p_if3(t) :
    'if_instr     : RIF expresion instrucciones  elseIfList'
    t[0] = If(t[2], t[3], None, t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_if4(t):
    '''elseIfList   : RELSEIF expresion instrucciones
                    | RELSEIF expresion instrucciones RELSE instrucciones
                    | RELSEIF expresion instrucciones  elseIfList'''
    if len(t) == 4:
        t[0] = If(t[2], t[3], None, None, t.lineno(1), find_column(input, t.slice[1]))
    elif len(t) == 6:
        t[0] = If(t[2], t[3], t[5], None, t.lineno(1), find_column(input, t.slice[1]))
    elif len(t) == 5:
        t[0] = If(t[2], t[3], None, t[4], t.lineno(1), find_column(input, t.slice[1]))

# DECLARACION DE FUNCION

def p_declaraFun(t):
    '''fun_inst :    RFUNCION ID PARIZQ PARDER instrucciones 
                    |    RFUNCION ID PARIZQ parametros PARDER instrucciones'''
    if len(t) == 6:
        t[0] = Function(t[2], [], t[5], t.lineno(1), t.lexpos(1))
    else:
        t[0] = Function(t[2], t[4], t[6], t.lineno(1), t.lexpos(1))



def p_parametros_1(t) :
    'parametros     : parametros COMA parametro'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_parametros_2(t) :
    'parametros    : parametro'
    t[0] = [t[1]]

# PARAMETRO FUNCION

def p_parametro(t) :
    '''
    parametro     : ID DPUNTOS tipo
                    | ID
                
    '''
    if len(t)== 4:
        t[0] = {'tipo':t[3],'Id':t[1]} # si en caso viene con un tipo si no solo se coloca como nulo
    else:
        
        t[0] = {'tipo':Type.NULO,'Id':t[1]} # si no viene el tipo solo el id no importa solo ingresaria

# TIPO 
def p_tipo(t) :
    '''tipo     : ID
                '''
    if t[1] == 'Int64':
        t[0] = Type.ENTERO
    elif t[1] == 'Float64':
        t[0] = Type.DECIMAL
    elif t[1] == 'String':
        t[0] = Type.CADENA
    elif t[1] == 'Bool':
        t[0] = Type.BOOLEANO
    elif t[1] == 'Char':
        t[0] = Type.CHARACTER
    elif t[1] == 'Null':
        t[0] = Type.NULO

# LLAMADA A FUNCION
def p_llamadaFunciones(t):
    'llamadaFuncion  : ID PARIZQ PARDER '
    t[0] = LlamadaFuncion(t[1], [],t.lineno(2), find_column(input, t.slice[2]))


def p_llamadaFuncionParametro (t):
    'llamadaFuncion  : ID PARIZQ parametros_llamada PARDER '
    t[0] = LlamadaFuncion(t[1], t[3],t.lineno(2), find_column(input, t.slice[2]))

# PARAMETROS LLAMADA A FUNCION

def p_parametrosLL_1(t) :
    'parametros_llamada     : parametros_llamada COMA parametro_llamada'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_parametrosLL_2(t) :
    'parametros_llamada    : parametro_llamada'
    t[0] = [t[1]]



# PARAMETRO LLAMADA A FUNCION

def p_parametroLL(t) :
    'parametro_llamada     : expresion'
    t[0] = t[1]

def p_retorno(t) :
    'return_instr     : RRETURN expresion'
    t[0] = Return(t[2],t.lineno(1), find_column(input, t.slice[1]))


# while

def p_while(t) :
    'while_instr     : RWHILE expresion instrucciones '
    t[0] = While(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]))

# BREAK
def p_break(t) :
    'break_instr     : RBREAK'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))

# CONTINUE
def p_continue(t) :
    'continue_instr     : RCONTINUE'
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))


# FOR


    ' expresiones : array_list'

def p_cicloFor(t):
    '''
        for_instr :     RFOR ID RIN expresion PUNTOS expresion instrucciones
                    |   RFOR ID RIN expresion instrucciones
                    |   RFOR ID RIN CORIZQ expresiones_array CORDER instrucciones 
    '''
    if len(t)==6:
            t[0]= For(t[2],t[4], t[5],t.lineno(1), find_column(input, t.slice[1]),None)

    elif t[4]=='[':
        t[0]= For(t[2],t[5], t[7],t.lineno(1), find_column(input, t.slice[1]),None)
    else:
        t[0]= For(t[2],t[4],t[7], t.lineno(1), find_column(input, t.slice[1]),t[6])


# DECLARACION DE LOS ARREGLOS

def p_arreglo(t):
    '''definicionArreglo_instr     : ID IGUAL CORIZQ expresiones_array CORDER'''
    t[0] = StatementArray(t[1], t[4], t.lineno(2), find_column(input, t.slice[2]))

# lista de dimensiones 
def p_array1(t):
    '''    
    expresiones_array : expresiones_array COMA ex
                    |   ex
    
    '''
    if len(t)==2:
        t[0]=[t[1]]
    else:
        t[1].append(t[3])
        t[0]=t[1]

def p_array2(t):
    '''ex : CORIZQ expresiones_array CORDER 
                | expresion
    
    '''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[2]

# ACCESO A ARREGLOS

def p_Acceso_ArregloS(t) :
    'expresion    : ID lista_expresiones'
    t[0] = t[2]

def p_lista_acceso_arreglo(t) :
    '''
    lista_expresiones : lista_expresiones CORIZQ expresion CORDER
                        |   CORIZQ expresion CORDER    
    '''
    if len(t)==5:
        t[0]=AccessArray(t[1], t[3] ,t.lineno(2), find_column(input, t.slice[2]))
        
    elif len(t)==4:
        id=  Id(t[-1], t.lineno(1), find_column(input, t.slice[1]))
        t[0]=AccessArray(id, t[2] ,t.lineno(1), find_column(input, t.slice[1]))

# MODIFICACION DE ARREGLOS

def p_ModArray(t) :
    'modifyArray_instr   : ID list_ac IGUAL expresion'
    t[0] = ModifyArray(t[1], t[2],t[4] ,t.lineno(3), find_column(input, t.slice[3]))

def p_lista_expresiones_1(t) :
    'list_ac    : list_ac CORIZQ expresion CORDER'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_lista_expresiones_2(t) :
    'list_ac    : CORIZQ expresion CORDER'
    t[0] = [t[2]]


#////////////////////////////////DEFINIR VARIABLE ////////////////////////

def p_instrucion_definicion(t):
    '''definicion_instr     : definicion_instr1
                            | definicion_instr2'''
    t[0]=t[1]

def p_instruccion_definicion1(t):
    'definicion_instr1       : VAR ID IGUAL expresion'
    t[0]=   Declaracion(t[1], str(t[2]).lower(), t.lineno(2), find_column(input, t.slice[2]), t[4])

def p_instruccion_definicion(t) :
    '''definicion_instr2     : VAR ID
        '''
    t[0] =Definicion(str(t[2]).lower(), t.lineno(1), find_column(input, t.slice[1]))





import ply.yacc as yacc
parser = yacc.yacc()
input = ''

def parse(inp) :
    global errores
    global lexer
    global parser 
    errores = []
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)


# FUNCIONES NATIVAS 


def crearNativas(ast):

    nombre = "uppercase"
    parametros = [{'tipo':Type.CADENA,'Id':'uppercase##param1'}]
    instrucciones = []
    toUpper = Uppercase(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(toUpper)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "lowercase"
    parametros = [{'tipo':Type.CADENA,'Id':'lowercase##param1'}]
    toLower = Lowercase(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(toLower)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "typeof"
    parametros = [{'tipo':Type.NULO,'Id':'typeof##param1'}]
    typeof = Typeof(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(typeof)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "float"
    parametros = [{'tipo':Type.NULO,'Id':'float##param1'}]
    flotante = Float(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(flotante)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "string"
    parametros = [{'tipo':Type.NULO,'Id':'string##param1'}]
    cad = String(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(cad)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "sqrt"
    parametros = [{'tipo':Type.NULO,'Id':'sqrt##param1'}]
    sqrtl = Sqrt(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(sqrtl)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "cos"
    parametros = [{'tipo':Type.NULO,'Id':'cos##param1'}]
    cosl = Cos(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(cosl)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "sin"
    parametros = [{'tipo':Type.NULO,'Id':'sin##param1'}]
    sinl = Sin(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(sinl)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "tan"
    parametros = [{'tipo':Type.NULO,'Id':'tan##param1'}]
    tanl = Tan(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(tanl)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "length"                       
    parametros = [{'tipo':Type.ENTERO,'Id':'length##param1'}]
    leng =Length(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(leng)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)


def tablaerror(tablaerrores):
    contador=1
    f = open('templates/reporte.html','w+')

    mensaje = """
    <!doctype html>
    <html lang="en">
    <head>
        <title>Tabla Errores</title>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <title>Hello, world!</title>
    </head>
    <body>
        <h1 class ="bg-success text-center">Tablas de Errores <h1>
        </br>
        <div class= container>
            <h4 class ="bg-warning">Errores lexicos y Sintacticos <h4>
            <table class="table  table-hover   table-bordered"" >
            <thead class="thead-dark"  >
                <tr>
                <th scope="col">#</th>
                <th scope="col">Tipo de Error</th>
                <th scope="col">Descripcion</th>
                <th scope="col">Fila</th>
                <th scope="col">Columna</th>
                <th scope="col">Hora</th>

                </tr>
            </thead>
            <tbody>
    """
    datos="<tr>"
    for x in tablaerrores:
        datos+="\n<th scope=\"row\">" +str(contador)+"</th>\n<td>"+x.type+"</td>\n<td>"+x.description+"</td><td>"+str(x.row)+"</td><td>"+str(x.column)+"</td><td>"+str(x.Hora)+"</td><tr>"
        contador=contador +1

    mensaje2="""    <tr>
        </tbody>
            </table>
        </div>
        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </body>
    </html>
        
    
    
    
    
    
    
    
    
    
    """

    f.write(mensaje+datos+mensaje2)
    f.close()


def graph(entrada):
    instrucciones = parse(entrada) #ARBOL AST
    Arbol_cst = Tree(instrucciones)
    TablaSimboloGlobal = Table(entorno="GLOBAL",declaracionTipo="variable",Row=0,Column=0)
    Arbol_cst.setTablaSimboloGlobal(TablaSimboloGlobal)

    # se crean las funciones nativas
    crearNativas(Arbol_cst)

    for error in errores:                   #CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
        Arbol_cst.getExcepciones().append(error)

    for instruccion in Arbol_cst.getInstrucciones():      # 1ERA PASADA SOlo verifica las funciones
        if isinstance(instruccion,Function):
            Arbol_cst.addFuncion(instruccion)

    for instruccion in Arbol_cst.getInstrucciones():      # 2da PASADA (DECLARACIONES Y ASIGNACIONES)
        if not isinstance(instruccion,Function):
            value = instruccion.interpreter(Arbol_cst,TablaSimboloGlobal)
            if isinstance(value,Exceptions):
                Arbol_cst.getExcepciones().append(value)



    init = NodoAST("ROOT")
    instr = NodoAST("INSTRUCTIONS")

    for instruccion in Arbol_cst.getInstrucciones():
        instr.Agregar_Hijo_Nodo(instruccion.getNodo())

    init.Agregar_Hijo_Nodo(instr)
    grafo = Arbol_cst.getDot(init) #DEVUELVE EL CODIGO GRAPHVIZ DEL AST

    dirname = os.path.dirname(__file__)
    direcc = os.path.join(dirname, 'templates/ast.dot')
    arch = open(direcc, "r+")
    arch.write(grafo)
    arch.close()
    os.system('dot -T svg -o templates/grafo.svg templates/ast.dot')


def ReporteTabla(entrada,funcio):
    contador=1
    f = open('templates/tabla.html','w+')

    mensaje = """
    <!doctype html>
    <html lang="en">
    <head>
        <title>Tabla Simbolos</title>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <title>Hello, world!</title>
    </head>
    <body>
        </br>
        <div class= container>
            <h4 class ="bg-warning">Tabla de Simbolos <h4>
            <table class="table  table-hover   table-bordered"" >
            <thead class="thead-dark"  >
                <tr>
                <th scope="col">#</th>
                <th scope="col">Nombre</th>
                <th scope="col">Descripcion</th>
                <th scope="col">Entorno</th>
                <th scope="col">Fila</th>
                <th scope="col">Columna</th>
                </tr>
            </thead>
            <tbody>
    """
    datos="<tr>"
    for x in entrada:
        datos+="\n<th scope=\"row\">" +str(contador)+"</th>\n<td>"+x.id+"</td>\n<td>"+x.descripcion+"</td>\n<td>"+x.entorno+"</td><td>"+str(x.Row)+"</td><td>"+str(x.Column)+"</td><tr>"
        contador=contador +1


    for x in funcio:
        datos+="\n<th scope=\"row\">" +str(contador)+"</th>\n<td>"+x.id+"</td>\n<td>"+x.descripcion+"</td>\n<td>"+x.entorno+"</td><td>"+str(x.Row)+"</td><td>"+str(x.Column)+"</td><tr>"
        contador=contador +1





    mensaje2="""    <tr>
        </tbody>
            </table>
        </div>
        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </body>
    </html>
        
    
    
    
    
    
    
    
    
    
    """

    f.write(mensaje+datos+mensaje2)
    f.close()

def clearfile():
    f = open('templates/reporte.html','w')
    f.close
    f = open('templates/tabla.html','w')
    f.close

'''
archivo=open("entrega.jl","r")
entrada=archivo.read()
instrucciones = parse(entrada) #ARBOL AST
Arbol_cst = Tree(instrucciones)
TablaSimboloGlobal = Table(entorno="GLOBAL",declaracionTipo="variable",Row=0,Column=0)
Arbol_cst.setTablaSimboloGlobal(TablaSimboloGlobal)

# se crean las funciones nativas
crearNativas(Arbol_cst)

for error in errores:                   #CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
    Arbol_cst.getExcepciones().append(error)

for instruccion in Arbol_cst.getInstrucciones():      # 1ERA PASADA SOlo verifica las funciones
    if isinstance(instruccion,Function):
        Arbol_cst.addFuncion(instruccion)

for instruccion in Arbol_cst.getInstrucciones():      # 2da PASADA (DECLARACIONES Y ASIGNACIONES)
    if not isinstance(instruccion,Function):
        value = instruccion.interpreter(Arbol_cst,TablaSimboloGlobal)
        if isinstance(value,Exceptions):
            Arbol_cst.getExcepciones().append(value)


ReporteTabla(TablaSimboloGlobal.generareporte(),Arbol_cst.repofunciones())


print("----------errores ------------")
for x in Arbol_cst.getExcepciones():
    print(x.toString())

print("----------salida ------------")
print(Arbol_cst.getConsola())


'''