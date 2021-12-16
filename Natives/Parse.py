from Abstract.Instruction import Instruction
from SymbolsTable.Type import Type
from SymbolsTable.Exceptions import Exceptions
from Abstract.NodoAST import NodoAST


class Parse(Instruction):
    def __init__(self, Type, expresion, Row, Column):
        self.expresion = expresion
        self.Row = Row
        self.Column = Column
        self.Type = Type

    
    def interpreter(self, tree, table):
        expresion = self.expresion.interpreter(tree, table)

        if self.VerificType(self.Type)==Type.ID:
            return Exceptions("Semantico", "No se puede operar Parse para ese tipo de dato " + self.getType(), self.Row, self.Column)

        self.setType(self.VerificType(self.getType())) # obtine el tipo de dato que le corresponde

        if self.getType() == Type.DECIMAL:

            if self.getExpresion().getType()== Type.ENTERO:
                try:
                    return float(self.ObtenerValor(self.getExpresion().getType(), expresion))
                except:
                    return Exceptions("Semantico", "No se puede operar Parse para Float.", self.Row, self.Column)
            
            elif self.getExpresion().getType() == Type.CADENA:
                try:
                    return float(self.ObtenerValor(self.getExpresion().getType(), expresion))
                except:
                    return Exceptions("Semantico", "No se puede operar Parse para Float.", self.Row, self.Column)
            
            elif self.getExpresion().getType() == Type.CHARACTER:
                try:
                    return float(self.ObtenerValor(self.getExpresion().getType(), expresion))
                except:
                    return Exceptions("Semantico", "No se puede operar Parse para Float.", self.Row, self.Column)
            
            return Exceptions("Semantico", "Type Erroneo de casteo para Double.", self.Row, self.Column)
      
        elif self.getType() == Type.ENTERO:

            if self.getExpresion().getType()== Type.DECIMAL:
                try:
                    return int(self.ObtenerValor(self.getExpresion().getType(), expresion))
                except:
                    return Exceptions("Semantico", "No se puede operar Parse para Int.", self.Row, self.Column)
            elif self.getExpresion().getType() == Type.CADENA:
                try:
                    return int(self.ObtenerValor(self.getExpresion().getType(), expresion))
                except:
                    return Exceptions("Semantico", "No se puede operar Parse para Int.", self.Row, self.Column)

            elif self.getExpresion().getType() == Type.CHARACTER:
                try:
                    return int(self.ObtenerValor(self.getExpresion().getType(), expresion))
                except:
                    return Exceptions("Semantico", "No se puede operar Parse para Int.", self.Row, self.Column)
            return Exceptions("Semantico", "Type Erroneo de casteo para Int.", self.Row, self.Column)

        elif self.getType() == Type.CADENA:

            if self.getExpresion().getType()== Type.DECIMAL:
                try:
                    return str(self.ObtenerValor(self.getExpresion().getType(), expresion))
                except:
                    return Exceptions("Semantico", "No se puede operar Parse para Int.", self.Row, self.Column)
            elif self.getExpresion().getType() == Type.ENTERO:
                try:
                    return str(self.ObtenerValor(self.getExpresion().getType(), expresion))
                except:
                    return Exceptions("Semantico", "No se puede operar Parse para Cadena.", self.Row, self.Column)
            return Exceptions("Semantico", "Type Erroneo de casteo para Cadena.", self.Row, self.Column)

        elif self.getType() == Type.CHARACTER:

            if self.getExpresion().getType()== Type.ENTERO:
                try:
                    return chr(self.ObtenerValor(self.getExpresion().getType(), expresion))
                except:
                    return Exceptions("Semantico", "No se puede operar Parse para Char.", self.Row, self.Column)
            return Exceptions("Semantico", "Type Erroneo de casteo para Char.", self.Row, self.Column)

        elif self.getType() == Type.BOOLEANO:

            if self.getExpresion().getType()== Type.CADENA:
                if expresion.lower() in ("true","false"):
                    if expresion.lower()=="true":
                        return True
                    else:
                        return False
                        
                return Exceptions("Semantico", "Type Erroneo de casteo para Booleno.", self.Row, self.Column)
            return Exceptions("Semantico", "Type Erroneo de casteo para Booleno.", self.Row, self.Column)



    def getNodo(self):
        nodo=NodoAST("PARSE")
        nodo.Agregar_Hijo(self.simb(self.getType().name))
        nodo.Agregar_Hijo_Nodo(self.getExpresion().getNodo())
        return nodo
        

    def ObtenerValor(self, Type, val):
        if Type == Type.ENTERO:
            return int(val)
        elif Type == Type.DECIMAL:
            return float(val)
        elif Type == Type.BOOLEANO:
            return bool(val)
        elif Type ==Type.CHARACTER:
            return ord(val)
        return str(val)

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
        else:
            return Type.ID

    def simb(self,Type):
        if Type=="ENTERO":
            return "Int"
        elif Type=="CADENA":
            return "String"
        elif Type=="BOOLEANO":
            return "Booleano"
        elif Type=="CHARACTER":
            return "Char"
        elif Type=="NULO":
            return "Null"
        elif Type=="ARREGLO":
            return "ARREGLO"
        elif Type=="DECIMAL":
            return "Double"

    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type

    def getExpresion(self):
        return self.expresion

    def setExpresion(self,expresion):
        self.expresion= expresion

    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column