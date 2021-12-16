from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Type import Type
from Abstract.Instruction import Instruction
from SymbolsTable.Table import Table
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Symbols import Symbols
from Abstract.NodoAST import NodoAST


class LlamadaFuncion(Instruction):
    def __init__(self, nombre,parametros,Row, Column):
        self.Id = nombre
        self.Row = Row
        self.parametros=parametros  
        self.Column = Column
        self.Type =None
        self.arreglo= False

        
    def interpreter(self, tree, table):
        #se obtiene la funcion , este esta en el arbol que nunca se cambia simpre es el mismo
        funcion = tree.getFuncion(self.Id)
        if funcion==None: # si no encontro la funcion entonces  genera un errro
            return Exceptions("Semantico", "No se encontro la funcion "+ self.Id, self.Row, self.Column)
        nuevaTabla=Table(tree.getTablaSimboloGlobal(),"llama a funcion "+str(self.getId()) ,declaracionTipo="variable",Row=self.Row,Column=self.Column)
        # obtener los parametros 
        if len(funcion.getparametros())==len(self.getparametros()) : # si trae la misma cantidad parametros que la funcion 
            contador=0
            for expresion in self.getparametros(): # se obtiene el valor del parametro en la llamada
                resultadoExpresion=expresion.interpreter(tree,table)
                if isinstance(resultadoExpresion,Exceptions): return resultadoExpresion

                # se debe validar que sean del mismo tipo, los parametrso de la llamada con los parametros de la funcion
                if funcion.parametros[contador]['Id'] in ('sqrt##param1','float##param1','string##param1','typeof##param1','round##param1','length##param1'):
                    funcion.parametros[contador]['tipo']=expresion.getType()
                    #creacion de simbolo e ingresandolo a la tabla de simbolo
                    simbolo = Symbols(str(funcion.parametros[contador]['Id']), funcion.parametros[contador]['tipo'], self.getRow(), self.getColumn(),resultadoExpresion)
                    result=nuevaTabla.setTabla(simbolo,nuevaTabla)
                    if isinstance(result,Exceptions): return result

                elif funcion.parametros[contador]['tipo']== Type.ARREGLO:
                    print("arreglo")
                    arregloGuardado = table.getTabla(expresion.getId()) # mando a interpretar para que me devuelva el arreglo que se envio en la llamada funcion

                    if arregloGuardado is None:
                        return Exceptions("Semantico", "Arreglo "+ str(expresion.getIdentificador()) +" no fue encontrada.", self.getFila(), self.getColumna() )

                    if arregloGuardado.getArreglo() is False:
                        return Exceptions("Semantico",str( expresion.getIdentificador())+" No es un Arreglo.", self.getFila(), self.getColumna() )

                    if funcion.parametros[contador]['dimensiones'] != arregloGuardado.getDimension():   #VERIFICACION DE DIMENSIONES
                        return Exceptions("Semantico", "Dimensiones diferentes parametro Arreglo.", self.getFila(), self.getColumna() )

                    #creacion de simbolo e ingresandolo a la tabla de simbolo
                    simbolo = Symbols(str(funcion.parametros[contador]['Id']).lower(), funcion.parametros[contador]['tipo-arreglo'],True, self.getFila(), self.getColumna(),resultadoExpresion)
                    
                    resultTabla=nuevaTabla.setTabla(simbolo,nuevaTabla)

                    if isinstance(resultTabla,Exceptions): return resultTabla
                    

                    print("arreglo")

                else:
                    if funcion.parametros[contador]['tipo']== expresion.getType() or funcion.parametros[contador]['tipo']==Type.NULO:
                      
                        #creacion de simbolo e ingresandolo a la tabla de simbolo
                        simbolo = Symbols(str(funcion.parametros[contador]['Id']), expresion.getType(), self.getRow(), self.getColumn(),resultadoExpresion)
                        resultTabla=nuevaTabla.setTabla(simbolo,nuevaTabla)
                        if isinstance(resultTabla,Exceptions): return resultTabla
                        
                    
                    else:
                        return Exceptions("Semantico", "Tipo Diferente en los parametros de llamada ", self.getRow(), self.getColumn())
                    
                contador+=1 # para ir paralelamente en los parametros


            resultado = funcion.interpreter(tree,nuevaTabla) # para ejecutar lo que tenga dentro de la funcion

            if isinstance(resultado,Exceptions): return resultado
            
            self.Type= funcion.getType() # es el tipo de la funcion
            #para saber si lo que devuelve es algun primitivo
            
            return resultado
            
        else :

            return Exceptions("Semantico", "Cantidad de parametros para la funcion \""+self.getId() + "\" NO VALIDO ", self.getRow(), self.getColumn())


    def PrintArray(self,tree,table,value):
        aux=None
        if isinstance(value,list):  
            for w in value:
                if isinstance(w,list):
                    aux=w
                else:
                    val=w.interpreter(tree,table)
                    if isinstance(val,list):
                        aux=(self.PrintArray(tree,table,w))
                    else:
                        aux=(w.interpreter(tree,table))
        
        try:
            value2 = value.interpreter(tree, table)  # RETORNA CUALQUIER VALOR para imprimir
        except:
            return aux
        if isinstance(value2,list):  
            aux=self.PrintArray(tree,table,value2)

        return aux


    def getNodo(self):
        nodo=NodoAST("LLAMADA A FUNCION")
        nodo.Agregar_Hijo(str(self.getId()))
        parametros =NodoAST("PARAMETROS")
        for param in self.getparametros():
            parametros.Agregar_Hijo_Nodo(param.getNodo())
        nodo.Agregar_Hijo_Nodo(parametros)

    
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

    def setparametros(self, parametros):
        self.parametros=parametros

        
    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column