__author__ = 'terrex'

from kivy.app import App
from kivy.uix.button import Button


class TestApp(App):
    def build(self):
        self.root_window
        return Button(text='Hello World')

TestApp().run()
