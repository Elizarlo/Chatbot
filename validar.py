
from video.video import Video
from crear.crear import Documento
from correo.correo import EnviarEmail
from fotos.fotos import Foto
from pygame import mixer
import os

class Validar:
	def __init__(self):
		return


	def validar(self, mensaje,persona):
		if (mensaje == None):
			mensaje = 'Recuperado'
		os.system('google_speech -l en -o hello.mp3 "' + str(mensaje)  + '"')
		mixer.init()
		mixer.music.load('hello.mp3')
		mixer.music.play()
		tipoArchivo = ''
		if(str(persona) == 'Draven'):
			nombre = 'Erick Draven Vega Rios'
			curp = 'DRAV980505HYSMSI08'
			matricula = '1630045'
			correo = '1630045@upv.edu.mx'
		elif(str(persona) == 'Caty'):
			nombre = 'Catherine Alessandra Torres Charles'
			curp = 'TORR981010HYSED01'
			matricula = '1630060'
			correo = '1630060@upv.edu.mx'
		elif(str(persona) == 'Alfredo'):
			nombre = 'Jesus Alfredo Cardenas Castillo'
			curp = 'CATE980122HTSUWS92'
			matricula = '1630065'
			correo = '1630065@upv.edu.mx'
		elif(str(persona) == 'Armando'):
			nombre = 'José Armando Olvera Osuna'
			curp = 'CATE980122HTSUWS92'
			matricula = '1630066'
			correo = '1630066@upv.edu.mx'
		elif(str(persona) == 'Linda'):
			nombre = 'Linda Margarita Rodríguez Terán'
			curp = 'CATE980122HTSUWS92'
			matricula = '1630098'
			correo = '1630098@upv.edu.mx'
		elif(str(persona) == 'Karen'):
			nombre = 'Ana Karen Molina Pastrana'
			curp = 'MOPA980409MTMCL08'
			matricula = '1630261'
			correo = '1630261@upv.edu.mx'
		elif(str(persona) == 'Eluis'):
			nombre = 'Eluis Carlo Ramos Lucio'
			curp = 'RALE980909HTSMCL09'
			matricula = '1630261'
			correo = '1630261@upv.edu.mx'
		elif(str(persona) == 'Fernanda'):
			nombre = 'María Fernanda Baéz Zapata'
			curp = 'BAEZ900606HFDKL92'
			matricula = '1630386'
			correo = '1630386@upv.edu.mx'
		elif(str(persona) == 'Yu'):
			nombre = 'Yu Hsiang Wang'
			curp = 'WAXY900606HFDKL92'
			matricula = '1630436'
			correo = '1630436@upv.edu.mx'
		elif(str(persona) == 'Alan'):
			nombre = 'Héctor Alán De la Fuente Anaya'
			curp = 'ANAY990606HFDKLl2'
			matricula = '1630444'
			correo = '1630444@upv.edu.mx'
		elif(str(persona) == 'Genaro'):
			nombre = 'Genaro Juan Sánchez Gallegos'
			curp = 'SANG980505HTSMCK08'
			matricula = '1630099'
			correo = '1630099@upv.edu.mx'

		nombre = 'Eluis Carlo Ramos Lucio'
		curp = 'RALE980909HTSMCL09'
		matricula = '1630261'
		correo = '1630261@upv.edu.mx'



		dc = Documento()
		em = EnviarEmail()

		if (str(mensaje) == "aqui esta la cancha futbol"):
			return 'fotos/cancha.jpg'
		if (str(mensaje) == "aqui esta la cafeteria 1"):
			return 'fotos/cafeteria1.jpg'
		if (str(mensaje) == "aqui esta la cafeteria 2"):
			return 'fotos/cafeteria2.jpg'
		if (str(mensaje) == "aqui estan los tutorados"):
			return 'fotos/tutorados.jpg'
		if (str(mensaje) == "aqui estan los baños (edificio a)"):
			return 'fotos/baños.jpg'
		if (str(mensaje) == "aqui estan los planos (edificio a)"):
			return 'fotos/maqueta.jpg'
		if (str(mensaje) == "perro 1"):
			return 'fotos/perro1.jpg'
		if (str(mensaje) == "perro 2"):
			return 'fotos/perro2.jpg'
		if (str(mensaje) == "aqui esta la cancha de volleyball"):
			return 'fotos/volleyball.jpg'
		if (str(mensaje) == "aqui esta el croquis"):
			return 'fotos/croquis.jpg'
		if (str(mensaje) == "aqui esta servicios escolares"):
			return 'fotos/escolares.jpg'
		if (str(mensaje) == "aqui esta la biblioteca"):
			return 'fotos/biblioteca.jpg'
		if (str(mensaje) == "aqui esta cai"):
			return 'fotos/cai.jpg'
		if (str(mensaje) == "edificio a"):
			return 'fotos/edificiob.jpg'
		if (str(mensaje) == "edificio b"):
			return 'fotos/edificiob.jpg'
		if (str(mensaje) == "edificio c"):
			return 'fotos/edificioc.jpg'
		if (str(mensaje) == "edificio h"):
			return 'fotos/edificioh.jpg'
		if (str(mensaje) == "edificio i"):
			return 'fotos/edificioi.jpg'

		if (str(mensaje) == "enviare la referencia de constancia"):
			tipoArchivo = 'constancia'

		if (str(mensaje) == "enviare la referencia de credencial de estudiante"):
			tipoArchivo = 'credencial'

		if (str(mensaje) == "enviare la referencia bancaria de historial"):
			tipoArchivo = 'historial'

		if (str(mensaje) == "enviare la referencia bancaria de toefl"):
			tipoArchivo = 'toefl'

		if (str(mensaje) == "enviare la referencia bancaria de kardex a tu email"):
			tipoArchivo = 'kardex'

		if(tipoArchivo != ''):
			dc.main(nombre,curp,matricula,correo,tipoArchivo)
			em.main(tipoArchivo,correo)
		return '0'
