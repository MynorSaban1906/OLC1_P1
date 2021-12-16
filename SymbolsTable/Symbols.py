# este es el objeto  de tipo simbolo

class Symbols:
    
    def __init__(self, id, type, row, column, value,arreglo=None ):
        self.id = id
        self.type = type
        self.row = row
        self.column = column
        self.value = value
        self.arreglo= arreglo
        self.dimension=None

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type  

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def getRow(self):
        return self.row

    def setRow(self, row):
        self.row= row 

    def getColumn(self):
        return self.column

    def setColumn(self, column):
        self.column= column



    def getArreglo(self):
        return self.arreglo


    def getDimension(self):
        return self.dimension

    def setDimension(self, dimension):
        self.dimension=dimension
