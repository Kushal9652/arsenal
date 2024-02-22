import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import cv2
import pygame
from threading import Thread

# Define initial window dimensions
initial_window_width = 400
initial_window_height = 300

def play_video_then_gui():
    def show_gui(window_width, window_height):
        cap.release()
        cv2.destroyAllWindows()
        initialize_gui(window_width, window_height)

    cap = cv2.VideoCapture("video.mp4")

    # Initialize Pygame for audio
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("audio.mp3")
    pygame.mixer.music.play()

    window_width, window_height = initial_window_width, initial_window_height

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow("initializing....", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    show_gui(window_width, window_height)

def initialize_gui(window_width, window_height):
    def call_arsenal():
        process = subprocess.Popen(
            ["python", "arsenal.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            shell=True
        )

        # Start a separate thread to read output in real-time
        thread = Thread(target=update_output, args=(process,))
        thread.start()

    def stop_execution():
        root.destroy()

    def update_output(process):
        while True:
            output_line = process.stdout.readline()
            error_line = process.stderr.readline()

            if not output_line and not error_line:
                break

            if output_line:
                output_text.insert(tk.END, output_line, "output")
            if error_line:
                output_text.insert(tk.END, error_line, "error")

            # Scroll to the bottom to show the latest output
            output_text.see(tk.END)
            output_text.update()

        process.wait()

    def increase_window():
        nonlocal window_width, window_height
        if window_width < screen_width and window_height < screen_height:
            window_width += 10
            window_height += 10
            root.geometry(f"{window_width}x{window_height}")
            root.after(20, increase_window)

    def reduce_window():
        nonlocal window_width, window_height
        new_width = int(window_width * 0.8)
        new_height = int(window_height * 0.8)
        root.geometry(f"{new_width}x{new_height}")

    def animate_text_color():
        colors = ['#ff0000', '#ff7f00', '#ffff00', '#00ff00', '#0000ff', '#2e2b5f', '#8b00ff']  # Modify colors as needed
        current_color = text_label['fg']
        try:
            next_color_index = (colors.index(current_color) + 1) % len(colors)
            next_color = colors[next_color_index]
        except ValueError:
            next_color = colors[0]  # Default to the first color if the current color is not found
        text_label.config(fg=next_color)
        root.after(500, animate_text_color)

    root = tk.Tk()
    root.title("arsenal")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    bg_image = Image.open("iron_man_background_image.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

    text_label = tk.Label(root, text="ARSENAL", font=("Arial", 30), fg="white")
    text_label.pack(pady=50)
    animate_text_color()

    button_style = {"font": ("Arial", 12), "bg": "#ff0000", "fg": "white", "relief": tk.RAISED,
                    "activebackground": "#d60000", "activeforeground": "white"}

    button = tk.Button(root, text="Start ARSENAL", command=call_arsenal, **button_style)
    button.pack(padx=10, pady=10)

    stop_button = tk.Button(root, text="Stop", command=stop_execution, **button_style)
    stop_button.pack(padx=10, pady=10)

    output_text = tk.Text(root, height=10, width=50, bg="black", fg="white", insertbackground="white")
    output_text.tag_configure("output", foreground="green")
    output_text.tag_configure("error", foreground="red")
    output_text.pack(pady=10)

    root.geometry(f"{window_width}x{window_height}")
    reduce_window()
    root.after(1000, increase_window)

    root.mainloop()

if __name__ == "__main__":
    play_video_then_gui()
