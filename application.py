#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A Tk Application for Watching the work
of the PowerMta 4 to control the "send rate"
( to prevent to be blacklisted ) . Every App Can
Control Up To 10 PowerMta 4 Websites .

I Hope you Enjoy It !

Done BY :  OUZROUR
Date : 13.4.23
"""

__author__ = "Ilyas Ouzrour"
__version__ = "1.0.0"
__email__ = "ilyas.ouzrour@gmail.com"
__status__ = "Production"

# =======================
# STANDARD Libs
# =======================

# Os Library
import os
# To Delay the time between checking
import time
# To open the link after finishing
import webbrowser
# To Get The HTML to be Parsed with Beautiful Soup
import requests
# To Scrap The Data From The HTML
from bs4 import BeautifulSoup
# To Avoid The Conflict with the mainloop ( Tkinter ) that block the GUI
from threading import Thread
# used to know the exact path
import sys
# used to play the sound of the warning
import playsound
# =======================
# Local Libs
# =======================
# contain all Functions + Tkinter are called into it
import tkinter_tools as tkt

# List of Booleans , it contains the Check Status ( True = Allowed
# / False = Not Allowed ) for Each row ( this gonna help us in to
# get out the while loop in the check test )

permissions = list()


# For Packaging with Pyinstaller in the end ( The path must be relative )
def resource_path(relative_path):
    """
    Change the relative path to an absolute
    Path ( to be used in Packaging with Pyinstaller )
    :param relative_path: The Relative Path
    """
    # Try to Get the base path ( for all OS )
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    # return the absolute path
    return os.path.join(base_path, relative_path)


def app(root):
    """
    The Main Logic of the application
    :param root: The Root Element ( TK )
    :return: None
    """
    # The Image in the header
    tkt.image_include(root, resource_path("header.png"), 0, 0)
    # The Globalisation of Variable "Permissions" defined Out this function
    global permissions

    # this variable going to represent the position of the element in the previous list ( rows )
    i = 0
    # a for loop that fill the distance x1=4 -> x2=4 / y1=180 -> y2->650 ,
    # with rows with a height of 50px ( translation by y = 50px while x is fixed = 4 )
    for position_y in (range(180, 650, 50)):
        # include the information using the function label_per_row
        # and inject them in the list(rows) ( row of position "i"  )
        label_per_row(root, 4, position_y, i)
        # move to the next position
        i = +1
        # inject True as the first option in the list of permissions (
        # watch out that "i" is unneeded , so the i = +1 don't go to
        # affect the permissions list , the most important is the
        # number of iteration , which in this case is 10 , so the list
        # going to include 10 True )
        permissions.append(True)
    # the last panel that give an explication of how this application work
    explication(root, 0, 652)


def label_and_textbox(root, x: int, shiftx: int, y: int, text: str, height: int, width: int, font: float = 8,
                      color: str = "DarkGoldenrod1", ):
    """
    Create a Tk Label with a textbox below it .
    :param root: The Main Root Element
    :param x: the position of the start ( in x direction )
    :param shiftx: the number of pixel to be translated from the position of start ( in x direction )
    :param y: the position of the start ( in y direction )
    :param text: the Text of the Label
    :param height: the height of the textbox ( number of rows )
    :param width: the width of the textbox ( number of columns )
    :param font: the size of the font
    :param color: the color of label's text
    :return: Textbox ( TK element )
    """
    # a short tkt ( library ) function to create label
    tkt.fast_label(root, x + shiftx, y - 17, text, font, color)
    # a short tkt ( library ) function to textbox
    # it return it to control it
    return tkt.textbox(root, x + shiftx, y, height, width)


def label_per_row(root, x_start: int, y_start: int, position: int):
    """
    The Main and Global Row , this function control each element in the row :
    canvas , name , ip , port , S/H(%) , total(%), refresh (s), button Start , button Stop ,
    button Restart .
    :param root: the main Element to be attached to
    :param x_start: the position of the start of the row ( in direction of x )
    :param y_start: the position of the start of the row ( in direction of x )
    :param position: the position of this row compared to the others ( ex : 0 - 9 if there is 10 rows)
    :return: Just Create the row
    """

    # =======================
    # Canvas Creation
    # =======================

    # Creation of the canvas
    canvas = tkt.Canvas(width=20, height=20, bg="black", border=0, highlightthickness=0)
    # Positioning the canvas to the first (x,y) of the row
    canvas.place(x=x_start, y=y_start)
    # Creating a circle using create_oval function and fill it with "gray81" ( Stopped )
    canvas.create_oval(5, 5, 15, 15, width=0, fill="gray81")

    # =======================
    # Textboxes and their labels
    # =======================

    # name : label + Textbox
    name = label_and_textbox(root, x_start, 20, y_start, "NAME", 1, 19)
    # IP/DNS : label + Textbox
    ip = label_and_textbox(root, x_start, 118 + 60, y_start, "IP / DNS", 1, 15)
    # PORT : label + Textbox
    port = label_and_textbox(root, x_start, 244 + 60, y_start, "PORT", 1, 4)
    # Rate Per H : label + Textbox
    rate_par_h = label_and_textbox(root, x_start, 283 + 60, y_start, "S/H(%)", 1, 5)
    # Total : label + Textbox
    total = label_and_textbox(root, x_start, 330 + 60, y_start, "total(%)", 1, 5)
    # Link : label + Textbox
    link = label_and_textbox(root, x_start, 376 + 60, y_start, "Link", 1, 20)
    # time : label + Textbox
    refresh = label_and_textbox(root, x_start, 542 + 60, y_start, "Refresh(s)", 1, 6, 7)

    # =======================
    # Buttons
    # =======================

    # Start : Start the process of watch
    # Created with Thread To Control avoid the conflict with the mainloop of the Tkinter
    # Without Thread , the while loop while obligate the mainloop to wait until it finished ,
    # which gonna cause the Freeze of the GUI ( Not Responding Window .. )

    tkt.Button(root, text="START", bg="chartreuse4", font=('arial', 8, 'bold'), fg="white", highlightthickness=0,
               command=lambda: Thread(target=start,
                                      args=(
                                          canvas, name, ip, port, rate_par_h, total, link, refresh, position)).start()) \
        .place(x=x_start + 600 + 60, y=y_start)

    # END : End The Process of watch
    tkt.Button(root, text="STOP", bg="firebrick3", font=('arial', 8, 'bold'), fg="white", highlightthickness=0,
               command=lambda: stop(canvas, position)) \
        .place(x=x_start + 648 + 60, y=y_start)

    # RESET : Stop The Process + Clean all the Textboxes
    tkt.Button(root, text="RESET", bg="gray40", font=('arial', 8, 'bold'), fg="white", highlightthickness=0,
               command=lambda: reset(canvas, name, ip, port, rate_par_h, total, link, refresh, position)) \
        .place(x=x_start + 690 + 60, y=y_start)


def play(music):
    """
    Play A sound with the library playsound
    :param music: The name of the file that you want to play , ex: "test.mp3"
    :return: Nothing . Just play the music
    """
    # using playsound function of the playsound library to play a song
    # the path is absolute to avoid problems when we gonna package it
    # with Pyinstaller
    playsound.playsound(resource_path(music), True)

def start(canvas, name, ip_widget, port, rate_per_h_widget, total_widget, link, refresh, position):
    """
    Start the process of watch . this function is related to a 1 unique row in position k .
    :param canvas: the circle canvas of the row
    :param name: the textbox of the name
    :param ip_widget: the textbox of the ip
    :param port: the textbox of the port
    :param rate_per_h_widget: the textbox of the S/H(%)
    :param total_widget: the textbox of the total(%)
    :param link: the textbox of the link
    :param refresh: the textbox of the refresh(s)
    :param position: the position of this row compared to the others
    :return: Nothing , it just starts The Process
    """
    # I used Try to avoid the problems caused by Connection or unreachable IP/Dns
    try:

        # Re-assign the Permission of this row for watching to True ( Watch Mod = Activated )
        permissions[position] = True

        # =======================
        # Colorization of the Canvas and Textboxes
        # =======================

        # Colorization of the circle canvas with "lime" color
        canvas.create_oval(5, 5, 15, 15, width=0, fill="lime")

        # Reset The Default Colorization to the name textbox ( White BG with Black Font )
        name.config({"background": "white", "fg": "black"})
        # Reset The Default Colorization to the ip textbox( White BG with Black Font )
        ip_widget.config({"background": "white", "fg": "black"})
        # Reset The Default Colorization to the S/H(%) textbox ( White BG with Black Font )
        rate_per_h_widget.config({"background": "white", "fg": "black"})
        # Reset The Default Colorization to the total(%) textbox ( White BG with Black Font )
        total_widget.config({"background": "white", "fg": "black"})

        # =======================
        # Get The Contents of The Textboxes to use them
        # =======================

        # ip content
        ip = ip_widget.get(1.0, "end-1c")
        # port content
        port = port.get(1.0, "end-1c")
        # S/H(%) content
        rate_per_h = rate_per_h_widget.get(1.0, "end-1c")
        # total(%) content
        total = total_widget.get(1.0, "end-1c")
        # link content
        link = link.get(1.0, "end-1c")
        # refresh(s) content
        times = refresh.get(1.0, "end-1c")

        # =======================
        # IP/DNS Fixer
        # =======================

        # initialisation of the ips as empty string
        ips = ""
        # if the ip/dns include the "https" word ,
        # then the person have entered a website ( so we must leave it like it was )
        if ip.find("https") != -1:
            ips = ip
        # The Same thing here also ( the word = "http" )
        elif ip.find("http") != -1:
            ips = ip
        # else if the ip/dns don't contain any of the word "http" or "https" , then it for sure ip or an unknown dns,
        # so I preferred going with http then SSL https because in my knowledge , all the PowerMta4 are installed
        # without an SSL certificate
        else:
            ips = "http://" + ip

        # =======================
        # The Watch Loop
        # =======================

        # Loop Only if The Permission is Allowed ( True )
        while permissions[position]:

            # =======================
            # Scraping The Data From The PMTA4
            # =======================

            # get the content of the dns/ip and inject it to this variable
            soup = BeautifulSoup(requests.get(ips + ":" + port).content, "html.parser")

            # extract and inject into this variable , the 2 values : (in,out) from the row of "total"
            total_real = extractor(soup)
            # extract and inject into this variable , the 2 values : (in,out) from the row of "last hour"
            rate_per_hour_real = extractor(soup, "hour")

            # =======================
            # Creating Conditions to Stop the watch mod
            # =======================

            # A condition based on S/H(%) value , the condition is false if 1 of these 3 rules aren't verified:
            # 1. the S/H(%) textbox isn't empty
            # 2. the scrapped "in" value of S/H(%) value is different from 0 ( division per 0 is impossible )
            # 3. the ratio (%) : " out/in x 100 " is less than the Value of S/H(%) .
            # The S/H (%) represent the Minimum that this value can reach

            condition_hour = len(rate_per_h) != 0 and rate_per_hour_real[0] != 0 and rate_per_hour_real[1] / \
                             rate_per_hour_real[0] * 100 < float(
                rate_per_h)

            # A condition based on total(%) value , the condition is false if 1 of these 3 rules aren't verified:
            # 1. the total(%) textbox isn't empty
            # 2. the scrapped "in" value of total(%) value is different from 0 ( division per 0 is impossible )
            # 3. the ratio (%) : " out/in x 100 " is less than the Value of total .
            # The total(%) represent the Minimum that this value can reach

            condition_total = len(total) != 0 and total_real[0] != 0 and total_real[1] / total_real[0] * 100 < float(
                total)

            # =======================
            # the impact of the realization of one of the 2 conditions
            # =======================

            if condition_hour or condition_total:
                # =======================
                # Colorization
                # =======================

                # Colorization of the circle canvas with "red" color
                canvas.create_oval(5, 5, 15, 15, width=0, fill="red")
                # Colorization of the name textbox with "pink" color to catch attention
                name.config({"background": "hot pink", "fg": "black"})
                # Colorization of the ip textbox with "pink" color to catch attention
                ip_widget.config({"background": "hot pink", "fg": "black"})
                if condition_hour:
                    # if the condition of S/H(%) is verified : Colorize the textbox of it with "pink" color
                    rate_per_h_widget.config({"background": "hot pink"})
                    # Play The Sound of beep ( to alert the user )
                    play('beep.mp3')
                if condition_total:
                    # if the condition of total(%) is verified : Colorize the textbox of it with "pink" color
                    total_widget.config({"background": "hot pink"})
                    # Play The Sound of beep ( to alert the user )
                    play('beep.mp3')
                # =======================
                # Redirection and shutdown the watch mod
                # =======================

                # if the link textbox isn't empty
                if len(link) != 0:
                    # redirect to the link
                    try :
                        # I prefer working with firefox , and not the spytool named "chrome"
                        # to recognize firefox as the browser that I want to work with
                        webbrowser.register('firefox',
                                            None,
                                            webbrowser.BackgroundBrowser(
                                                "C://Program Files//Mozilla Firefox//firefox.exe"))
                        # now , webrowser gonna open the wanted url with the software named "firefox"
                        # ( or whatever you want , the name is just for using them and not specially the name
                        # of the browser itself ) who is direction is "C:...." , in a NEW TAB ( to avoid
                        # the multiple windows problem ) .
                        webbrowser.get("firefox").open_new_tab(link)
                    except:
                        webbrowser.open(link,2)
                # set the permission as denied ( False )
                permissions[position] = False
                # End The Loop While immediately ( The End of the watch mod )
                break

            # if the refresh(s) textbox isn't empty , then : delay the repetition of the code for this value
            if len(times) != 0:
                time.sleep(float(times))
            # delay the repetition of the code for 1 second ( to avoid the while "desaster effect" )
            else:
                time.sleep(1)
    # if any other error happened
    except :
        # Colorize the circle canvas with "orange" color
        canvas.create_oval(5, 5, 15, 15, width=0, fill="orange")


def extractor(soup, wanted: str = "total"):
    """
    A function to Extract the 2 values In / Out From The Scraped HTML page
    :param soup: the scraped page
    :param wanted: "total" or "hour" , this param specify the wanted value
    :return: ( in , out ) corresponding to the wanted value : total or per hour
    """
    # First , we Detect the <tr></tr> that have "width:340" as attribute ,
    # after that , we search for all <tr> that included into it and we all of them into a variable "tr"
    tr = soup.find("td", attrs={'width': 340}).findAll('tr')

    # if we wanted the in / out corresponding to the "total" value
    if wanted == "total":
        # after my analysis , I detected that the second "tr" is the one that include ( In / Out ) for "total"
        total = tr[2]
    # if we wanted the in / out corresponding to the "per hour" value
    else:
        # after my analysis , I detected that the second "tr" is the one that include ( In / Out ) for "per hour"
        total = tr[3]

    # when the choice of variable to be used is done ( "total" or "per hour" ) ,
    # we inject the IN and OUT from the variables chosen to the 2 variables

    total_in = int(total.findAll("td")[0].get_text().replace(",", ""))
    total_out = int(total.findAll("td")[1].get_text().replace(",", ""))

    # Return the result (IN,OUT)
    return total_in, total_out


def stop(canvas, position):
    """
    Function to stop The Watch Mod
    :param canvas: the circle canvas ( we gonna change the color )
    :param position: the position of the row ( to control it )
    :return: Just stop the watch mod
    """
    # Recolorize to gray81 again
    canvas.create_oval(5, 5, 15, 15, width=0, fill="gray81")
    # Set up the permission of row in position "i" to False ( if the while loop
    # in the start function is running ... he gonna break immediately )
    permissions[position] = False


def delete_textbox(widget):
    """
    Delete The Content of the textbox.
    :param widget: The Textbox Widget that you want to delete it content.
    :return: Nothing , Just Delete the content.
    """
    # Delete All The Content of The Textbox
    widget.delete(1.0, tkt.END)


def reset(canvas, name, ip_widget, port, rate_per_h_widget, total_widget, link, refresh, position):
    """
    A function that clean all textbox and stop the Process of watching
    :param canvas: the circle canvas of the row
    :param name: the textbox of the name
    :param ip_widget: the textbox of the name
    :param port: the textbox of the port
    :param rate_per_h_widget: the textbox of the S/H(%)
    :param total_widget: the textbox of the total(%)
    :param link: the textbox of the link
    :param refresh: the textbox of the refresh(s)
    :param position: the position of this row compared to the other rows
    :return: Nothing . Just clean all the tabs + Stop the Process
    """
    # =======================
    # Stop The Process
    # =======================

    # use the function "stop" to stop the process of watching
    stop(canvas, position)

    # =======================
    # Decolorization of colorized boxes
    # =======================

    # decolorization of the textbox : name
    name.config({"background": "white", "fg": "black"})
    # decolorization of the textbox : ip/dns
    ip_widget.config({"background": "white", "fg": "black"})
    # decolorization of the textbox : S/H(%)
    rate_per_h_widget.config({"background": "white", "fg": "black"})
    # decolorization of the textbox : total(%)
    total_widget.config({"background": "white", "fg": "black"})

    # =======================
    # Empty all the textboxes
    # =======================
    # Delete All the content of the textbox : name
    delete_textbox(name)
    # Delete All the content of the textbox : ip/dns
    delete_textbox(ip_widget)
    # Delete All the content of the textbox : port
    delete_textbox(port)
    # Delete All the content of the textbox : S/H(%)
    delete_textbox(rate_per_h_widget)
    # Delete All the content of the textbox : total(%)
    delete_textbox(total_widget)
    # Delete All the content of the textbox : link
    delete_textbox(link)
    # Delete All the content of the textbox : refresh(s)
    delete_textbox(refresh)


def label_and_explication_short(root, pos_x, pos_y, shiftx, name, definition):
    """
    A function to create 2 labels : 1st for the term to be explained , and 2nd 
    for the explication ( this function is useful for the explication tha can 
    be done in just 1 line )
    :param root: the Main Root Element ( Tk Element ) 
    :param pos_x: the position of the start of the explication ( in direction of x )
    :param pos_y: the position of the start of the explication ( in direction of y )
    :param shiftx: the distance between the term and the explication
    :param name: the term that you want to explain
    :param definition: the explication
    :return: Nothing . It just creates 2 labels 
    """
    # create a label for the term 
    tkt.fast_label(root, pos_x, pos_y, name, 8, "DarkGoldenrod1")
    # create a label for the explication ( shifted with x px in direction of x) 
    tkt.fast_label(root, pos_x + shiftx, pos_y, definition, 8, "white")


def label_and_explication_long(root, pos_x, pos_y, shiftx, shifty, name, definition_part1, definition_part2):
    """
    A function to create 2 labels : 1st for the term to be explained , and 2nd 
    for the explication ( this function is useful for the explication tha can 
    be done in 2 lines )
    :param root: the Main Root Element ( Tk Element ) 
    :param pos_x: the position of the start of the explication ( in direction of x )
    :param pos_y: the position of the start of the explication ( in direction of y )
    :param shiftx: the distance between the term and the explication ( in direction of x )
    :param shifty: the distance between the term and the explication ( in direction of y )
    :param name: the term that you want to explain
    :param definition_part1: the explication ( 1st line )
    :param definition_part2: the explication ( 2nd line )
    :return: Nothing . It just creates 2 labels 
    """
    # create a label for the term 
    tkt.fast_label(root, pos_x, pos_y, name, 8, "DarkGoldenrod1")
    # create a label for the explication ( shifted with x px in direction of x) 
    tkt.fast_label(root, pos_x + shiftx, pos_y, definition_part1, 8, "white")
    # create a label for the explication ( shifted with the same x px in direction of x and y in direction of y ) 
    tkt.fast_label(root, pos_x + shiftx, pos_y + shifty, definition_part2, 8, "white")


def canvas_explication(root, pos_x, pos_y, shiftx, color, definition):
    """
    A function that create a colored circle canvas and a label to explain the signification of this color
    :param root: the Main Root Element ( Tk Element )
    :param pos_x: the position of the start of the explication ( in direction of x )
    :param pos_y: the position of the start of the explication ( in direction of y )
    :param shiftx: the distance between the term and the explication ( in direction of x )
    :param color: the color of the circle canvas
    :param definition: the explication of the color
    :return: Nothing . Just Create a colored circle canvas with the signification of this color
    """
    # create the canvas
    canvas = tkt.Canvas(root, width=20, height=20, bg="black", border=0, highlightthickness=0)
    # place it to the right position ( the start of x and y )
    canvas.place(x=pos_x, y=pos_y)
    # creating a circle into this canvas and fill it with a variable color
    canvas.create_oval(5, 5, 15, 15, width=0, fill=color)
    # create a label that explain the signification of this color
    # ( shifted from the canvas with "shiftx" pixels in direction of x )
    tkt.fast_label(root, pos_x + shiftx, pos_y, definition, 8, color)


def explication(root, x, y):
    """
    A Function that include All the explications of the app to help the user
    to well use this tool ( positioned in the bottom )
    :param root: the Main Root Element ( Tk Element )
    :param x: the position of the start of the explication ( in direction of x )
    :param y: the position of the start of the explication ( in direction of y )
    :return: Nothing . Just create the frame that include all the necessary elements
    """
    # =======================
    # Creation of the Frame
    # =======================

    # Create The Frame ( the height is selected with calculating the equation :
    # 800 ( the size total of windows ) =  652 (the value of y , fixed in the app function ) + height ( of the frame )
    # so , height = 800 - 652 = 148
    frame = tkt.Frame(root, bg="black", height=148, width=800)
    # Place it to the position of the start
    frame.place(x=x, y=y)

    # =======================
    # Explications
    # =======================

    # Explication 1 line: Name
    label_and_explication_short(frame, 0, 5, 40, "Name : ", "(STRING) The Name of The Server")
    # Explication 1 line: Ip/Dns
    label_and_explication_short(frame, 0, 25, 46, "IP/DNS : ", "(STRING) The IP of The Server")
    # Explication 1 line: Port
    label_and_explication_short(frame, 0, 45, 40, "PORT : ", "(NUMBER) The PORT of The Server")
    # Explication 1 line: Link
    label_and_explication_short(frame, 0, 65, 40, "Link : ",
                                "(STRING) The Link where you want to be redirected when 1 of the Tests Fail")
    # Explication 1 line: Refresh
    label_and_explication_short(frame, 0, 85, 56, "Refresh : ",
                                "(NUMBER) Number of second to wait between tests , Recommanded : 5 "
                                ". ( The More = The Best = The Less Ress. consumption )")
    # =====================================
    # Explication 2 lines: S/H(%)
    label_and_explication_long(frame, 430, 5, 50, 17, 'S/H(%) :', "(NUMBER between 1-100) The Minimum % wanted value ",
                               "for the Ratio (OUT/IN) per Hour .")
    # Explication 2 lines: total(%)
    label_and_explication_long(frame, 430, 45, 50, 17, 'total(%) :',
                               "(NUMBER between 1-100) The Minimum % wanted value ",
                               "for the Ratio (OUT/IN) [in total] .")
    # =====================================
    # Explication Color , 1 line: gray
    canvas_explication(frame, 2, 108, 20, "gray81", "Inactive/Stopped", )
    # Explication Color , 1 line: lime
    canvas_explication(frame, 200, 108, 20, "lime", "In Work ( Watch Mod )")
    # Explication Color , 1 line: red
    canvas_explication(frame, 400, 108, 20, "red", "Test Failure ")
    # Explication Color , 1 line: orange
    canvas_explication(frame, 580, 108, 20, "orange", "Wrong URL / Connection Problem")

    # =======================
    # Footer
    # =======================

    # The Footer
    tkt.fast_label(frame, 250, 130, "CREATED BY: OUZROUR ILYAS (2023) . I Hope You Enjoy It ;)", 7, "gold")


def on_closing(root):
    """
    A function to be executed before closing the window .
    we must change the value to all permissions to False . Otherwise , the loop don't gonna
    be ended and even if you close the window , the Thread gonna keep working in the background .
    :param root: the Main Root Element ( Tk Element )
    :return: Nothing . Deny all permissions
    """
    for position in range(10):
        permissions[position] = False


class PmtaWatcher:
    """
    Header Class that Do Everything
    """

    def __init__(self):
        # the root of the App
        self.root = tkt.Tk()
        # the Logic of the app
        app(self.root)
        # import the image
        icon = tkt.PhotoImage(file=resource_path('icon.png'))
        # set up the image as icon
        self.root.iconphoto(False, icon)
        # Tkinter supports a mechanism called protocol handlers. Here, the term protocol refers
        # to the interaction between the application and the window manager. The most commonly
        # used protocol is called WM_DELETE_WINDOW, and is used to define what happens when the
        # user explicitly closes a window using the window manager.
        # You can use the protocol method to install a handler for this protocol (the widget
        # must be a Tk or Toplevel widget):
        self.root.protocol("WM_DELETE_WINDOW", on_closing(self.root))
        # the mainloop with fixed width and height
        tkt.mainloop_fixed(self.root, 800, 800, "PMTA4 Watcher v 1.0 By. Ouzrour")


if __name__ == "__main__":
    # Run the Main Class
    PmtaWatcher()
