
from video.video import Video
from crear.crear import Documento
from correo.correo import EnviarEmail
from fotos.fotos import Foto
from pygame import mixer
import os

class Validar:
	def __init__(self):
		print('')
		return


	def validar(self, mensaje):
		print(str(mensaje))
		if (mensaje == None):
			mensaje = 'Recuperado'
		os.system('google_speech -l en -o hello.mp3 "' + str(mensaje)  + '"')
		mixer.init()
		mixer.music.load('hello.mp3')
		mixer.music.play()
		nombre = 'Eluis Carlo Ramos Lucio'
		curp = 'RALE980909HTSMCL09'
		matricula = '1630261'
		correo = '1630261@upv.edu.mx'
		tipoArchivo = ''

		dc = Documento()
		em = EnviarEmail()
		video = Video()
		foto = Foto()

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
		if (str(mensaje) == "aqui esta el video promocional"):
			video.mainVideo('video/promocional1.mp4')
			return
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