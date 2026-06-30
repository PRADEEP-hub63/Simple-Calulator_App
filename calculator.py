import tkinter as tk
import math

# Windows-style dark calculator theme
BG = "#1f1f1f"
BTN_BG = "#333333"
BTN_FG = "#ffffff"
EQUALS_BG = "#4cc2ff"
EQUALS_FG = "#1f1f1f"
DISPLAY_BG = "#1f1f1f"
DISPLAY_FG = "#ffffff"
FONT = ("Segoe UI", 13)
DISPLAY_FONT = ("Segoe UI", 32, "bold")


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("340x520")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.display_var = tk.StringVar(value="0")
        self.stored_value = None
        self.current_operator = None
        self.reset_on_next = False

        self._build_ui()

    def _build_ui(self):
        display_frame = tk.Frame(self.root, bg=BG, padx=16, pady=20)
        display_frame.pack(fill="x")

        tk.Label(
            display_frame,
            textvariable=self.display_var,
            anchor="e",
            bg=DISPLAY_BG,
            fg=DISPLAY_FG,
            font=DISPLAY_FONT,
            padx=4,
            pady=8,
        ).pack(fill="x")

        keypad = tk.Frame(self.root, bg=BG, padx=10, pady=8)
        keypad.pack(fill="both", expand=True)

        buttons = [
            ("%", self.percent, BTN_BG),
            ("CE", self.clear_entry, BTN_BG),
            ("C", self.clear_all, BTN_BG),
            ("⌫", self.backspace, BTN_BG),
            ("1/x", self.reciprocal, BTN_BG),
            ("x²", self.square, BTN_BG),
            ("²√x", self.square_root, BTN_BG),
            ("÷", lambda: self.set_operator("/"), BTN_BG),
            ("7", lambda: self.append_digit("7"), BTN_BG),
            ("8", lambda: self.append_digit("8"), BTN_BG),
            ("9", lambda: self.append_digit("9"), BTN_BG),
            ("×", lambda: self.set_operator("*"), BTN_BG),
            ("4", lambda: self.append_digit("4"), BTN_BG),
            ("5", lambda: self.append_digit("5"), BTN_BG),
            ("6", lambda: self.append_digit("6"), BTN_BG),
            ("−", lambda: self.set_operator("-"), BTN_BG),
            ("1", lambda: self.append_digit("1"), BTN_BG),
            ("2", lambda: self.append_digit("2"), BTN_BG),
            ("3", lambda: self.append_digit("3"), BTN_BG),
            ("+", lambda: self.set_operator("+"), BTN_BG),
            ("+/-", self.toggle_sign, BTN_BG),
            ("0", lambda: self.append_digit("0"), BTN_BG),
            (".", self.append_decimal, BTN_BG),
            ("=", self.calculate, EQUALS_BG),
        ]

        for index, (text, command, bg) in enumerate(buttons):
            row, col = divmod(index, 4)
            fg = EQUALS_FG if text == "=" else BTN_FG
            btn = tk.Button(
                keypad,
                text=text,
                command=command,
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                relief="flat",
                borderwidth=0,
                highlightthickness=0,
                font=FONT,
            )
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        for i in range(4):
            keypad.columnconfigure(i, weight=1, uniform="btn")
        for i in range(6):
            keypad.rowconfigure(i, weight=1, uniform="btn")

    def get_value(self):
        try:
            return float(self.display_var.get())
        except ValueError:
            return 0.0

    def set_display(self, value):
        if isinstance(value, float) and value.is_integer():
            text = str(int(value))
        else:
            text = str(value)
            if len(text) > 12:
                text = f"{value:.6g}"
        self.display_var.set(text)

    def append_digit(self, digit):
        current = self.display_var.get()
        if current == "Error":
            current = "0"
        if self.reset_on_next or current == "0":
            self.display_var.set(digit)
            self.reset_on_next = False
        else:
            self.display_var.set(current + digit)

    def append_decimal(self):
        current = self.display_var.get()
        if current == "Error":
            current = "0"
        if self.reset_on_next:
            self.display_var.set("0.")
            self.reset_on_next = False
        elif "." not in current:
            self.display_var.set(current + ".")

    def toggle_sign(self):
        if self.display_var.get() == "Error":
            return
        value = self.get_value()
        self.set_display(-value)

    def percent(self):
        if self.display_var.get() == "Error":
            return
        self.set_display(self.get_value() / 100)
        self.reset_on_next = True

    def clear_entry(self):
        self.display_var.set("0")
        self.reset_on_next = False

    def clear_all(self):
        self.display_var.set("0")
        self.stored_value = None
        self.current_operator = None
        self.reset_on_next = False

    def backspace(self):
        current = self.display_var.get()
        if self.reset_on_next or current in ("0", "Error"):
            return
        if len(current) == 1 or (len(current) == 2 and current.startswith("-")):
            self.display_var.set("0")
        else:
            self.display_var.set(current[:-1])

    def reciprocal(self):
        value = self.get_value()
        if value == 0:
            self.display_var.set("Error")
            self.reset_on_next = True
        else:
            self.set_display(1 / value)
            self.reset_on_next = True

    def square(self):
        value = self.get_value()
        self.set_display(value ** 2)
        self.reset_on_next = True

    def square_root(self):
        value = self.get_value()
        if value < 0:
            self.display_var.set("Error")
            self.reset_on_next = True
        else:
            self.set_display(math.sqrt(value))
            self.reset_on_next = True

    def set_operator(self, operator):
        if self.display_var.get() == "Error":
            return
        if self.current_operator and not self.reset_on_next:
            self.calculate()
        self.stored_value = self.get_value()
        self.current_operator = operator
        self.reset_on_next = True

    def calculate(self):
        if self.current_operator is None or self.stored_value is None:
            return

        current = self.get_value()
        op = self.current_operator

        if op == "+":
            result = self.stored_value + current
        elif op == "-":
            result = self.stored_value - current
        elif op == "*":
            result = self.stored_value * current
        elif op == "/":
            if current == 0:
                self.display_var.set("Error")
                self.reset_on_next = True
                self.current_operator = None
                self.stored_value = None
                return
            result = self.stored_value / current
        else:
            return

        self.set_display(result)
        self.current_operator = None
        self.stored_value = None
        self.reset_on_next = True


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
