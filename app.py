from tkinter import (
    filedialog,
    messagebox
)
import tkinter as tk
from puzzle import read_board
from math import sqrt


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
        
    def get_board_size(self):
        return int(self._board_size)


class NumbrixBoard(tk.Canvas):
    def __init__(self):
        self.width = 400
        self.height = 400
        super().__init__(width=self.width, height=self.height, background="lightgrey", highlightthickness=0)

    def draw_board(self, board : Board):
        board_size = board.get_board_size()
        rect_size = self.width / board_size
        it = 0
        for y in range(0, board_size):
            for x in range(0, board_size):
                rect_value = board.board[it][1]
                if rect_value != 0:
                    self.create_rectangle(x * rect_size, y * rect_size, 
                                          x * rect_size + rect_size, 
                                          y * rect_size + rect_size, 
                                          fill="lightblue", 
                                          outline="black")
                    self.create_text(x * rect_size + rect_size / 2, 
                                     y * rect_size + rect_size / 2, text=rect_value)
                else:
                    self.create_rectangle(x * rect_size, 
                                          y * rect_size, 
                                          x * rect_size + rect_size, 
                                          y * rect_size + rect_size, 
                                          fill="darkgrey", 
                                          outline="black")
                it+=1


class Menubar(tk.Menu):
    def __init__(self, win: tk.Tk):
        super().__init__(win)

        self.filemenu = tk.Menu(self, tearoff=0)
        self.filemenu.add_command(label="Otwórz planszę...", command=lambda: self.select_file(win))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Wyjście", command=lambda: self.close_app(win))
        self.add_cascade(label="Plik", menu=self.filemenu)

        self.solvemenu = tk.Menu(self, tearoff=0)
        self.solvemenu.add_command(label="Rozwiąż wybraną planszę")
        self.add_cascade(label="Rozwiązanie", menu=self.solvemenu)

        self.numbrix = None

    def select_file(self, win: tk.Tk):
        self.filename = tk.filedialog.askopenfilename(initialdir="C:\\", 
                                                      title="Wybierz plik", 
                                                      filetypes = (("Pliki tekstowe", "*.txt*"), ("Wszystkie pliki", "*.*")))
        try:
            board = Board(self.filename)

            if not board.valid:
                return

            if self.numbrix == None:
                self.numbrix = NumbrixBoard()
                self.numbrix.pack()
                self.numbrix.draw_board(board)
            else:
                self.numbrix.draw_board(board)
        except FileNotFoundError:
            print("Użytkownik anulował operację")

    def close_app(self, win: tk.Tk):
        win.destroy()


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
