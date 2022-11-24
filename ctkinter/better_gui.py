import customtkinter
import tkinter.messagebox

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

def search():
    pass

main_window = customtkinter.CTk()
main_window.wm_title('youtube downloader')
main_window.geometry('500x500')
main_window.iconbitmap(default='../youtube.ico')

link_frame = customtkinter.CTkFrame(main_window)
link_frame.pack(fill='x', padx=5, pady=5, ipady=5)
youtube_link_input_entry = customtkinter.CTkEntry(link_frame)
youtube_link_input_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5, ipady=5)
link_confirm_button = customtkinter.CTkButton(link_frame, text='찾아보기', command=search)
link_confirm_button.pack(side='right', fill='x', expand=False, padx=5, pady=5, ipady=5)



main_window.mainloop()
