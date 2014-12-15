__author__ = 'terrex'

import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup

class PfcsamrApp(App):

    def on_touch_up_2(self):
        popup = Popup(title='eyy', content=Label(text='tocado!'))
        popup.open()

if __name__ == '__main__':
        PfcsamrApp().run()
