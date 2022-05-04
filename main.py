# !/usr/bin/env
# -*- coding: utf-8 -*-

import time
import threading
 
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox

import kociemba

class KeyTracker():
    '''KeyTracker Class | Source: Jeffery from stack overflow (for tetsing)'''

    key = ''
    last_press_time = 0
    last_release_time = 0

    def __init__(self, on_press, on_release):
        self.on_press = on_press
        self.on_release = on_release

    def track(self, key):
        self.key = key
        self.first_press = True

    def is_pressed(self):
        if self.first_press:
            return time.time() - self.last_press_time < .1

    def report_key_press(self, event):
        if event.keysym == self.key:
            if not self.is_pressed():
                self.on_press()
            self.last_press_time = time.time()

    def report_key_release(self, event):
        if event.keysym == self.key:
            timer = threading.Timer(.1, self.report_key_release_callback, args=[event])
            timer.start()

    def report_key_release_callback(self, event):
        if not self.is_pressed():
            self.on_release()
        self.last_release_time = time.time()

class TimeLog():
    '''Instantiated with a log template. Recieves logs and submits them to entries.'''

    def __init__(self, template, app):
        self.template = template
        self.entries = []
        self.times = []
        self.app = app
    
    def submit_time(self, time):
        self.times.append(time)
        
        # Calculate ao5 if there is enough data
        if len(self.times) >= 5:
            ao5 = round(sum(self.times[len(self.times)-5:])/5, 2)
            self.app.ao5.set(f'ao5: {ao5}')
        else:
            ao5 = '-.--'
        
        # Calculate ao12 if there is enough data
        if len(self.times) >= 12:
            ao12 = round(sum(self.times[len(self.times)-12:])/12, 2)
            self.app.ao12.set(f'ao12: {ao12}')
        else:
            ao12 = '-.--'

        self.add_entry(len(self.entries)+1, time, ao5, ao12)

    def add_entry(self, *args):
        # Attempt to add the submission to the log
        try:
            assert len(args) == len(self.template), 'entry must have the same length as the set template'

            self.entries.append(args)
        except AssertionError:
            return False

class App(tk.Tk):
    '''CubeTools App Class'''

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

        # Main buttons
        buttons_frame = LabelFrame(self, height=20)
        buttons_frame.pack(side=TOP, fill=X)

        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(5, weight=1)

        btn_timer = Button(buttons_frame, text='Timer', bd=0, command=self.init_timer_screen)
        btn_timer.grid(row=0, column=2, padx=5, pady=5)

        btn_tracking = Button(buttons_frame, text='Tracking', bd=0, command=self.init_tracking_screen)
        btn_tracking.grid(row=0, column=3, padx=5, pady=5)

        btn_wip = Button(buttons_frame, text='Solver', bd=0, command=self.init_solver_screen)
        btn_wip.grid(row=0, column=4, padx=5, pady=5)

        # btn hover effect
        buttons = [btn_timer, btn_tracking, btn_wip]

        for btn in buttons:
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)

        # Init TimeLog
        self.log = TimeLog(['num', 'time', 'ao5', 'ao12'], self)

    def init_solver_screen(self):
        self.init_blank_screen()

        # cube input
        cube_input = Frame(self.mainframe, width=600, height=450)
        cube_input.pack(side=TOP)

        cube_input.grid_propagate(False)


        # Create faces and blanks
        blank = Frame(cube_input, width=150, height=150, bg=self.light_grey)


        # Row 0
        blank.grid(column=0, row=0)

        white = Frame(cube_input, width=150, height=150, bg='white')
        white.grid(column=1, row=0)

        blank.grid(column=2, row=0)

        blank.grid(column=3, row=0)

        # Row 1
        orange = Frame(cube_input, width=150, height=150, bg='orange')
        orange.grid(column=0, row=1)

        green = Frame(cube_input, width=150, height=150, bg='green')
        green.grid(column=1, row=1)

        red = Frame(cube_input, width=150, height=150, bg='red')
        red.grid(column=2, row=1)

        blue = Frame(cube_input, width=150, height=150, bg='blue')
        blue.grid(column=3, row=1)
        
        # Row 2
        blank.grid(column=0, row=2)
        
        yellow = Frame(cube_input, width=150, height=150, bg='yellow')
        yellow.grid(column=1, row=2)

        blank.grid(column=2, row=2)

        blank.grid(column=2, row=3)


        faces = [white, red, green, yellow, orange, blue]
        
        
        # Create stickers
        self.active_color = 'green'

        def set_color(e):
            e.widget.configure(bg=self.active_color, activebackground=self.active_color)

        def key_press(e):
            faces = {
                'u': 'white',
                'r': 'red',
                'f': 'green',
                'd': 'yellow',
                'l': 'orange',
                'b': 'blue'
            }

            # Set the active color to the selected key | generate solution if g pressed
            if e.keysym in faces.keys():
                self.active_color = faces[e.keysym]
            elif e.keysym == 'g':
                self.cubestring = gen_cubestring()

                # Try to solve the solution
                try:
                    self.solution = kociemba.solve(cubestring=self.cubestring)
                    messagebox.showinfo('Solution', self.solution)
                except ValueError:
                    messagebox.showwarning('Invalid cubestring!', 'The cubestring you entered was invalid! Please check again.')


        # Gen stickers
        stickers = {}
        for face in faces:
            stickers[face] = [None for i in range(9)]
            face.grid_propagate(False)
            for row in range(3):
                for column in range(3):
                    # Create the sticker
                    sticker_frame = Frame(face, width=50, height=50, bg='black')
                    sticker_frame.grid(row=row, column=column)
                    sticker_frame.pack_propagate(False)

                    sticker = Button(sticker_frame, width=40, height=40, bg=face['background'], activebackground=face['background'], relief=RIDGE, borderwidth=3)
                    sticker.pack()
                    sticker.bind('<Button>', set_color)

                    stickers[face][row*3 + column] = sticker

        # Kind any key press to set the active color (to the key)                   
        self.bind('<Key>', key_press)

        button = Button(cube_input, width=5, height=5, text='', command=lambda: set_color(button), bg='white', activebackground='white')
        button.grid()

        def gen_cubestring():
            orientation = {
                'white': 'U',
                'red': 'R',
                'green': 'F',
                'yellow': 'D',
                'orange': 'L',
                'blue': 'B',
            }

            # Gen cubestring via stickers
            cubestring = ''
            for face in stickers.values():
                # Append face representation of sticker color to cubestring
                for sticker in face:
                    cubestring += orientation[sticker['background']]
            
            return cubestring

    def init_tracking_screen(self):
        self.init_blank_screen()
        
        # datalabels
        datalabels = Frame(self.mainframe, width=500, height=25)
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

        # data entries
        dataentries = Frame(self.mainframe, width=500, height=26)
        dataentries.pack(side=TOP)

        for i, entry in enumerate(self.log.entries):
            if i % 2 == 0:
                bg = self.light_grey
            else:
                bg = self.defaultbg

            entry_frame = Frame(self.mainframe, width=500, height=22, bg=bg)

            entry_frame.grid_propagate(False)

            entry_frame.columnconfigure(0, weight=1)
            entry_frame.columnconfigure(1, weight=2)
            entry_frame.columnconfigure(2, weight=2)
            entry_frame.columnconfigure(3, weight=2)

            # Unpack entry
            num, time, ao5, ao12 = entry

            # Add entry data
            Label(entry_frame, text=num, bg=bg, anchor=W, width=10).grid(row=0, column=0, sticky=W, padx=1, pady=1)
            Label(entry_frame, text=time, bg=bg, anchor=W, width=10).grid(row=0, column=1, sticky=W, padx=1, pady=1)
            Label(entry_frame, text=ao5, bg=bg, anchor=W, width=10).grid(row=0, column=2, sticky=W, padx=1, pady=1)
            Label(entry_frame, text=ao12, bg=bg, anchor=W, width=10).grid(row=0, column=3, sticky=W, padx=1, pady=1)

            # Pack entry frame
            entry_frame.pack(side=TOP)


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

        Label(scramble, text='just do a hand scramble you lazy end-user', font=('Times New Roman', 15)).pack(side=TOP, padx=10, pady=10)

        # timer
        self.time = StringVar()
        self.timer_started = False
        self.timer_primed = False
        
        # ao5 and ao12
        self.ao5 = StringVar()
        self.ao12 = StringVar()

        # Timer labels
        timer = Frame(self.mainframe, width=500, height=250)
        timer.pack(side=TOP)

        timer.pack_propagate(False)
        
        self.time.set('0.00')
        self.ao5.set('ao5: ')
        self.ao12.set('ao12: ')

        Label(timer, textvariable=self.time, font=('Times New Roman', 45)).pack(side=TOP)
        Label(timer, textvariable=self.ao5, font = ('Times New Roman', 20)).pack(side=TOP)
        Label(timer, textvariable=self.ao12, font = ('Times New Roman', 20)).pack(side=TOP)
        
        self.timer_primed = False
        self.timer_started = False

        def space_pressed():
            if self.timer_started:
                # End timer
                self.timer_started = False
                solve_time = round(time.time() - self.starttime, 2)
                self.log.submit_time(solve_time)              
                print(f'timer stopped | {self.log.entries[-1]}')
            else:
                # Prime timer
                self.timer_primed = True

        def space_released():
            if self.timer_primed:
                # Start timer
                self.timer_started = True
                self.timer_primed = False
                self.start_timer()

        # Remove key debouncing / pain
        key_tracker = KeyTracker(space_pressed, space_released)
        self.bind_all('<KeyPress>', key_tracker.report_key_press)
        self.bind_all('<KeyRelease>', key_tracker.report_key_release)
        key_tracker.track('space')
    
    def start_timer(self):
        self.starttime = time.time()

        while True:
            self.time.set(round(time.time() - self.starttime, 2))
            self.update()
            if self.timer_started == False:
                break
    
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
    app = App()
    mainloop()
  
if __name__ == '__main__':
    main()