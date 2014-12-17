from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

__author__ = 'terrex'

import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

class PfcsamrApp(App):


    def build(self):

        # create a default grid layout with custom width/height
        layout = GridLayout(cols=1, padding=2, spacing=2,
                size_hint=(None, None), width=60)

        # when we add children to the grid layout, its size doesn't change at
        # all. we need to ensure that the height will be the minimum required to
        # contain all the childs. (otherwise, we'll child outside the bounding
        # box of the childs)
        layout.bind(minimum_height=layout.setter('height'))

        # add button into that grid
        for i in range(30):
            btn = Button(text=str(i), size=(48, 48),
                         size_hint=(None, None))
            layout.add_widget(btn)

        # create a scroll view, with a size < size of the grid
        left_panel = ScrollView(size_hint=(None, 1), size=(52, 320),
                do_scroll_x=False)
        left_panel.add_widget(layout)

        root = BoxLayout(cols=2)

        root.add_widget(left_panel)

        right_panel = FloatLayout(size_hint=(1, 1))

        root.add_widget(right_panel)

        return root


    def on_touch_up_2(self):
        popup = Popup(title='eyy', content=Label(text='tocado!'))
        popup.open()

if __name__ == '__main__':
        PfcsamrApp().run()
