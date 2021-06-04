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
    def __init__(self, board: list):
        self.__board = board
        self.__board_size = sqrt(len(self.__board))

        if not self.__board_size.is_integer():
            tk.messagebox.showwarning(title="Błąd", message="Wybrany plik nie posiada planszy o poprawnym rozmiarze")
            self.__valid_size = False
        else:
            tk.messagebox.showinfo(title="Info", message="Plansza posiada wymiary {} x {}".format(int(self.__board_size), int(self.__board_size)))
            self.__valid_size = True

        if self.__valid_size is True:
            self.__puzzle = Puzzle(self.__board)
            solved_puzzle_data = self.__puzzle.solve()
            self.__solved_puzzle = solved_puzzle_data[0]
            self.__solvable = solved_puzzle_data[1]
        
    def get_board_size(self):
        return int(self.__board_size)

    def is_board_valid(self):
        return self.__valid_size

    def is_puzzle_solvable(self):
        return self.__solvable

    def get_unsolved_puzzle(self):
        return self.__board

    def get_solved_puzzle(self):
        return self.__solved_puzzle


class NumbrixBoard(tk.Canvas):
    def __init__(self):
        self.__width = 400
        self.__height = 400
        super().__init__(width=self.__width, height=self.__height, background="lightgrey", highlightthickness=0)

    def draw_empty_board(self, size):
        self.__inputs_IDs = []
        self.__user_inputs = []
        rect_size = self.__width / size
        it = 0
        for y in range(0, size):
            for x in range(0, size):
                self.__user_inputs.append(tk.StringVar(self, "", '{}_{}'.format(x, y)))
                textentry = tk.Entry(self, font=14, justify=tk.CENTER, bg="lightgrey", bd=1, textvariable=self.__user_inputs[it])
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
                self.__inputs_IDs.append(id)
                it+=1

    def draw_board(self, board : Board):
        self.__inputs_IDs = []
        self.__user_inputs = []
        board_size = board.get_board_size()
        rect_size = self.__width / board_size
        it = 0
        for y in range(0, board_size):
            for x in range(0, board_size):
                rect_value = board.get_unsolved_puzzle()[it][1]
                if rect_value != 0:
                    self.__user_inputs.append(tk.StringVar(self, str(rect_value), '{}_{}'.format(x, y)))
                    self.create_rectangle(x * rect_size,
                                          y * rect_size, 
                                          x * rect_size + rect_size - 1, 
                                          y * rect_size + rect_size - 1, 
                                          fill="lightblue", 
                                          outline="black")
                else:
                    self.__user_inputs.append(tk.StringVar(self, "", '{}_{}'.format(x, y)))
                    textentry = tk.Entry(self, font=14, justify=tk.CENTER, bg="lightgrey", bd=1, textvariable=self.__user_inputs[it])
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
                    self.__inputs_IDs.append(id)
                it+=1

    def draw_solution(self, board : Board):
        board_size = board.get_board_size()
        rect_size = self.__width / board_size

        value = 1
        print((board_size*board_size))
        while value < (board_size*board_size)+1:
            it = 0
            for y in range(0, board_size):
                for x in range(0, board_size):
                    rect_value = board.get_solved_puzzle()[it][1]
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
                                         y * rect_size + rect_size / 2, 
                                         text=rect_value)
                    it+=1

    def draw_text(self, board : Board):
        board_size = board.get_board_size()
        rect_size = self.__width / board_size

        it = 0
        for y in range(0, board_size):
            for x in range(0, board_size):
                rect_value = board.get_unsolved_puzzle()[it][1]
                if rect_value != 0:
                    self.create_text(x * rect_size + rect_size / 2,
                                     y * rect_size + rect_size / 2, text=rect_value)
                it+=1
    
    def get_user_inputs(self):
        return self.__user_inputs

    def get_inputs_IDs(self):
        return self.__inputs_IDs


class Menubar(tk.Menu):
    def __init__(self, win: tk.Tk):
        super().__init__(win)
        # Set parent window for menubar
        self.__win = win
        # Create file menu
        self.__filemenu = tk.Menu(self, tearoff=0)
        self.__filemenu.add_command(label="Otwórz plik z łamigłówką...", command=lambda: self.select_file())
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Wyjście", command=lambda: self.close_app())
        self.add_cascade(label="Plik", menu=self.__filemenu)
        # Create solve menu
        self.__solvemenu = tk.Menu(self, tearoff=0)
        self.__solvemenu.add_command(label="Rozwiąż wybraną łamigłówkę", command=lambda: self.resolve())
        self.__solvemenu.add_command(label="Sprawdź poprawność rozwiązania łamigłówki", command=lambda: self.check_solution())
        self.__solvemenu.add_separator()
        self.__solvemenu.add_command(label="Uruchom opcję rozgrywki", command=lambda: self.enable_user_gameplay())
        self.add_cascade(label="Rozwiązanie", menu=self.__solvemenu)
        # Create user's puzzle menu
        self.__myownpuzzlemenu = tk.Menu(self, tearoff=0)
        self.__myownpuzzlemenu.add_command(label="Stwórz własną łamigłówkę", command=lambda: self.popup())
        self.__myownpuzzlemenu.add_command(label="Sprawdź rozwiązywalność", command=lambda: self.is_your_puzzle_solvable())
        self.__myownpuzzlemenu.add_command(label="Rozwiąż własną łamigłówkę", command=lambda: self.solve_my_own_puzzle())
        self.add_cascade(label="Własna łamigłówka", menu=self.__myownpuzzlemenu)
        # Set default values for numbrix board, user's board size and gameplay mode
        self.__board = None
        self.__numbrix = None
        self.__my_own_puzzle_size = 0
        self.__gameplay_mode = 0

    def popup(self):
        self.__popup_win = tk.Toplevel(self.__win)
        self.__popup_win.wm_title("Podaj rozmiary planszy")
        new_board_size = tk.Entry(self.__popup_win, text="Wpisz rozmiar...")
        new_board_size.grid(row=0, column=0)
        apply_button = tk.Button(self.__popup_win, text="Zatwierdź", command=lambda: self.close_popup(win, new_board_size))
        apply_button.grid(row=1, column=0)

    def close_popup(self, popup_win, new_board_size):
        try:
            self.__my_own_puzzle_size = int(new_board_size.get())
        except:
            print("Podana wartość nie jest wartością całkowitą")
            return

        self.__popup_win.destroy()
        if self.__numbrix == None:
            self.__numbrix = NumbrixBoard()
            self.__numbrix.pack()
        self.__numbrix.draw_empty_board(self.__my_own_puzzle_size)

    def is_your_puzzle_solvable(self):
        if self.__my_own_puzzle_size != 0:
            int_inputs = []
            for it in range(0, len(self.__numbrix.get_user_inputs())):
                if self.__numbrix.get_user_inputs()[it].get() == "":
                    int_inputs.append((it + 1, 0))
                else:
                    int_inputs.append((it + 1, int(self.__numbrix.get_user_inputs()[it].get())))
            try:
                self.__board = Board(int_inputs)
                if self.__board.is_puzzle_solvable() is True:
                    tk.messagebox.showinfo(title="Info", message="Wpisana przez Ciebie łamigłówka jest rozwiązywalna!")
                    return 1
            except TypeError:
                tk.messagebox.showinfo(title="Info", message="Wpisana przez Ciebie łamigłówka nie jest rozwiązywalna :(")
                return 0
        else:
            print("Nie można sprawdzić rozwiązywalności łamigłówki, która nie istnieje")

    def solve_my_own_puzzle(self):
        if self.__my_own_puzzle_size != 0:
            if self.is_your_puzzle_solvable() == 1:
                self.__numbrix.draw_text(self.__board)
                self.disable_user_gameplay()
                self.resolve()
        else:
            print("Nie stworzono łamigłówki")

    def entryValue(self):
        return self.__my_own_puzzle_size

    def enable_user_gameplay(self):
        if self.__numbrix == None:
            print("Nie wybrano planszy")
            return
        elif self.__numbrix != None and self.__my_own_puzzle_size == 0:
            for input_ID in self.__numbrix.get_inputs_IDs():
                self.__numbrix.itemconfigure(input_ID, state=tk.NORMAL)
            self.__gameplay_mode = 1

    def disable_user_gameplay(self):
        if self.__numbrix == None:
            return
        elif self.__numbrix != None:
            for input_ID in self.__numbrix.get_inputs_IDs():
                self.__numbrix.itemconfigure(input_ID, state=tk.HIDDEN)
            self.__gameplay_mode = 0

    def select_file(self):
        self.__my_own_puzzle_size = 0
        filename = tk.filedialog.askopenfilename(initialdir="C:\\", 
                                                 title="Wybierz plik", 
                                                 filetypes = (("Pliki tekstowe", "*.txt*"), ("Wszystkie pliki", "*.*")))
        try:
            self.__board = Board(read_board(filename))

            if not self.__board.is_board_valid() or not self.__board.is_puzzle_solvable():
                print("Wybrana plansza nie posiada poprawnych rozmiarów lub jest nierozwiązywalna")
                return

            if self.__numbrix == None:
                self.__numbrix = NumbrixBoard()
                self.__numbrix.pack()
                self.__numbrix.draw_board(self.__board)
                self.__numbrix.draw_text(self.__board)
            else:
                self.__numbrix.delete("all")
                self.__numbrix.draw_board(self.__board)
                self.__numbrix.draw_text(self.__board)

            ''' PRINTING DATA FROM USER INPUTS 
            inputs = [s.get() for s in self.numbrix.user_inputs]
            print(inputs)
            '''
        except FileNotFoundError:
            print("Użytkownik anulował operację")

    def close_app(self):
        self.__win.destroy()

    def check_solution(self):
        ''' PRINT SOLVED PUZZLE AND USER INPUTS - CHECK EQUALITY
        print([int(s.get()) for s in self.numbrix.user_inputs])
        print([s[1] for s in self.board.solved_puzzle])
        '''
        if self.__numbrix == None:
            print("Nie wybrano planszy")
            return
        elif self.__gameplay_mode == 0:
            print("Nie włączono trybu rozgrywki")
            return 

        try:
            if [int(s.get()) for s in self.__numbrix.get_user_inputs()] == [s[1] for s in self.__board.get_solved_puzzle()]:
                tk.messagebox.showinfo(title="Info", message="Brawo! Rozwiązałeś łamigłówkę!")
            else:
                tk.messagebox.showinfo(title="Info", message="Niestety Twoje rozwiązanie nie jest poprawne :(")
        except ValueError:
            tk.messagebox.showinfo(title="Info", message="Niestety Twoje rozwiązanie nie jest poprawne :(")
            return

    def resolve(self):
        if not self.__board:
            print("Nie wybrano planszy do rozwiązania")
            return
        elif self.__my_own_puzzle_size == 0:
            if self.__gameplay_mode == 1:
                self.disable_user_gameplay()

            if self.__board.is_board_valid() == True and self.__board.is_puzzle_solvable() == True:
                if self.__numbrix == None:
                    self.__numbrix = NumbrixBoard()
                    self.__numbrix.pack()
                    self.__numbrix.draw_solution(self.__board)
                else:
                    self.__numbrix.draw_solution(self.__board)
        else:
            print("Brak wczytanej planszy do rozwiązania")


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
