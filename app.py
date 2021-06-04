from tkinter import (
    filedialog,
    messagebox
)
import tkinter as tk
from puzzle import read_board
from puzzle import Puzzle
from math import sqrt
import time
import sys

class Board():
    def __init__(self, file_name: str):
        self.board = read_board(file_name)
        self._board_size = sqrt(len(self.board))
        self.valid = True

        if not self._board_size.is_integer():
            tk.messagebox.showwarning(title="Błąd", message="Wybrany plik nie posiada planszy o poprawnym rozmiarze")
            self.valid = False
        else:
            tk.messagebox.showinfo(title="Info", message="Wybrana plansza posiada wymiary {} x {}".format(int(self._board_size), int(self._board_size)))

        if self.valid is True:
            self.puzzle = Puzzle(self.board)
            self.solved_puzzle = self.puzzle.solve()[0]
        
    def get_board_size(self):
        return int(self._board_size)


class NumbrixBoard(tk.Canvas):
    def __init__(self):
        self.values = []
        self.user_inputs = []
        self.width = 400
        self.height = 400
        super().__init__(width=self.width, height=self.height, background="lightgrey", highlightthickness=0)

    def draw_empty_board(self, size):
        self.inputs_ID = []
        rect_size = self.width / size
        it = 0
        for y in range(0, size):
            for x in range(0, size):
                self.user_inputs.append(tk.StringVar(self, "", '{}_{}'.format(x, y)))
                textentry = tk.Entry(self, font=14, justify=tk.CENTER, bg="lightgrey", bd=1, textvariable=self.user_inputs[it])
                id = self.create_window(x * rect_size, 
                                        y * rect_size,
                                        anchor=tk.NW,
                                        width=rect_size,
                                        height=rect_size,
                                        window=textentry,
                                        state=tk.NORMAL)
                self.create_rectangle(x * rect_size, 
                                        y * rect_size, 
                                        x * rect_size + rect_size, 
                                        y * rect_size + rect_size, 
                                        fill="darkgrey", 
                                        outline="black")
                self.inputs_ID.append(id)
                it+=1

    def draw_board(self, board : Board):
        self.inputs_ID = []
        board_size = board.get_board_size()
        rect_size = self.width / board_size
        it = 0
        for y in range(0, board_size):
            for x in range(0, board_size):
                rect_value = board.board[it][1]
                if rect_value != 0:
                    self.user_inputs.append(tk.StringVar(self, str(rect_value), '{}_{}'.format(x, y)))
                    self.create_rectangle(x * rect_size,
                                          y * rect_size, 
                                          x * rect_size + rect_size - 1, 
                                          y * rect_size + rect_size - 1, 
                                          fill="lightblue", 
                                          outline="black")
                else:
                    self.user_inputs.append(tk.StringVar(self, "", '{}_{}'.format(x, y)))
                    textentry = tk.Entry(self, font=14, justify=tk.CENTER, bg="lightgrey", bd=1, textvariable=self.user_inputs[it])
                    id = self.create_window(x * rect_size, 
                                       y * rect_size,
                                       anchor=tk.NW,
                                       width=rect_size,
                                       height=rect_size,
                                       window=textentry,
                                       state=tk.HIDDEN)
                    self.create_rectangle(x * rect_size, 
                                          y * rect_size, 
                                          x * rect_size + rect_size, 
                                          y * rect_size + rect_size, 
                                          fill="darkgrey", 
                                          outline="black")
                    self.inputs_ID.append(id)
                it+=1

    def draw_solution(self, board : Board):
        board_size = board.get_board_size()
        rect_size = self.width / board_size

        value = 1
        print((board_size*board_size))
        while value < (board_size*board_size)+1:
            it = 0
            for y in range(0, board_size):
                for x in range(0, board_size):
                    rect_value = board.board[it][1]
                    if rect_value == value:
                        value += 1
                        self.update()
                        time.sleep(0.1)
                        self.create_rectangle(x * rect_size,
                                              y * rect_size,
                                              x * rect_size + rect_size,
                                              y * rect_size + rect_size,
                                              fill="orange",
                                              outline="black")
                        self.create_text(x * rect_size + rect_size / 2,
                                         y * rect_size + rect_size / 2, text=rect_value)
                    it+=1

    def draw_text(self, board : Board):
        board_size = board.get_board_size()
        rect_size = self.width / board_size

        it = 0
        for y in range(0, board_size):
            for x in range(0, board_size):
                rect_value = board.board[it][1]
                if rect_value != 0:
                    self.create_text(x * rect_size + rect_size / 2,
                                     y * rect_size + rect_size / 2, text=rect_value)
                it+=1


class PopupWindow(object):
    def __init__(self, win: tk.Tk):
        top=self.top=Toplevel(win)
        self.l=Label(top,text="Hello World")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok', command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()


class Menubar(tk.Menu):
    def __init__(self, win: tk.Tk):
        super().__init__(win)
        self.win = win
        self.filemenu = tk.Menu(self, tearoff=0)
        self.filemenu.add_command(label="Otwórz plik z łamigłówką...", command=lambda: self.select_file(win))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Wyjście", command=lambda: self.close_app(win))
        self.add_cascade(label="Plik", menu=self.filemenu)

        self.solvemenu = tk.Menu(self, tearoff=0)
        self.solvemenu.add_command(label="Rozwiąż wybraną łamigłówkę", command=lambda: self.resolve(win))
        self.solvemenu.add_command(label="Sprawdź poprawność rozwiązania łamigłówki", command=lambda: self.check_solution(win))
        self.solvemenu.add_separator()
        self.solvemenu.add_command(label="Uruchom opcję rozgrywki", command=lambda: self.enable_user_gameplay(win))
        self.add_cascade(label="Rozwiązanie", menu=self.solvemenu)

        self.myownpuzzlemenu = tk.Menu(self, tearoff=0)
        self.myownpuzzlemenu.add_command(label="Stwórz własną łamigłówkę", command=lambda: self.popup())
        self.myownpuzzlemenu.add_command(label="Sprawdź rozwiązywalność", command=lambda: self.check_solvability())
        self.myownpuzzlemenu.add_command(label="Rozwiąż własną łamigłówkę", command=lambda: self.solve_my_own_puzzle())
        self.add_cascade(label="Własna łamigłówka", menu=self.myownpuzzlemenu)

        self.numbrix = None
        self.myownpuzzlesize = 0

    def popup(self):
        self.popup_win = tk.Toplevel(self.win)
        self.popup_win.wm_title("Podaj rozmiary planszy")
        l = tk.Entry(self.popup_win, text="Wpisz rozmiar...")
        l.grid(row=0, column=0)
        b = tk.Button(self.popup_win, text="Zatwierdź", command=lambda: self.close_popup(win, l))
        b.grid(row=1, column=0)

    def close_popup(self, popup_win, l):
        try:
            self.myownpuzzlesize = int(l.get())
        except:
            print("ERROR")
            return

        self.popup_win.destroy()
        self.numbrix = NumbrixBoard()
        self.numbrix.pack()
        self.numbrix.draw_empty_board(self.myownpuzzlesize)

    def check_solvability(self):
        if self.myownpuzzlesize != 0:
            self.int_inputs = []
            for it in range(0, len(self.numbrix.user_inputs)):
                if self.numbrix.user_inputs[it].get() == "":
                    self.int_inputs.append((it + 1, 0))
                else:
                    self.int_inputs.append((it + 1, int(self.numbrix.user_inputs[it].get())))
            
            puzzle = Puzzle(self.int_inputs)
            try:
                if puzzle.solve()[1] is True:
                    tk.messagebox.showinfo(title="Info", message="Wpisana przez Ciebie łamigłówka jest rozwiązywalna!")
            except TypeError:
                tk.messagebox.showinfo(title="Info", message="Wpisana przez Ciebie łamigłówka nie jest rozwiązywalna :(")

    def solve_my_own_puzzle(self):
        # TODO: Solve puzzle mad by user
        pass

    def entryValue(self):
        return self.myownpuzzlesize

    def enable_user_gameplay(self, win: tk.Tk):
        if self.numbrix == None:
            print("Nie wybrano planszy")
            return
        else:
            for input_ID in self.numbrix.inputs_ID:
                self.numbrix.itemconfigure(input_ID, state=tk.NORMAL)

    def disable_user_gameplay(self):
        if self.numbrix == None:
            return
        else:
            for input_ID in self.numbrix.inputs_ID:
                self.numbrix.itemconfigure(input_ID, state=tk.HIDDEN)

    def select_file(self, win: tk.Tk):
        self.filename = tk.filedialog.askopenfilename(initialdir="C:\\", 
                                                      title="Wybierz plik", 
                                                      filetypes = (("Pliki tekstowe", "*.txt*"), ("Wszystkie pliki", "*.*")))
        try:
            self.board = Board(self.filename)

            if not self.board.valid:
                return

            if self.numbrix == None:
                self.numbrix = NumbrixBoard()
                self.numbrix.pack()
                self.numbrix.draw_board(self.board)
                self.numbrix.draw_text(self.board)
            else:
                self.numbrix.delete("all")
                self.numbrix.draw_board(self.board)
                self.numbrix.draw_text(self.board)

            ''' PRINTING DATA FROM USER INPUTS 
            inputs = [s.get() for s in self.numbrix.user_inputs]
            print(inputs)
            '''
        except FileNotFoundError:
            print("Użytkownik anulował operację")

    def close_app(self, win: tk.Tk):
        win.destroy()

    def check_solution(self, win: tk.Tk):
        ''' PRINT SOLVED PUZZLE AND USER INPUTS - CHECK EQUALITY
        print([int(s.get()) for s in self.numbrix.user_inputs])
        print([s[1] for s in self.board.solved_puzzle])
        '''
        if self.numbrix == None:
            print("Nie wybrano planszy")
            return        

        try:
            if [int(s.get()) for s in self.numbrix.user_inputs] == [s[1] for s in self.board.solved_puzzle]:
                tk.messagebox.showinfo(title="Info", message="Brawo! Rozwiązałeś łamigłówkę!")
            else:
                tk.messagebox.showinfo(title="Info", message="Niestety Twoje rozwiązanie nie jest poprawne :(")
        except ValueError:
            tk.messagebox.showinfo(title="Info", message="Niestety Twoje rozwiązanie nie jest poprawne :(")
            return


    def resolve(self, win: tk.Tk ):
        try:
            board = Board(self.filename)
        except:
            print("Brak planszy do rozwiazania")
            return
        puzzle = Puzzle(board.board)
        board.board = puzzle.solve()[0]
        self.disable_user_gameplay()

        if self.numbrix == None:
            self.numbrix = NumbrixBoard()
            self.numbrix.pack()
            self.numbrix.draw_solution(board)
        else:
            self.numbrix.draw_solution(board)


if __name__ == "__main__":
    win = tk.Tk()
    win.geometry("400x400")
    win.title("Numbrix - SAT Solver")
    win.resizable(False, False)
    menubar = Menubar(win)
    win.config(menu=menubar)
    main_label = tk.Label(win, text='Proszę wybrać plik z planszą')
    main_label.place(relx=0.5, rely=0.5, anchor="center")

    win.mainloop()
