#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TK Tools That I use

Done BY :  OUZROUR
Date : 27.3.23
"""

__author__ = "Ilyas Ouzrour"
__version__ = "1.0.0"
__email__ = "ilyas.ouzrour@gmail.com"
__status__ = "Production"

# =======================
# STANDARD Libs
# =======================
# Tkinter
from tkinter import *
# IMAGE Control ( For Adding The Banner to the tkinter App)
from PIL import ImageTk, Image


def image_include(root, source: str, x: int, y: int):
    """
    Function for including the banner
    :param root: Tk Root Element
    :param source: The Source of image ( Absolute or Relative )
    :param x: position in axis of x
    :param y: position in axis of y
    :return: return a Tk label that include the image
    """
    # make the image readable with ImageTk module
    image = Image.open(source)
    imagetk = ImageTk.PhotoImage(image)
    # include it to a label
    label = Label(root, image=imagetk, borderwidth=0)
    label.image = imagetk
    label.place(x=x, y=y)
    return label


def textbox_scroll(root, x: int, y: int, height: int, width: int, font: float = 11, background: str = "white",
                   color: str = "black", position=RIGHT):
    """
    These Function add a Textbox Frame with scrollbar in the wanted position ( RIGHT / LEFT )
    :param root: Tk Root Element
    :param x: position of The Global Frame in axis of x
    :param y: position of The Global Frame in axis of y
    :param height: the height of the Textbox
    :param width: the width of the Textbox
    :param font: the size of font used ( normal : 12 )
    :param background: the background of the Textbox
    :param color: the color of the text in the Textbox
    :param position: the position of scrollbar relative to the textbox ( RIGHT / LEFT )
    :return: a TK Textbox with scrollbar in the right
    """
    # Frame
    frame = Frame(root)
    frame.place(x=x, y=y)
    # Scrollbar
    scrollbar = Scrollbar(frame)
    # Text
    text = Text(frame, height=height, width=width, yscrollcommand=scrollbar.set, bg=background, fg=color,
                font=('arial', font, 'bold'))
    # scrollbar CONFIG
    scrollbar.config(command=text.yview())
    scrollbar.pack(side=position, fill=Y)
    # text position
    text.pack(side="left")
    # Return text
    return text


def textbox(root, x: int, y: int, height: int, width: int, font: float = 11, background: str = "white",
            color: str = "black"):
    """
    These Function add a Textbox Frame with scrollbar in the wanted position ( RIGHT / LEFT )
    :param root: Tk Root Element
    :param x: position of The Global Frame in axis of x
    :param y: position of The Global Frame in axis of y
    :param height: the height of the Textbox
    :param width: the width of the Textbox
    :param font: the size of font used ( normal : 11 )
    :param background: the background of the Textbox
    :param color: the color of the text in the Textbox
    :return: a Tk TextBox
    """
    # Frame
    frame = Frame(root)
    frame.place(x=x, y=y)
    # Text
    text = Text(frame, height=height, width=width, bg=background, fg=color, font=('arial', font, 'bold'))
    # text position
    text.pack(side="left")
    # Return text
    return text


def fast_label(root, x: int, y: int, text: str, font: float, fg: str = "seagreen2", bg: str = "black"):
    """
    a short version of label to speed up my work
    :param root: Tk Root Element
    :param x: position of The Global Frame in axis of x
    :param y: position of The Global Frame in axis of y
    :param text: what this label going to contain
    :param font: the size of font used ( normal : 11 )
    :param fg: the color of the text in the Label
    :param bg: the background of the Label
    :return: A Tk Label
    """
    return Label(root, text=text, font=('arial', font, 'bold'), fg=fg, bg=bg).place(x=x, y=y)


def mainloop_fixed(root, width: float, height: float, title: str, bg: str = "black"):
    """
    start a Tk mainloop with a precise width and height ( fixed )
    :param root: Tk Root Element
    :param width: The width of the windows
    :param height: The height of the windows
    :param title: The title of the windows
    :param bg: The Color of background ( default : "black" )
    :return:None
    """
    root.geometry(str(width) + 'x' + str(height))
    root.title(title)
    root.minsize(width=width, height=height)
    root.maxsize(width=width, height=height)
    root.configure(bg=bg)
    root.mainloop()


def list_multiplechoice(root, width: int, height: int, x: float, y: float, bg: str = "white", color="black"):
    """
    Create a list of multiple choices
    :param root: Tk Root Element
    :param x: the Position of Frame (o,i)
    :param y: the Position of Frame (o,j)
    :param width: the width of the Frame
    :param height: the height of the Frame
    :param bg: the background of the list
    :param color: the color of the text of the list
    :return: Tk.Frame
    """
    # for scrolling vertically
    frame = Frame(root, bg="gray15")
    frame.place(x=x, y=y)
    yscrollbar = Scrollbar(frame)
    yscrollbar.pack(side=RIGHT, fill=Y)
    list_multiple = Listbox(frame, selectmode="multiple",
                            yscrollcommand=yscrollbar.set, bg=bg, foreground=color, width=width, height=height)

    # Widget expands horizontally and
    # vertically by assigning both to
    # fill option
    list_multiple.pack(padx=10, pady=10,
                       expand=YES, fill="both")
    # Attach listbox to vertical scrollbar
    yscrollbar.config(command=list_multiple.yview)
    return list_multiple


def selected_list_multiple(listbox):
    """
    Detect the index of the selected elements in a listbox ( multiple )
    :param listbox: the listbox ( multiple ) that we want to detect it selected elements
    :return: a list of indexes who are selected
    """
    curselection = list(listbox.curselection())
    return curselection
    # print(curselection)
    # selected_text_list = [listbox.get(i) for i in listbox.curselection()]
    # print(selected_text_list)


def empty_list(listbox):
    """
    Delete All The List ( Tk Element )  Content and Make me sure that the list going to be empty in the end
    :param listbox: The Multiple/Singe ListBox ( Tk Element )
    :return: None
    """
    # if the listbox have a size of = 0 , that mean is already empty => GOOD
    # Else if the listbox have a size diff than 0 then delete All the elements
    if listbox.size() != 0:
        listbox.delete(0, END)

