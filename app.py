from flask import Flask, render_template, redirect, url_for,Flask, request, jsonify, session, redirect, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os
import uuid  # Para generar nombres únicos de archivos
from datetime import datetime
from datetime import timedelta

# Crear una instancia de la clase Flask
app = Flask(__name__)
app.secret_key = 'keysecret'  # Necesario para que Flask maneje las sesiones

UPLOAD_FOLDER = 'static/principal/'  # Carpeta donde se guardarán los archivos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # Tipos de archivos permitidos

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sicacenter'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(extension):
    return str(uuid.uuid4()) + '.' + extension

# Inicializar la conexión MySQL
mysql = MySQL(app)
bcrypt = Bcrypt(app)

# Definir la ruta para la página principal
@app.route('/',methods=('GET',))
def home():

    cur = mysql.connection.cursor()
    cur.execute("SELECT titulo FROM texto_principal WHERE id=1")
    titulo=cur.fetchall()
    titulo=titulo[0][0]
    titulo=str(titulo)

    if len(titulo)>0:
        ifTitulo=True
    else:
        ifTitulo=False


    cur = mysql.connection.cursor()
    cur.execute("SELECT description FROM texto_principal WHERE id=1")
    description=cur.fetchall()
    description=description[0][0]
    description=str(description)

    if len(description)>0:
        ifDescription=True
    else:
        ifDescription=False

    cur = mysql.connection.cursor()
    cur.execute("SELECT imagen FROM texto_principal WHERE id=1")
    imagen=cur.fetchall()
    imagen=imagen[0][0]
    imagen=str(imagen)


    if len(imagen)>0:
        ifImagen=True
    else:
        ifImagen=False


    return render_template('principal.html',titulo=titulo,ifTitulo=ifTitulo,ifDescription=ifDescription,description=description,imagen=imagen,ifImagen=ifImagen)

@app.route('/sys', methods=('POST','GET',)) #Ruta de inicio de sesión para el administrador del sistema
def sys():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS empresa (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            contacto VARCHAR(100) NOT NULL,
            subfijo VARCHAR(100) NOT NULL
        )
        """)
        mysql.connection.commit()  # Aplicar los cambios
        cur.close()

        if "id" in session:

            return redirect(url_for('system'))


        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT COUNT(*) FROM empresa")
        mysql.connection.commit()  # Aplicar los cambios
        countUsers = cur1.fetchall()
        countUsers=countUsers[0]
        countUsers=int(countUsers[0])
        cur1.close()
        
        if countUsers==0:
            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                user VARCHAR(100) NOT NULL,
                password VARCHAR(100) NOT NULL,
                telefono VARCHAR(100),
                genero VARCHAR(100),
                nacimiento DATE,
                id_gruops_users INT NOT NULL,
                id_sedes INT NOT NULL,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """)
            mysql.connection.commit()  # Aplicar los cambios
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS texto_principal (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(30),
                description VARCHAR(180),
                imagen VARCHAR(100)
            )
            """)
            mysql.connection.commit()  # Aplicar los cambios
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO texto_principal (titulo,description,imagen) VALUES (%s,%s,%s) ",["","",""])
            mysql.connection.commit()
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS group_users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                id_horarios INT,
                p_empresa BOOLEAN NOT NULL,
                p_config_empresa BOOLEAN NOT NULL,
                p_config_asistencia BOOLEAN NOT NULL,
                p_horarios BOOLEAN NOT NULL,
                p_sedes BOOLEAN NOT NULL,
                p_admin_user BOOLEAN NOT NULL,
                p_grupos_user BOOLEAN NOT NULL,
                p_usuarios BOOLEAN NOT NULL,
                p_reportes BOOLEAN NOT NULL,
                p_asistencia BOOLEAN NOT NULL,
                p_acceso BOOLEAN NOT NULL,
                p_ventas BOOLEAN NOT NULL,
                p_config_campanas BOOLEAN NOT NULL,
                p_campanas BOOLEAN NOT NULL,
                p_pestanas BOOLEAN NOT NULL,
                p_estados BOOLEAN NOT NULL,
                p_bloques BOOLEAN NOT NULL,
                p_campos BOOLEAN NOT NULL,
                p_reportes_ventas BOOLEAN NOT NULL,
                p_reportes1 BOOLEAN NOT NULL,
                p_reportes2 BOOLEAN NOT NULL

            )
            """)
            mysql.connection.commit()  # Aplicar los cambios
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS pestanas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                orden INT NOT NULL,
                id_campana INT NOT NULL
            )
            """)
            mysql.connection.commit()  # Aplicar los cambios
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS bloques (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                orden INT NOT NULL,
                id_campana INT NOT NULL
            )
            """)
            mysql.connection.commit()  # Aplicar los cambios
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS estados (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                color VARCHAR(100) NOT NULL,
                id_pestana INT NOT NULL,
                orden INT NOT NULL,
                id_usado INT NOT NULL
            )
            """)
            mysql.connection.commit()
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS estado_cambiar_estado (
                id_estado1 INT NOT NULL,
                id_estado2 INT NOT NULL
            )
            """)
            mysql.connection.commit()
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS permisos_grupos_estados (
                id_estado INT NOT NULL,
                id_group_user INT NOT NULL,
                type INT NOT NULL
            )
            """)
            mysql.connection.commit()
            cur.close()




            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS campanas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                id_sedes INT NOT NULL 
            )
            """)
            mysql.connection.commit()
            cur.close()



            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS sedes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                address VARCHAR(100) NOT NULL
            )
            """)
            mysql.connection.commit()  # Aplicar los cambios
            cur.close()



            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS actividad (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_user INT NOT NULL,
                type VARCHAR(100) NOT NULL,
                fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                ip VARCHAR(100) NOT NULL
            )
            """)
            mysql.connection.commit()  # Aplicar los cambios
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS horarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                tolerancia INT NOT NULL,
                lunesE TIME NOT NULL,
                lunesS TIME NOT NULL,
                martesE TIME NOT NULL,
                martesS TIME NOT NULL,
                miercolesE TIME NOT NULL,
                miercolesS TIME NOT NULL,
                juevesE TIME NOT NULL,
                juevesS TIME NOT NULL,
                viernesE TIME NOT NULL,
                viernesS TIME NOT NULL,
                sabadoE TIME NOT NULL,
                sabadoS TIME NOT NULL,
                domingoE TIME NOT NULL,
                domingoS TIME NOT NULL
            )
            """)
            mysql.connection.commit()  # Aplicar los cambios
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS recordatorios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cliente VARCHAR(100) NOT NULL,
                dni VARCHAR(100) NOT NULL,
                celular VARCHAR(100) NOT NULL,
                fecha TIMESTAMP NOT NULL
            )
            """)
            mysql.connection.commit()
            cur.close()



            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS campos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                id_bloque INT NOT NULL,
                orden INT NOT NULL,
                type INT NOT NULL,
                obligatory BOOLEAN NOT NULL,
                depende INT,
                ancho VARCHAR(100) NOT NULL,
                valores TEXT
            )
            """)
            mysql.connection.commit()  # Aplicar los cambios
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS estados_campos (
                id_estado INT NOT NULL,
                id_campo INT NOT NULL
            )
            """)
            mysql.connection.commit()  # Aplicar los cambios
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS permisos_grupos_campos (
                id_campo INT NOT NULL,
                id_grupo INT NOT NULL,
                type INT NOT NULL
            )
            """)
            mysql.connection.commit() # 1:pueden editar, 2:pueden ver
            cur.close()



            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                edicion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                id_supervisor INT NOT NULL,
                id_agente INT NOT NULL,
                estado INT NOT NULL
            )
            """)
            mysql.connection.commit()  # Aplicar los cambios
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS content_campo (
                id_campo INT NOT NULL,
                id_venta INT NOT NULL,
                content TEXT NOT NULL
            )
            """)
            mysql.connection.commit()
            cur.close()


            return redirect(url_for('register'))
        elif countUsers==1:
            return render_template('sys.html')

    elif request.method == 'POST':

        user = request.form['user']
        password = request.form['password']
        print (user)
        print (password)
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM users WHERE user = %s", [user])
        password_hasheada = cur.fetchall()
        print (password_hasheada)
        
        cur.close()
        
        if password_hasheada:
            password_hasheada=password_hasheada[0][0]
            if bcrypt.check_password_hash(password_hasheada, password):
            # Iniciar sesión, guardar el id de usuario en la sesión
                cur = mysql.connection.cursor()
                cur.execute("SELECT id FROM users WHERE user = %s", [user])
                id_user = cur.fetchall()
                id_user = id_user[0][0]
                id_user = int(id_user)

                print("id de usuario")
                print(id_user)

                cur = mysql.connection.cursor()
                cur.execute("SELECT id_gruops_users FROM users WHERE id=%s",[id_user])
                id_gruops_users = cur.fetchall()
                id_gruops_users = id_gruops_users[0][0]
                id_gruops_users = int(id_gruops_users)

                cur = mysql.connection.cursor()
                cur.execute("SELECT id_horarios FROM group_users WHERE id=%s",[id_gruops_users])
                id_horarios = cur.fetchall()
                id_horarios = id_horarios[0][0]
                id_horarios = int(id_horarios)

                if (id_horarios==0):
                    hora_permiso = True
                else:
                    now = datetime.now()
                    dia = now.weekday()
                    dia = int(dia)
                    if (dia==0):
                        #Lunes

                        cur = mysql.connection.cursor()
                        cur.execute("SELECT lunesE,lunesS,tolerancia FROM horarios WHERE id=%s",[id_horarios])
                        datos_es = cur.fetchall()
                        entrada = str(datos_es[0][0])
                        salida = str(datos_es[0][1])
                        tolerancia = datos_es[0][2]
                        entrada = datetime.strptime(entrada, "%X").time()
                        salida = datetime.strptime(salida, "%X").time()
                        now = datetime.now().time()
                        
                        tolerancia = int(tolerancia)
                        #entrada_tolerancia = entrada + timedelta(hours=tolerancia)

                        if now > entrada and now < salida:
                            hora_permiso = True
                        else:
                            hora_permiso = False




                    elif (dia==1):
                        #Martes
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT martesE,martesS,tolerancia FROM horarios WHERE id=%s",[id_horarios])
                        datos_es = cur.fetchall()
                        entrada = str(datos_es[0][0])
                        salida = str(datos_es[0][1])
                        tolerancia = datos_es[0][2]
                        entrada = datetime.strptime(entrada, "%X").time()
                        salida = datetime.strptime(salida, "%X").time()
                        now = datetime.now().time()
                        
                        tolerancia = int(tolerancia)
                        #entrada_tolerancia = entrada + timedelta(hours=tolerancia)

                        if now > entrada and now < salida:
                            hora_permiso = True
                        else:
                            hora_permiso = False

                    elif (dia==2):
                        #Miercoles
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT miercolesE,miercolesS,tolerancia FROM horarios WHERE id=%s",[id_horarios])
                        datos_es = cur.fetchall()
                        entrada = str(datos_es[0][0])
                        salida = str(datos_es[0][1])
                        tolerancia = datos_es[0][2]
                        entrada = datetime.strptime(entrada, "%X").time()
                        salida = datetime.strptime(salida, "%X").time()
                        now = datetime.now().time()
                        
                        tolerancia = int(tolerancia)
                        #entrada_tolerancia = entrada + timedelta(hours=tolerancia)

                        if now > entrada and now < salida:
                            hora_permiso = True
                        else:
                            hora_permiso = False

                    elif (dia==3):
                        #Jueves
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT juevesE,juevesS,tolerancia FROM horarios WHERE id=%s",[id_horarios])
                        datos_es = cur.fetchall()
                        entrada = str(datos_es[0][0])
                        salida = str(datos_es[0][1])
                        tolerancia = datos_es[0][2]
                        entrada = datetime.strptime(entrada, "%X").time()
                        salida = datetime.strptime(salida, "%X").time()
                        now = datetime.now().time()
                        
                        tolerancia = int(tolerancia)
                        #entrada_tolerancia = entrada + timedelta(hours=tolerancia)

                        if now > entrada and now < salida:
                            hora_permiso = True
                        else:
                            hora_permiso = False

                    elif (dia==4):
                        #Viernes
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT viernesE,viernesS,tolerancia FROM horarios WHERE id=%s",[id_horarios])
                        datos_es = cur.fetchall()
                        entrada = str(datos_es[0][0])
                        salida = str(datos_es[0][1])
                        tolerancia = datos_es[0][2]
                        entrada = datetime.strptime(entrada, "%X").time()
                        salida = datetime.strptime(salida, "%X").time()
                        now = datetime.now().time()
                        
                        tolerancia = int(tolerancia)
                        #entrada_tolerancia = entrada + timedelta(hours=tolerancia)

                        if now > entrada and now < salida:
                            hora_permiso = True
                        else:
                            hora_permiso = False

                    elif (dia==5):
                        #Sabado
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT sabadoE,sabadoS,tolerancia FROM horarios WHERE id=%s",[id_horarios])
                        datos_es = cur.fetchall()
                        entrada = str(datos_es[0][0])
                        salida = str(datos_es[0][1])
                        tolerancia = datos_es[0][2]
                        entrada = datetime.strptime(entrada, "%X").time()
                        salida = datetime.strptime(salida, "%X").time()
                        now = datetime.now().time()
                        
                        tolerancia = int(tolerancia)
                        #entrada_tolerancia = entrada + timedelta(hours=tolerancia)

                        if now > entrada and now < salida:
                            hora_permiso = True
                        else:
                            hora_permiso = False

                    elif (dia==6):
                        #Domingo
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT domingoE,domingoS,tolerancia FROM horarios WHERE id=%s",[id_horarios])
                        datos_es = cur.fetchall()
                        entrada = str(datos_es[0][0])
                        salida = str(datos_es[0][1])
                        tolerancia = datos_es[0][2]
                        entrada = datetime.strptime(entrada, "%X").time()
                        salida = datetime.strptime(salida, "%X").time()
                        now = datetime.now().time()
                        
                        tolerancia = int(tolerancia)
                        #entrada_tolerancia = entrada + timedelta(hours=tolerancia)

                        if now > entrada and now < salida:
                            hora_permiso = True
                        else:
                            hora_permiso = False

                if (hora_permiso):

                    session['id'] = id_user
                    type_actividad="Login"

                    ip_actividad = request.environ['REMOTE_ADDR']
                    ip_actividad = str(ip_actividad)

                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO actividad (id_user,type,ip) VALUES (%s,%s,%s)", (id_user,type_actividad,ip_actividad))
                    mysql.connection.commit()

                    return redirect(url_for('system'))

                else:

                    return render_template('sys.html',message="Horario no permitido")

                #return "login completado"
            else:
                return render_template('sys.html',message="Contraseña incorrecta")
        return render_template('sys.html',message="Email incorrecto")


@app.route('/register',methods=('POST','GET',))
def register():
    if request.method == 'POST':

        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT COUNT(*) FROM empresa")
        mysql.connection.commit()  # Aplicar los cambios
        countUsers = cur1.fetchall()
        countUsers=countUsers[0]
        countUsers=int(countUsers[0])
        cur1.close()
        
        if countUsers==0:
            nombre_empresa = request.form['nombre-empresa']
            contacto=request.form['contacto']
            subfijo=request.form['subfijo']
            nombre = request.form['nombre']
            user = request.form['user'] 
            password = request.form['password']
            nombre_grupo = request.form['nombre-grupo']
            user=user+subfijo
            id_gruop_users=int(1)
            id_sedes=int(0)
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO empresa (nombre,contacto, subfijo) VALUES (%s,%s,%s)", (nombre_empresa,contacto, subfijo))
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (nombre,user,password,id_gruops_users,id_sedes) VALUES (%s,%s,%s,%s,%s)", (nombre,user, hashed_password,id_gruop_users,id_sedes))
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO group_users (nombre,id_horarios,p_empresa,p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso,p_ventas,p_config_campanas,p_campanas,p_pestanas,p_estados,p_bloques,p_campos,p_reportes_ventas,p_reportes1,p_reportes2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (nombre_grupo,0,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('sys'))
        elif countUsers==1:
            return redirect(url_for('sys'))

    elif request.method == 'GET':

        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT COUNT(*) FROM empresa")
        mysql.connection.commit()  # Aplicar los cambios
        countUsers = cur1.fetchall()
        countUsers=countUsers[0]
        countUsers=int(countUsers[0])
        cur1.close()
        
        if countUsers==0:
            return render_template("sign-up.html")
        elif countUsers==1:
            return redirect(url_for('sys'))

@app.route('/logout',methods=('GET',))
def logout():
    if request.method == 'GET':
        if "id" in session:
            id_user = session['id'] 
            type_actividad="Logout"
            ip_actividad = request.environ['REMOTE_ADDR']
            ip_actividad = str(ip_actividad)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO actividad (id_user,type,ip) VALUES (%s,%s,%s)", (id_user,type_actividad,ip_actividad))
            mysql.connection.commit()
            session.pop('id', None)
            return redirect(url_for('sys'))
        return redirect(url_for('sys'))

@app.route('/system',methods=('GET',))
def system():
    if request.method == 'GET':
        if "id" in session:

            id_sesion=session['id']

            print("el id de la sesion es: ", id_sesion)

            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()
            
            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            if id_gruops_users==0:

                return render_template('system.html',username=id_user)
            
            elif id_gruops_users!=0:

                cur = mysql.connection.cursor()
                cur.execute("SELECT p_empresa,p_ventas FROM group_users WHERE id = %s", [id_gruops_users])
                p_empresa_ventas = cur.fetchall()
                p_empresa_ventas = p_empresa_ventas[0]
                p_empresa = p_empresa_ventas[0]
                p_ventas = p_empresa_ventas[1]
                cur.close()

                
                if p_empresa==True and p_ventas==False:
                    return redirect(url_for('empresa'))
                elif p_empresa==False and p_ventas==True:
                    return redirect(url_for('ventas'))
                elif p_empresa==True and p_ventas==True:
                    return render_template('system.html',username=id_user)
                else:
                    return redirect(url_for('logout'))


        return redirect(url_for('sys'))
    

@app.route('/empresa',methods=('GET',))
def empresa():
    if request.method == 'GET':
        if "id" in session:

            id_sesion=session['id']

            print("el id de la sesion es: ", id_sesion)

            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()
            




            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas FROM group_users WHERE id = %s", [id_gruops_users])
            p_empresa = cur.fetchall()
            p_ventas = p_empresa[0][1]
            p_empresa = p_empresa[0][0]
            cur.close()

            if p_empresa==True :

                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_empresa = p_datos[0][0]
                p_config_asistencia = p_datos[0][1]
                p_horarios = p_datos[0][2]
                p_sedes = p_datos[0][3]
                p_admin_user = p_datos[0][4]
                p_grupos_user = p_datos[0][5]
                p_usuarios = p_datos[0][6]
                p_reportes = p_datos[0][7]
                p_asistencia = p_datos[0][8]
                p_acceso = p_datos[0][9]
                
                
                cur.close()

                cur = mysql.connection.cursor()
                #cur.execute("SELECT * FROM actividad")
                cur.execute("SELECT actividad.id, users.nombre, actividad.type, actividad.fecha, actividad.ip FROM actividad INNER JOIN users ON actividad.id_user=users.id ORDER BY id DESC")
                actividades = cur.fetchall()
                
                
                cur.close()


                ahora=datetime.now()


                print(ahora)




                return render_template('index.html',ahora=ahora,actividades=actividades,username=id_user,config_empresa=p_config_empresa,config_asistencia=p_config_asistencia,horarios=p_horarios,sedes=p_sedes,admin_usuarios=p_admin_user,grupos=p_grupos_user,usuarios=p_usuarios,reportes=p_reportes,asistencia=p_asistencia,accesos=p_acceso)
            elif p_empresa==False and p_ventas==True :
                return redirect(url_for('sys'))
            elif p_empresa==False and p_ventas==False :
                return redirect(url_for('logout'))



            

            
            

        return redirect(url_for('sys'))


@app.route('/config-general',methods=('GET','POST',))
def config_general():
    if request.method == 'GET':

        if "id" in session:

            id_sesion=session['id']           

            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_empresa FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config = p_data[0][2]
            cur.close()

            

            if p_empresa==True and p_config==True :

                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_empresa = p_datos[0][0]
                p_config_asistencia = p_datos[0][1]
                p_horarios = p_datos[0][2]
                p_sedes = p_datos[0][3]
                p_admin_user = p_datos[0][4]
                p_grupos_user = p_datos[0][5]
                p_usuarios = p_datos[0][6]
                p_reportes = p_datos[0][7]
                p_asistencia = p_datos[0][8]
                p_acceso = p_datos[0][9]
                
                
                cur.close()


                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM empresa WHERE id = %s", [1])

                info_empresa = cur.fetchall()
                info_empresa = info_empresa[0]
                cur.close()



                cur = mysql.connection.cursor()
                cur.execute("SELECT titulo,description,imagen FROM texto_principal WHERE id = %s", [1])
                principal = cur.fetchall()
                principal = principal[0]
                cur.close()



                return render_template('config-general.html',principal=principal,info_empresa=info_empresa,username=id_user,config_empresa=p_config_empresa,config_asistencia=p_config_asistencia,horarios=p_horarios,sedes=p_sedes,admin_usuarios=p_admin_user,grupos=p_grupos_user,usuarios=p_usuarios,reportes=p_reportes,asistencia=p_asistencia,accesos=p_acceso)


            elif p_empresa==True and p_config==False :


                return redirect(url_for('empresa'))

            elif p_empresa==False and p_ventas==True :
                return redirect(url_for('sys'))
            elif p_empresa==False and p_ventas==False :
                return redirect(url_for('logout'))







        return redirect(url_for('sys'))



    elif request.method == 'POST':


        if "id" in session:

            id_sesion=session['id']

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_empresa FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config = p_data[0][2]
            cur.close()

            if p_empresa==True and p_config==True :

                nombre_empresa = request.form['empresa']
                contacto_empresa = request.form['contacto']
                subfijo_empresa = request.form['subfijo']

                print(nombre_empresa)
                print(contacto_empresa)
                print(subfijo_empresa)

                cur = mysql.connection.cursor()
                cur.execute("UPDATE empresa SET nombre=%s,contacto=%s,subfijo=%s WHERE id=%s ", (nombre_empresa,contacto_empresa, subfijo_empresa,1))
                mysql.connection.commit()
                cur.close()


                titulo = request.form['titulo']
                titulo = str(titulo)
                description = request.form['description']
                description = str(description)

                cur = mysql.connection.cursor()
                cur.execute("UPDATE texto_principal SET titulo=%s,description=%s WHERE id=1 ", (titulo,description))
                mysql.connection.commit()
                cur.close()

                print(request.files['imagen'])

                if 'imagen' not in request.files:
                    return redirect(url_for('config_general'))

                imagen = request.files['imagen']

                if imagen.filename == '':
                    return redirect(url_for('config_general'))

                if imagen and allowed_file(imagen.filename):


                    cur = mysql.connection.cursor()
                    cur.execute("SELECT imagen FROM texto_principal WHERE id = %s", [1])
                    image_name = cur.fetchall()


                    if image_name and len(image_name[0][0])>0:
                        profile_image = image_name[0][0]  # Suponiendo que la columna 'profile_image' es el primer campo
                        
                        if profile_image:
                            image_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_image)
                    
                            if os.path.exists(image_path):
                                os.remove(image_path) 





                    extension = imagen.filename.rsplit('.', 1)[1].lower()
                    filename = generate_unique_filename(extension)  # Asegura el nombre del archivo
                    namestr=str(filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)                    
                    
                    
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE texto_principal SET imagen=%s WHERE id=%s ", [namestr,1])
                    mysql.connection.commit()
                    cur.close()
                    
                    imagen.save(filepath)







                return redirect(url_for('config_general'))


            elif p_empresa==True and p_config==False :


                return redirect(url_for('empresa'))

            elif p_empresa==False and p_ventas==True :
                return redirect(url_for('sys'))
            elif p_empresa==False and p_ventas==False :
                return redirect(url_for('logout'))




             



        return redirect(url_for('sys'))
























@app.route('/change-password',methods=('GET','POST',))
def change_password():
    if request.method == 'GET':
        if "id" in session:

            id_sesion=session['id']

            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()



            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_empresa FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config = p_data[0][2]
            cur.close()


            if p_empresa==True:

                
                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_empresa = p_datos[0][0]
                p_config_asistencia = p_datos[0][1]
                p_horarios = p_datos[0][2]
                p_sedes = p_datos[0][3]
                p_admin_user = p_datos[0][4]
                p_grupos_user = p_datos[0][5]
                p_usuarios = p_datos[0][6]
                p_reportes = p_datos[0][7]
                p_asistencia = p_datos[0][8]
                p_acceso = p_datos[0][9]
                
                
                cur.close()






                return render_template('change-password.html',username=id_user,config_empresa=p_config_empresa,config_asistencia=p_config_asistencia,horarios=p_horarios,sedes=p_sedes,admin_usuarios=p_admin_user,grupos=p_grupos_user,usuarios=p_usuarios,reportes=p_reportes,asistencia=p_asistencia,accesos=p_acceso)


            elif p_empresa==False and p_ventas==True :
                return redirect(url_for('sys'))
            elif p_empresa==False and p_ventas==False :
                return redirect(url_for('logout'))

        return redirect(url_for('sys'))



    if request.method == 'POST':

        if "id" in session:

            id_sesion=session['id']

            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()



            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_empresa FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config = p_data[0][2]
            cur.close()



            if p_empresa==True or p_ventas==True:





                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_empresa = p_datos[0][0]
                p_config_asistencia = p_datos[0][1]
                p_horarios = p_datos[0][2]
                p_sedes = p_datos[0][3]
                p_admin_user = p_datos[0][4]
                p_grupos_user = p_datos[0][5]
                p_usuarios = p_datos[0][6]
                p_reportes = p_datos[0][7]
                p_asistencia = p_datos[0][8]
                p_acceso = p_datos[0][9]
                
                cur.close()




                old_password=request.form['old-password']
                new_password=request.form['new-password']



                cur = mysql.connection.cursor()
                cur.execute("SELECT password FROM users WHERE id = %s", [id_sesion])
                password_hasheada = cur.fetchall()
                password_hasheada=password_hasheada[0][0]
                print (password_hasheada)
                cur.close()




                if bcrypt.check_password_hash(password_hasheada, old_password):



                    new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE users SET password = %s WHERE id = %s", [new_password,id_sesion])
                    mysql.connection.commit()
                    cur.close()


          


                    session.pop('id', None)

                    return render_template('sys.html',message="Password cambiada correctamente.")
                
                session.pop('id', None)
                
                return render_template('sys.html',message="Error al cambiar Password, intente nuevamente.")

            elif p_empresa==False and p_ventas==False :
                return redirect(url_for('logout'))
        return redirect(url_for('sys'))


@app.route('/horarios',methods=('GET','POST',))

def horarios():

    if request.method == "GET":
        
        if "id" in session:

            id_sesion=session['id']


            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_asistencia,p_horarios FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_asistencia = p_data[0][2]
            p_horarios = p_data[0][3]
            cur.close()



            if p_empresa==True and p_asistencia==True and p_horarios==True:




                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM horarios")
                horarios = cur.fetchall()
                horarios = horarios
                cur.close()



                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_empresa = p_datos[0][0]
                p_config_asistencia = p_datos[0][1]
                p_horarios = p_datos[0][2]
                p_sedes = p_datos[0][3]
                p_admin_user = p_datos[0][4]
                p_grupos_user = p_datos[0][5]
                p_usuarios = p_datos[0][6]
                p_reportes = p_datos[0][7]
                p_asistencia = p_datos[0][8]
                p_acceso = p_datos[0][9]
                
                
                cur.close()











                return render_template('horarios.html',get_horarios=horarios,username=id_user,config_empresa=p_config_empresa,config_asistencia=p_config_asistencia,horarios=p_horarios,sedes=p_sedes,admin_usuarios=p_admin_user,grupos=p_grupos_user,usuarios=p_usuarios,reportes=p_reportes,asistencia=p_asistencia,accesos=p_acceso)

            elif p_empresa==True and p_asistencia==False and p_horarios==False :


                return redirect(url_for('empresa'))

            elif p_empresa==True and p_asistencia==True and p_horarios==False :


                return redirect(url_for('empresa'))

            elif p_empresa==False and p_ventas==True :
                return redirect(url_for('sys'))
            elif p_empresa==False and p_ventas==False :
                return redirect(url_for('logout'))

                
                
        return redirect(url_for('sys'))       

        



    elif request.method == "POST":

        if "id" in session:

            id_sesion=session['id']


            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_asistencia,p_horarios FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_asistencia = p_data[0][2]
            p_horarios = p_data[0][3]
            cur.close()

            nombre = request.form['nombre']
            tolerancia = request.form['tolerancia']

            lunesE = request.form['lunesE']
            lunesS = request.form['lunesS']

            martesE = request.form['martesE']
            martesS = request.form['martesS']
            
            miercolesE = request.form['miercolesE']
            miercolesS = request.form['miercolesS']
            
            juevesE = request.form['juevesE']
            juevesS = request.form['juevesS']
            
            viernesE = request.form['viernesE']
            viernesS = request.form['viernesS']

            sabadoE = request.form['sabadoE']
            sabadoS = request.form['sabadoS']

            domingoE = request.form['domingoE']
            domingoS = request.form['domingoS']

            print(nombre)
            print(tolerancia)
            print(lunesE)
            print(lunesS)

            print(martesE)
            print(martesS)

            print(miercolesE)
            print(miercolesS)

            print(juevesE)
            print(juevesS)

            print(viernesE)
            print(viernesS)

            print(sabadoE)
            print(sabadoS)

            print(domingoE)
            print(domingoS)

            
            if p_empresa==True and p_asistencia==True and p_horarios==True:


                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO horarios (nombre,tolerancia,lunesE,lunesS,martesE,martesS,miercolesE,miercolesS,juevesE,juevesS,viernesE,viernesS,sabadoE,sabadoS,domingoE,domingoS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (nombre,tolerancia,lunesE,lunesS,martesE,martesS,miercolesE,miercolesS,juevesE,juevesS,viernesE,viernesS,sabadoE,sabadoS,domingoE,domingoS))
                mysql.connection.commit()

                return redirect(url_for('horarios'))


            elif p_empresa==True and p_asistencia==False and p_horarios==False:


                return redirect(url_for('empresa'))

            elif p_empresa==True and p_asistencia==True and p_horarios==False:


                return redirect(url_for('empresa'))

            elif p_empresa==False and p_ventas==True :
                return redirect(url_for('sys'))
            elif p_empresa==False and p_ventas==False :
                return redirect(url_for('logout'))
        

        return redirect(url_for('sys')) 


@app.route('/horarios/delete/<int:idH>',methods=('GET',))
def eliminarHorario(idH):
    idH=int(idH)

    if "id" in session:

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_config_asistencia,p_horarios FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_asistencia = p_data[0][2]
        p_horarios = p_data[0][3]
        cur.close()

        if p_empresa==True and p_asistencia==True and p_horarios==True:


                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM horarios WHERE id = %s ", [idH])
                mysql.connection.commit()

                return redirect(url_for('horarios'))


        elif p_empresa==True and p_asistencia==False and p_horarios==False:


            return redirect(url_for('empresa'))

        elif p_empresa==True and p_asistencia==True and p_horarios==False:


            return redirect(url_for('empresa'))

        elif p_empresa==False and p_ventas==True :
            return redirect(url_for('sys'))
        elif p_empresa==False and p_ventas==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))


@app.route('/horarios/edit/<int:idH>',methods=('POST',))
def editHorario(idH):
    idH=int(idH)

    if "id" in session:

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_config_asistencia,p_horarios FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_asistencia = p_data[0][2]
        p_horarios = p_data[0][3]
        cur.close()

        if p_empresa==True and p_asistencia==True and p_horarios==True:


                

            nombre = request.form['nombre']
            tolerancia = request.form['tolerancia']

            lunesE = request.form['lunesE']
            lunesS = request.form['lunesS']

            martesE = request.form['martesE']
            martesS = request.form['martesS']
            
            miercolesE = request.form['miercolesE']
            miercolesS = request.form['miercolesS']
            
            juevesE = request.form['juevesE']
            juevesS = request.form['juevesS']
            
            viernesE = request.form['viernesE']
            viernesS = request.form['viernesS']

            sabadoE = request.form['sabadoE']
            sabadoS = request.form['sabadoS']

            domingoE = request.form['domingoE']
            domingoS = request.form['domingoS']

            print(nombre)
            print(tolerancia)
            print(lunesE)
            print(lunesS)

            print(martesE)
            print(martesS)

            print(miercolesE)
            print(miercolesS)

            print(juevesE)
            print(juevesS)

            print(viernesE)
            print(viernesS)

            print(sabadoE)
            print(sabadoS)

            print(domingoE)
            print(domingoS)



            cur = mysql.connection.cursor()
            cur.execute("UPDATE horarios SET nombre=%s,tolerancia=%s,lunesE=%s,lunesS=%s,martesE=%s,martesS=%s,miercolesE=%s,miercolesS=%s,juevesE=%s,juevesS=%s,viernesE=%s,viernesS=%s,sabadoE=%s,sabadoS=%s,domingoE=%s,domingoS=%s WHERE id=%s ", (nombre,tolerancia,lunesE,lunesS,martesE,martesS,miercolesE,miercolesS,juevesE,juevesS,viernesE,viernesS,sabadoE,sabadoS,domingoE,domingoS,idH))
            mysql.connection.commit()
            cur.close()

            





            return redirect(url_for('horarios'))


        elif p_empresa==True and p_asistencia==False and p_horarios==False:


            return redirect(url_for('empresa'))

        elif p_empresa==True and p_asistencia==True and p_horarios==False:


            return redirect(url_for('empresa'))

        elif p_empresa==False and p_ventas==True:
            return redirect(url_for('sys'))
        elif p_empresa==False and p_ventas==False:
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))




@app.route('/sedes',methods=('GET','POST',))

def sedes():

    if request.method == "GET":
        
        if "id" in session:

            id_sesion=session['id']


            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_asistencia,p_sedes FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_asistencia = p_data[0][2]
            p_sedes = p_data[0][3]
            cur.close()



            if p_empresa==True and p_asistencia==True and p_sedes==True:




                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM sedes")
                get_sedes = cur.fetchall()
                cur.close()



                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_empresa = p_datos[0][0]
                p_config_asistencia = p_datos[0][1]
                p_horarios = p_datos[0][2]
                p_sedes = p_datos[0][3]
                p_admin_user = p_datos[0][4]
                p_grupos_user = p_datos[0][5]
                p_usuarios = p_datos[0][6]
                p_reportes = p_datos[0][7]
                p_asistencia = p_datos[0][8]
                p_acceso = p_datos[0][9]
                
                
                cur.close()














                return render_template('sedes.html',get_sedes=get_sedes,username=id_user,config_empresa=p_config_empresa,config_asistencia=p_config_asistencia,horarios=p_horarios,sedes=p_sedes,admin_usuarios=p_admin_user,grupos=p_grupos_user,usuarios=p_usuarios,reportes=p_reportes,asistencia=p_asistencia,accesos=p_acceso)

            elif p_empresa==True and p_asistencia==False and p_sedes==False :


                return redirect(url_for('empresa'))

            elif p_empresa==True and p_asistencia==True and p_sedes==False :


                return redirect(url_for('empresa'))

            elif p_empresa==False and p_ventas==True :
                return redirect(url_for('sys'))
            elif p_empresa==False and p_ventas==False :
                return redirect(url_for('logout'))

                
                
        return redirect(url_for('sys'))       

        



    elif request.method == "POST":

        if "id" in session:

            id_sesion=session['id']


            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_asistencia,p_sedes FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_asistencia = p_data[0][2]
            p_sedes = p_data[0][3]
            cur.close()

            nombre = request.form['nombre']
            address = request.form['address']


            print(nombre)
            print(address)
            

            
            if p_empresa==True and p_asistencia==True and p_sedes==True:


                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO sedes (nombre,address) VALUES (%s,%s)", (nombre,address))
                mysql.connection.commit()

                return redirect(url_for('sedes'))


            elif p_empresa==True and p_asistencia==False and p_sedes==False:


                return redirect(url_for('empresa'))

            elif p_empresa==True and p_asistencia==True and p_sedes==False:


                return redirect(url_for('empresa'))

            elif p_empresa==False and p_ventas==True :
                return redirect(url_for('sys'))
            elif p_empresa==False and p_ventas==False :
                return redirect(url_for('logout'))
        

        return redirect(url_for('sys')) 



@app.route('/sedes/delete/<int:idH>',methods=('GET',))
def eliminarSedes(idH):
    idH=int(idH)

    if "id" in session:

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_config_asistencia,p_sedes FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_asistencia = p_data[0][2]
        p_sedes = p_data[0][3]
        cur.close()

        if p_empresa==True and p_asistencia==True and p_sedes==True:


                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM sedes WHERE id = %s ", [idH])
                mysql.connection.commit()

                return redirect(url_for('sedes'))


        elif p_empresa==True and p_asistencia==False and p_sedes==False:


            return redirect(url_for('empresa'))

        elif p_empresa==True and p_asistencia==True and p_sedes==False:


            return redirect(url_for('empresa'))

        elif p_empresa==False and p_ventas==True :
            return redirect(url_for('sys'))
        elif p_empresa==False and p_ventas==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))


@app.route('/sedes/edit/<int:idH>',methods=('POST',))
def editSede(idH):
    idH=int(idH)

    if "id" in session:

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_config_asistencia,p_sedes FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_asistencia = p_data[0][2]
        p_sedes = p_data[0][3]
        cur.close()

        if p_empresa==True and p_asistencia==True and p_sedes==True: 

            nombre = request.form['nombre']
            address = request.form['address']

            print(nombre)
            print(address)
            
            cur = mysql.connection.cursor()
            cur.execute("UPDATE sedes SET nombre=%s,address=%s WHERE id=%s ", (nombre,address,idH))
            mysql.connection.commit()
            cur.close()
            
            return redirect(url_for('sedes'))


        elif p_empresa==True and p_asistencia==False and p_sedes==False:


            return redirect(url_for('empresa'))

        elif p_empresa==True and p_asistencia==True and p_sedes==False:


            return redirect(url_for('empresa'))

        elif p_empresa==False and p_ventas==True :
            return redirect(url_for('sys'))
        elif p_empresa==False and p_ventas==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))












@app.route('/grupos-usuarios',methods=('GET','POST',))

def grupos_usuarios():

    if request.method == "GET":
        
        if "id" in session:

            id_sesion=session['id']


            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_admin_user,p_grupos_user FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_admin_user = p_data[0][2]
            p_grupos_user = p_data[0][3]
            cur.close()



            if p_empresa==True and p_admin_user==True and p_grupos_user==True:



                cur = mysql.connection.cursor()
                cur.execute("SELECT id,nombre,id_horarios,p_empresa,p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso,p_ventas,p_config_campanas,p_campanas,p_pestanas,p_estados,p_bloques,p_campos,p_reportes_ventas,p_reportes1,p_reportes2 FROM group_users")
                get_grupos = cur.fetchall()
                get_grupos_list=list()
                cur.close()

                i=0
                for x in get_grupos:
                    get_grupos_list_temp=list(x)
                    
                    get_grupos_list.append(get_grupos_list_temp)
                    id_horario_temp=x[2]
                    id_horario_temp=int(id_horario_temp)
                    
                    if id_horario_temp==0:
                        get_grupos_list[i][2]=""
                    else:
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT nombre FROM horarios WHERE id = %s",[id_horario_temp])
                        nombre_temp=cur.fetchall()
                        nombre_temp=nombre_temp[0][0]
                        get_grupos_list[i][2]=nombre_temp
                    
                    i=i+1

                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM horarios")
                get_horarios = cur.fetchall()
                cur.close()

                

                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_empresa = p_datos[0][0]
                p_config_asistencia = p_datos[0][1]
                p_horarios = p_datos[0][2]
                p_sedes = p_datos[0][3]
                p_admin_user = p_datos[0][4]
                p_grupos_user = p_datos[0][5]
                p_usuarios = p_datos[0][6]
                p_reportes = p_datos[0][7]
                p_asistencia = p_datos[0][8]
                p_acceso = p_datos[0][9]
                
                
                cur.close()


                return render_template('grupos-usuarios.html',get_horarios=get_horarios,get_grupos=get_grupos_list,username=id_user,config_empresa=p_config_empresa,config_asistencia=p_config_asistencia,horarios=p_horarios,sedes=p_sedes,admin_usuarios=p_admin_user,grupos=p_grupos_user,usuarios=p_usuarios,reportes=p_reportes,asistencia=p_asistencia,accesos=p_acceso)

            elif p_empresa==True and p_admin_user==False and p_grupos_user==False :


                return redirect(url_for('empresa'))

            elif p_empresa==True and p_admin_user==True and p_grupos_user==False :


                return redirect(url_for('empresa'))

            elif p_empresa==False and p_ventas==True :
                return redirect(url_for('sys'))
            elif p_empresa==False and p_ventas==False :
                return redirect(url_for('logout'))

                
                
        return redirect(url_for('sys'))       


    elif request.method == "POST":

        if "id" in session:

            id_sesion=session['id']

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_admin_user,p_grupos_user FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_admin_user = p_data[0][2]
            p_grupos_user = p_data[0][3]
            cur.close()

            nombre = request.form['nombre']
            horario = request.form['horario']
            horario = int(horario)

            checkboxs = request.form.getlist('checkbox')


            print(nombre)
            print(horario)
            print(checkboxs)
            

            
            if p_empresa==True and p_admin_user==True and p_grupos_user==True:
                
                permisos=[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]

                for checkbox in checkboxs:
                    j=int(checkbox)
                    j=j-1
                    print(j)
                    permisos[j]=True

                print(permisos)

                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO group_users (nombre,id_horarios,p_empresa,p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso,p_ventas,p_config_campanas,p_campanas,p_pestanas,p_estados,p_bloques,p_campos,p_reportes_ventas,p_reportes1,p_reportes2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (nombre,horario,permisos[0],permisos[1],permisos[2],permisos[3],permisos[4],permisos[5],permisos[6],permisos[7],permisos[8],permisos[9],permisos[10],permisos[11],permisos[12],permisos[13],permisos[14],permisos[15],permisos[16],permisos[17],permisos[18],permisos[19],permisos[20]))
                mysql.connection.commit()

                return redirect(url_for('grupos_usuarios'))


            elif p_empresa==True and p_admin_user==False and p_grupos_user==False:


                return redirect(url_for('empresa'))

            elif p_empresa==True and p_admin_user==True and p_grupos_user==False:


                return redirect(url_for('empresa'))

            elif p_empresa==False and p_ventas==True :
                return redirect(url_for('sys'))
            elif p_empresa==False and p_ventas==False :
                return redirect(url_for('logout'))
        

        return redirect(url_for('sys')) 





@app.route('/grupos-usuarios/delete/<int:idH>',methods=('GET',))
def eliminarGUsuarios(idH):
    idH=int(idH)

    if "id" in session:

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_admin_user,p_grupos_user FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_admin_user = p_data[0][2]
        p_grupos_user = p_data[0][3]
        cur.close()

        if p_empresa==True and p_admin_user==True and p_grupos_user==True:


                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM group_users WHERE id = %s ", [idH])
                mysql.connection.commit()

                return redirect(url_for('grupos_usuarios'))


        elif p_empresa==True and p_admin_user==False and p_grupos_user==False:


            return redirect(url_for('empresa'))

        elif p_empresa==True and p_admin_user==True and p_grupos_user==False:


            return redirect(url_for('empresa'))

        elif p_empresa==False and p_ventas==True :
            return redirect(url_for('sys'))
        elif p_empresa==False and p_ventas==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))



@app.route('/grupos-usuarios/edit/<int:idH>',methods=('POST',))
def editGUsuarios(idH):
    idH=int(idH)

    if "id" in session:

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_admin_user,p_grupos_user FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_admin_user = p_data[0][2]
        p_grupos_user = p_data[0][3]
        cur.close()

        

        if p_empresa==True and p_admin_user==True and p_grupos_user==True: 

            nombre = request.form['nombre']
            horario = request.form['horario']
            horario = int(horario)
            checkboxs = request.form.getlist('checkbox')

            
            permisos=[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]


            for checkbox in checkboxs:
                k=int(checkbox)
                k=k-1
                print(k)
                permisos[k]=True

            print(permisos)

            
            cur = mysql.connection.cursor()
            cur.execute("UPDATE group_users SET nombre=%s,id_horarios=%s,p_empresa=%s,p_config_empresa=%s,p_config_asistencia=%s,p_horarios=%s,p_sedes=%s,p_admin_user=%s,p_grupos_user=%s,p_usuarios=%s,p_reportes=%s,p_asistencia=%s,p_acceso=%s,p_ventas=%s,p_config_campanas=%s,p_campanas=%s,p_pestanas=%s,p_estados=%s,p_bloques=%s,p_campos=%s,p_reportes_ventas=%s,p_reportes1=%s,p_reportes2=%s WHERE id=%s ", (nombre,horario,permisos[0],permisos[1],permisos[2],permisos[3],permisos[4],permisos[5],permisos[6],permisos[7],permisos[8],permisos[9],permisos[10],permisos[11],permisos[12],permisos[13],permisos[14],permisos[15],permisos[16],permisos[17],permisos[18],permisos[19],permisos[20],idH))
            mysql.connection.commit()
            cur.close()
            
            return redirect(url_for('grupos_usuarios'))


        elif p_empresa==True and p_admin_user==False and p_grupos_user==False:


            return redirect(url_for('empresa'))

        elif p_empresa==True and p_admin_user==True and p_grupos_user==False:


            return redirect(url_for('empresa'))

        elif p_empresa==False and p_ventas==True :
            return redirect(url_for('sys'))
        elif p_empresa==False and p_ventas==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))


@app.route('/usuarios',methods=('GET','POST',))

def usuarios():

    if request.method == "GET":
        
        if "id" in session:

            id_sesion=session['id']


            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_admin_user,p_usuarios FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_admin_user = p_data[0][2]
            p_usuarios = p_data[0][3]
            cur.close()



            if p_empresa==True and p_admin_user==True and p_usuarios==True:

                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_empresa = p_datos[0][0]
                p_config_asistencia = p_datos[0][1]
                p_horarios = p_datos[0][2]
                p_sedes = p_datos[0][3]
                p_admin_user = p_datos[0][4]
                p_grupos_user = p_datos[0][5]
                p_usuarios = p_datos[0][6]
                p_reportes = p_datos[0][7]
                p_asistencia = p_datos[0][8]
                p_acceso = p_datos[0][9]
                cur.close()


                cur = mysql.connection.cursor()
                cur.execute("SELECT id_sedes FROM users WHERE id=%s",[id_sesion])
                data_sedes = cur.fetchall()
                id_sedess = data_sedes[0][0]
                
                id_sedess=int(id_sedess)

                #probar
                if (id_sedess==0):

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT id,nombre,address FROM sedes")
                    datos_sedes = cur.fetchall()


                    cur = mysql.connection.cursor()
                    cur.execute("SELECT users.id,users.nombre,users.user,users.telefono,users.genero,users.nacimiento,users.id_gruops_users,users.id_sedes,users.created,group_users.nombre FROM users INNER JOIN group_users ON users.id_gruops_users=group_users.id")
                    datos_usuarios = cur.fetchall()

                    

                        

                else:


                    cur = mysql.connection.cursor()
                    cur.execute("SELECT id,nombre,address FROM sedes WHERE id=%s",[id_sedess])
                    datos_sedes = cur.fetchall()


                    cur = mysql.connection.cursor()
                    cur.execute("SELECT users.id,users.nombre,users.user,users.telefono,users.genero,users.nacimiento,users.id_gruops_users,users.id_sedes,users.created,group_users.nombre FROM users INNER JOIN group_users ON users.id_gruops_users=group_users.id WHERE users.id_sedes=%s",[id_sedess])
                    datos_usuarios = cur.fetchall()

                    

                        
                cur = mysql.connection.cursor()
                cur.execute("SELECT id,nombre FROM group_users")
                datos_grupos = cur.fetchall()
                

                cur = mysql.connection.cursor()
                cur.execute("SELECT subfijo FROM empresa")
                subfijo=cur.fetchall()
                subfijo=subfijo[0][0]
                
                


                return render_template('usuarios.html',id_sedess=id_sedess,datos_grupos=datos_grupos,datos_sedes=datos_sedes,subfijo=subfijo,datos_usuarios=datos_usuarios,username=id_user,config_empresa=p_config_empresa,config_asistencia=p_config_asistencia,horarios=p_horarios,sedes=p_sedes,admin_usuarios=p_admin_user,grupos=p_grupos_user,usuarios=p_usuarios,reportes=p_reportes,asistencia=p_asistencia,accesos=p_acceso)

            elif p_empresa==True and p_admin_user==False and p_usuarios==False :


                return redirect(url_for('empresa'))

            elif p_empresa==True and p_admin_user==True and p_usuarios==False :


                return redirect(url_for('empresa'))

            elif p_empresa==False and p_ventas==True :
                return redirect(url_for('sys'))
            elif p_empresa==False and p_ventas==False :
                return redirect(url_for('logout'))

                
                
        return redirect(url_for('sys'))       


    elif request.method == "POST":

        if "id" in session:

            id_sesion=session['id']

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_admin_user,p_usuarios FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_admin_user = p_data[0][2]
            p_usuarios = p_data[0][3]
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("SELECT subfijo FROM empresa")
            subfijo = cur.fetchall()
            subfijo=subfijo[0][0]
            subfijo=str(subfijo)

            
            if p_empresa==True and p_admin_user==True and p_usuarios==True:
                
                nombre = request.form['nombre']
                nombre = str(nombre)
                print(nombre)

                usuario = request.form['usuario']
                usuario = str(usuario)
                print(usuario)
                user=usuario+subfijo

                password = request.form['password']
                print(password)
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                
                telefono = request.form['telefono']
                telefono = str(telefono)
                
                genero = request.form['genero']
                genero = str(genero)
                

                nacimiento = request.form['nacimiento']
                print(nacimiento)
                
                
                grupos = request.form['grupos']
                grupos = int(grupos)
                print(grupos)

                sedes = request.form['sedes']
                sedes = int(sedes)
                print(sedes)

                


                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users (nombre,user,password,telefono,genero,nacimiento,id_gruops_users,id_sedes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (nombre,user, hashed_password,telefono,genero,nacimiento,grupos,sedes))
                mysql.connection.commit()

                
                # cur = mysql.connection.cursor()
                # cur.execute("INSERT INTO group_users (nombre,id_horarios,p_empresa,p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso,p_ventas,p_config_campanas,p_campanas,p_pestanas,p_estados,p_bloques,p_campos,p_reportes_ventas,p_reportes1,p_reportes2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (nombre,horario,permisos[0],permisos[1],permisos[2],permisos[3],permisos[4],permisos[5],permisos[6],permisos[7],permisos[8],permisos[9],permisos[10],permisos[11],permisos[12],permisos[13],permisos[14],permisos[15],permisos[16],permisos[17],permisos[18],permisos[19],permisos[20]))
                # mysql.connection.commit()



                return redirect(url_for('usuarios'))


            elif p_empresa==True and p_admin_user==False and p_usuarios==False:


                return redirect(url_for('empresa'))

            elif p_empresa==True and p_admin_user==True and p_usuarios==False:


                return redirect(url_for('empresa'))

            elif p_empresa==False and p_ventas==True :
                return redirect(url_for('sys'))
            elif p_empresa==False and p_ventas==False :
                return redirect(url_for('logout'))
        

        return redirect(url_for('sys')) 



@app.route('/usuarios/delete/<int:idH>',methods=('GET',))
def eliminarUsuarios(idH):
    idH=int(idH)

    if "id" in session:

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_admin_user,p_usuarios FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_admin_user = p_data[0][2]
        p_usuarios = p_data[0][3]
        cur.close()

        if p_empresa==True and p_admin_user==True and p_usuarios==True:


            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM users WHERE id = %s ", [idH])
            mysql.connection.commit()

            return redirect(url_for('usuarios'))


        elif p_empresa==True and p_admin_user==False and p_usuarios==False:


            return redirect(url_for('empresa'))

        elif p_empresa==True and p_admin_user==True and p_usuarios==False:


            return redirect(url_for('empresa'))

        elif p_empresa==False and p_ventas==True :
            return redirect(url_for('sys'))
        elif p_empresa==False and p_ventas==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))




@app.route('/usuarios/edit/<int:idH>',methods=('POST',))
def editUsuarios(idH):
    idH=int(idH)

    if "id" in session:

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_admin_user,p_usuarios FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_admin_user = p_data[0][2]
        p_usuarios = p_data[0][3]
        cur.close()

        

        if p_empresa==True and p_admin_user==True and p_usuarios==True: 

            nombre = request.form['nombre']
            nombre = str(nombre)
            print(nombre)

            usuario = request.form['usuario']
            usuario = str(usuario)
            print(usuario)
            

            
            telefono = request.form['telefono']
            telefono = str(telefono)
            
            genero = request.form['genero']
            genero = str(genero)
            

            nacimiento = request.form['nacimiento']
            print(nacimiento)
            
            
            grupos = request.form['grupos']
            grupos = int(grupos)
            print(grupos)

            sedes = request.form['sedes']
            sedes = int(sedes)
            print(sedes)

            
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET nombre=%s,user=%s,telefono=%s,genero=%s,nacimiento=%s,id_gruops_users=%s,id_sedes=%s WHERE id=%s ", (nombre,usuario,telefono,genero,nacimiento,grupos,sedes,idH))
            mysql.connection.commit()
            cur.close()
            
            return redirect(url_for('usuarios'))


        elif p_empresa==True and p_admin_user==False and p_usuarios==False:


            return redirect(url_for('empresa'))

        elif p_empresa==True and p_admin_user==True and p_usuarios==False:


            return redirect(url_for('empresa'))

        elif p_empresa==False and p_ventas==True :
            return redirect(url_for('sys'))
        elif p_empresa==False and p_ventas==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))


@app.route('/asistencia',methods=('GET',))
def asistencia():
        
    if "id" in session:

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
        id_user = cur.fetchall()
        id_user = id_user[0]
        cur.close()


        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_reportes,p_asistencia FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_reportes = p_data[0][2]
        p_asistencia = p_data[0][3]
        cur.close()



        if p_empresa==True and p_reportes==True and p_asistencia==True:

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso FROM group_users WHERE id = %s", [id_gruops_users])
            p_datos = cur.fetchall()
            p_config_empresa = p_datos[0][0]
            p_config_asistencia = p_datos[0][1]
            p_horarios = p_datos[0][2]
            p_sedes = p_datos[0][3]
            p_admin_user = p_datos[0][4]
            p_grupos_user = p_datos[0][5]
            p_usuarios = p_datos[0][6]
            p_reportes = p_datos[0][7]
            p_asistencia = p_datos[0][8]
            p_acceso = p_datos[0][9]
            cur.close()

                
            return render_template('asistencia.html',username=id_user,config_empresa=p_config_empresa,config_asistencia=p_config_asistencia,horarios=p_horarios,sedes=p_sedes,admin_usuarios=p_admin_user,grupos=p_grupos_user,usuarios=p_usuarios,reportes=p_reportes,asistencia=p_asistencia,accesos=p_acceso)


        elif p_empresa==True and p_reportes==False and p_asistencia==False :

            return redirect(url_for('empresa'))

        elif p_empresa==True and p_reportes==True and p_asistencia==False :

            return redirect(url_for('empresa'))

        elif p_empresa==False and p_ventas==True :

            return redirect(url_for('sys'))

        elif p_empresa==False and p_ventas==False :

            return redirect(url_for('logout'))

    return redirect(url_for('sys'))






#falta terminar
@app.route('/accesos',methods=('GET',))
def acceso():
        
    if "id" in session:

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
        id_user = cur.fetchall()
        id_user = id_user[0]
        cur.close()


        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_reportes,p_acceso FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_reportes = p_data[0][2]
        p_acceso = p_data[0][3]
        cur.close()



        if p_empresa==True and p_reportes==True and p_acceso==True:

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso FROM group_users WHERE id = %s", [id_gruops_users])
            p_datos = cur.fetchall()
            p_config_empresa = p_datos[0][0]
            p_config_asistencia = p_datos[0][1]
            p_horarios = p_datos[0][2]
            p_sedes = p_datos[0][3]
            p_admin_user = p_datos[0][4]
            p_grupos_user = p_datos[0][5]
            p_usuarios = p_datos[0][6]
            p_reportes = p_datos[0][7]
            p_asistencia = p_datos[0][8]
            p_acceso = p_datos[0][9]
            cur.close()



            cur = mysql.connection.cursor()
            cur.execute("SELECT actividad.id, actividad.id_user, actividad.type, actividad.fecha, actividad.ip, users.nombre, users.user FROM actividad INNER JOIN users ON actividad.id_user=users.id ORDER BY actividad.id DESC")
            data_accesos = cur.fetchall()
            print(data_accesos[0][3])
            jj=data_accesos[0][3]
            print(type(jj))

            cur = mysql.connection.cursor()
            cur.execute("SELECT id,nombre FROM users")
            personal = cur.fetchall()

                
            return render_template('accesos.html',personal=personal,data_accesos=data_accesos,username=id_user,config_empresa=p_config_empresa,config_asistencia=p_config_asistencia,horarios=p_horarios,sedes=p_sedes,admin_usuarios=p_admin_user,grupos=p_grupos_user,usuarios=p_usuarios,reportes=p_reportes,asistencia=p_asistencia,accesos=p_acceso)


        elif p_empresa==True and p_reportes==False and p_acceso==False :

            return redirect(url_for('empresa'))

        elif p_empresa==True and p_reportes==True and p_acceso==False :

            return redirect(url_for('empresa'))

        elif p_empresa==False and p_ventas==True :

            return redirect(url_for('sys'))

        elif p_empresa==False and p_ventas==False :

            return redirect(url_for('logout'))

    return redirect(url_for('sys'))



@app.errorhandler(404)
def page_not_found(error):
    return render_template("401-error.html"), 404


#falta terminar
@app.route('/accesos/query',methods=('GET',))
def search():

    if "id" in session:

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
        id_user = cur.fetchall()
        id_user = id_user[0]
        cur.close()


        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_reportes,p_acceso FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_reportes = p_data[0][2]
        p_acceso = p_data[0][3]
        cur.close()



        if p_empresa==True and p_reportes==True and p_acceso==True:

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_config_empresa,p_config_asistencia,p_horarios,p_sedes,p_admin_user,p_grupos_user,p_usuarios,p_reportes,p_asistencia,p_acceso FROM group_users WHERE id = %s", [id_gruops_users])
            p_datos = cur.fetchall()
            p_config_empresa = p_datos[0][0]
            p_config_asistencia = p_datos[0][1]
            p_horarios = p_datos[0][2]
            p_sedes = p_datos[0][3]
            p_admin_user = p_datos[0][4]
            p_grupos_user = p_datos[0][5]
            p_usuarios = p_datos[0][6]
            p_reportes = p_datos[0][7]
            p_asistencia = p_datos[0][8]
            p_acceso = p_datos[0][9]
            cur.close()


            personal_select = request.args.get('personal')
            if (len(personal_select)>0):
                personal_select=int(personal_select)
            inicio_select = request.args.get('inicio')
            fin_select = request.args.get('fin')


            cur = mysql.connection.cursor()
            cur.execute("SELECT actividad.id, actividad.id_user, actividad.type, actividad.fecha, actividad.ip, users.nombre, users.user FROM actividad INNER JOIN users ON actividad.id_user=users.id WHERE (  actividad.fecha BETWEEN %s AND %s  AND actividad.id_user=%s ) ORDER BY actividad.id DESC ",[personal_select,inicio_select,fin_select])
            data_accesos = cur.fetchall()
            print(data_accesos[0][3])

            cur = mysql.connection.cursor()
            cur.execute("SELECT id,nombre FROM users")
            personal = cur.fetchall()

                
            return render_template('accesos.html',personal_select=personal_select,inicio_select=inicio_select,fin_select=fin_select,personal=personal,data_accesos=data_accesos,username=id_user,config_empresa=p_config_empresa,config_asistencia=p_config_asistencia,horarios=p_horarios,sedes=p_sedes,admin_usuarios=p_admin_user,grupos=p_grupos_user,usuarios=p_usuarios,reportes=p_reportes,asistencia=p_asistencia,accesos=p_acceso)


        elif p_empresa==True and p_reportes==False and p_acceso==False :

            return redirect(url_for('empresa'))

        elif p_empresa==True and p_reportes==True and p_acceso==False :

            return redirect(url_for('empresa'))

        elif p_empresa==False and p_ventas==True :

            return redirect(url_for('sys'))

        elif p_empresa==False and p_ventas==False :

            return redirect(url_for('logout'))

    return redirect(url_for('sys'))



@app.route('/empresa-ventas',methods=('GET',))
def empresa_ventas():
    if request.method == 'GET':
        if "id" in session:

            id_sesion=session['id']

            print("el id de la sesion es: ", id_sesion)

            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()
            
            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas FROM group_users WHERE id = %s", [id_gruops_users])
            p_empresa = cur.fetchall()
            p_ventas = p_empresa[0][1]
            p_empresa = p_empresa[0][0]
            cur.close()

            if p_ventas==True :

                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_campanas,p_campanas,p_pestanas,p_estados,p_bloques,p_campos,p_reportes_ventas,p_reportes1,p_reportes2,p_config_empresa FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_campanas = p_datos[0][0]
                p_campanas = p_datos[0][1]
                p_pestanas = p_datos[0][2]
                p_estados = p_datos[0][3]
                p_bloques = p_datos[0][4]
                p_campos = p_datos[0][5]
                p_reportes_ventas = p_datos[0][6]
                p_reportes1 = p_datos[0][7]
                p_reportes2 = p_datos[0][8]
                p_config_empresa = p_datos[0][9]
                
                cur.close()


                cur = mysql.connection.cursor()
                cur.execute("SELECT actividad.id, users.nombre, actividad.type, actividad.fecha, actividad.ip FROM actividad INNER JOIN users ON actividad.id_user=users.id ORDER BY id DESC")
                actividades = cur.fetchall()
                
                
                cur.close()


                ahora=datetime.now()

                return render_template('index-ventas.html',ahora=ahora,actividades=actividades,config_empresa=p_config_empresa,username=id_user,config_campanas=p_config_campanas,campanas=p_campanas,pestanas=p_pestanas,estados=p_estados,bloques=p_bloques,campos=p_campos,reportes_ventas=p_reportes_ventas,reportes1=p_reportes1,reportes2=p_reportes2)
            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))

        return redirect(url_for('sys'))






@app.route('/campanas',methods=('GET','POST',))

def campanas():

    if request.method == "GET":
        
        if "id" in session:

            id_sesion=session['id']
            id_sesion=int(id_sesion)


            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_campanas FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config_campanas = p_data[0][2]
            p_campanas = p_data[0][3]
            cur.close()

            



            if p_ventas==True and p_config_campanas==True and p_campanas==True:

                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_campanas,p_campanas,p_pestanas,p_estados,p_bloques,p_campos,p_reportes_ventas,p_reportes1,p_reportes2,p_config_empresa FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_campanas = p_datos[0][0]
                p_campanas = p_datos[0][1]
                p_pestanas = p_datos[0][2]
                p_estados = p_datos[0][3]
                p_bloques = p_datos[0][4]
                p_campos = p_datos[0][5]
                p_reportes_ventas = p_datos[0][6]
                p_reportes1 = p_datos[0][7]
                p_reportes2 = p_datos[0][8]
                p_config_empresa = p_datos[0][9]
                cur.close()


                cur = mysql.connection.cursor()
                cur.execute("SELECT id_sedes FROM users WHERE id=%s",[id_sesion])
                data_sedes = cur.fetchall()
                id_sedess = data_sedes[0][0]
                id_sedess=int(id_sedess)


                if (id_sedess==0):

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT id,nombre,address FROM sedes")
                    sedes_post = cur.fetchall()


                    cur = mysql.connection.cursor()
                    cur.execute("SELECT campanas.id,campanas.nombre,campanas.id_sedes,sedes.nombre FROM campanas INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    datos_campanas = cur.fetchall()


                else:

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT id,nombre,address FROM sedes WHERE id=%s",[id_sedess])
                    sedes_post = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT campanas.id,campanas.nombre,campanas.id_sedes,sedes.nombre FROM campanas INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    datos_campanas = cur.fetchall()



                return render_template('campanas.html',datos_campanas=datos_campanas,sedes_post=sedes_post,config_empresa=p_config_empresa,username=id_user,config_campanas=p_config_campanas,campanas=p_campanas,pestanas=p_pestanas,estados=p_estados,bloques=p_bloques,campos=p_campos,reportes_ventas=p_reportes_ventas,reportes1=p_reportes1,reportes2=p_reportes2)

            elif p_ventas==True and p_config_campanas==False and p_campanas==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==True and p_config_campanas==True and p_campanas==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))

                
                
        return redirect(url_for('sys'))       


    elif request.method == "POST":

        if "id" in session:
            

            id_sesion=session['id']

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_campanas FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config_campanas = p_data[0][2]
            p_campanas = p_data[0][3]
            cur.close()

            if p_ventas==True and p_config_campanas==True and p_campanas==True:
                
                nombre = request.form['nombre']
                nombre = str(nombre)
                print(nombre)

                sede_id = request.form['sede']
                sede_id = int(sede_id)
               
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO campanas (nombre,id_sedes) VALUES (%s,%s)", (nombre,sede_id))
                mysql.connection.commit()

                return redirect(url_for('campanas'))


            elif p_ventas==True and p_config_campanas==False and p_campanas==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==True and p_config_campanas==True and p_campanas==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))
        

        return redirect(url_for('sys')) 


        
@app.route('/campanas/edit/<int:idC>',methods=('POST',))
def campanaEdit(idC):

    if "id" in session:

        idC=int(idC)

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_campanas FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_config_campanas = p_data[0][2]
        p_campanas = p_data[0][3]
        cur.close()

        if p_ventas==True and p_config_campanas==True and p_campanas==True:

            nombre = request.form['nombre']
            nombre = str(nombre)
            print(nombre)

            sede_id = request.form['sede']
            sede_id = int(sede_id)

            cur = mysql.connection.cursor()
            cur.execute("UPDATE campanas SET nombre=%s,id_sedes=%s WHERE id=%s", (nombre,sede_id,idC))
            mysql.connection.commit()

            return redirect(url_for('campanas'))


        elif p_ventas==True and p_config_campanas==False and p_campanas==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==True and p_config_campanas==True and p_campanas==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==False and p_empresa==True :
            return redirect(url_for('sys'))
        elif p_ventas==False and p_empresa==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))







@app.route('/campanas/delete/<int:idC>',methods=('GET',))
def campanaDelete(idC):

    if "id" in session:

        idC=int(idC)

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_campanas FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_config_campanas = p_data[0][2]
        p_campanas = p_data[0][3]
        cur.close()

        if p_ventas==True and p_config_campanas==True and p_campanas==True:

            
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM campanas WHERE id=%s", [idC])
            mysql.connection.commit()

            return redirect(url_for('campanas'))


        elif p_ventas==True and p_config_campanas==False and p_campanas==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==True and p_config_campanas==True and p_campanas==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==False and p_empresa==True :
            return redirect(url_for('sys'))
        elif p_ventas==False and p_empresa==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))













@app.route('/pestanas',methods=('GET','POST',))

def pestanas():

    if request.method == "GET":
        
        if "id" in session:


            id_sesion=session['id']
            id_sesion=int(id_sesion)


            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_pestanas FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config_campanas = p_data[0][2]
            p_pestanas = p_data[0][3]
            cur.close()

            



            if p_ventas==True and p_config_campanas==True and p_pestanas==True:

                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_campanas,p_campanas,p_pestanas,p_estados,p_bloques,p_campos,p_reportes_ventas,p_reportes1,p_reportes2,p_config_empresa FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_campanas = p_datos[0][0]
                p_campanas = p_datos[0][1]
                p_pestanas = p_datos[0][2]
                p_estados = p_datos[0][3]
                p_bloques = p_datos[0][4]
                p_campos = p_datos[0][5]
                p_reportes_ventas = p_datos[0][6]
                p_reportes1 = p_datos[0][7]
                p_reportes2 = p_datos[0][8]
                p_config_empresa = p_datos[0][9]
                cur.close()


                cur = mysql.connection.cursor()
                cur.execute("SELECT id_sedes FROM users WHERE id=%s",[id_sesion])
                data_sedes = cur.fetchall()
                id_sedess = data_sedes[0][0]
                id_sedess=int(id_sedess)


                if (id_sedess==0):



                    

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT pestanas.id,pestanas.nombre,pestanas.orden,pestanas.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM pestanas INNER JOIN campanas ON pestanas.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    datosPCS = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT campanas.id,campanas.nombre,campanas.id_sedes,sedes.nombre FROM campanas INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    CSposts = cur.fetchall()




                else:

                    
                    cur = mysql.connection.cursor()
                    cur.execute("SELECT pestanas.id,pestanas.nombre,pestanas.orden,pestanas.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM pestanas INNER JOIN campanas ON pestanas.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    datosPCS = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT campanas.id,campanas.nombre,campanas.id_sedes,sedes.nombre FROM campanas INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    CSposts = cur.fetchall()


                return render_template('p-estados.html',datosPCS=datosPCS,CSposts=CSposts,config_empresa=p_config_empresa,username=id_user,config_campanas=p_config_campanas,campanas=p_campanas,pestanas=p_pestanas,estados=p_estados,bloques=p_bloques,campos=p_campos,reportes_ventas=p_reportes_ventas,reportes1=p_reportes1,reportes2=p_reportes2)

            elif p_ventas==True and p_config_campanas==False and p_pestanas==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==True and p_config_campanas==True and p_pestanas==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))

                
                
        return redirect(url_for('sys'))       


    elif request.method == "POST":

        if "id" in session:
            

            id_sesion=session['id']

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_pestanas FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config_campanas = p_data[0][2]
            p_pestanas = p_data[0][3]
            cur.close()

            if p_ventas==True and p_config_campanas==True and p_pestanas==True:
                
                nombre = request.form['nombre']
                nombre = str(nombre)
                print(nombre)

                orden = request.form['orden']
                orden = int(orden)

                id_campana = request.form['campana']
                id_campana = int(id_campana)
               
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO pestanas (nombre,orden,id_campana) VALUES (%s,%s,%s)", [nombre,orden,id_campana])
                mysql.connection.commit()

                return redirect(url_for('pestanas'))


            elif p_ventas==True and p_config_campanas==False and p_pestanas==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==True and p_config_campanas==True and p_pestanas==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))
        

        return redirect(url_for('sys'))



@app.route('/pestanas/delete/<int:idP>',methods=('GET',))
def pestanaDelete(idP):

    if "id" in session:

        idP=int(idP)

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_pestanas FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_config_campanas = p_data[0][2]
        p_pestanas = p_data[0][3]
        cur.close()

        if p_ventas==True and p_config_campanas==True and p_pestanas==True:

            
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM pestanas WHERE id=%s", [idP])
            mysql.connection.commit()

            return redirect(url_for('pestanas'))


        elif p_ventas==True and p_config_campanas==False and p_pestanas==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==True and p_config_campanas==True and p_pestanas==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==False and p_empresa==True :
            return redirect(url_for('sys'))
        elif p_ventas==False and p_empresa==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))





@app.route('/pestanas/edit/<int:idP>',methods=('POST',))
def pestanaEdit(idP):

    if "id" in session:

        idP=int(idP)

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_pestanas FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_config_campanas = p_data[0][2]
        p_pestanas = p_data[0][3]
        cur.close()

        if p_ventas==True and p_config_campanas==True and p_pestanas==True:

            nombre = request.form['nombre']
            nombre = str(nombre)
            print(nombre)

            orden = request.form['orden']
            orden = int(orden)

            campana_id = request.form['campana']
            campana_id = int(campana_id)

            cur = mysql.connection.cursor()
            cur.execute("UPDATE pestanas SET nombre=%s,orden=%s,id_campana=%s WHERE id=%s", (nombre,orden,campana_id,idP))
            mysql.connection.commit()

            return redirect(url_for('pestanas'))


        elif p_ventas==True and p_config_campanas==False and p_pestanas==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==True and p_config_campanas==True and p_pestanas==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==False and p_empresa==True :
            return redirect(url_for('sys'))
        elif p_ventas==False and p_empresa==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))











































@app.route('/estados',methods=('GET','POST',))

def estados():

    if request.method == "GET":
        
        if "id" in session:


            id_sesion=session['id']
            id_sesion=int(id_sesion)


            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_estados FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config_campanas = p_data[0][2]
            p_estados = p_data[0][3]
            cur.close()

            



            if p_ventas==True and p_config_campanas==True and p_estados==True:

                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_campanas,p_campanas,p_pestanas,p_estados,p_bloques,p_campos,p_reportes_ventas,p_reportes1,p_reportes2,p_config_empresa FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_campanas = p_datos[0][0]
                p_campanas = p_datos[0][1]
                p_pestanas = p_datos[0][2]
                p_estados = p_datos[0][3]
                p_bloques = p_datos[0][4]
                p_campos = p_datos[0][5]
                p_reportes_ventas = p_datos[0][6]
                p_reportes1 = p_datos[0][7]
                p_reportes2 = p_datos[0][8]
                p_config_empresa = p_datos[0][9]
                cur.close()


                cur = mysql.connection.cursor()
                cur.execute("SELECT id_sedes FROM users WHERE id=%s",[id_sesion])
                data_sedes = cur.fetchall()
                id_sedess = data_sedes[0][0]
                id_sedess=int(id_sedess)


                if (id_sedess==0):


                #     cur = mysql.connection.cursor()
                #     cur.execute("SELECT pestanas.id,pestanas.nombre,pestanas.orden,pestanas.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM pestanas INNER JOIN campanas ON pestanas.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                #     datosPCS = cur.fetchall()

                #     cur = mysql.connection.cursor()
                #     cur.execute("SELECT campanas.id,campanas.nombre,campanas.id_sedes,sedes.nombre FROM campanas INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                #     CSposts = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT pestanas.id,pestanas.nombre,pestanas.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM pestanas INNER JOIN campanas ON pestanas.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    PCSposts = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT id,nombre FROM group_users")
                    Gposts = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT estados.id,estados.nombre,estados.id_pestana,pestanas.nombre,pestanas.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM estados INNER JOIN pestanas ON estados.id_pestana=pestanas.id INNER JOIN campanas ON pestanas.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    Eposts = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT estados.id,estados.nombre,estados.color,estados.id_pestana,estados.orden,estados.id_usado,pestanas.nombre,pestanas.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM estados INNER JOIN pestanas ON estados.id_pestana=pestanas.id INNER JOIN campanas ON pestanas.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    datosE = cur.fetchall()

                    

                else:

                    
                #     cur = mysql.connection.cursor()
                #     cur.execute("SELECT pestanas.id,pestanas.nombre,pestanas.orden,pestanas.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM pestanas INNER JOIN campanas ON pestanas.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                #     datosPCS = cur.fetchall()

                #     cur = mysql.connection.cursor()
                #     cur.execute("SELECT campanas.id,campanas.nombre,campanas.id_sedes,sedes.nombre FROM campanas INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                #     CSposts = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT pestanas.id,pestanas.nombre,pestanas.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM pestanas INNER JOIN campanas ON pestanas.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    PCSposts = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT id,nombre FROM group_users")
                    Gposts = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT estados.id,estados.nombre,estados.id_pestana,pestanas.nombre,pestanas.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM estados INNER JOIN pestanas ON estados.id_pestana=pestanas.id INNER JOIN campanas ON pestanas.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    Eposts = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT estados.id,estados.nombre,estados.color,estados.id_pestana,estados.orden,estados.id_usado,pestanas.nombre,pestanas.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM estados INNER JOIN pestanas ON estados.id_pestana=pestanas.id INNER JOIN campanas ON pestanas.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    datosE = cur.fetchall()

                cur = mysql.connection.cursor()
                cur.execute("SELECT permisos_grupos_estados.id_estado,permisos_grupos_estados.id_group_user,permisos_grupos_estados.type,estados.nombre,group_users.nombre FROM permisos_grupos_estados INNER JOIN estados ON permisos_grupos_estados.id_estado=estados.id INNER JOIN group_users ON permisos_grupos_estados.id_group_user=group_users.id")
                pges=cur.fetchall()

                cur=mysql.connection.cursor()
                cur.execute("SELECT id_estado1, id_estado2 FROM estado_cambiar_estado")
                EEposts = cur.fetchall()


                return render_template('estados.html',EEposts=EEposts,pges=pges,datosE=datosE,Eposts=Eposts,Gposts=Gposts,PCSposts=PCSposts,config_empresa=p_config_empresa,username=id_user,config_campanas=p_config_campanas,campanas=p_campanas,pestanas=p_pestanas,estados=p_estados,bloques=p_bloques,campos=p_campos,reportes_ventas=p_reportes_ventas,reportes1=p_reportes1,reportes2=p_reportes2)

            elif p_ventas==True and p_config_campanas==False and p_estados==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==True and p_config_campanas==True and p_estados==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))

                
                
        return redirect(url_for('sys'))       


    elif request.method == "POST":

        if "id" in session:
            

            id_sesion=session['id']

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_estados FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config_campanas = p_data[0][2]
            p_estados = p_data[0][3]
            cur.close()

            if p_ventas==True and p_config_campanas==True and p_estados==True:
                
                nombre = request.form['nombre']
                nombre = str(nombre)
                
                color = request.form['color']
                color = str(color)

                pestana = request.form['pestanas']
                pestana = int(pestana)

                orden = request.form['orden']
                orden = int(orden)

                usado = request.form['usado']
                usado = int(usado)
                # 1 Crear
                # 2 Editar
                # 3 Crear y/o Editar

                estado_estados=request.form.getlist('estado-estado')
                if (len(estado_estados)>0):
                    for estado_estado in estado_estados:
                        estado1=int(estado_estado)
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT id_pestana FROM estados WHERE id=%s", [estado1])
                        id_pestana = cur.fetchall()
                        id_pestana = id_pestana[0][0]
                        id_pestana = int(id_pestana)
                        cur.close()
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT id_campana FROM pestanas WHERE id=%s", [id_pestana])
                        id_campana = cur.fetchall()
                        id_campana = id_campana[0][0]
                        id_campana = int(id_campana)

                        cur = mysql.connection.cursor()
                        cur.execute("SELECT id_campana FROM pestanas WHERE id=%s", [pestana])
                        id_campana_new = cur.fetchall()
                        id_campana_new = id_campana_new[0][0]
                        id_campana_new = int(id_campana_new)

                        if (id_campana != id_campana_new ):
                            return "campanas diferentes"

                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO estados (nombre,color,id_pestana,orden,id_usado) VALUES (%s,%s,%s,%s,%s)", [nombre,color,pestana,orden,usado])
                mysql.connection.commit()

                cur = mysql.connection.cursor()
                cur.execute("SELECT id FROM estados WHERE nombre=%s AND color=%s AND id_pestana=%s AND orden=%s AND id_usado=%s", [nombre,color,pestana,orden,usado])
                id_estado_actual = cur.fetchall()
                id_estado_actual = id_estado_actual[0][0]
                id_estado_actual = int(id_estado_actual)
                cur.close()

                estado_estados=request.form.getlist('estado-estado')
                if (len(estado_estados)>0):
                    for estado_estado in estado_estados:
                        estado1=int(estado_estado)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO estado_cambiar_estado (id_estado1,id_estado2) VALUES (%s,%s)", [estado1,id_estado_actual])
                        mysql.connection.commit()
                    

                crear_cambiars=request.form.getlist('crear-cambiar')#type 1
                if (len(crear_cambiars)>0):
                    for crear_cambiar in crear_cambiars:
                        id_group_user=int(crear_cambiar)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_estados (id_estado,id_group_user,type) VALUES (%s,%s,%s)", [id_estado_actual,id_group_user,1])
                        mysql.connection.commit()


                editars=request.form.getlist('editar')#type 2
                if (len(editars)>0):
                    for editar in editars:
                        id_group_user=int(editar)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_estados (id_estado,id_group_user,type) VALUES (%s,%s,%s)", [id_estado_actual,id_group_user,2])
                        mysql.connection.commit()


                vers=request.form.getlist('ver')#type 3
                if (len(vers)>0):
                    for ver in vers:
                        id_group_user=int(ver)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_estados (id_estado,id_group_user,type) VALUES (%s,%s,%s)", [id_estado_actual,id_group_user,3])
                        mysql.connection.commit()


                eliminars=request.form.getlist('eliminar')#type 4
                if (len(eliminars)>0):
                    for eliminar in eliminars:
                        id_group_user=int(eliminar)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_estados (id_estado,id_group_user,type) VALUES (%s,%s,%s)", [id_estado_actual,id_group_user,4])
                        mysql.connection.commit()

                historials=request.form.getlist('historial')#type 5
                if (len(historials)>0):
                    for historial in historials:
                        id_group_user=int(historial)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_estados (id_estado,id_group_user,type) VALUES (%s,%s,%s)", [id_estado_actual,id_group_user,5])
                        mysql.connection.commit()
                
                # cur = mysql.connection.cursor()
                # cur.execute("INSERT INTO estados (nombre,color,id_pestana,orden,id_usado) VALUES (%s,%s,%s,%s,%s)", [nombre,color,pestana,orden,usado])
                # mysql.connection.commit()

                return redirect(url_for('estados'))


            elif p_ventas==True and p_config_campanas==False and p_estados==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==True and p_config_campanas==True and p_estados==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))
        

        return redirect(url_for('sys'))








@app.route('/estados/edit/<int:idE>',methods=('POST',))

def estadoEdit(idE):

    if request.method == "POST":

        if "id" in session:

            idE=int(idE)

            id_sesion=session['id']
            id_sesion=int(id_sesion)

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_estados FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config_campanas = p_data[0][2]
            p_estados = p_data[0][3]
            cur.close()

            if p_ventas==True and p_config_campanas==True and p_estados==True:
                
                nombre = request.form['nombre']
                nombre = str(nombre)
                
                color = request.form['color']
                color = str(color)

                pestana = request.form['pestanas']
                pestana = int(pestana)

                orden = request.form['orden']
                orden = int(orden)

                usado = request.form['usado']
                usado = int(usado)
                # 1 Crear
                # 2 Editar
                # 3 Crear y/o Editar

                estado_estados=request.form.getlist('estado-estado')
                if (len(estado_estados)>0):
                    for estado_estado in estado_estados:
                        estado1=int(estado_estado)
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT id_pestana FROM estados WHERE id=%s", [estado1])
                        id_pestana = cur.fetchall()
                        id_pestana = id_pestana[0][0]
                        id_pestana = int(id_pestana)
                        cur.close()
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT id_campana FROM pestanas WHERE id=%s", [id_pestana])
                        id_campana = cur.fetchall()
                        id_campana = id_campana[0][0]
                        id_campana = int(id_campana)

                        cur = mysql.connection.cursor()
                        cur.execute("SELECT id_campana FROM pestanas WHERE id=%s", [pestana])
                        id_campana_new = cur.fetchall()
                        id_campana_new = id_campana_new[0][0]
                        id_campana_new = int(id_campana_new)

                        if (id_campana != id_campana_new ):
                            return "campanas diferentes"


                id_estado_actual = idE

                cur = mysql.connection.cursor()
                cur.execute("UPDATE estados SET nombre=%s,color=%s,id_pestana=%s,orden=%s,id_usado=%s WHERE id=%s", [nombre,color,pestana,orden,usado,id_estado_actual])
                mysql.connection.commit()


                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM estado_cambiar_estado WHERE id_estado2=%s", [id_estado_actual])
                mysql.connection.commit()

                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM permisos_grupos_estados WHERE id_estado=%s", [id_estado_actual])
                mysql.connection.commit()
                

                estado_estados=request.form.getlist('estado-estado')
                if (len(estado_estados)>0):
                    for estado_estado in estado_estados:
                        estado1=int(estado_estado)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO estado_cambiar_estado (id_estado1,id_estado2) VALUES (%s,%s)", [estado1,id_estado_actual])
                        mysql.connection.commit()
                    

                crear_cambiars=request.form.getlist('crear-cambiar')#type 1
                if (len(crear_cambiars)>0):
                    for crear_cambiar in crear_cambiars:
                        id_group_user=int(crear_cambiar)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_estados (id_estado,id_group_user,type) VALUES (%s,%s,%s)", [id_estado_actual,id_group_user,1])
                        mysql.connection.commit()


                editars=request.form.getlist('editar')#type 2
                if (len(editars)>0):
                    for editar in editars:
                        id_group_user=int(editar)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_estados (id_estado,id_group_user,type) VALUES (%s,%s,%s)", [id_estado_actual,id_group_user,2])
                        mysql.connection.commit()


                vers=request.form.getlist('ver')#type 3
                if (len(vers)>0):
                    for ver in vers:
                        id_group_user=int(ver)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_estados (id_estado,id_group_user,type) VALUES (%s,%s,%s)", [id_estado_actual,id_group_user,3])
                        mysql.connection.commit()


                eliminars=request.form.getlist('eliminar')#type 4
                if (len(eliminars)>0):
                    for eliminar in eliminars:
                        id_group_user=int(eliminar)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_estados (id_estado,id_group_user,type) VALUES (%s,%s,%s)", [id_estado_actual,id_group_user,4])
                        mysql.connection.commit()

                historials=request.form.getlist('historial')#type 5
                if (len(historials)>0):
                    for historial in historials:
                        id_group_user=int(historial)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_estados (id_estado,id_group_user,type) VALUES (%s,%s,%s)", [id_estado_actual,id_group_user,5])
                        mysql.connection.commit()
                
                # cur = mysql.connection.cursor()
                # cur.execute("INSERT INTO estados (nombre,color,id_pestana,orden,id_usado) VALUES (%s,%s,%s,%s,%s)", [nombre,color,pestana,orden,usado])
                # mysql.connection.commit()

                return redirect(url_for('estados'))


            elif p_ventas==True and p_config_campanas==False and p_estados==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==True and p_config_campanas==True and p_estados==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))
        

        return redirect(url_for('sys'))









@app.route('/estados/delete/<int:idE>',methods=('GET',))

def estadoDelete(idE):

    if request.method == "GET":
        
        if "id" in session:

            idE=int(idE)


            id_sesion=session['id']
            id_sesion=int(id_sesion)


            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_estados FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config_campanas = p_data[0][2]
            p_estados = p_data[0][3]
            cur.close()


            if p_ventas==True and p_config_campanas==True and p_estados==True:




                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM estados WHERE id=%s",[idE])
                mysql.connection.commit()





                return redirect(url_for('estados'))

            elif p_ventas==True and p_config_campanas==False and p_estados==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==True and p_config_campanas==True and p_estados==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))

                
                
        return redirect(url_for('sys'))     
















































































@app.route('/bloques',methods=('GET','POST',))

def bloques():

    if request.method == "GET":
        
        if "id" in session:

            id_sesion=session['id']
            id_sesion=int(id_sesion)


            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_bloques FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config_campanas = p_data[0][2]
            p_bloques = p_data[0][3]
            cur.close()

            



            if p_ventas==True and p_config_campanas==True and p_bloques==True:

                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_campanas,p_campanas,p_pestanas,p_estados,p_bloques,p_campos,p_reportes_ventas,p_reportes1,p_reportes2,p_config_empresa FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_campanas = p_datos[0][0]
                p_campanas = p_datos[0][1]
                p_pestanas = p_datos[0][2]
                p_estados = p_datos[0][3]
                p_bloques = p_datos[0][4]
                p_campos = p_datos[0][5]
                p_reportes_ventas = p_datos[0][6]
                p_reportes1 = p_datos[0][7]
                p_reportes2 = p_datos[0][8]
                p_config_empresa = p_datos[0][9]
                cur.close()


                cur = mysql.connection.cursor()
                cur.execute("SELECT id_sedes FROM users WHERE id=%s",[id_sesion])
                data_sedes = cur.fetchall()
                id_sedess = data_sedes[0][0]
                id_sedess=int(id_sedess)


                if (id_sedess==0):



                    

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT bloques.id,bloques.nombre,bloques.orden,bloques.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM bloques INNER JOIN campanas ON bloques.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    datosBCS = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT campanas.id,campanas.nombre,campanas.id_sedes,sedes.nombre FROM campanas INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    CSposts = cur.fetchall()




                else:

                    
                    cur = mysql.connection.cursor()
                    cur.execute("SELECT bloques.id,bloques.nombre,bloques.orden,bloques.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM bloques INNER JOIN campanas ON bloques.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    datosBCS = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT campanas.id,campanas.nombre,campanas.id_sedes,sedes.nombre FROM campanas INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    CSposts = cur.fetchall()


                return render_template('b-campos.html',datosBCS=datosBCS,CSposts=CSposts,config_empresa=p_config_empresa,username=id_user,config_campanas=p_config_campanas,campanas=p_campanas,pestanas=p_pestanas,estados=p_estados,bloques=p_bloques,campos=p_campos,reportes_ventas=p_reportes_ventas,reportes1=p_reportes1,reportes2=p_reportes2)

            elif p_ventas==True and p_config_campanas==False and p_bloques==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==True and p_config_campanas==True and p_bloques==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))

                
                
        return redirect(url_for('sys'))       


    elif request.method == "POST":

        if "id" in session:
            

            id_sesion=session['id']

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_bloques FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config_campanas = p_data[0][2]
            p_bloques = p_data[0][3]
            cur.close()

            if p_ventas==True and p_config_campanas==True and p_bloques==True:
                
                print("seccion bloques")

                nombre = request.form['nombre']
                nombre = str(nombre)
                print(nombre)

                orden = request.form['orden']
                orden = int(orden)
                print(orden)

                id_campana = request.form['campana']
                id_campana = int(id_campana)
                print(id_campana)
               
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO bloques (nombre,orden,id_campana) VALUES (%s,%s,%s)", [nombre,orden,id_campana])
                mysql.connection.commit()

                return redirect(url_for('bloques'))


            elif p_ventas==True and p_config_campanas==False and p_bloques==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==True and p_config_campanas==True and p_bloques==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))
        

        return redirect(url_for('sys'))



@app.route('/bloques/edit/<int:idB>',methods=('POST',))
def bloqueEdit(idB):

    if "id" in session:

        idB=int(idB)

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_bloques FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_config_campanas = p_data[0][2]
        p_bloques = p_data[0][3]
        cur.close()

        if p_ventas==True and p_config_campanas==True and p_bloques==True:

            nombre = request.form['nombre']
            nombre = str(nombre)
            print(nombre)

            orden = request.form['orden']
            orden = int(orden)

            campana_id = request.form['campana']
            campana_id = int(campana_id)

            cur = mysql.connection.cursor()
            cur.execute("UPDATE bloques SET nombre=%s,orden=%s,id_campana=%s WHERE id=%s", (nombre,orden,campana_id,idB))
            mysql.connection.commit()

            return redirect(url_for('bloques'))


        elif p_ventas==True and p_config_campanas==False and p_bloques==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==True and p_config_campanas==True and p_bloques==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==False and p_empresa==True :
            return redirect(url_for('sys'))
        elif p_ventas==False and p_empresa==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))



@app.route('/bloques/delete/<int:idB>',methods=('GET',))
def bloqueDelete(idB):

    if "id" in session:

        idB=int(idB)

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_bloques FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_config_campanas = p_data[0][2]
        p_bloques = p_data[0][3]
        cur.close()

        if p_ventas==True and p_config_campanas==True and p_bloques==True:

            
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM bloques WHERE id=%s", [idB])
            mysql.connection.commit()

            return redirect(url_for('bloques'))


        elif p_ventas==True and p_config_campanas==False and p_bloques==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==True and p_config_campanas==True and p_bloques==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==False and p_empresa==True :
            return redirect(url_for('sys'))
        elif p_ventas==False and p_empresa==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))
















































@app.route('/campos',methods=('GET','POST',))

def campos():

    if request.method == "GET":
        
        if "id" in session:




            id_sesion=session['id']
            id_sesion=int(id_sesion)


            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()


            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_campos FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config_campanas = p_data[0][2]
            p_campos = p_data[0][3]
            cur.close()

            



            if p_ventas==True and p_config_campanas==True and p_campos==True:

                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_campanas,p_campanas,p_pestanas,p_estados,p_bloques,p_campos,p_reportes_ventas,p_reportes1,p_reportes2,p_config_empresa FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_campanas = p_datos[0][0]
                p_campanas = p_datos[0][1]
                p_pestanas = p_datos[0][2]
                p_estados = p_datos[0][3]
                p_bloques = p_datos[0][4]
                p_campos = p_datos[0][5]
                p_reportes_ventas = p_datos[0][6]
                p_reportes1 = p_datos[0][7]
                p_reportes2 = p_datos[0][8]
                p_config_empresa = p_datos[0][9]
                cur.close()


                cur = mysql.connection.cursor()
                cur.execute("SELECT id_sedes FROM users WHERE id=%s",[id_sesion])
                data_sedes = cur.fetchall()
                id_sedess = data_sedes[0][0]
                id_sedess=int(id_sedess)



                if (id_sedess==0):


                    cur = mysql.connection.cursor()
                    cur.execute("SELECT campos.id,campos.nombre,campos.id_bloque,bloques.nombre,bloques.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre,campos.orden,campos.type,campos.obligatory,campos.depende,campos.valores,campos.ancho FROM campos INNER JOIN bloques ON campos.id_bloque=bloques.id INNER JOIN campanas ON bloques.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    datosC = cur.fetchall()


                    # cur = mysql.connection.cursor()
                    # cur.execute("SELECT bloques.id,bloques.nombre,bloques.orden,bloques.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM bloques INNER JOIN campanas ON bloques.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    # datosBCS = cur.fetchall()

                    # cur = mysql.connection.cursor()
                    # cur.execute("SELECT campanas.id,campanas.nombre,campanas.id_sedes,sedes.nombre FROM campanas INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    # CSposts = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT bloques.id,bloques.nombre,bloques.orden,bloques.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM bloques INNER JOIN campanas ON bloques.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    BCSposts = cur.fetchall()


                    cur = mysql.connection.cursor()
                    cur.execute("SELECT campos.id,campos.nombre,campos.id_bloque,bloques.nombre,bloques.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM campos INNER JOIN bloques ON campos.id_bloque=bloques.id INNER JOIN campanas ON bloques.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    Camposs = cur.fetchall()


                    cur = mysql.connection.cursor()
                    cur.execute("SELECT estados.id,estados.nombre,estados.id_pestana,pestanas.nombre,pestanas.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM estados INNER JOIN pestanas ON estados.id_pestana=pestanas.id INNER JOIN campanas ON pestanas.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id")
                    Eposts = cur.fetchall()


                else:

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT campos.id,campos.nombre,campos.id_bloque,bloques.nombre,bloques.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre,campos.orden,campos.type,campos.obligatory,campos.depende,campos.valores,campos.ancho FROM campos INNER JOIN bloques ON campos.id_bloque=bloques.id INNER JOIN campanas ON bloques.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    datosC = cur.fetchall()

                    
                    # cur = mysql.connection.cursor()
                    # cur.execute("SELECT bloques.id,bloques.nombre,bloques.orden,bloques.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM bloques INNER JOIN campanas ON bloques.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    # datosBCS = cur.fetchall()

                    # cur = mysql.connection.cursor()
                    # cur.execute("SELECT campanas.id,campanas.nombre,campanas.id_sedes,sedes.nombre FROM campanas INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    # CSposts = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT bloques.id,bloques.nombre,bloques.orden,bloques.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM bloques INNER JOIN campanas ON bloques.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    BCSposts = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT campos.id,campos.nombre,campos.id_bloque,bloques.nombre,bloques.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM campos INNER JOIN bloques ON campos.id_bloque=bloques.id INNER JOIN campanas ON bloques.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    Camposs = cur.fetchall()

                    cur = mysql.connection.cursor()
                    cur.execute("SELECT estados.id,estados.nombre,estados.id_pestana,pestanas.nombre,pestanas.id_campana,campanas.nombre,campanas.id_sedes,sedes.nombre FROM estados INNER JOIN pestanas ON estados.id_pestana=pestanas.id INNER JOIN campanas ON pestanas.id_campana=campanas.id INNER JOIN sedes ON campanas.id_sedes=sedes.id WHERE campanas.id_sedes=%s",[id_sedess])
                    Eposts = cur.fetchall()


                cur = mysql.connection.cursor()
                cur.execute("SELECT id,nombre FROM group_users")
                Gposts = cur.fetchall()

                cur = mysql.connection.cursor()
                cur.execute("SELECT estados_campos.id_estado,estados.nombre,estados_campos.id_campo,campos.nombre FROM estados_campos INNER JOIN estados ON estados_campos.id_estado=estados.id INNER JOIN campos ON estados_campos.id_campo=campos.id")
                ecs = cur.fetchall()

                cur = mysql.connection.cursor()
                cur.execute("SELECT permisos_grupos_campos.id_campo,campos.nombre,permisos_grupos_campos.id_grupo,group_users.nombre,permisos_grupos_campos.type FROM permisos_grupos_campos INNER JOIN campos ON permisos_grupos_campos.id_campo=campos.id INNER JOIN group_users ON permisos_grupos_campos.id_grupo=group_users.id")
                pgcs = cur.fetchall()


                return render_template('campos.html',pgcs=pgcs,ecs=ecs,datosC=datosC,Gposts=Gposts,Eposts=Eposts,Camposs=Camposs,BCSposts=BCSposts,config_empresa=p_config_empresa,username=id_user,config_campanas=p_config_campanas,campanas=p_campanas,pestanas=p_pestanas,estados=p_estados,bloques=p_bloques,campos=p_campos,reportes_ventas=p_reportes_ventas,reportes1=p_reportes1,reportes2=p_reportes2)

            elif p_ventas==True and p_config_campanas==False and p_campos==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==True and p_config_campanas==True and p_campos==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))

                
                
        return redirect(url_for('sys'))       


    elif request.method == "POST":

        if "id" in session:
            

            id_sesion=session['id']

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_campos FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config_campanas = p_data[0][2]
            p_campos = p_data[0][3]
            cur.close()

            if p_ventas==True and p_config_campanas==True and p_campos==True:
                
                print("seccion campos")

                nombre = request.form['nombre']
                nombre = str(nombre)
                print(nombre)

                orden = request.form['orden']
                orden = int(orden)
                print(orden)

                bloque = request.form['bloque']
                bloque = int(bloque)
                print(bloque)

                type_campo = request.form['type']
                type_campo = int(type_campo)
                print(type_campo)

                ancho = request.form['ancho']
                ancho = str(ancho)
                print(ancho)

                obligatorio = request.form['obligatorio']
                if obligatorio=="True":
                    obli = True
                else:
                    obli = False
                print(obligatorio)






                estado_campos=request.form.getlist('estados')
                if (len(estado_campos)>0):
                    for estado_campo in estado_campos:
                        estado1=int(estado_campo)
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT id_pestana FROM estados WHERE id=%s", [estado1])
                        id_pestana = cur.fetchall()
                        id_pestana = id_pestana[0][0]
                        id_pestana = int(id_pestana)
                        cur.close()
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT id_campana FROM pestanas WHERE id=%s", [id_pestana])
                        id_campana = cur.fetchall()
                        id_campana = id_campana[0][0]
                        id_campana = int(id_campana)

                        cur = mysql.connection.cursor()
                        cur.execute("SELECT id_campana FROM bloques WHERE id=%s", [bloque])
                        id_campana_new = cur.fetchall()
                        id_campana_new = id_campana_new[0][0]
                        id_campana_new = int(id_campana_new)

                        if (id_campana != id_campana_new ):
                            return "campanas diferentes"


                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO campos (nombre,id_bloque,orden,type,obligatory,ancho) VALUES (%s,%s,%s,%s,%s,%s)", [nombre,bloque,orden,type_campo,obli,ancho])
                mysql.connection.commit()

                cur = mysql.connection.cursor()
                cur.execute("SELECT id FROM campos WHERE nombre=%s AND id_bloque=%s AND orden=%s AND type=%s AND obligatory=%s AND ancho=%s",[nombre,bloque,orden,type_campo,obli,ancho])
                id_campo_nuevo = cur.fetchall()
                id_campo_nuevo = int(id_campo_nuevo[0][0])


                if (int(request.form['depende'])>0):

                    depende = request.form['depende']
                    depende = int(depende)
                    print(depende)

                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE campos SET depende=%s WHERE id=%s ", [depende,id_campo_nuevo])
                    mysql.connection.commit()
                    cur.close()


                if (len(str(request.form['valores']))>0):

                    valores = request.form['valores']
                    print(valores)

                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE campos SET valores=%s WHERE id=%s ", [valores,id_campo_nuevo])
                    mysql.connection.commit()
                    cur.close()


                estado_campos=request.form.getlist('estados')
                if (len(estado_campos)>0):
                    for estado_campo in estado_campos:
                        estado1=int(estado_campo)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO estados_campos (id_estado,id_campo) VALUES (%s,%s)", [estado1,id_campo_nuevo])
                        mysql.connection.commit()
                    

                editars=request.form.getlist('editar')#type 1
                if (len(editars)>0):
                    for editar in editars:
                        id_group_user=int(editar)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_campos (id_campo,id_grupo,type) VALUES (%s,%s,%s)", [id_campo_nuevo,id_group_user,1])
                        mysql.connection.commit()

                vers=request.form.getlist('ver')#type 2
                if (len(vers)>0):
                    for ver in vers:
                        id_group_user=int(ver)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_campos (id_campo,id_grupo,type) VALUES (%s,%s,%s)", [id_campo_nuevo,id_group_user,2])
                        mysql.connection.commit()        
                



                # cur = mysql.connection.cursor()
                # cur.execute("INSERT INTO campos (nombre,id_bloque,orden,type,obligatory,depende,ancho,valores) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", [nombre,orden,bloque,type_campo,ancho,obligatorio,depende,valores])
                # mysql.connection.commit()

                return redirect(url_for('campos'))


            elif p_ventas==True and p_config_campanas==False and p_campos==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==True and p_config_campanas==True and p_campos==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))
        

        return redirect(url_for('sys'))


@app.route('/campos/editar/<int:idC>',methods=('POST',))

def camposEdit(idC):

    if request.method == "POST":

        if "id" in session:

            idC=int(idC)

            id_sesion=session['id']
            id_sesion=int(id_sesion)

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_campos FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config_campanas = p_data[0][2]
            p_campos = p_data[0][3]
            cur.close()

            if p_ventas==True and p_config_campanas==True and p_campos==True:
                

                print("seccion campos")

                nombre = request.form['nombre']
                nombre = str(nombre)
                print(nombre)

                orden = request.form['orden']
                orden = int(orden)
                print(orden)

                bloque = request.form['bloque']
                bloque = int(bloque)
                print(bloque)

                type_campo = request.form['type']
                type_campo = int(type_campo)
                print(type_campo)

                ancho = request.form['ancho']
                ancho = str(ancho)
                print(ancho)

                obligatorio = request.form['obligatorio']
                if obligatorio=="True":
                    obli = True
                else:
                    obli = False
                print(obligatorio)


                estado_campos=request.form.getlist('estados')
                if (len(estado_campos)>0):
                    for estado_campo in estado_campos:
                        estado1=int(estado_campo)
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT id_pestana FROM estados WHERE id=%s", [estado1])
                        id_pestana = cur.fetchall()
                        id_pestana = id_pestana[0][0]
                        id_pestana = int(id_pestana)
                        cur.close()
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT id_campana FROM pestanas WHERE id=%s", [id_pestana])
                        id_campana = cur.fetchall()
                        id_campana = id_campana[0][0]
                        id_campana = int(id_campana)

                        cur = mysql.connection.cursor()
                        cur.execute("SELECT id_campana FROM bloques WHERE id=%s", [bloque])
                        id_campana_new = cur.fetchall()
                        id_campana_new = id_campana_new[0][0]
                        id_campana_new = int(id_campana_new)

                        if (id_campana != id_campana_new ):
                            return "campanas diferentes"


                cur = mysql.connection.cursor()
                cur.execute("UPDATE campos SET nombre=%s,id_bloque=%s,orden=%s,type=%s,obligatory=%s,ancho=%s WHERE id=%s", [nombre,bloque,orden,type_campo,obli,ancho,idC])
                mysql.connection.commit()


                if (int(request.form['depende'])>=0):

                    depende = request.form['depende']
                    depende = int(depende)
                    print(depende)

                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE campos SET depende=%s WHERE id=%s ", [depende,idC])
                    mysql.connection.commit()
                    cur.close()


                if (len(str(request.form['valores']))>0):

                    valores = request.form['valores']
                    print(valores)

                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE campos SET valores=%s WHERE id=%s ", [valores,idC])
                    mysql.connection.commit()
                    cur.close()

                
                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM estados_campos WHERE id_campo=%s", [idC])
                mysql.connection.commit()

                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM permisos_grupos_campos WHERE id_campo=%s", [idC])
                mysql.connection.commit()



                estado_campos=request.form.getlist('estados')
                if (len(estado_campos)>0):
                    for estado_campo in estado_campos:
                        estado1=int(estado_campo)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO estados_campos (id_estado,id_campo) VALUES (%s,%s)", [estado1,idC])
                        mysql.connection.commit()


                editars=request.form.getlist('editar')#type 1
                if (len(editars)>0):
                    for editar in editars:
                        id_group_user=int(editar)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_campos (id_campo,id_grupo,type) VALUES (%s,%s,%s)", [idC,id_group_user,1])
                        mysql.connection.commit()


                vers=request.form.getlist('ver')#type 2
                if (len(vers)>0):
                    for ver in vers:
                        id_group_user=int(ver)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO permisos_grupos_campos (id_campo,id_grupo,type) VALUES (%s,%s,%s)", [idC,id_group_user,2])
                        mysql.connection.commit()


                return redirect(url_for('campos'))


            elif p_ventas==True and p_config_campanas==False and p_campos==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==True and p_config_campanas==True and p_campos==False :


                return redirect(url_for('empresa_ventas'))

            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))
        

        return redirect(url_for('sys'))



@app.route('/campos/delete/<int:idC>',methods=('GET',))
def camposDelete(idC):

    if "id" in session:

        idC=int(idC)

        id_sesion=session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
        id_gruops_users = cur.fetchall()
        id_gruops_users = id_gruops_users[0][0]
        id_gruops_users = int(id_gruops_users)
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT p_empresa,p_ventas,p_config_campanas,p_campos FROM group_users WHERE id = %s", [id_gruops_users])
        p_data = cur.fetchall()
        p_ventas = p_data[0][1]
        p_empresa = p_data[0][0]
        p_config_campanas = p_data[0][2]
        p_campos = p_data[0][3]
        cur.close()

        if p_ventas==True and p_config_campanas==True and p_campos==True:

            
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM campos WHERE id=%s", [idC])
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM estados_campos WHERE id_campo=%s", [idC])
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM permisos_grupos_campos WHERE id_campo=%s", [idC])
            mysql.connection.commit()


            return redirect(url_for('campos'))


        elif p_ventas==True and p_config_campanas==False and p_campos==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==True and p_config_campanas==True and p_campos==False :


            return redirect(url_for('empresa_ventas'))

        elif p_ventas==False and p_empresa==True :
            return redirect(url_for('sys'))
        elif p_ventas==False and p_empresa==False :
            return redirect(url_for('logout'))

    return redirect(url_for('sys'))






@app.route('/recordatorios',methods=('GET','POST',))
def recordatorios():
    if request.method == 'GET':

        if "id" in session:

            id_sesion=session['id']           

            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre,user FROM users WHERE id = %s", [id_sesion])
            id_user = cur.fetchall()
            id_user = id_user[0]
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_empresa FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config = p_data[0][2]
            cur.close()

            

            if p_ventas==True:

                cur = mysql.connection.cursor()
                cur.execute("SELECT p_config_campanas,p_campanas,p_pestanas,p_estados,p_bloques,p_campos,p_reportes_ventas,p_reportes1,p_reportes2,p_config_empresa FROM group_users WHERE id = %s", [id_gruops_users])
                p_datos = cur.fetchall()
                p_config_campanas = p_datos[0][0]
                p_campanas = p_datos[0][1]
                p_pestanas = p_datos[0][2]
                p_estados = p_datos[0][3]
                p_bloques = p_datos[0][4]
                p_campos = p_datos[0][5]
                p_reportes_ventas = p_datos[0][6]
                p_reportes1 = p_datos[0][7]
                p_reportes2 = p_datos[0][8]
                p_config_empresa = p_datos[0][9]
                cur.close()
                
                
                cur.close()



                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM recordatorios")
                recordatorios = cur.fetchall()


                




                return render_template('recordatorios.html',recordatorios=recordatorios,config_empresa=p_config_empresa,username=id_user,config_campanas=p_config_campanas,campanas=p_campanas,pestanas=p_pestanas,estados=p_estados,bloques=p_bloques,campos=p_campos,reportes_ventas=p_reportes_ventas,reportes1=p_reportes1,reportes2=p_reportes2)


            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))


        return redirect(url_for('sys'))



    elif request.method == 'POST':


        if "id" in session:

            id_sesion=session['id']

            cur = mysql.connection.cursor()
            cur.execute("SELECT id_gruops_users FROM users WHERE id = %s", [id_sesion])
            id_gruops_users = cur.fetchall()
            id_gruops_users = id_gruops_users[0][0]
            id_gruops_users = int(id_gruops_users)
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("SELECT p_empresa,p_ventas,p_config_empresa FROM group_users WHERE id = %s", [id_gruops_users])
            p_data = cur.fetchall()
            p_ventas = p_data[0][1]
            p_empresa = p_data[0][0]
            p_config = p_data[0][2]
            cur.close()

            if p_ventas==True:

                nombre = request.form['nombre']
                nombre = str(nombre)

                dni = request.form['dni']
                dni = str(dni)
                
                celular = request.form['celular']
                celular = str(celular)

                fecha = request.form['fecha']

                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO recordatorios (cliente,dni,celular,fecha) VALUES (%s,%s,%s,%s) ",[nombre,dni,celular,fecha])
                mysql.connection.commit()
                cur.close()






                return redirect(url_for('recordatorios'))


            elif p_ventas==False and p_empresa==True :
                return redirect(url_for('sys'))
            elif p_ventas==False and p_empresa==False :
                return redirect(url_for('logout'))



        return redirect(url_for('sys'))





    

# Ejecutar la aplicación en el servidor local
if __name__ == '__main__':
    app.run(debug=True,host='192.168.18.5',port=3000)
