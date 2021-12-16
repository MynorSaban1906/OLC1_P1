from Abstract.Instruction import Instruction
from SymbolsTable.Type import Type
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Table import Table
from Instruction.Break import Break
from Instruction.Return import Return
from Abstract.NodoAST import NodoAST


class Function(Instruction):

    def __init__(self, Id, parametros, Instr, Row, Column):
        self.Id = Id
        self.parametros = parametros
        self.Instr = Instr
        self.Row = Row
        self.Column = Column
        self.Type=Type.NULO

    def interpreter(self, tree, table):
        tablaNueva = Table(table,entorno="Funcion",declaracionTipo="variable",Row=self.Row,Column=self.Column)
        for instruccion in self.Instr:      # recorrre las instruciones dentro de las funciones
            value = instruccion.interpreter(tree,tablaNueva)
            if isinstance(value, Exceptions) :
                tree.getExcepciones().append(value)
            if isinstance(value, Break): 
                err = Exceptions("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.Row, instruccion.Column)
                tree.getExcepciones().append(err)
                tree.updateConsola(err.toString())

            if isinstance(value, Return): # cuando encuetre un Return 
                self.setType(value.getType()) # tomaria el Type de lo que devuelve la funcion
                return value.result # si encontro el return entonces devulve el valor que tenia el return # si encontro el return entonces devulve el valor que tenia el return

        return None # por defecto


    def getNodo(self):
        nodo=NodoAST("FUNCION")
        nodo.Agregar_Hijo(str(self.getId()))
        parametros =NodoAST("PARAMETROS")
        for param in self.getparametros():
            parametro= NodoAST("PARAMETRO")
            parametro.Agregar_Hijo(param["Id"])
            parametros.Agregar_Hijo_Nodo(parametro)
            
        nodo.Agregar_Hijo_Nodo(parametros)

        instrucciones=NodoAST("INSTRUCCIONES")
        for instr in self.Instr:
            instrucciones.Agregar_Hijo_Nodo(instr.getNodo())

        nodo.Agregar_Hijo_Nodo(instrucciones)
        
        return nodo
        

    def getId(self):
        return self.Id

    def setId(self, Id):
        self.Id=Id

    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type


    def getparametros(self):
        return self.parametros

    def setparametros(self,  parametros):
        self.parametros= parametros