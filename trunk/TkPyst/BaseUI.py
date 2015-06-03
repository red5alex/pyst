__author__ = 'are'

# command_properties.py
import sys
import tkinter as tk
from tkinter import messagebox
import pygubu

# define the function callbacks
def on_buttonOK_click():
    messagebox.showinfo('Message', 'You clicked OK')
        
def on_buttonCancel_click():
    sys.exit()

class BaseApplication(pygubu.TkApplication):

    def _create_ui(self):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('vBaseUI.ui')

        #3: Create the widget using self.master as parent
        self.mainwindow = builder.get_object('Toplevel_1', self.master)

        # Configure callbacks
        callbacks = {
            'on_buttonOK_clicked': on_buttonOK_click,
            'on_buttonCancel_clicked': on_buttonCancel_click,
        }

        builder.connect_callbacks(callbacks)


if __name__ == '__main__':
    root = tk.Tk()
    app = BaseApplication(root)
    app.run()
