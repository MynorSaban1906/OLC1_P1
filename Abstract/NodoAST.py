class NodoAST():
    
    def __init__(self,valor):
        self.Nodo_Hijos=[]
        self.valor= valor
        
    def setNodos_Hijos(self,hijos):
        self.Nodo_Hijos= hijos

    def getNodos_Hijos(self):
        return self.Nodo_Hijos

    def Agregar_Hijo(self,valorhijos):
        self.Nodo_Hijos.append(NodoAST(valorhijos))

    def Agregar_Hijos(self,hijos):
        for hijo in hijos:
            self.Nodo_Hijos.append(hijo)

    def Agregar_Hijo_Nodo(self, hijo):
        self.Nodo_Hijos.append(hijo)

    def Agregar_Primer_Hijo(self, valorhijo):
        self.Nodo_Hijos.insert(0, NodoAST(valorhijo))

    def Agregar_Primer_Hijo_Nodo(self, hijo):
        self.Nodo_Hijos.insert(0, hijo)

    def setValor(self,valor):
        self.valor=valor

    def getValor(self):
        return str(self.valor)