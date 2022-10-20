from tkinter import *
import pandas
from requirement import Requirement

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"




class Calculator:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("375x667+500+700")
        self.window.title("calculator")
        
        previous_expression = pandas.read_csv("calculator/history.csv")
        previous_calculation = str(previous_expression.previousCalculation[0])
        self.total_expression = previous_calculation

        #keeping history of the total expression done previously

        previous_total = pandas.read_csv("calculator/history.csv")
        previously = str(previous_total.previousTotal[0])
        self.current_expression = previously


        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()

        self.digits = Requirement().digits
        self.operations = Requirement().operations

        self.buttons_frame = self.create_buttons_frame()

        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()


    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))
    
    def create_special_buttons(self):
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_clear_button()


    def create_equals_button(self):
        equalButton = Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.equals)
        equalButton.grid(row=4, column=3, columnspan=2, sticky=NSEW)
        
    def equals(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "0"
            self.clear()

        finally:
            save_total = pandas.read_csv("calculator/history.csv")
            save_total.loc[0, "previousTotal"] = self.current_expression
            save_total.to_csv("history.csv", index=False)


            self.update_label()


        
    def create_square_button(self):
        equalButton = Button(self.buttons_frame, text="x\u00b2", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.square)
        equalButton.grid(row=0, column=2, sticky=NSEW)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_sqrt_button(self):
        equalButton = Button(self.buttons_frame, text="\u221ax", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.sqrt)
        equalButton.grid(row=0, column=3, sticky=NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_clear_button(self):
        equalButton = Button(self.buttons_frame, text="C", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.clear)
        equalButton.grid(row=0, column=1, sticky=NSEW)

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_buttons_frame(self):
        frame = Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=NSEW)
            i += 1

    def append_operator(self, operator):
        self.current_expression += operator   # suppose "+"
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()
        

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f'{symbol}')

            expression_data = pandas.read_csv("calculator/history.csv")
            expression_data.loc[0, "previousCalculation"] = expression
            expression_data.to_csv("history.csv", index=False)

        self.total_label.config(text=expression)

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=NSEW)
        

    def create_display_labels(self):
        total_label = Label(self.display_frame, text=self.total_expression, anchor=E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = Label(self.display_frame, text=self.current_expression, anchor=E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = Frame(self.window, height=211, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame
        
    def run(self):
        self.window.mainloop()




if __name__=="__main__":
    calculator = Calculator()
    calculator.run()
   

