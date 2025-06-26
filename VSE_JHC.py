import pyautogui as pya
import time as ti
import keyboard as key
import threading as thr
import tkinter as tk
import sys
import ctypes

e_stop = False
restart_flag = False
stop_message_printed = False
purple_thread = None

coords = [
    (1490, 513),
    (1194, 184),
    (1194, 322),
    (1195, 444),
    (1202, 581),
    (1202, 691),
    (799, 663),
    (56, 145)
]

def purple_place_clothes():
    global e_stop
    try:
        while not e_stop:
            for x, y in coords:
                print(f"Moving to: x={x}, y={y}")
                pya.moveTo(x, y)
                pya.click(x, y)
                ti.sleep(sleep_duration)
                if e_stop:
                    break
        if not stop_message_printed:
            stop_message_printed = True
        print('Stopped Script due to E_stop..')
    except KeyboardInterrupt:
        pass

def e_stop_act():
    global e_stop, restart_flag
    while True:
        key.wait('f6')
        e_stop = True
        print('Emergency stop executed. Killing Program...')
        while e_stop:
            key.wait('f7')
            e_stop = False
            restart_flag = True
            print('Restarting Script... ')
            break

def disable_typing(event):
    return "break"

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, output):
        self.text_widget.insert(tk.END, output)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

def start_threads():
    global purple_thread, stop_message_printed, sleep_duration

    sleep_duration_str = variable_text.get('1.0', tk.END).strip()

    if sleep_duration_str == '' or sleep_duration_str == '.' or sleep_duration_str == '/':
        sleep_duration = 1.0
    else:
        sleep_duration = float(sleep_duration_str)

    if not stop_message_printed:
        stop_message_printed = True

    if purple_thread and purple_thread.is_alive():
        e_stop = True
        purple_thread.join()

    purple_thread = thr.Thread(target=purple_place_clothes, daemon=True)
    purple_thread.start()

def minimize_console():
    if sys.platform == "win32":
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 6)

if __name__ == "__main__":
    minimize_console()

window = tk.Tk()
window.title("Purple Place VSE Auto Script 1.3")

window.geometry("400x300+4+240")
window.resizable(False, False)

window.attributes('-topmost', True)

output_text = tk.Text(window, borderwidth=2, relief="solid", height=13)
output_text.pack(expand=True, fill=tk.X, pady=0)
output_text.bind("<Key>", disable_typing)

sys.stdout = StdoutRedirector(output_text)
output_text.insert(tk.END, "| Purple Place Game |\n| Very Sharp Eye Auto Achievement Script |\n| Made by JHCode |\n| F6 to stop | F7 to start |\n", 'welcome')
output_text.tag_config('welcome', foreground='#0000FF', font=('Arial', 12, 'bold'))

variable_text = tk.Text(window, borderwidth=2, relief="solid", height=1, width=5)
variable_text.pack(expand=True, fill=tk.BOTH)
variable_text.insert(tk.END, "1.0")

def disable_enter(event):
    return "break"

variable_text.bind('<Return>', disable_enter)

window.update_idletasks()
variable_text.place(relx=1.0, rely=1.0, anchor=tk.SE, bordermode='outside', x=-3, y=-10)

instruct_text = tk.Label(window, text="Add the time variable you want to use \n in 10th's of a second.\n ex: .3, .5, 1, 2, etc. ------------>",padx=5, pady=10, font=('Arial', 12, 'bold'))
instruct_text.pack(side=tk.LEFT, anchor=tk.W)

stop_thread = thr.Thread(target=e_stop_act, daemon=True)
stop_thread.start()

start_threads()

def main_loop():
    global restart_flag
    while True:
        if restart_flag or not purple_thread.is_alive():
            restart_flag = False
            start_threads()
        window.update_idletasks()
        window.update()

main_thread = thr.Thread(target=main_loop, daemon=True)
main_thread.start()

window.mainloop()
