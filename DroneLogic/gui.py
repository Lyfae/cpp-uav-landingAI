from os import replace
import cv2
import tkinter as tk
from _thread import *
import threading

from PIL import Image, ImageTk
from main import main 

def tkinter():
    # tkinter default varaiables

    HEIGHT = 550
    WIDTH = 1800
    BGCOLOR = '#E9EBE2'
    BTCOLOR = 'black'
    TITLECOLOR = '#8E0101'
    SUBTITLECOLOR = '#914FA6'
    BTNLABELCOLOR = 'white'
    BTNLABELCOLORACTIVE = '#3fb559'
    BTNLABELCOLORINACTIVE = '#cf483c'
    REFRESH_RATE = 50

    # declaring some variables
    global isLocationToggled
    isLocationToggled = False

    global isOrientationToggled
    isOrientationToggled = False

    global isDockingToggled
    isDockingToggled = False

    global isLandingToggled
    isLandingToggled = False

    global isTakeoffToggled 
    isTakeoffToggled = False


    # initialization
    # creating the program window root
    root = tk.Tk()
    root.resizable(False,False)
    main_canvas = tk.Canvas(root,height=HEIGHT,width=WIDTH,bg=BGCOLOR,highlightthickness=0)
    main_canvas.pack()

    #Instantiate the icons
    location_icon = tk.PhotoImage(file='icons/one.png')
    orientation_icon = tk.PhotoImage(file='icons/two.png')
    docking_icon = tk.PhotoImage(file='icons/three.png')
    landing_icon = tk.PhotoImage(file='icons/four.png')
    takeoff_icon = tk.PhotoImage(file='icons/five.png')

    # creating the canvas
    location_canvas = tk.Canvas(main_canvas,width = 300, height = 450, highlightthickness=0, bg=BGCOLOR)
    location_canvas.place(x=50,y=60, anchor='nw')

    orientation_canvas = tk.Canvas(main_canvas,width = 300, height = 450, highlightthickness=0, bg=BGCOLOR)
    orientation_canvas.place(x =400, y= 60, anchor = 'nw') 

    docking_canvas = tk.Canvas(main_canvas, width = 300, height=450, highlightthickness=0, bg = BGCOLOR)
    docking_canvas.place(x= 750, y= 60, anchor='nw')

    landing_canvas = tk.Canvas(main_canvas, width= 300, height= 450, highlightthickness=0, bg=BGCOLOR)
    landing_canvas.place(x= 1100, y= 60, anchor='nw')

    takeoff_canvas = tk.Canvas(main_canvas,width=300, height=450, highlightthickness=0, bg=BGCOLOR)
    takeoff_canvas.place(x=1450,y=60,anchor='nw')

    #creating the labels
    title = tk.Label(main_canvas,text="Robotics Team Super Duper Swag Controller!", font = ('impact',28,'bold italic'), justify='center', bg = BGCOLOR, fg=TITLECOLOR)
    title.place(relx = 0.5, rely=0.075, anchor='center')

    location_title = tk.Label(location_canvas, text="Location", font=('arial',24,'bold'), justify='center', bg=BGCOLOR, fg=TITLECOLOR,)
    location_title.place(relx = 0.5,rely = 0.08,anchor='center')

    orientation_title = tk.Label(orientation_canvas, text="Orientation", font=('arial',24,'bold'), justify='center', bg=BGCOLOR, fg=TITLECOLOR,)
    orientation_title.place(relx = 0.5,rely = 0.08,anchor='center')
    
    docking_title = tk.Label(docking_canvas, text="Docking", font=('arial',24,'bold'), justify='center', bg=BGCOLOR, fg=TITLECOLOR,)
    docking_title.place(relx = 0.5,rely = 0.08,anchor='center')

    landing_title = tk.Label(landing_canvas, text="Landing", font=('arial',24,'bold'), justify='center', bg=BGCOLOR, fg=TITLECOLOR,)
    landing_title.place(relx = 0.5,rely = 0.08,anchor='center')

    takeoff_title = tk.Label(takeoff_canvas, text="TakeOff", font=('arial',24,'bold'), justify='center', bg=BGCOLOR, fg=TITLECOLOR,)
    takeoff_title.place(relx = 0.5,rely = 0.08,anchor='center')

    #functions to control the buttons
    def toggle_location():
        global isLocBtnPressed
        isLocBtnPressed = True

    def toggle_orientation():
        global isOriBtnPressed
        global isLocationToggled

        if isLocationToggled:
            isOriBtnPressed = True
        else:
            print("Press on the previous button before moving onto the next button")
    
    def toggle_docking(): 
        global isDockBtnPressed
        global isLocationToggled
        global isOrientationToggled

        if isOrientationToggled and isLocationToggled:
            isDockBtnPressed = True
        else:
            print("Press on the previous button before moving onto the next button")

    def toggle_landing():
        global isLndBtnPressed
        global isLocationToggled
        global isOrientationToggled
        global isDockingToggled
        
        if isDockingToggled and isOrientationToggled and isLocationToggled:
            isLndBtnPressed = True
        else:
            print("Press on the previous button before moving onto the next button")

    def toggle_takeoff():
        global isTakeoffBtnPressed
        global isLocationToggled
        global isOrientationToggled
        global isDockingToggled
        global isLandingToggled

        if isTakeoffToggled and isDockingToggled and isOrientationToggled and isLocationToggled:
            isTakeoffBtnPressed = True
        else: 
            print("Press on the previous button before moving onto the next button")

    

    #control buttons
    display_location = tk.Button(location_canvas,image = location_icon, command=toggle_location, justify='center', padx=10, pady=10, bg='green', fg='black')
    display_location.place(relx=.5,rely=.5,anchor='center')

    display_orientation = tk.Button(orientation_canvas,image = orientation_icon, command=toggle_orientation, justify='center', padx=10, pady=10, bg='green', fg='black')
    display_orientation.place(relx=.5,rely=.5,anchor='center')


    display_docking = tk.Button(docking_canvas,image = docking_icon, command=toggle_docking, justify='center', padx=10, pady=10, bg='green', fg='black')
    display_docking.place(relx=.5,rely=.5,anchor='center')


    display_landing = tk.Button(landing_canvas,image = landing_icon, command=toggle_landing, justify='center', padx=10, pady=10, bg='green', fg='black')
    display_landing.place(relx=.5,rely=.5,anchor='center')

    display_takeoff = tk.Button(takeoff_canvas,image = takeoff_icon, command=toggle_takeoff, justify='center', padx=10, pady=10, bg='green', fg='black')
    display_takeoff.place(relx=.5,rely=.5,anchor='center')


    #refresh
    root.after(REFRESH_RATE)

    #execute tkinter
    root.mainloop()


# begin tkinter threading
tk_thread = threading.Thread(target = tkinter)
tk_thread.start()


    

