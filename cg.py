import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.colorchooser import askcolor
from PIL import Image, ImageDraw, ImageTk, ImageGrab
import random

class DrawingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Drawing App")
        self.geometry("900x600")

        # Custom ttk style
        style = ttk.Style()
        style.configure("TButton", padding=10, relief="raised", font=("Helvetica", 12))
        style.configure("TLabel", font=("Helvetica", 12))

        # Initial settings
        self.current_tool = "pencil"
        self.start_x, self.start_y = 0, 0
        self.color = "black"
        self.size = 2
        self.shapes = []

        # Setting up the canvas
        self.canvas = tk.Canvas(self, width=800, height=600, bg="white", relief="sunken", borderwidth=2)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tool frame
        self.tools_frame = ttk.Frame(self, padding=(10, 10))
        self.tools_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Tools and shape selection
        self.tools_box = ttk.LabelFrame(self.tools_frame, text="Tools", padding=(10, 10))
        self.shapes_box = ttk.LabelFrame(self.tools_frame, text="Shapes", padding=(10, 10))
        self.tools_box.pack(pady=10, padx=10, fill=tk.X)
        self.shapes_box.pack(pady=10, padx=10, fill=tk.X)

        self.tool_buttons = {
            "Pencil": ttk.Button(self.tools_box, text="Pencil", command=lambda: self.set_tool("pencil")),
            "Eraser": ttk.Button(self.tools_box, text="Eraser", command=lambda: self.set_tool("eraser")),
            "Spray": ttk.Button(self.tools_box, text="Spray", command=lambda: self.set_tool("spray")),
        }

        for button in self.tool_buttons.values():
            button.pack(pady=5, fill=tk.X)

        self.shape_buttons = {
            "Line": ttk.Button(self.shapes_box, text="Line", command=lambda: self.set_tool("line")),
            "Rectangle": ttk.Button(self.shapes_box, text="Rectangle", command=lambda: self.set_tool("rectangle")),
            "Circle": ttk.Button(self.shapes_box, text="Circle", command=lambda: self.set_tool("circle")),
        }

        for button in self.shape_buttons.values():
            button.pack(pady=5, fill=tk.X)

        # Brush size control
        self.brush_size_label = ttk.Label(self.tools_box, text="Brush Size:")
        self.brush_size_label.pack(pady=5, fill=tk.X)
        self.brush_size_frame = ttk.Frame(self.tools_box)
        self.brush_size_frame.pack(pady=5, fill=tk.X)

        self.size_minus_button = ttk.Button(self.brush_size_frame, text="-", command=self.decrease_brush_size)
        self.size_minus_button.grid(row=0, column=0, padx=5)
        self.brush_size_entry = ttk.Label(self.brush_size_frame, text=str(self.size))
        self.brush_size_entry.grid(row=0, column=1)
        self.size_plus_button = ttk.Button(self.brush_size_frame, text="+", command=self.increase_brush_size)
        self.size_plus_button.grid(row=0, column=2, padx=5)

        # Color Picker
        self.color_button = ttk.Button(self.tools_box, text="Pick Color", command=self.set_color)
        self.color_button.pack(pady=5, fill=tk.X)

        # Save and Load
        self.save_button = ttk.Button(self.tools_frame, text="Save", command=self.save_image)
        self.save_button.pack(pady=5, fill=tk.X)
        self.load_button = ttk.Button(self.tools_frame, text="Load", command=self.load_image)
        self.load_button.pack(pady=5, fill=tk.X)

        # Clear Canvas
        self.clear_button = ttk.Button(self.tools_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(pady=5, fill=tk.X)

        # Canvas bindings
        self.canvas.bind("<Button-1>", self.on_start)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)

    def set_tool(self, tool_name):
        self.current_tool = tool_name

    def set_color(self):
        color_code = askcolor()
        if color_code:
            self.color = color_code[1]

    def increase_brush_size(self):
        self.size += 1
        self.update_brush_size_label()

    def decrease_brush_size(self):
        if self.size > 1:
            self.size -= 1
            self.update_brush_size_label()

    def update_brush_size_label(self):
        self.brush_size_entry.config(text=str(self.size))

    def clear_canvas(self):
        self.shapes = []
        self.canvas.delete("all")

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png")])
        if file_path:
            x = self.winfo_rootx() + self.canvas.winfo_x()
            y = self.winfo_rooty() + self.canvas.winfo_y()
            width = x + self.canvas.winfo_width()
            height = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, width, height)).save(file_path)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            img = Image.open(file_path)
            self.bg_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

    def on_start(self, event):
        self.start_x, self.start_y = event.x, event.y

    def on_drag(self, event):
        if self.current_tool == "pencil":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=self.size)
            self.start_x, self.start_y = event.x, event.y
        elif self.current_tool == "eraser":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill="white", width=self.size)
            self.start_x, self.start_y = event.x, event.y
        elif self.current_tool == "spray":
            for _ in range(50):
                x, y = random.randint(-self.size, self.size), random.randint(-self.size, self.size)
                self.canvas.create_oval(event.x + x, event.y + y, event.x + x + 1, event.y + y + 1, fill=self.color)

    def on_drop(self, event):
        if self.current_tool == "line":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=self.size)
        elif self.current_tool == "rectangle":
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.color, width=self.size)
        elif self.current_tool == "circle":
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.color, width=self.size)

if __name__ == "__main__":
    app = DrawingApp()
    app.mainloop()
