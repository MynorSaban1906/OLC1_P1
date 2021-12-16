
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Type import Type
from Abstract.Instruction import Instruction
from SymbolsTable.Symbols import Symbols
from SymbolsTable.Table import Table
from SymbolsTable.Exceptions import Exceptions
from Instruction.Assignment import Assignment
import copy
from Abstract.NodoAST import NodoAST




class Statement(Instruction):
    def __init__(self, id, Row, Column, Expression=0, Type=None):
        self.id = id
        self.Type = Type
        self.Expression = Expression
        self.Row = Row
        self.Column = Column
        self.arreglo = False


    def interpreter(self, tree, table):
        
        value = self.Expression.interpreter(tree, table) # Valor a asignar a la variable

        if isinstance(value, Exceptions): return value


        simbolo = Symbols(self.id, self.Expression.Type , self.Row, self.Column, value)

        if(table.SearchAux(simbolo)):

            result = table.updateTable(simbolo)

            if isinstance(result, Exceptions): return result
            
        
            return None
            
        else:

            if self.getType()==self.Expression.Type:

                result = table.setTabla(simbolo,table)

                if isinstance(result, Exceptions): return result

        
                return None

            elif self.getType()!=self.Expression.Type and self.getType()!=None and self.Expression.Type!=None:

                return Exceptions("Semantico","tipo no compatible",self.getRow(), self.getColumn())

            else:   

                result = table.setTabla(simbolo,table)

                if isinstance(result, Exceptions): return result

                self.setType(simbolo.getType())  # AUN ESTA EN PRUEBA
        
                return None
                
        
    def VerificType(self,string):
        if string=="Int64":
            return Type.ENTERO
        elif string=="Float64":
            return Type.DECIMAL
        elif string=="Char":
            return Type.CHARACTER
        elif string=="String":
            return Type.CADENA
        elif string=="bool":
            return Type.BOOLEANO
        elif string=="None":
            return Type.NULO
        else:
            return Type.ID


    def getNodo(self):
        nodo=NodoAST("ASIGNACION")
        nodo.Agregar_Hijo(str(self.getid()))
        nodo.Agregar_Hijo("=")
        nodo.Agregar_Hijo_Nodo(self.getExpression().getNodo())
        return nodo
        


    def getid(self):
        return self.id

    def setid(self, id):
        self.id=id

        
    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type

    def getExpression(self):
        return self.Expression

    def setExpression(self,Expression):
        self.Expression= Expression

    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column
