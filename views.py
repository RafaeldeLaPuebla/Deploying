#Definimos nuestros puntos de entrada a nuestra página web.
from flask import render_template, request, redirect, url_for #es un mandato de Flask, el render template, hay que importarlo.
from app import app
import psycopg2

#un decorador:
@app.route('/')
def index():
    dbParams = app.config['DATABASE']
    try:
        conn = psycopg2.connect(host=dbParams['host'], port=dbParams['port'], dbname=dbParams['dbname'], user=dbParams['dbuser']), password=dbParams['password']
        cur = conn.cursor()


        query = "SELECT * FROM movimientos;"#Me sacas todos los campos

        cur.execute(query); #Esta consulta hay que tratarla porque me puede devolver varias filas.

        fila = cur.fetchone()#leo la fila, que me devuelve todos los campos.
        movimientos = [] #creo un array de movimientos vacíos que es lo que voy a devolver
        while fila != None:
            movimiento = {} #creo un diccionario vacío.
            
            #voy recorriendo campo a campo de cada fila.
            for ix in range(0, len(fila)):
                columnName = cur.description[ix][0]
                if columnName == 'fecha_hora':
                    dato = str(fila[ix])
                    movimiento['fecha'] = dato[:10]
                    movimiento['hora'] = dato[11:16]
                else:
                    movimiento[columnName]=fila[ix]#cogemos la siguiente
            movimientos.append(movimiento)

            #<procesar fila para transformar en movimientos>
            file = cur.fetchone() #volver a leer para que el bucle no sea infinito.

        cur.close()
        conn.close()

        
    except Exception as e:
        print(e.pgerror)
        cur.close()
        conn.close()
    
    return render_template('index.html', registros = [])


@app.route('/nuevoregistro', methods=['GET','POST'])
def nuevoregistro():
    if request.method == 'GET':
        return  render_template('nuevoregistro.html')
    else:
        dbParams = app.config('DATABASE')
        try:
            conn = psycopg2.connect(host=dbParams['host'], port=dbParams['port'], dbname=dbParams['dbname'], user=dbParams['dbuser']), password=dbParams['password']
            cur = conn.cursor()
            query = """INSERT INTO movimientos (fecha_hora, descripcion, moneda_comprada, cantidad_comprada, moneda_pagada, cantidad_pagada)
                        VALUES ('{} {}:00.000000', '{}','{}','{}','{}','{}');"""
            f = request.form 
            '''
            'YYYY-MM-DD' + 'HH:MM' => 'YYYY-MM-DD HH:MM:00.000000'
            '''
        
            
            query = query.format(f['fecha'], f['hora'], f['descripcion'], f['monedaComprada'], f['cantidadComprada'], f['monedaPagada'], f['cantidadPagada'])

            cur.execute(query)

            conn.commit() #Así lo fijas con el commit
        except Exception as e: #Daría un error, pero el programa no se caería.
            print(e.pgerror)
            cur.close()
            conn.close()

        return redirect(url_for('index'))
