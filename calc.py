import tkinter as tk
from math import sqrt

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("350x550")


        self.expression = ""
        self.memory = 0
        self.entry_text = tk.StringVar()      
        self.last_button = None
        # Отслеживание был ли показан результат для перемотки в начало или конец и функциональности CE
        self.result_shown = False  

        self.display()
        self.buttons()

        # Возможность ввода с клавиатуры
        self.bind("<Key>", self.keyboard)

    def display(self):
        
        display_frame = tk.Frame(self)
        display_frame.pack(expand=True, fill="both")

        # Экран калькулятора
        self.entry = tk.Entry(display_frame, textvariable=self.entry_text, font=("Arial", 26), justify="right", bd=0, bg="#eee")
        self.entry.pack(expand=True, fill="both", padx=10)

    def buttons(self):
        # Кнопки памяти
        first_row_frame = tk.Frame(self)
        first_row_frame.pack(fill="x", padx=5, pady=1)

        first_row_buttons = {
            "MC": (0, 0), "MR": (0, 1), "MS": (0, 2), "M+": (0, 3), "M-": (0, 4)
        }
        for btn_text, grid_value in first_row_buttons.items():
            button = tk.Button(first_row_frame, text=btn_text, bg="#eee", fg="lightgrey" if btn_text in ("MC", "MR") else "black", font=("Arial", 12), borderwidth=0, width=6)
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW, padx=1, pady=1)
            button.bind('<Button-1>', lambda event, b=btn_text: self.click(b))                     # Связывание нажатия левой кнопки мыши с текстом кнопки
            setattr(self, f"button_{btn_text}", button)

        # Остальные кнопки калькулятора
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(expand=True, fill="both")

        buttons = {
            "7": (1, 0), "8": (1, 1), "9": (1, 2), "/": (1, 3),
            "4": (2, 0), "5": (2, 1), "6": (2, 2), "*": (2, 3),
            "1": (3, 0), "2": (3, 1), "3": (3, 2), "-": (3, 3),
            "pow": (4, 0), "0": (4, 1), ".": (4, 2), "+": (4, 3),
            "sqrt": (5, 0), "C": (5, 1), "CE": (5, 2), "=": (5, 3)
        }
        for btn_text, grid_value in buttons.items():
            button = tk.Button(buttons_frame, text=btn_text, bg="white", fg="black", font=("Arial", 14), borderwidth=0, width=10)
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW, padx=1, pady=1)
            button.bind('<Button-1>', lambda event, b=btn_text: self.click(b))

        for i in range(6):
            buttons_frame.rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1)

    def color_buttons(self):
        # Изменение цвета кнопок памяти
        if self.memory == 0:
            self.button_MC.config(fg="lightgrey")
            self.button_MR.config(fg="lightgrey")
        else:
            self.button_MC.config(fg="black")
            self.button_MR.config(fg="black")

    def click(self, button):
        # Обработка нажатий 
        if button == "=":
            try:
                # Вычисление выражения с помощью eval
                result = eval(self.expression)
                # Преобразование в целое число
                self.expression = str(int(result)) if result == int(result) else str(result)
                self.result_shown = True
            except Exception:
                self.expression = "Error"
                self.result_shown = True
        # Сброс
        elif button == "C":
            self.expression = ""
        # Если результат был получен, то CE сбрасывает, если нет, то удаляет последний символ 
        elif button == "CE":
            if self.result_shown:
                self.expression = "0"
            else:
                self.expression = self.expression[:-1]
                
        elif button == "sqrt":
            try:
                result = sqrt(eval(self.expression))
                self.expression = str(int(result)) if result == int(result) else str(result)
                self.result_shown = True
            except Exception:
                self.expression = "Error"
                self.result_shown = True
        # Ввод символа функции возведения в степень
        elif button == "pow":
            self.expression += "**"
            self.result_shown = False
            
        # Функциональность кнопок памяти с изменением цвета     
        elif button == "MC":
            self.memory = 0   
            self.color_buttons()     
        elif button == "MR":                   
            if self.expression == "0" or self.result_shown:
                self.expression = str(self.memory)
            elif self.last_button != "MR":
                self.expression += str(self.memory) 
            self.result_shown = False        
        elif button == "MS":
            try:
                self.memory = eval(self.expression)
                self.color_buttons()
            except Exception:
                self.expression = "Error"
                self.result_shown = True
        elif button == "M+":
            try:
                self.memory += eval(self.expression)
                self.color_buttons()
            except Exception:
                self.expression = "Error"
                self.result_shown = True
        elif button == "M-":
            try:
                self.memory -= eval(self.expression)
                self.color_buttons()
            except Exception:
                self.expression = "Error"
                self.result_shown = True
        else:
            if self.expression == "0" or self.expression == "Error":
                self.expression = ""
            # Продолжение ввода
            self.expression += button
            self.result_shown = False  

        # Обновление экрана
        self.entry_text.set(self.expression)
        
        if self.result_shown:
            self.entry.xview_moveto(0)  # Прокрутка к началу если результат был получен
        else:
            self.entry.icursor(tk.END)
            self.entry.xview_moveto(1)  # Прокрутка к концу если ввод продолжается
        self.last_button = button

    def keyboard(self, event):
        # Обработка нажатий с клавиатуры
        char = event.char
        if char.isdigit() or char in '+-*/.':
            self.click(char)
        elif char == '\r':  # Клавиша '=' на клавиатуре
            self.click('=')
        elif char == '\b':  # Клавиша Backspace 
            self.click('CE')

if __name__ == "__main__":
    calc = Calculator()
    calc.mainloop()
