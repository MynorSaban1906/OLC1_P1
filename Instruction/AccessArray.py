
from Expressions.Primitive import Primitive
from typing import List
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Type import Type
from Abstract.Instruction import Instruction
from SymbolsTable.Symbols import Symbols
from SymbolsTable.Table import Table
from Abstract.NodoAST import NodoAST
import copy


class AccessArray(Instruction):

    def __init__(self,Id,Lista, Row, Column):
        self.Id=Id
        self.Lista=Lista
        self.Row=Row
        self.Column=Column
        self.Type=None


    def interpreter(self, tree, table):
        simbo = self.Id.interpreter(tree,table)

        if simbo == None:
            return Exceptions("Semantico", "Arreglo " + self.getId() + " no encontrado", self.getRow(), self.getColumn() )

        # obtiene el arreglo 
        
        Arreglo = self.Buscar(tree, table, copy.copy(self.Lista),simbo)   #RETORNA EL ARREGLO DE DIMENSIONES
    
        if isinstance(Arreglo,Exceptions):return Arreglo
        
        if isinstance(Arreglo,list):

            return Arreglo
        else:
            return Arreglo



    def Buscar(self, tree, table, expresiones,arreglo):
        arr=[]
        valorArreglo =None
        if not isinstance(arreglo, list):
            num = expresiones.interpreter(tree, table)

            if isinstance(num, Exceptions): return num

            if isinstance(arreglo,str):
                self.setType(Type.ENTERO)
                return arreglo[num-1]

            return Exceptions("Semantico", "Accesos de más en un Arreglo.", self.getRow(), self.getRow())
       
       
        
        num = expresiones.interpreter(tree, table)

        if isinstance(num, Exceptions): return num
        
        valorArreglo = arreglo[num-1] # entra al arreglo ue se necesita
        self.setType(self.typearr(type(valorArreglo).__name__ ) )
        
        return valorArreglo


    def typearr(self,name):
        if name=='int':
            return Type.ENTERO
        elif name=='float':
            return Type.DECIMAL
        else:
            return Type.CADENA



    def getNodo(self):
        nodo = NodoAST("ACCESO ARREGLO")
        nodo.Agregar_Hijo(str(self.getId().Id))
        exp = NodoAST("DIMENSIONES ARREGLO")
        exp.Agregar_Hijo_Nodo(self.Lista.getNodo())
        nodo.Agregar_Hijo_Nodo(exp)
        return nodo



    def getId(self):
        return self.Id

    def setId(self, Id):
        self.Id=Id


    def getLista(self):
        return self.Lista

    def setLista(self, Lista):
        self.Lista=Lista


    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column

    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type
