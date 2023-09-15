import tkinter as tk
from tkinter import Button, Entry, Label, Toplevel, Scale, HORIZONTAL, OptionMenu, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading

# Global variables for storing settings
speed_var = None
color_var = None
color_line_var = None
size_var = None
button_press_time = 0
cur_pos = (500, 500, 500)
end_pos = (365, 450, 465)
is_paused = False
is_running = False
is_force_stopped = False
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']



def step_3d(current_pos, target_pos):
    x0, y0, z0 = current_pos
    x1, y1, z1 = target_pos
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    dz = abs(z1 - z0)

    if x0 < x1:
        sx = 1
    else:
        sx = -1

    if y0 < y1:
        sy = 1
    else:
        sy = -1

    if z0 < z1:
        sz = 1
    else:
        sz = -1

    if dx >= dy and dx >= dz:
        err1 = 2 * dy - dx
        err2 = 2 * dz - dx
        x0 += sx
        if err1 > 0:
            y0 += sy
            err1 -= 2 * dx
        if err2 > 0:
            z0 += sz
            err2 -= 2 * dx
        err1 += 2 * dy
        err2 += 2 * dz

    elif dy >= dx and dy >= dz:
        err1 = 2 * dx - dy
        err2 = 2 * dz - dy
        y0 += sy
        if err1 > 0:
            x0 += sx
            err1 -= 2 * dy
        if err2 > 0:
            z0 += sz
            err2 -= 2 * dy
        err1 += 2 * dx
        err2 += 2 * dz

    else:  # dz is the dominant axis
        err1 = 2 * dy - dz
        err2 = 2 * dx - dz
        z0 += sz
        if err1 > 0:
            y0 += sy
            err1 -= 2 * dz
        if err2 > 0:
            x0 += sx
            err2 -= 2 * dz
        err1 += 2 * dy
        err2 += 2 * dx

    return (x0, y0, z0)

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    
def stop_visualization():
    global is_running
    is_running = False
    
def force_stop_visualization():
    global is_force_stopped
    is_force_stopped = True   
    
def visualize_movement():
    global speed_var, color_var, cur_pos, end_pos, canvas, is_paused, is_running, is_force_stopped, color_line_var, size_var
    positions_x = positions_y = positions_z = None
    positions_x = [cur_pos[0]]
    positions_y = [cur_pos[1]]
    positions_z = [cur_pos[2]]
    is_running = True
    is_force_stopped = False
    while cur_pos != end_pos and is_running:
        
        if is_force_stopped:
            break
        
        if(is_paused):
            time.sleep(0.1)
            continue
        
        cur_pos = step_3d(cur_pos, end_pos)
        positions_x.append(cur_pos[0])
        positions_y.append(cur_pos[1])
        positions_z.append(cur_pos[2])
        # Clear the chart before drawing a new line
        ax.plot(positions_x, positions_y, positions_z, linestyle='-',color = color_var.get(), marker ='s', markersize = size_var.get(), markeredgecolor=color_line_var.get())
        # Set the current position
        coord_label.config(text=f"Position: {cur_pos}")
        canvas.draw()
        canvas.flush_events()
        # Refreshing the Tkinter window
        time.sleep(speed_var.get() / 1000.0)
        
    is_running = False  # Complete the visualization
    
    # Lock/Unlock the button after the animation is complete
    start_button.config(state=tk.NORMAL)
    pause_button.config(state=tk.DISABLED)
    reset_button.config(state=tk.DISABLED)

# Function to open a new window for setting chart parameters
def open_settings_window():
    global speed_var, color_var, colors, color_line_var, size_var
    settings_window = Toplevel(root)
    settings_window.geometry("250x350")
    settings_window.title("Settings")
    def set_speed(value):
        speed_var.set(value)
        return
    def set_color(value):
        color_var.set(value)
        return
    def set_line_color(value):
        color_line_var.set(value)
        return
    def set_size(value):
        size_var.set(value)
        return
    # Label and Scale to select the speed between chart steps
    speed_label = Label(settings_window, text="Speed (ms):")
    speed_label.pack()
    
    speed_scale = Scale(settings_window, from_=1, to=1000, orient=HORIZONTAL, command=set_speed)
    speed_scale.set(speed_var.get()) 
    speed_scale.pack(pady=10)
    
    # Label and menu for selecting the color of chart points from predefined options
    pcolor_label = Label(settings_window, text="Point color:")
    pcolor_label.pack()
    
    pcolor_menu = OptionMenu(settings_window, color_var, *colors, command = set_color)
    pcolor_menu.pack(pady=10)
    
    #Label and menu to select the chart line color from predefined options
    color_label = Label(settings_window, text="Line color:")
    color_label.pack()
    
    color_menu = OptionMenu(settings_window, color_line_var, *colors, command = set_line_color)
    color_menu.pack(pady=10)
    
   # Label and Scale to select the size between chart steps
    size_label = Label(settings_window, text="Size: ")
    size_label.pack()
    
    size_scale = Scale(settings_window, from_ = 1, to = 10, orient=HORIZONTAL, command=set_size)
    size_scale.set(size_var.get())
    size_scale.pack(pady=10)

def open_coordinates_window():
    global end_pos
    coordinates_window = Toplevel(root)
    coordinates_window.title("Set coords:")
    
    coordinates_window.resizable(False, False)
    
    coord_frame = tk.Frame(coordinates_window)
    coord_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    # Label and Entry to set the X coordinate
    x_label = Label(coord_frame, text="X:")
    x_label.grid(row = 0, column = 0)
    x_scale = Scale(coord_frame, from_ = 0, to = 500, orient=HORIZONTAL)
    x_scale.set(end_pos[0]) 
    x_scale.grid(row = 1, column = 0)
    
    # Label and Entry to set the Y coordinate
    y_label = Label(coord_frame, text="Y:")
    y_label.grid(row = 0, column = 1)
    y_scale = Scale(coord_frame, from_ = 0, to = 500, orient=HORIZONTAL)
    y_scale.set(end_pos[1]) 
    y_scale.grid(row = 1, column = 1)
    
    # Label and Entry to set the Z coordinate
    z_label = Label(coord_frame, text="Z:")
    z_label.grid(row = 0, column = 2)
    z_scale = Scale(coord_frame, from_ = 0, to = 500, orient=HORIZONTAL)
    z_scale.set(end_pos[2]) 
    z_scale.grid(row = 1, column = 2)
    
    # Button to confirm the selected coordinates
    confirm_button = Button(coordinates_window, text="Submit", command=lambda: set_coordinates(int(x_scale.get()), int(y_scale.get()), int(z_scale.get()), coordinates_window))
    confirm_button.pack(pady = 10)

def set_coordinates(x, y, z, window):
    global end_pos, is_running
    if(is_running):
        return
    try:
        x = int(x)
        y = int(y)
        z = int(z)
        if 0 <= x <= 500 and 0 <= y <= 500 and 0 <= z <= 500:
            end_pos = (x, y, z)
            coord_label2.config(text=f"End position: {end_pos}")
            window.destroy()  # Close the window after selecting coordinates
        else:
            messagebox.showerror("Error", "The coordinates must be between 0 and 500.")
    except ValueError:
        messagebox.showerror("Error", f"Enter the correct numeric values for the coordinates. {x},{y},{z}")


def start_visualization():
    global cur_pos, end_pos, is_paused, is_running
    if is_running:
        messagebox.showinfo("Warning", "The visualization is already up and running.")
        return
    
    is_running = True
    start_button.config(state=tk.DISABLED)
    pause_button.config(state=tk.NORMAL)
    reset_button.config(state=tk.NORMAL)
    visualization_thread = threading.Thread(target=visualize_movement)
    visualization_thread.start()

# Create a Tkinter window
root = tk.Tk()
root.title("Visualization 3d motion")
root.geometry("550x700")
root.resizable(False, False)

# Creating a canvas for drawing matplotlib
fig = Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_xlim(0, 500)
ax.set_ylim(0, 500)
ax.set_zlim(0, 500)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

def zoom_zero(event):
    global button_press_time
    if(event.button!=2):
        return
    else:
        current_time = time.time()
        # Check if it's a double-click (within 0.5 seconds)
        if current_time - button_press_time < 0.5:
            ax.set_xlim(0, 500)
            ax.set_ylim(0, 500)
            ax.set_zlim(0, 500)
            fig.canvas.draw()
        button_press_time = current_time
         
fig.canvas.mpl_connect('button_press_event', zoom_zero)

def zoom(event):
    # Get the current axis limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    zlim = ax.get_zlim()
    # Determine the zoom factor
    zoom_factor = 1.1

    if event.button == 'up':
        # Zoom in by decreasing the axis limits
        new_xlim = (xlim[0] / zoom_factor, xlim[1] / zoom_factor)
        new_ylim = (ylim[0] / zoom_factor, ylim[1] / zoom_factor)
        new_zlim = (zlim[0] / zoom_factor, zlim[1] / zoom_factor)
    elif event.button == 'down':
        # Zoom out by increasing the axis limits
        new_xlim = (xlim[0] * zoom_factor, xlim[1] * zoom_factor)
        new_ylim = (ylim[0] * zoom_factor, ylim[1] * zoom_factor)
        new_zlim = (zlim[0] * zoom_factor, zlim[1] * zoom_factor)
    else:
        return  # Ignore other mouse events

    # Set the new axis limits to zoom in or out
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)
    ax.set_zlim(new_zlim)

    # Redraw the plot
    fig.canvas.draw()
    
fig.canvas.mpl_connect('scroll_event', zoom)

# Create a Frame for placing the buttons
btn_frame = tk.Frame(root)
btn_frame.pack(side=tk.TOP, expand=True, anchor=tk.CENTER)

# Create a button to start drawing
start_button = Button(btn_frame, text="▶", command=start_visualization, width=2, height=1, disabledforeground="pink")
start_button.pack(side=tk.LEFT, padx=5, pady =10)

pause_button = Button(btn_frame, text="||", command=toggle_pause, width=2, height=1, disabledforeground="pink")
pause_button.pack(side=tk.LEFT, padx=5, pady =10)
pause_button.config(state=tk.DISABLED)

reset_button = Button(btn_frame, text="∎", command=force_stop_visualization, width=2, height=1, disabledforeground="pink")
reset_button.pack(side=tk.LEFT, padx=5, pady =10)
reset_button.config(state=tk.DISABLED)

set_button = Button(btn_frame, text="📈", command=open_coordinates_window, width=2, height=1, disabledforeground="pink")
set_button.pack(side=tk.LEFT, padx=5, pady =10)

# Create Frame to place Label with coordinate
coord_frame = tk.Frame(root)
coord_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create Label to display the current coordinate
coord_label = Label(coord_frame, text="Position: (0, 0, 0)")
coord_label.pack(pady=10)
coord_label2 = Label(coord_frame, text=f"End position: {end_pos}")
coord_label2.pack(pady=10)

# Create a button to open the settings window and automatically apply settings
settings_button = Button(root, text="Settings", command=open_settings_window)
settings_button.pack(pady=10)

# Create variables to store the settings
speed_var = tk.IntVar()
speed_var.set(1) 

color_var = tk.StringVar()
color_var.set('b')

color_line_var = tk.StringVar()
color_line_var.set('y')

size_var = tk.IntVar()
size_var.set(2) 

try:
    icon_path = "icon.ico"  
    root.iconbitmap(icon_path)
except:
    print("Problem with icon")

root.mainloop()