from flask import Flask, request, render_template
from os import remove
from grammar import *
from Export import output
from SymbolsTable.Table import Table
from Abstract.NodoAST import NodoAST

app = Flask(__name__)

# ESTE SERA UNA APLICACION DE FLASK WEB. Esta contendrá todos los archivos HTML necesarios para mostrar todo
# LA FORMA DE REALIZAR EL DEPLOY A HEROKU LO PUEDEN VER ACA: https://www.geeksforgeeks.org/deploy-python-flask-app-on-heroku/
@app.route("/execute", methods=['POST'])
def home():
    try:

        output.init
        inpt = request.json['input']
        
        output.ast = parse(inpt) #ARBOL AST
        
        Arbol_cst = Tree(output.ast)
        TablaSimboloGlobal = Table(entorno="GLOBAL",declaracionTipo="variable",Row=0,Column=0)
        crearNativas(Arbol_cst)
        Arbol_cst.setTablaSimboloGlobal(TablaSimboloGlobal)
        try:
            for instruccion in Arbol_cst.getInstrucciones():      # 1ERA PASADA SOlo verifica las funciones
                if isinstance(instruccion,Function):
                    Arbol_cst.addFuncion(instruccion)

            for instruccion in Arbol_cst.getInstrucciones():      # 2da PASADA (DECLARACIONES Y ASIGNACIONES)
                if not isinstance(instruccion,Function):
                    value = instruccion.interpreter(Arbol_cst,TablaSimboloGlobal)
                    if isinstance(value,Exceptions):
                        Arbol_cst.getExcepciones().append(value)
                        errores.append(value)
                        
            output.output=Arbol_cst.getConsola()

            tablaerror(errores)
            graph(inpt)
            ReporteTabla(TablaSimboloGlobal.generareporte(),Arbol_cst.repofunciones())
            print("----------errores ------------")
            for x in errores:
                print(x.toString())

            print("----------salida ------------")
            print(Arbol_cst.getConsola())

        except:
            print("Error al ejecutar instrucciones")
            
        return { 'msg': output.output, 'code': 200 }
    except:
        return { 'msg': 'ERROR', 'code': 500 }


@app.route("/report")
def report():
    return render_template('reporte.html')

@app.route("/grafo")
def grafo():
    return render_template('grafo.svg')


@app.route("/table")
def table():
    return render_template('tabla.html')

@app.route("/", methods=['GET'])
def home_view():
    return render_template('index.html')

if __name__ == '__main__':
    app.run( port=3000,debug=True)
   
   