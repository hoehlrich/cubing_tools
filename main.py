# !/usr/bin/env
# -*- coding: utf-8 -*-

'''
The deliverable was completed
- A basic gui was created (adapted from a previous project)
- The main two pages are completed (timer and tracking)
- Still need to make labels dynamic
- Tracking page is set up and ready to recieve time data (already formatted as a table)
'''

from json.decoder import JSONDecodeError
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import json
from functools import partial
import random
from turtle import bgcolor

import kociemba

class App(tk.Tk):
    'App Class'

    def __init__(self):
        super().__init__()

        # Configure win
        self.geometry('960x540')
        self.title('cubetools')

        self.columnconfigure(0, weight=1)

        self.light_grey = '#D3D3D3'
        self.defaultbg = self.cget('bg')

        # Initisalize main buttons (outside of mainframe)
        self.init_main_buttons()

        # self.mainframe
        self.mainframe = Frame(self)
        self.mainframe.pack(side=TOP, fill=BOTH)

        self.init_timer_screen()
    
    def init_main_buttons(self):
        # buttons
        buttons_frame = LabelFrame(self, height=20)
        buttons_frame.pack(side=TOP, fill=X)

        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(5, weight=1)

        btn_timer = Button(buttons_frame, text='Timer', bd=0, command=self.init_timer_screen)
        btn_timer.grid(row=0, column=2, padx=5, pady=5)

        btn_tracking = Button(buttons_frame, text='Tracking', bd=0, command=self.init_tracking_screen)
        btn_tracking.grid(row=0, column=3, padx=5, pady=5)

        btn_wip = Button(buttons_frame, text='WIP <3', bd=0)
        btn_wip.grid(row=0, column=4, padx=5, pady=5)

        # btn hover effect
        buttons = [btn_timer, btn_tracking, btn_wip]

        for btn in buttons:
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)

    def init_tracking_screen(self):
        self.init_blank_screen()
        
        # datalabels
        datalabels = Frame(self.mainframe, width=500, height=50)
        datalabels.pack(side=TOP)

        datalabels.columnconfigure(0, weight=1)
        datalabels.columnconfigure(1, weight=2)
        datalabels.columnconfigure(2, weight=2)
        datalabels.columnconfigure(3, weight=2)

        datalabels.grid_propagate(False)

        Label(datalabels, text='Num').grid(row=0, column=0, sticky=W, padx=5, pady=5)
        Label(datalabels, text='Time').grid(row=0, column=1, sticky=W, padx=5, pady=5)
        Label(datalabels, text='ao5').grid(row=0, column=2, sticky=W, padx=5, pady=5)
        Label(datalabels, text='ao12').grid(row=0, column=3, sticky=W, padx=5, pady=5)

        # bottom buttons
        btn_frame = Frame(self.mainframe, width=300, height=24)
        btn_frame.pack(side=BOTTOM, anchor=S, padx=2, pady=2)

        Button(btn_frame, text='New Session', bg=self.light_grey).grid(row=0, column=0, padx=2, pady=2)
        Button(btn_frame, text='Export Session', bg=self.light_grey).grid(row=0, column=1, padx=2, pady=2)
        Button(btn_frame, text='Import Session', bg=self.light_grey, command=self.upload_file).grid(row=0, column=2, padx=2, pady=2)

    def init_timer_screen(self):
        self.init_blank_screen()

        # scramble
        scramble = Frame(self.mainframe, width=1000, height=150)
        scramble.pack(side=TOP)

        scramble.pack_propagate(False)

        Label(scramble, text="R2 D' F' R' D' L' B2 D' F' R2 U2 B2 U' F2 R2 B2 R2 U' R2 U' L2", font=('Times New Roman', 15)).pack(side=TOP, padx=10, pady=10)

        # timer
        timer = Frame(self.mainframe, width=500, height=250)
        timer.pack(side=TOP)

        timer.pack_propagate(False)

        Label(timer, text='0.00', font=('Times New Roman', 45)).pack(side=TOP)
        Label(timer, text='ao5: ', font = ('Times New Roman', 20)).pack(side=TOP)
        Label(timer, text='ao12: ', font = ('Times New Roman', 20)).pack(side=TOP)

    def init_blank_screen(self):
        for widget in self.mainframe.winfo_children():
            widget.destroy()

    def on_enter(self, e):
        e.widget['foreground'] = 'grey'

    def on_leave(self, e):
        e.widget['foreground'] = 'black'

    def upload_file(self):
        filename = filedialog.askopenfilename()
        
        if '.json' in filename:
            messagebox.showinfo('pog', 'it worked bro')
        else:
            messagebox.showerror('Import Error', 'Invalid File.')

def main():
    print(len(kociemba.solve('BLBFULLLFUDLURUDFUFBRRFRBURRLFDDDDFLDRDRLBLBUUFRBBDFUB').split(' ')))

    app = App()
    mainloop()


if __name__ == '__main__':
    main()