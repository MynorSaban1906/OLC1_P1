from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Type import Type
from Abstract.Instruction import Instruction
from SymbolsTable.Symbols import Symbols
from SymbolsTable.Table import Table
from SymbolsTable.Exceptions import Exceptions
from Instruction.Assignment import Assignment
import copy
from Abstract.NodoAST import NodoAST




class Local(Instruction):
    def __init__(self, id, Row, Column,expresion):
        self.Id = id
        self.expresion=expresion
        self.Type = None
        self.Row = Row
        self.Column = Column
        self.arreglo = False


    def interpreter(self, tree, table):

        simbolo = table.getTablaLocal(self.Id) # busca en la tabla actual 
        
        if simbolo == None: # si no esta entonces la declaramos 
            if self.expresion==None: # si la expresion es nula
                value = self.expresion.interpreter(tree, table) # Valor a asignar a la variablef
                if isinstance(value, Exceptions): return value
                simbolo = Symbols(self.id, Type.NULO, self.Row, self.Column, None)

                result = table.setTabla(simbolo,table)
                if isinstance(result, Exceptions): return result
                self.setType(simbolo.getType())  # AUN ESTA EN PRUEBA
                return None
                
            else:
                value = self.expresion.interpreter(tree, table) # Valor a asignar a la variablef
                if isinstance(value, Exceptions): return value
                simbolo = Symbols(self.Id, self.expresion.Type , self.Row, self.Column, value)

                result = table.setTabla(simbolo,table)
                if isinstance(result, Exceptions): return result
                self.setType(simbolo.getType())  # AUN ESTA EN PRUEBA
    
                return None

        else:
            if self.expresion==None: # si en caso no viene con ninguna expresion
                # devuelvo datos importantes
                self.Type = simbolo.getType()
                
                return simbolo.getValue()

            else: # viene con una expresion el local 
                
                value = self.expresion.interpreter(tree, table) # Valor a asignar a la variable

                if isinstance(value, Exceptions): return value

                simbolo = Symbols(self.Id, self.expresion.Type , self.Row, self.Column, value)

                result = table.updateTable(simbolo)

                if isinstance(result, Exceptions): return result

                self.Type = simbolo.getType()
                
                return simbolo.getValue()
                

        


    def getNodo(self):
        nodo=NodoAST("Gobal")
        nodo.Agregar_Hijo_Nodo(self.expresion.getNodo())
        return nodo
        


    def getid(self):
        return self.id

    def setid(self, id):
        self.id=id

        
    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type

    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column
