import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


def convert_temperature():
    try:
        temp = float(entry_temp.get())
        unit = combo_from.get()

        if unit == "Celsius":
            c = temp
        elif unit == "Fahrenheit":
            c = (temp - 32) * 5 / 9
        elif unit == "Kelvin":
            c = temp - 273.15

        f = (c * 9 / 5) + 32
        k = c + 273.15

        label_result.config(
            text=f"Celsius: {c:.2f} °C\nFahrenheit: {f:.2f} °F\nKelvin: {k:.2f} K"
        )

        if c < 0:
            desc = "Freezing ❄️"
            color = "#90e0ef"
        elif c < 20:
            desc = "Cold 🧊"
            color = "#48cae4"
        elif c < 30:
            desc = "Pleasant 🌤️"
            color = "#95d5b2"
        else:
            desc = "Hot ☀️"
            color = "#f4a261"

        label_desc.config(text="Condition: " + desc, bg=color)

        global graph_values
        graph_values = [c, f, k]

    except ValueError:
        messagebox.showerror("Error", "Enter a valid number")


def show_graph():
    try:
        units = ["Celsius", "Fahrenheit", "Kelvin"]

        plt.figure()
        plt.bar(units, graph_values)
        plt.title("Temperature Comparison")
        plt.xlabel("Units")
        plt.ylabel("Temperature")
        plt.show()

    except NameError:
        messagebox.showwarning("Warning", "Convert temperature first")


def resize_bg(event):
    global current_bg

    # Ignore tiny startup events
    if event.width < 2 or event.height < 2:
        return

    # Resize only when size changes
    if event.width == resize_bg.last_width and event.height == resize_bg.last_height:
        return

    resize_bg.last_width = event.width
    resize_bg.last_height = event.height

    resized = original_bg_image.resize((event.width, event.height))
    current_bg = ImageTk.PhotoImage(resized)
    bg_label.config(image=current_bg)


resize_bg.last_width = 0
resize_bg.last_height = 0

# ---------------- GUI Window ----------------
root = tk.Tk()
root.title("Temperature Converter")
root.geometry("500x400")
root.resizable(True, True)

# Force window to calculate size first
root.update_idletasks()

# ---------------- Background Image using Pillow ----------------
original_bg_image = Image.open("background.jpg")

initial_width = 500
initial_height = 400
current_bg = ImageTk.PhotoImage(original_bg_image.resize((initial_width, initial_height)))

bg_label = tk.Label(root, image=current_bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Bind resize after initial background is already shown
root.bind("<Configure>", resize_bg)

# ---------------- Title ----------------
title = tk.Label(
    root,
    text="Temperature Converter",
    font=("Arial", 16, "bold"),
    bg="lightblue"
)
title.pack(pady=10)

# ---------------- Input ----------------
tk.Label(root, text="Enter Temperature:", bg="lightblue").pack()

entry_temp = tk.Entry(root)
entry_temp.pack(pady=5)

# ---------------- Unit Selection ----------------
tk.Label(root, text="Select Unit:", bg="lightblue").pack()

combo_from = ttk.Combobox(
    root,
    values=["Celsius", "Fahrenheit", "Kelvin"],
    state="readonly"
)
combo_from.current(0)
combo_from.pack(pady=5)

# ---------------- Convert Button ----------------
btn_convert = tk.Button(root, text="Convert", command=convert_temperature)
btn_convert.pack(pady=10)

# ---------------- Result ----------------
label_result = tk.Label(
    root,
    text="Result",
    font=("Arial", 12),
    bg="lightblue"
)
label_result.pack(pady=5)

# ---------------- Description ----------------
label_desc = tk.Label(
    root,
    text="Condition",
    font=("Arial", 20, "bold"),
    bg="lightblue"
)
label_desc.pack(pady=5)

# ---------------- Graph Button ----------------
btn_graph = tk.Button(root, text="Show Graph", command=show_graph)
btn_graph.pack(pady=10)

root.mainloop()
