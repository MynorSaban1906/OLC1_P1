import re
from SymbolsTable.Table import repo
class Tree:
    def __init__(self, instrucciones ):
        self.instrucciones = instrucciones # son de tipo instrucciones
        self.excepciones = [] #para las excepciones, estas se guardan en objetos en esta tabla
        self.funciones=[] # lista para las funciones guardadas
        self.consola = ""
        self.TablaSimboloGlobal = None # al inicial inicia en NOne
        self.dot=""
        self.contador=0
  
    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones

    def getExcepciones(self):
        return self.excepciones

    def setExcepciones(self, excepciones):
        self.excepciones = excepciones

    def getConsola(self):
        return self.consola
    
    def setConsola(self, consola):
        self.consola = consola

    def updateConsola(self,cadena):
        self.consola += str(cadena)

    def getTablaSimboloGlobal(self):
        return self.TablaSimboloGlobal
    
    def setTablaSimboloGlobal(self, TablaSimboloGlobal):
        self.TablaSimboloGlobal = TablaSimboloGlobal



    def getFunciones(self):
        return self.funciones

    def getFuncion(self, identificador):
        for funcion in self.funciones:
            if funcion.getId() == identificador:
                return funcion
        return None
    
    def addFuncion(self, funcion):
        self.funciones.append(funcion)



    def getDot(self, raiz): ## DEVUELVE EL STRING DE LA GRAFICA EN GRAPHVIZ
        self.dot = ""
        self.dot += "digraph {\n"
        self.dot += 'bgcolor="#21495c ";\n edge[color ="#b9ff00"];\nnode[style="filled" fillcolor="#2b8ea4 " fontcolor="white" color ="#007add"]'
        self.dot += "n0[label=\"" + raiz.getValor().replace("\"", "\\\"") + "\"];\n"
        self.contador = 1
        self.recorrerAST("n0", raiz)
        self.dot += "}"
        return self.dot

    def recorrerAST(self, idPadre, nodoPadre):
        for hijo in nodoPadre.getNodos_Hijos():
            nombreHijo = "n" + str(self.contador)

            print(hijo.getValor())
            try:
                self.dot += nombreHijo + "[label=\"" + hijo.valor.replace("\"", "\\\"") + "\"];\n"
            except:
                self.dot += nombreHijo + "[label=\"" + str(hijo.valor)+ "\"];\n"

            print(hijo.valor)
            self.dot += nombreHijo + "[label=\"" + hijo.getValor().replace("\"", "\\\"") + "\"];\n"

    def recorrerAST(self, idPadre, nodoPadre):
        for hijo in nodoPadre.getNodos_Hijos():
            nombreHijo = "n" + str(self.contador)

            print(str(hijo.valor))
            try:
                self.dot += nombreHijo + "[label=\"" + hijo.valor.replace("\"", "\\\"") + "\"];\n"
            except:
                self.dot += nombreHijo + "[label=\"" + str(hijo.valor)+ "\"];\n"

          
            self.dot += nombreHijo + "[label=\"" + hijo.getValor().replace("\"", "\\\"") + "\"];\n"

            self.dot += idPadre + "->" + nombreHijo + ";\n"
            self.contador += 1
            self.recorrerAST(nombreHijo, hijo) 


    def repofunciones(self):
        aux=[]
        for x in self.getFunciones():
            t=repo(x.Id,"FUNCION","GLOBAL",x.Row,x.Column)
            aux.append(t)
        return aux
