from Abstract.Instruction import Instruction
from SymbolsTable.Type import OperationsMath,Type
from SymbolsTable.Exceptions import Exceptions
import math
from Instruction.Function import Function
from Abstract.NodoAST import NodoAST
import copy

class Push(Instruction):

    def __init__(self, Id, expresion, Row, Column):
        self.Id = Id
        self.expresion = expresion
        self.Row = Row
        self.Column = Column
        self.Type = Type



    def interpreter(self, tree, table):
           
        simbo= self.Id.interpreter(tree,table)

        if simbo == None:
            return Exceptions("Semantico", "Arreglo " + str(self.getId()) + " no encontrado", self.getRow(), self.getColumn() )

        # obtiene el arreglo 
        
        Arreglo = self.Buscar(tree, table,self.expresion,simbo)   #RETORNA EL ARREGLO DE DIMENSIONES
    
        if isinstance(Arreglo,Exceptions):return Arreglo
        
        return None


    def Buscar(self, tree, table, expresiones,arreglo):
        
        if isinstance(expresiones,list):
            arreglo.append(self.PrintArray(tree,table,expresiones))
        else:
            arreglo.append(expresiones.interpreter(tree,table))

       
        return arreglo
    def PrintArray(self,tree,table,value):
        aux=[]
        
        if isinstance(value,list):  
            for w in value:
                if isinstance(w,list):
                    aux.append(self.PrintArray(tree,table,w))
                else:
                    val=w.interpreter(tree,table)
                    if isinstance(val,list):
                        aux.append(self.PrintArray(tree,table,w))
                    else:
                        aux.append(w.interpreter(tree,table))
        
        try:
            value2 = value.interpreter(tree, table)  # RETORNA CUALQUIER VALOR para imprimir
        except:
            return aux
        if isinstance(value2,list):  
            aux=self.PrintArray(tree,table,value2)

        return aux


    def getNodo(self):
        nodo=NodoAST("PUSH")
        nodo.Agregar_Hijo_Nodo(self.Id.getNodo())
        if isinstance(self.expresion,list):
            nodo.Agregar_Hijo_Nodo(self.Printray(self.expresion))
        else:
            nodo.Agregar_Hijo_Nodo(self.expresion.getNodo())

        return nodo
        
    def Printray(self,value):
        aux=NodoAST("ARREGLO")
        if isinstance(value,list):  
            for w in value:
                if isinstance(w,list):
                    aux.Agregar_Hijo_Nodo(self.Printray(w))
                else:
                    val=w.getNodo()
                    if isinstance(val,list):
                        aux.Agregar_Hijo_Nodo( self.PrintArray(w))
                    else:
                        aux.Agregar_Hijo_Nodo(w.getNodo())
        
        try:
            value2 = value.getNodo()  # RETORNA CUALQUIER VALOR para imprimir
        except:
            return aux
        if isinstance(value2,list):  
            aux.Agregar_Hijo_Nodo(self.PrintArray(value2))

        return aux



    def getId(self):
        return self.Id

    def setId(self, Id):
        self.Id=Id


    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column



