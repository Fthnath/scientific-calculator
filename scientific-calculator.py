import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class UltimateCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Scientific Calculator")
        self.root.geometry("800x600")  # Reduced screen size
        self.root.minsize(700, 500)
        
        # Custom color scheme
        self.bg_color = "#2E3440"  # Dark blue-gray
        self.display_bg = "#3B4252"  # Slightly lighter
        self.display_fg = "#ECEFF4"  # Light gray
        self.number_btn = "#4C566A"  # Medium gray-blue
        self.number_fg = "#D8DEE9"  # Light gray
        self.operation_btn = "#5E81AC"  # Blue
        self.operation_fg = "#E5E9F0"  # Very light gray
        self.function_btn = "#88C0D0"  # Light blue
        self.function_fg = "#2E3440"  # Dark text
        self.memory_btn = "#A3BE8C"  # Green
        self.memory_fg = "#2E3440"  # Dark text
        self.special_btn = "#BF616A"  # Red
        self.special_fg = "#E5E9F0"  # Light text
        self.equals_btn = "#D08770"  # Orange
        self.equals_fg = "#2E3440"  # Dark text
        
        # Configure root background
        self.root.configure(bg=self.bg_color)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Provides better theming options
        
        # Configure the main frames
        self.style.configure('TFrame', background=self.bg_color)
        
        # Configure entry style
        self.style.configure('Calculator.TEntry', 
                            font=('Helvetica', 24),
                            foreground=self.display_fg,
                            background=self.display_bg,
                            borderwidth=0,
                            relief='flat',
                            padding=10)
        
        # Configure label styles
        self.style.configure('Title.TLabel', 
                           font=('Helvetica', 16, 'bold'),
                           foreground=self.display_fg,
                           background=self.bg_color)
        self.style.configure('Memory.TLabel',
                           font=('Helvetica', 10),
                           foreground=self.display_fg,
                           background=self.bg_color)
        
        # Configure button styles for different categories
        # Number buttons
        self.style.configure('Number.TButton',
                           font=('Helvetica', 14, 'bold'),
                           foreground=self.number_fg,
                           background=self.number_btn,
                           borderwidth=1,
                           relief='raised',
                           padding=5)
        
        # Operation buttons
        self.style.configure('Operation.TButton',
                           font=('Helvetica', 14, 'bold'),
                           foreground=self.operation_fg,
                           background=self.operation_btn,
                           borderwidth=1,
                           relief='raised',
                           padding=5)
        
        # Function buttons
        self.style.configure('Function.TButton',
                           font=('Helvetica', 12),
                           foreground=self.function_fg,
                           background=self.function_btn,
                           borderwidth=1,
                           relief='raised',
                           padding=5)
        
        # Memory buttons
        self.style.configure('Memory.TButton',
                           font=('Helvetica', 10),
                           foreground=self.memory_fg,
                           background=self.memory_btn,
                           borderwidth=1,
                           relief='raised',
                           padding=3)
        
        # Special buttons (clear, delete, etc.)
        self.style.configure('Special.TButton',
                           font=('Helvetica', 12),
                           foreground=self.special_fg,
                           background=self.special_btn,
                           borderwidth=1,
                           relief='raised',
                           padding=5)
        
        # Equals button
        self.style.configure('Equals.TButton',
                           font=('Helvetica', 14, 'bold'),
                           foreground=self.equals_fg,
                           background=self.equals_btn,
                           borderwidth=1,
                           relief='raised',
                           padding=5)
        
        # Notebook style
        self.style.configure('TNotebook', background=self.bg_color)
        self.style.configure('TNotebook.Tab', 
                           font=('Helvetica', 10),
                           foreground=self.display_fg,
                           background=self.bg_color,
                           padding=[10, 5])
        self.style.map('TNotebook.Tab', 
                      background=[('selected', self.display_bg)],
                      foreground=[('selected', self.display_fg)])
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')
        
        # Calculator tab
        self.create_calculator_tab()
        
        # Graphing tab
        self.create_graphing_tab()
        
        # Games tab
        self.create_games_tab()
        
        # History tab
        self.create_history_tab()
        
        # Initialize variables
        self.current_expression = ""
        self.history = []
        self.graph_functions = []
        
    def create_calculator_tab(self):
        """Create the calculator tab with scientific functions"""
        calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(calc_frame, text="Calculator")
        
        # Configure grid weights for responsive layout
        for i in range(12):
            calc_frame.grid_rowconfigure(i, weight=1)
        for i in range(6):
            calc_frame.grid_columnconfigure(i, weight=1)
        
        # Display
        self.entry_var = tk.StringVar()
        entry = ttk.Entry(calc_frame, textvariable=self.entry_var, 
                         style='Calculator.TEntry', justify='right')
        entry.grid(row=0, column=0, columnspan=6, sticky='nsew', padx=5, pady=5)
        
        # Memory display
        self.memory_var = tk.StringVar(value="Memory: 0")
        memory_label = ttk.Label(calc_frame, textvariable=self.memory_var,
                               style='Memory.TLabel')
        memory_label.grid(row=1, column=0, columnspan=6, sticky='w', padx=5)
        
        # Memory buttons
        mem_buttons = [
            ('MC', 2, 0, 'Memory.TButton'), 
            ('MR', 2, 1, 'Memory.TButton'), 
            ('M+', 2, 2, 'Memory.TButton'), 
            ('M-', 2, 3, 'Memory.TButton'), 
            ('MS', 2, 4, 'Memory.TButton'), 
            ('M▷', 2, 5, 'Memory.TButton'),
        ]
        
        for (text, row, col, style) in mem_buttons:
            button = ttk.Button(calc_frame, text=text, style=style,
                              command=lambda t=text: self.memory_operation(t))
            button.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        # Scientific buttons with their styles
        sci_buttons = [
            ('sin', 3, 0, 'Function.TButton'), ('cos', 3, 1, 'Function.TButton'), 
            ('tan', 3, 2, 'Function.TButton'), ('π', 3, 3, 'Function.TButton'), 
            ('e', 3, 4, 'Function.TButton'), ('⌫', 3, 5, 'Special.TButton'),
            ('asin', 4, 0, 'Function.TButton'), ('acos', 4, 1, 'Function.TButton'), 
            ('atan', 4, 2, 'Function.TButton'), ('x²', 4, 3, 'Function.TButton'), 
            ('x^y', 4, 4, 'Function.TButton'), ('C', 4, 5, 'Special.TButton'),
            ('sinh', 5, 0, 'Function.TButton'), ('cosh', 5, 1, 'Function.TButton'), 
            ('tanh', 5, 2, 'Function.TButton'), ('√x', 5, 3, 'Function.TButton'), 
            ('10^x', 5, 4, 'Function.TButton'), ('CE', 5, 5, 'Special.TButton'),
            ('log', 6, 0, 'Function.TButton'), ('ln', 6, 1, 'Function.TButton'), 
            ('x!', 6, 2, 'Function.TButton'), ('1/x', 6, 3, 'Function.TButton'), 
            ('e^x', 6, 4, 'Function.TButton'), ('±', 6, 5, 'Function.TButton'),
            ('(', 7, 0, 'Function.TButton'), (')', 7, 1, 'Function.TButton'), 
            ('Rand', 7, 2, 'Function.TButton'), ('|x|', 7, 3, 'Function.TButton'), 
            ('mod', 7, 4, 'Function.TButton'), ('=', 7, 5, 'Equals.TButton'),
            ('7', 8, 0, 'Number.TButton'), ('8', 8, 1, 'Number.TButton'), 
            ('9', 8, 2, 'Number.TButton'), ('+', 8, 3, 'Operation.TButton'), 
            ('Hex', 8, 4, 'Function.TButton'), ('Bin', 8, 5, 'Function.TButton'),
            ('4', 9, 0, 'Number.TButton'), ('5', 9, 1, 'Number.TButton'), 
            ('6', 9, 2, 'Number.TButton'), ('-', 9, 3, 'Operation.TButton'), 
            ('Deg', 9, 4, 'Function.TButton'), ('Rad', 9, 5, 'Function.TButton'),
            ('1', 10, 0, 'Number.TButton'), ('2', 10, 1, 'Number.TButton'), 
            ('3', 10, 2, 'Number.TButton'), ('*', 10, 3, 'Operation.TButton'), 
            ('F-E', 10, 4, 'Function.TButton'), ('Hist', 10, 5, 'Function.TButton'),
            ('0', 11, 0, 'Number.TButton'), ('.', 11, 1, 'Number.TButton'), 
            ('%', 11, 2, 'Number.TButton'), ('/', 11, 3, 'Operation.TButton'), 
            ('(', 11, 4, 'Function.TButton'), (')', 11, 5, 'Function.TButton'),
        ]
        
        # Create buttons with appropriate styles
        for (text, row, col, style) in sci_buttons:
            button = ttk.Button(calc_frame, text=text, style=style,
                              command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        # Initialize memory
        self.memory = 0
        self.angle_mode = 'deg'  # 'deg' or 'rad'
        self.number_format = 'normal'  # 'normal' or 'scientific'
    
    def create_graphing_tab(self):
        """Create the graphing tab with function plotting"""
        graph_frame = ttk.Frame(self.notebook)
        self.notebook.add(graph_frame, text="Graphing")
        
        # Configure grid weights
        graph_frame.grid_rowconfigure(1, weight=1)
        graph_frame.grid_columnconfigure(0, weight=1)
        
        # Graph controls
        control_frame = ttk.Frame(graph_frame)
        control_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Style for graph controls
        self.style.configure('Graph.TLabel',
                           font=('Helvetica', 10),
                           foreground=self.display_fg,
                           background=self.bg_color)
        
        self.style.configure('Graph.TEntry',
                           font=('Helvetica', 10),
                           foreground=self.function_fg,
                           background=self.display_bg,
                           borderwidth=1,
                           relief='sunken',
                           padding=3)
        
        self.style.configure('Graph.TButton',
                           font=('Helvetica', 10),
                           foreground=self.function_fg,
                           background=self.function_btn,
                           borderwidth=1,
                           relief='raised',
                           padding=3)
        
        ttk.Label(control_frame, text="Function:", style='Graph.TLabel').grid(row=0, column=0, padx=5)
        self.function_entry = ttk.Entry(control_frame, style='Graph.TEntry', width=30)
        self.function_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(control_frame, text="X min:", style='Graph.TLabel').grid(row=0, column=2, padx=5)
        self.xmin_entry = ttk.Entry(control_frame, style='Graph.TEntry', width=8)
        self.xmin_entry.insert(0, "-10")
        self.xmin_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(control_frame, text="X max:", style='Graph.TLabel').grid(row=0, column=4, padx=5)
        self.xmax_entry = ttk.Entry(control_frame, style='Graph.TEntry', width=8)
        self.xmax_entry.insert(0, "10")
        self.xmax_entry.grid(row=0, column=5, padx=5)
        
        plot_button = ttk.Button(control_frame, text="Plot", style='Graph.TButton', 
                               command=self.plot_function)
        plot_button.grid(row=0, column=6, padx=5)
        
        clear_button = ttk.Button(control_frame, text="Clear", style='Graph.TButton',
                                command=self.clear_graph)
        clear_button.grid(row=0, column=7, padx=5)
        
        # Matplotlib figure with dark theme
        plt.style.use('dark_background')
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#3B4252')  # Match the dark theme
        self.figure.patch.set_facecolor(self.bg_color)
        
        self.canvas = FigureCanvasTkAgg(self.figure, graph_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Function list
        list_frame = ttk.Frame(graph_frame)
        list_frame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
        
        self.function_listbox = tk.Listbox(list_frame, 
                                         height=5,
                                         bg=self.display_bg,
                                         fg=self.display_fg,
                                         selectbackground=self.operation_btn,
                                         selectforeground=self.operation_fg,
                                         font=('Courier', 10))
        self.function_listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        self.function_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.function_listbox.yview)
        
        # Function list controls
        list_control_frame = ttk.Frame(graph_frame)
        list_control_frame.grid(row=3, column=0, sticky='ew', padx=5, pady=5)
        
        ttk.Button(list_control_frame, text="Remove", style='Graph.TButton',
                  command=self.remove_function).pack(side='left', padx=5)
        ttk.Button(list_control_frame, text="Save Graph", style='Graph.TButton',
                  command=self.save_graph).pack(side='left', padx=5)
    
    def create_games_tab(self):
        """Create the games tab with simple math games"""
        games_frame = ttk.Frame(self.notebook)
        self.notebook.add(games_frame, text="Games")
        
        # Game selection
        game_choice_frame = ttk.Frame(games_frame)
        game_choice_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(game_choice_frame, text="Select Game:", style='Title.TLabel').pack(side='left', padx=5)
        
        self.game_var = tk.StringVar(value="math_quiz")
        
        # Style for radio buttons
        self.style.configure('Game.TRadiobutton',
                           font=('Helvetica', 10),
                           foreground=self.display_fg,
                           background=self.bg_color)
        
        games = [
            ("Math Quiz", "math_quiz"),
            ("Number Guesser", "number_guesser"),
            ("Equation Solver", "equation_solver"),
            ("Graph Challenge", "graph_challenge")
        ]
        
        for text, mode in games:
            ttk.Radiobutton(game_choice_frame, text=text, variable=self.game_var, 
                           value=mode, style='Game.TRadiobutton').pack(side='left', padx=5)
        
        # Game display area
        self.game_display = ttk.Frame(games_frame)
        self.game_display.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Start game button
        ttk.Button(games_frame, text="Start Game", style='Operation.TButton',
                  command=self.start_game).pack(pady=10)
    
    def create_history_tab(self):
        """Create the history tab to show previous calculations"""
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="History")
        
        # Configure grid weights
        history_frame.grid_rowconfigure(0, weight=1)
        history_frame.grid_columnconfigure(0, weight=1)
        
        # History listbox with scrollbar
        list_frame = ttk.Frame(history_frame)
        list_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        self.history_listbox = tk.Listbox(
            list_frame, 
            yscrollcommand=ttk.Scrollbar(list_frame).set,
            bg=self.display_bg,
            fg=self.display_fg,
            selectbackground=self.operation_btn,
            selectforeground=self.operation_fg,
            font=('Courier', 12),
            height=25
        )
        self.history_listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)
        
        # History controls
        control_frame = ttk.Frame(history_frame)
        control_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        
        ttk.Button(control_frame, text="Copy Selected", style='Memory.TButton',
                  command=self.copy_history_item).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Clear History", style='Memory.TButton',
                  command=self.clear_history).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Save History", style='Memory.TButton',
                  command=self.save_history).pack(side='left', padx=5)

    # [Rest of the methods remain exactly the same as in your original code]
    # All the calculator functions, graphing functions, and game functions
    # remain unchanged - I've only added styling to the UI components

    def on_button_click(self, button_text):
        # [Previous implementation remains exactly the same]
        if button_text == 'C':
            self.clear()
        elif button_text == 'CE':
            self.clear_entry()
        elif button_text == '⌫':
            self.backspace()
        elif button_text == '=':
            self.evaluate()
        elif button_text == 'π':
            self.add_to_expression(str(math.pi))
        elif button_text == 'e':
            self.add_to_expression(str(math.e))
        elif button_text == '±':
            self.negate()
        elif button_text == 'x²':
            self.add_to_expression('**2')
            self.evaluate()
        elif button_text == 'x^y':
            self.add_to_expression('**')
        elif button_text == 'x!':
            self.factorial()
        elif button_text == '1/x':
            self.reciprocal()
        elif button_text == '√x':
            self.add_to_expression('math.sqrt(')
        elif button_text == '10^x':
            self.add_to_expression('10**')
        elif button_text == 'e^x':
            self.add_to_expression('math.exp(')
        elif button_text == '|x|':
            self.add_to_expression('abs(')
        elif button_text == 'mod':
            self.add_to_expression('%')
        elif button_text == 'Rand':
            self.add_to_expression(str(random.random()))
        elif button_text == 'Deg':
            self.angle_mode = 'deg'
            messagebox.showinfo("Angle Mode", "Angle mode set to Degrees")
        elif button_text == 'Rad':
            self.angle_mode = 'rad'
            messagebox.showinfo("Angle Mode", "Angle mode set to Radians")
        elif button_text == 'F-E':
            self.toggle_number_format()
        elif button_text == 'Hex':
            self.convert_to_hex()
        elif button_text == 'Bin':
            self.convert_to_bin()
        elif button_text == 'Hist':
            self.notebook.select(3)  # Switch to history tab
        elif button_text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'log', 'ln']:
            self.add_to_expression(f'math.{button_text}(')
        else:
            self.add_to_expression(button_text)
    
    def memory_operation(self, op):
        # [Previous implementation remains exactly the same]
        try:
            if op == 'MC':  # Memory Clear
                self.memory = 0
            elif op == 'MR':  # Memory Recall
                self.add_to_expression(str(self.memory))
            elif op == 'M+':  # Memory Add
                self.memory += float(self.entry_var.get())
            elif op == 'M-':  # Memory Subtract
                self.memory -= float(self.entry_var.get())
            elif op == 'MS':  # Memory Store
                self.memory = float(self.entry_var.get())
            elif op == 'M▷':  # Memory Show
                self.notebook.select(3)  # History tab
                self.history_listbox.insert(tk.END, f"Memory Value: {self.memory}")
            
            self.memory_var.set(f"Memory: {self.memory}")
        except:
            messagebox.showerror("Error", "Invalid memory operation")
    
    def add_to_expression(self, value):
        # [Previous implementation remains exactly the same]
        self.current_expression += str(value)
        self.entry_var.set(self.current_expression)
    
    def clear(self):
        # [Previous implementation remains exactly the same]
        self.current_expression = ""
        self.entry_var.set("")
    
    def clear_entry(self):
        # [Previous implementation remains exactly the same]
        self.current_expression = ""
        self.entry_var.set("")
    
    def backspace(self):
        # [Previous implementation remains exactly the same]
        self.current_expression = self.current_expression[:-1]
        self.entry_var.set(self.current_expression)
    
    def negate(self):
        # [Previous implementation remains exactly the same]
        if self.current_expression:
            if self.current_expression[0] == '-':
                self.current_expression = self.current_expression[1:]
            else:
                self.current_expression = '-' + self.current_expression
            self.entry_var.set(self.current_expression)
    
    def factorial(self):
        # [Previous implementation remains exactly the same]
        try:
            num = float(self.current_expression)
            if num.is_integer() and num >= 0:
                result = math.factorial(int(num))
                self.current_expression = str(result)
                self.entry_var.set(self.current_expression)
                self.add_to_history(f"{int(num)}! = {result}")
            else:
                self.entry_var.set("Error: Integer >= 0 required")
                self.current_expression = ""
        except:
            self.entry_var.set("Error")
            self.current_expression = ""
    
    def reciprocal(self):
        # [Previous implementation remains exactly the same]
        try:
            num = float(self.current_expression)
            if num != 0:
                result = 1 / num
                self.current_expression = str(result)
                self.entry_var.set(self.current_expression)
                self.add_to_history(f"1/{num} = {result}")
            else:
                self.entry_var.set("Error: Division by zero")
                self.current_expression = ""
        except:
            self.entry_var.set("Error")
            self.current_expression = ""
    
    def toggle_number_format(self):
        # [Previous implementation remains exactly the same]
        try:
            num = float(self.entry_var.get())
            if self.number_format == 'normal':
                self.entry_var.set("{:.4e}".format(num))
                self.number_format = 'scientific'
            else:
                self.entry_var.set(str(num))
                self.number_format = 'normal'
        except:
            pass
    
    def convert_to_hex(self):
        # [Previous implementation remains exactly the same]
        try:
            num = int(float(self.entry_var.get()))
            self.entry_var.set(hex(num))
            self.add_to_history(f"{num} in hex = {hex(num)}")
        except:
            self.entry_var.set("Error")
            self.current_expression = ""
    
    def convert_to_bin(self):
        # [Previous implementation remains exactly the same]
        try:
            num = int(float(self.entry_var.get()))
            self.entry_var.set(bin(num))
            self.add_to_history(f"{num} in binary = {bin(num)}")
        except:
            self.entry_var.set("Error")
            self.current_expression = ""
    
    def evaluate(self):
        # [Previous implementation remains exactly the same]
        expression = self.current_expression
        
        try:
            # Replace special symbols and functions
            expression = expression.replace('^', '**')
            expression = expression.replace('mod', '%')
            
            # Handle angle mode for trigonometric functions
            if self.angle_mode == 'deg':
                expression = expression.replace('sin(', 'math.sin(math.radians(')
                expression = expression.replace('cos(', 'math.cos(math.radians(')
                expression = expression.replace('tan(', 'math.tan(math.radians(')
                expression = expression.replace('asin(', 'math.degrees(math.asin(')
                expression = expression.replace('acos(', 'math.degrees(math.acos(')
                expression = expression.replace('atan(', 'math.degrees(math.atan(')
            else:
                expression = expression.replace('sin(', 'math.sin(')
                expression = expression.replace('cos(', 'math.cos(')
                expression = expression.replace('tan(', 'math.tan(')
                expression = expression.replace('asin(', 'math.asin(')
                expression = expression.replace('acos(', 'math.acos(')
                expression = expression.replace('atan(', 'math.atan(')
            
            # Add closing parentheses for functions that might be missing them
            open_parens = expression.count('(')
            close_parens = expression.count(')')
            expression += ')' * (open_parens - close_parens)
            
            # Evaluate the expression
            result = eval(expression, {'math': math, 'np': np})
            
            self.current_expression = str(result)
            self.entry_var.set(self.current_expression)
            self.add_to_history(f"{self.current_expression} = {result}")
        except Exception as e:
            self.entry_var.set("Error")
            self.current_expression = ""
            self.add_to_history(f"Error evaluating: {expression}")
    
    def add_to_history(self, item):
        # [Previous implementation remains exactly the same]
        self.history.append(item)
        self.history_listbox.insert(tk.END, item)
        if len(self.history) > 100:  # Limit history size
            self.history.pop(0)
            self.history_listbox.delete(0)
    
    def copy_history_item(self):
        # [Previous implementation remains exactly the same]
        try:
            selection = self.history_listbox.get(self.history_listbox.curselection())
            self.root.clipboard_clear()
            self.root.clipboard_append(selection)
        except:
            pass
    
    def clear_history(self):
        # [Previous implementation remains exactly the same]
        self.history = []
        self.history_listbox.delete(0, tk.END)
    
    def save_history(self):
        # [Previous implementation remains exactly the same]
        try:
            with open('calculator_history.txt', 'w') as f:
                for item in self.history:
                    f.write(item + "\n")
            messagebox.showinfo("Success", "History saved to calculator_history.txt")
        except:
            messagebox.showerror("Error", "Could not save history")
    
    # Graphing functions
    def plot_function(self):
        # [Previous implementation remains exactly the same]
        func_text = self.function_entry.get()
        if not func_text:
            messagebox.showerror("Error", "Please enter a function")
            return
        
        try:
            x_min = float(self.xmin_entry.get())
            x_max = float(self.xmax_entry.get())
            
            if x_min >= x_max:
                messagebox.showerror("Error", "X min must be less than X max")
                return
            
            x = np.linspace(x_min, x_max, 400)
            
            # Prepare the function for evaluation
            func_str = func_text.replace('^', '**')
            func_str = func_str.replace('sin', 'np.sin')
            func_str = func_str.replace('cos', 'np.cos')
            func_str = func_str.replace('tan', 'np.tan')
            func_str = func_str.replace('log', 'np.log10')
            func_str = func_str.replace('ln', 'np.log')
            func_str = func_str.replace('sqrt', 'np.sqrt')
            func_str = func_str.replace('exp', 'np.exp')
            func_str = func_str.replace('abs', 'np.abs')
            
            # Handle angle mode
            if self.angle_mode == 'deg':
                func_str = func_str.replace('sin(', 'np.sin(np.deg2rad(')
                func_str = func_str.replace('cos(', 'np.cos(np.deg2rad(')
                func_str = func_str.replace('tan(', 'np.tan(np.deg2rad(')
            
            y = eval(func_str, {'np': np, 'x': x, 'math': math})
            
            # Plot the function
            self.ax.clear()
            self.ax.plot(x, y, label=func_text)
            self.ax.axhline(0, color='black', linewidth=0.5)
            self.ax.axvline(0, color='black', linewidth=0.5)
            self.ax.grid(True)
            self.ax.legend()
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_title(f'Graph of {func_text}')
            
            self.canvas.draw()
            
            # Add to function list
            self.graph_functions.append(func_text)
            self.function_listbox.insert(tk.END, func_text)
            
            # Add to history
            self.add_to_history(f"Plotted: {func_text} from {x_min} to {x_max}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not plot function: {str(e)}")
    
    def remove_function(self):
        # [Previous implementation remains exactly the same]
        try:
            index = self.function_listbox.curselection()[0]
            self.function_listbox.delete(index)
            self.graph_functions.pop(index)
            
            # Redraw all remaining functions
            self.ax.clear()
            x_min = float(self.xmin_entry.get())
            x_max = float(self.xmax_entry.get())
            x = np.linspace(x_min, x_max, 400)
            
            for func_text in self.graph_functions:
                func_str = func_text.replace('^', '**')
                func_str = func_str.replace('sin', 'np.sin')
                func_str = func_str.replace('cos', 'np.cos')
                func_str = func_str.replace('tan', 'np.tan')
                func_str = func_str.replace('log', 'np.log10')
                func_str = func_str.replace('ln', 'np.log')
                func_str = func_str.replace('sqrt', 'np.sqrt')
                func_str = func_str.replace('exp', 'np.exp')
                func_str = func_str.replace('abs', 'np.abs')
                
                if self.angle_mode == 'deg':
                    func_str = func_str.replace('sin(', 'np.sin(np.deg2rad(')
                    func_str = func_str.replace('cos(', 'np.cos(np.deg2rad(')
                    func_str = func_str.replace('tan(', 'np.tan(np.deg2rad(')
                
                y = eval(func_str, {'np': np, 'x': x, 'math': math})
                self.ax.plot(x, y, label=func_text)
            
            self.ax.axhline(0, color='black', linewidth=0.5)
            self.ax.axvline(0, color='black', linewidth=0.5)
            self.ax.grid(True)
            if self.graph_functions:
                self.ax.legend()
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_title('Graph of Functions')
            
            self.canvas.draw()
        except:
            pass
    
    def clear_graph(self):
        # [Previous implementation remains exactly the same]
        self.ax.clear()
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        self.ax.grid(True)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('Graph of Functions')
        self.canvas.draw()
        
        self.graph_functions = []
        self.function_listbox.delete(0, tk.END)
    
    def save_graph(self):
        # [Previous implementation remains exactly the same]
        try:
            file_path = simpledialog.askstring("Save Graph", "Enter file name (without extension):")
            if file_path:
                self.figure.savefig(f"{file_path}.png")
                messagebox.showinfo("Success", f"Graph saved as {file_path}.png")
                self.add_to_history(f"Graph saved as {file_path}.png")
        except:
            messagebox.showerror("Error", "Could not save graph")
    
    # Game functions
    def start_game(self):
        # [Previous implementation remains exactly the same]
        game_type = self.game_var.get()
        
        # Clear previous game
        for widget in self.game_display.winfo_children():
            widget.destroy()
        
        if game_type == "math_quiz":
            self.math_quiz_game()
        elif game_type == "number_guesser":
            self.number_guesser_game()
        elif game_type == "equation_solver":
            self.equation_solver_game()
        elif game_type == "graph_challenge":
            self.graph_challenge_game()

    def math_quiz_game(self):
        self.quiz_score = 0
        self.quiz_question_count = 0
        
        # Game title
        ttk.Label(self.game_display, text="Math Quiz Challenge", 
                 style='Title.TLabel').pack(pady=10)
        
        # Score display
        self.quiz_score_var = tk.StringVar(value="Score: 0/0")
        ttk.Label(self.game_display, textvariable=self.quiz_score_var,
                 style='Title.TLabel').pack()
        
        # Question display
        self.quiz_question_var = tk.StringVar()
        question_label = ttk.Label(self.game_display, 
                                 textvariable=self.quiz_question_var,
                                 style='Title.TLabel',
                                 font=('Helvetica', 14))
        question_label.pack(pady=20)
        
        # Answer entry
        answer_frame = ttk.Frame(self.game_display)
        answer_frame.pack(pady=10)
        
        ttk.Label(answer_frame, text="Your Answer:", style='Title.TLabel').pack(side='left')
        
        self.quiz_answer_entry = ttk.Entry(answer_frame, style='Calculator.TEntry', width=15)
        self.quiz_answer_entry.pack(side='left', padx=5)
        
        # Submit button
        submit_button = ttk.Button(self.game_display, text="Submit", 
                                 style='Operation.TButton',
                                 command=self.check_quiz_answer)
        submit_button.pack(pady=10)
        
        # Next question button
        next_button = ttk.Button(self.game_display, text="Next Question", 
                               style='Operation.TButton',
                               command=self.generate_quiz_question)
        next_button.pack(pady=5)
        
        # Generate first question
        self.generate_quiz_question()
    
    def generate_quiz_question(self):
        """Generate a random math question"""
        operations = ['+', '-', '*', '/']
        operation = random.choice(operations)
        
        if operation == '+':
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            self.correct_answer = num1 + num2
        elif operation == '-':
            num1 = random.randint(1, 100)
            num2 = random.randint(1, num1)  # Ensure positive result
            self.correct_answer = num1 - num2
        elif operation == '*':
            num1 = random.randint(1, 12)
            num2 = random.randint(1, 12)
            self.correct_answer = num1 * num2
        else:  # division
            num2 = random.randint(1, 10)
            self.correct_answer = random.randint(1, 10)
            num1 = num2 * self.correct_answer  # Ensure integer result
        
        self.quiz_question_var.set(f"What is {num1} {operation} {num2}?")
        self.quiz_answer_entry.delete(0, tk.END)
        self.quiz_answer_entry.focus()
    
    def check_quiz_answer(self):
        """Check if the user's answer is correct"""
        try:
            user_answer = float(self.quiz_answer_entry.get())
            if abs(user_answer - self.correct_answer) < 0.0001:  # Account for floating point
                self.quiz_score += 1
                messagebox.showinfo("Correct!", "Your answer is correct!")
            else:
                messagebox.showinfo("Incorrect", 
                                  f"Sorry, the correct answer was {self.correct_answer}")
            
            self.quiz_question_count += 1
            self.quiz_score_var.set(f"Score: {self.quiz_score}/{self.quiz_question_count}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def number_guesser_game(self):
        """Number guessing game"""
        self.secret_number = random.randint(1, 100)
        self.guess_count = 0
        
        # Game title
        ttk.Label(self.game_display, text="Number Guesser", 
                 style='Title.TLabel').pack(pady=10)
        
        # Instructions
        ttk.Label(self.game_display, 
                 text="I'm thinking of a number between 1 and 100.",
                 style='Title.TLabel').pack()
        
        # Guess entry
        guess_frame = ttk.Frame(self.game_display)
        guess_frame.pack(pady=10)
        
        ttk.Label(guess_frame, text="Your Guess:", style='Title.TLabel').pack(side='left')
        
        self.guess_entry = ttk.Entry(guess_frame, style='Calculator.TEntry', width=10)
        self.guess_entry.pack(side='left', padx=5)
        
        # Submit button
        submit_button = ttk.Button(self.game_display, text="Guess", 
                                 style='Operation.TButton',
                                 command=self.check_guess)
        submit_button.pack(pady=10)
        
        # Feedback label
        self.guess_feedback = ttk.Label(self.game_display, text="",
                                       style='Title.TLabel')
        self.guess_feedback.pack()
        
        # New game button
        new_game_button = ttk.Button(self.game_display, text="New Game", 
                                   style='Operation.TButton',
                                   command=self.number_guesser_game)
        new_game_button.pack(pady=5)
    
    def check_guess(self):
        """Check the user's guess against the secret number"""
        try:
            guess = int(self.guess_entry.get())
            self.guess_count += 1
            
            if guess < self.secret_number:
                self.guess_feedback.config(text="Too low! Try a higher number.")
            elif guess > self.secret_number:
                self.guess_feedback.config(text="Too high! Try a lower number.")
            else:
                self.guess_feedback.config(
                    text=f"Congratulations! You found the number in {self.guess_count} guesses!")
                self.secret_number = None  # Prevent further guessing
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer between 1 and 100")
    
    def equation_solver_game(self):
        """Game where the user solves random equations"""
        self.equation_score = 0
        self.equation_attempts = 0
        
        # Game title
        ttk.Label(self.game_display, text="Equation Solver Challenge", 
                 style='Title.TLabel').pack(pady=10)
        
        # Score display
        self.equation_score_var = tk.StringVar(value="Score: 0/0")
        ttk.Label(self.game_display, textvariable=self.equation_score_var,
                 style='Title.TLabel').pack()
        
        # Equation display
        self.equation_var = tk.StringVar()
        equation_label = ttk.Label(self.game_display, 
                                  textvariable=self.equation_var,
                                  style='Title.TLabel',
                                  font=('Helvetica', 14))
        equation_label.pack(pady=20)
        
        # Answer entry
        answer_frame = ttk.Frame(self.game_display)
        answer_frame.pack(pady=10)
        
        ttk.Label(answer_frame, text="x =", style='Title.TLabel').pack(side='left')
        
        self.equation_answer_entry = ttk.Entry(answer_frame, 
                                             style='Calculator.TEntry', 
                                             width=10)
        self.equation_answer_entry.pack(side='left', padx=5)
        
        # Submit button
        submit_button = ttk.Button(self.game_display, text="Submit", 
                                 style='Operation.TButton',
                                 command=self.check_equation_solution)
        submit_button.pack(pady=10)
        
        # New equation button
        new_eq_button = ttk.Button(self.game_display, text="New Equation", 
                                 style='Operation.TButton',
                                 command=self.generate_equation)
        new_eq_button.pack(pady=5)
        
        # Generate first equation
        self.generate_equation()
    
    def generate_equation(self):
        """Generate a random linear equation to solve"""
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        c = random.randint(1, 10)
        
        # Equation form: ax + b = c
        self.equation_solution = (c - b) / a
        
        self.equation_var.set(f"{a}x + {b} = {c}")
        self.equation_answer_entry.delete(0, tk.END)
        self.equation_answer_entry.focus()
    
    def check_equation_solution(self):
        """Check if the user's solution is correct"""
        try:
            user_solution = float(self.equation_answer_entry.get())
            if abs(user_solution - self.equation_solution) < 0.0001:  # Account for floating point
                self.equation_score += 1
                messagebox.showinfo("Correct!", "Your solution is correct!")
            else:
                messagebox.showinfo("Incorrect", 
                                  f"Sorry, the correct solution was x = {self.equation_solution}")
            
            self.equation_attempts += 1
            self.equation_score_var.set(f"Score: {self.equation_score}/{self.equation_attempts}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def graph_challenge_game(self):
        """Game where the user identifies functions from graphs"""
        self.graph_score = 0
        self.graph_attempts = 0
        
        # Game title
        ttk.Label(self.game_display, text="Graph Challenge", 
                 style='Title.TLabel').pack(pady=10)
        
        # Score display
        self.graph_score_var = tk.StringVar(value="Score: 0/0")
        ttk.Label(self.game_display, textvariable=self.graph_score_var,
                 style='Title.TLabel').pack()
        
        # Create a frame for the graph
        graph_frame = ttk.Frame(self.game_display)
        graph_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Matplotlib figure for the game
        self.game_figure = plt.Figure(figsize=(5, 3), dpi=100)
        self.game_ax = self.game_figure.add_subplot(111)
        self.game_ax.set_facecolor('#3B4252')
        self.game_figure.patch.set_facecolor(self.bg_color)
        
        self.game_canvas = FigureCanvasTkAgg(self.game_figure, graph_frame)
        self.game_canvas.get_tk_widget().pack(expand=True, fill='both')
        
        # Function options
        self.function_options = [
            "x", "x**2", "x**3", "sqrt(x)", "sin(x)", "cos(x)", 
            "tan(x)", "exp(x)", "log(x)", "abs(x)"
        ]
        
        # Current correct function
        self.correct_function = ""
        
        # Options frame
        options_frame = ttk.Frame(self.game_display)
        options_frame.pack(pady=10)
        
        # Radio buttons for function selection
        self.selected_function = tk.StringVar()
        
        for i, func in enumerate(self.function_options):
            rb = ttk.Radiobutton(options_frame, text=func, 
                                variable=self.selected_function,
                                value=func,
                                style='Game.TRadiobutton')
            rb.grid(row=i//2, column=i%2, sticky='w', padx=5)
        
        # Submit button
        submit_button = ttk.Button(self.game_display, text="Submit", 
                                 style='Operation.TButton',
                                 command=self.check_graph_answer)
        submit_button.pack(pady=10)
        
        # New graph button
        new_graph_button = ttk.Button(self.game_display, text="New Graph", 
                                    style='Operation.TButton',
                                    command=self.generate_graph_question)
        new_graph_button.pack(pady=5)
        
        # Generate first question
        self.generate_graph_question()
    
    def generate_graph_question(self):
        """Generate a random graph for the user to identify"""
        self.game_ax.clear()
        
        # Select a random function
        self.correct_function = random.choice(self.function_options)
        
        # Generate the graph
        x = np.linspace(-5, 5, 400)
        
        if self.correct_function == "sqrt(x)":
            x = np.linspace(0, 5, 400)
        
        y = eval(self.correct_function, {'np': np, 'x': x, 'math': math, 'sqrt': np.sqrt})
        
        self.game_ax.plot(x, y)
        self.game_ax.axhline(0, color='white', linewidth=0.5)
        self.game_ax.axvline(0, color='white', linewidth=0.5)
        self.game_ax.grid(True)
        self.game_ax.set_title("Identify this function")
        
        self.game_canvas.draw()
        self.selected_function.set("")  # Clear selection
    
    def check_graph_answer(self):
        """Check if the user correctly identified the function"""
        if not self.selected_function.get():
            messagebox.showerror("Error", "Please select a function")
            return
        
        if self.selected_function.get() == self.correct_function:
            self.graph_score += 1
            messagebox.showinfo("Correct!", "You identified the function correctly!")
        else:
            messagebox.showinfo("Incorrect", 
                              f"Sorry, the correct function was {self.correct_function}")
        
        self.graph_attempts += 1
        self.graph_score_var.set(f"Score: {self.graph_score}/{self.graph_attempts}")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateCalculator(root)
    root.mainloop()
