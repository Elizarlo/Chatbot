from __future__ import print_function
#Librerias para el funcionamiento del chatbot
import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from oauth2client import file
from crear.crear import Documento
from correo.correo import EnviarEmail
from validar import Validar
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

#Librerias para las interfaces
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image

#Librerias para vision
import requests
import json
import cv2

#Hilo
import threading
import time
from kivy.clock import mainthread

imagen = '0'
imagenMuestra = ''
i = 0
persona = ''
validacion = ''
ip = '148.247.204.59'


#Pantalla de menu principal--------------------------------------------------------------------------
class MenuWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global imagenMuestra

        self.titulo = Label(markup=True, text="Sistema Inteligente UPV" , size_hint=(0.8, 0.2), pos_hint= {"x":0.4, "y":0.7},
            font_size = (Window.size[0]**2 + Window.size[1]**2) / 14**4)

        self.btn = Button(text ='Chat Bot', size_hint =(0.6,0.2), pos_hint ={"x": 0.2, "y":0.5})

        self.btn.bind(on_press=self.chatbot_pantalla)

        #imagenMuestra = Image(source='imagen/imagen0.png', size_hint =(0.5,0.5), pos_hint ={"x": 0.3, "y":0.2})


        with self.canvas:
            Rectangle(pos= self.pos, size= (Window.size[0],Window.size[1]), source = 'fondo.png')
            Rectangle(pos=(Window.size[0]*0.8,Window.size[1]*0.8), size= (Window.size[0]*0.2,Window.size[1]*0.2), source = 'logo.png')

        # Add text widget to the layout
        #self.add_widget(imagenMuestra)
        self.add_widget(self.titulo)
        #self.add_widget(self.btn)
        self.iniciar_hilo()

    def chatbot_pantalla(self):
        sistema.create_chat_page()
        sistema.screen_manager.current = 'chatbot'
        sistema.screen_manager.transition.direction = "left"

    def iniciar_hilo(self, *args):
        t = threading.Thread(target=self.worker)
        t.start()

    def worker(self):
        global i
        i+=1
        self.update_label(i)


    @mainthread
    def update_label(self,i):
        global persona,validacion
        addr = 'http://'+ ip + ':5000'
        test_url = addr + '/api/test'

        # prepare headers for http request
        content_type = 'image/jpeg'
        headers = {'content-type': content_type}

        cam = cv2.VideoCapture(0)
        ret_val, img = cam.read()
        cv2.imwrite("imagen/imagen"+ str(i) +".png",img)
        # encode image as jpeg
        _, img_encoded = cv2.imencode('.png', img)

        # send http request with image and receive response
        try:
            response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
            # decode response
            print(json.loads(response.text))
        except:
            print('error')

        cv2.destroyAllWindows()
        #time.sleep(1)
        imagen = 'imagen/imagen'+ str(i) +'.png'
        imagenMuestra = Image(source=imagen, size_hint =(0.4,0.55), pos_hint ={"x": 0.15, "y":0.350})
        self.add_widget(imagenMuestra)
        os.remove(imagen)
        mensaje = ''
        try:
            mensaje = str(json.loads(response.text))
            if(mensaje != 'Desconocido'):
                persona = mensaje
            else:
                mensaje = ''
        except:
            mensaje = ''
        if(mensaje == ''):
            self.iniciar_hilo()
        else:
            if(validacion == ''):
                validacion = mensaje
                self.iniciar_hilo()
            else:
                if(validacion == mensaje):
                    self.chatbot_pantalla()
                else:
                    validacion = ''
                    self.iniciar_hilo()

#------------------------------------------------------------------------------------------------------


#Pantalla de chat bot--------------------------------------------------------------------------
class ChatBotWindow(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(size=self.adjust_fields)
        # We are going to use 1 column and 2 rows
        self.cols = 1
        self.rows = 3

        self.btn = Button(text ='Menu', width=Window.size[0]*0.1)

        self.btn.bind(on_press=self.menu_pantalla)

        # Add text widget to the layout
        self.add_widget(self.btn)

        self.history = ScrollableLabel(height=Window.size[1]*0.9, size_hint_y=None)
        self.add_widget(self.history)

        # In the second row, we want to have input fields and Send button
        # Input field should take 80% of window width
        # We also want to bind button click to send_message method
        self.new_message = TextInput(width=Window.size[0]*0.8, size_hint_x=None, multiline=False)
        self.send = Button(text="Enviar")
        self.send.bind(on_press=self.send_message)

        # To be able to add 2 widgets into a layout with just one collumn, we use additional layout,
        # add widgets there, then add this layout to main layout as second row
        bottom_line = GridLayout(cols=2)
        bottom_line.add_widget(self.new_message)
        bottom_line.add_widget(self.send)
        self.add_widget(bottom_line)

        # To be able to send message on Enter key, we want to listen to keypresses
        Window.bind(on_key_down=self.on_key_down)

        # We also want to focus on our text input field
        # Kivy by default takes focus out out of it once we are sending message
        # The problem here is that 'self.new_message.focus = True' does not work when called directly,
        # so we have to schedule it to be called in one second
        # The other problem is that schedule_once() have no ability to pass any parameters, so we have
        # to create and call a function that takes no parameters
        Clock.schedule_once(self.focus_text_input, 1)

        # And now, as we have out layout ready and everything set, we can start listening for incimmong messages
        # Listening method is going to call a callback method to update chat history with new messages,
        # so we have to start listening for new messages after we create this layout

        self.chatbot = ChatBot(
            "Jarvis",
            trainer='chatterbot.trainers.ChatterBotCorpusTrainer' ,
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch'
                }
            ]
        )


        # Create a new trainer for the chatbot
        #self.trainer = ChatterBotCorpusTrainer(self.chatbot)

        #self.trainer.train("./datos.yml")

        self.history.update_chat_history('[color=20dd20]ChatBot[/color] > Bienvenido al sistema de Ayuda UPV ' + str(persona) + ' para comenzar puedes preguntarme por ayuda, yo te guiaré.', 2)


    def menu_pantalla(self, _):
        sistema.screen_manager.current = 'menu'
        sistema.screen_manager.transition.direction = "right"

    # Gets called on key press
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):

        # But we want to take an action only when Enter key is being pressed, and send a message
        if keycode == 40:
            self.send_message(None)

    # Gets called when either Send button or Enter key is being pressed
    # (kivy passes button object here as well, but we don;t care about it)
    def send_message(self, _):

        # Get message text and clear message input field
        message = self.new_message.text
        self.new_message.text = ''

        # If there is any message - add it to chat history and send to the server
        if message:
            # Our messages - use red color for the name
            self.history.update_chat_history('[color=dd2020]Usuario[/color] >' + str(message), 1)

            bot_response = self.chatbot.get_response(message)
            global imagen

            vali = Validar()
            imagen = '0'
            imagen = vali.validar(bot_response,persona)

            self.history.update_chat_history('[color=20dd20]ChatBot[/color] > ' + str(bot_response), 2)

            #socket_client.send(message)

        # As mentioned above, we have to shedule for refocusing to input field
        Clock.schedule_once(self.focus_text_input, 0.1)


    # Sets focus to text input field
    def focus_text_input(self, _):
        self.new_message.focus = True

    def adjust_fields(self, *_):

        # Chat history height - 90%, but at least 50px for bottom new message/send button part
        if Window.size[1] * 0.1 < 50:
            new_height = Window.size[1] - 50
        else:
            new_height = Window.size[1] * 0.9
        self.history.height = new_height

        # New message input width - 80%, but at least 160px for send button
        if Window.size[0] * 0.2 < 160:
            new_width = Window.size[0] - 160
        else:
            new_width = Window.size[0] * 0.8
        self.new_message.width = new_width

        # Update chat history layout
        self.history.update_chat_history_layout()
        Clock.schedule_once(self.history.update_chat_history_layout, 0.01)

#------------------------------------------------------------------------------------------------


#Scroll--------------------------------------------------------------------------------------------
class ScrollableLabel(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ScrollView does not allow us to add more than one widget, so we need to trick it
        # by creating a layout and placing two widgets inside it
        # Layout is going to have one collumn and and size_hint_y set to None,
        # so height wo't default to any size (we are going to set it on our own)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.layout.bind(minimum_height= self.layout.setter("height"))
        self.add_widget(self.layout)

    # Methos called externally to add new message to the chat history
    def update_chat_history(self, message, tipo):

        # First add new line and message itself
        #self.chat_history.text += '\n' + message

        if(tipo == 1):
            texto = Label(markup=True, text=message, size = (Window.size[0], Window.size[1]*0.1) , size_hint=(None, None), halign="right")

        else:
            texto = Label(markup=True, text=message, size = (Window.size[0], Window.size[1]*0.1) , size_hint=(None, None), halign="left")

        texto.text_size = texto.size

        self.layout.add_widget(texto)
        global imagen
        if(imagen != '0'):
            imagenVer = Image(source=imagen, size = (250,120) , size_hint=(None, None))
            self.layout.add_widget(imagenVer)
            imagen = '0'

        self.scroll_to(texto)


    def update_chat_history_layout(self, _=None):
        # Set layout height to whatever height of chat history text is + 15 pixels
        # (adds a bit of space at the bottom)
        # Set chat history label to whatever height of chat history text is
        # Set width of chat history text to 98 of the label width (adds small margins)
        print("")
        #self.layout.height = self.chat_history.texture_size[1] + 15
        #self.chat_history.height = self.chat_history.texture_size[1]
        #self.chat_history.text_size = (self.chat_history.width * 0.98, None)
#------------------------------------------------------------------------------------------------


#Main--------------------------------------------------------------------------------------------
class MyMainApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.menu = MenuWindow()
        screen = Screen(name='menu')
        screen.add_widget(self.menu)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

    def create_chat_page(self):
        self.chatbot = ChatBotWindow()
        screen = Screen(name='chatbot')
        screen.add_widget(self.chatbot)
        self.screen_manager.add_widget(screen)


if __name__ == "__main__":
    #Window.fullscreen = True
    sistema = MyMainApp()
    sistema.run()



#-----------------------------------------------------------------------------------------------
