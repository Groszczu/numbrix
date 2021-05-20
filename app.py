from tkinter import (
    filedialog,
    messagebox
)
import tkinter as tk
from puzzle import read_board
from puzzle import Puzzle
from math import sqrt
import time

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
            self.solved_puzzle = self.puzzle.solve()
        
    def get_board_size(self):
        return int(self._board_size)


class NumbrixBoard(tk.Canvas):
    def __init__(self):
        self.values = []
        self.user_inputs = []
        self.width = 400
        self.height = 400
        super().__init__(width=self.width, height=self.height, background="lightgrey", highlightthickness=0)

    def clear_user_inputs(self):
        self.user_inputs.clear()

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

    def draw_text(self, board : Board):
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

    def draw_text2(self, board : Board):
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


class Menubar(tk.Menu):
    def __init__(self, win: tk.Tk):
        super().__init__(win)

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

        self.numbrix = None

    def enable_user_gameplay(self, win: tk.Tk):
        if self.numbrix == None:
            return
        else:
            for input_ID in self.numbrix.inputs_ID:
                self.numbrix.itemconfigure(input_ID, state=tk.NORMAL)

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
                self.numbrix.draw_text2(self.board)
            else:
                self.numbrix.clear_user_inputs()
                self.numbrix.delete("all")
                self.numbrix.draw_board(self.board)
                self.numbrix.draw_text2(self.board)

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
        try:
            if [int(s.get()) for s in self.numbrix.user_inputs] == [s[1] for s in self.board.solved_puzzle]:
                tk.messagebox.showinfo(title="Info", message="Brawo! Rozwiązałeś łamigłówkę!")
            else:
                tk.messagebox.showinfo(title="Info", message="Niestety Twoje rozwiązanie nie jest poprawne :(")
        except ValueError:
            tk.messagebox.showinfo(title="Info", message="Niestety Twoje rozwiązanie nie jest poprawne :(")
            return


    def resolve(self, win: tk.Tk ):
        board = Board(self.filename)
        puzzle = Puzzle(board.board)
        board.board = puzzle.solve()

        if self.numbrix == None:
            self.numbrix = NumbrixBoard()
            self.numbrix.pack()
            self.numbrix.draw_text(board)
        else:
            self.numbrix.draw_text(board)


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
