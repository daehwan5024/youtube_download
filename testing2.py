import tkinter as tk
import threading
import time


main_window = tk.Tk()
main_window.geometry('200x200')

sub_window = tk.Toplevel(main_window)
sub_window.geometry('100x100')

sub_window.mainloop()
print('ended')
main_window.mainloop()
