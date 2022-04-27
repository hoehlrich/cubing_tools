# !/usr/bin/env
# -*- coding: utf-8 -*-

import random
import copy

import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox

import kociemba

class Cubestring():
    '''Cubestring Class'''

    def __init__(self, random_valid=False):
        self.cubestring = ''

        if random_valid == True:
            self.generate_random_valid_cubestring()
    
    def generate_random_valid_cubestring(self):
        faces = ['U', 'R', 'F', 'D', 'L', 'B']

        corners = {
            'c1': [('U', 1), ('L', 3), ('B', 7)],
            'c2': [('U', 3), ('R', 1), ('B', 9)],
            'c3': [('U', 7), ('L', 9), ('F', 1)],
            'c4': [('U', 9), ('R', 7), ('F', 3)],
            'c5': [('D', 1), ('R', 3), ('B', 3)],
            'c6': [('D', 3), ('L', 1), ('B', 1)],
            'c7': [('D', 7), ('R', 9), ('F', 9)],
            'c8': [('D', 9), ('L', 7), ('F', 7)]
        }

        edges = {
            'e1': [('U', 2), ('B', 8)],
            'e2': [('U', 4), ('L', 6)],
            'e3': [('U', 6), ('R', 4)],
            'e4': [('U', 8), ('F', 2)],
            'e5': [('B', 4), ('L', 2)],
            'e6': [('B', 6), ('R', 2)],
            'e7': [('F', 4), ('L', 8)],
            'e8': [('F', 6), ('R', 8)],
            'e9': [('D', 2), ('B', 2)],
            'e10': [('D', 4), ('R', 6)],
            'e11': [('D', 6), ('L', 4)],
            'e12': [('D', 8), ('F', 8)]
        }

        faces = {
            'U': 0,
            'R': 1,
            'F': 2,
            'D': 3,
            'L': 4,
            'B': 5,
        }

        # Repeat until a valid result
        while True:
            try:
                cubestring = list(''.join(f'____{face}____' for face in faces))


                remaining_corners = list(corners.keys())
                random.shuffle(remaining_corners)

                # Assign corners to cubestring at random
                for corner_pos in corners:
                    # Get chosen corner info and isolate sticker colors
                    chosen_corner = corners[remaining_corners.pop()]
                    corner_colors = [sticker[0] for sticker in chosen_corner]

                    # Change permutation and orientation
                    random.shuffle(corner_colors)

                    # Assign the stickers
                    for i, sticker in enumerate(corners[corner_pos]):
                        face, num = sticker
                        cubestring[faces[face] * 9 + num - 1] = corner_colors[i]

                remaining_edges = list(edges.keys())
                random.shuffle(remaining_edges)

                # Assign edges to cubestring at random
                for i, edge_pos in enumerate(edges):
                    # Get chosen edge info and isolate sticker colors
                    chosen_edge = edges[remaining_edges.pop()]
                    edge_colors = [sticker[0] for sticker in chosen_edge]

                    # Change permutation and orientation
                    random.shuffle(edge_colors)

                    # Assign the stickers
                    for i, sticker in enumerate(edges[edge_pos]):
                        face, num = sticker

                        cubestring[faces[face] * 9 + num - 1] = edge_colors[i]

                str_cubestring = ''.join(sticker for sticker in cubestring)
                
                print(cubestring)
                solve = kociemba.solve(str_cubestring)
                print(solve)

                break
            except ValueError:
                pass

class Log():
    '''Log Class'''

    def __init__(self, name, template):
        self.name = name
        self.template = template
        self.entries = []

    def add_entry(self, *args):
        try:
            assert len(args) == len(self.template), 'entry must have the same length as the set template'

            self.entries.append(args)
        except AssertionError:
            pass

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

        # Initialize main buttons (outside of mainframe)
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
    # print(len(kociemba.solve('BLBFULLLFUDLURUDFUFBRRFRBURRLFDDDDFLDRDRLBLBUUFRBBDFUB').split(' ')))

    # app = App()
    # mainloop()

    cubestring = Cubestring(random_valid=True)

  
if __name__ == '__main__':
    main()