# Author Loïc Rutabana, developing code by Dr. Dejongh

from tkinter import filedialog
import customtkinter as ctk
import os

class LogFile:
  def __init__(self, filename, pathname, first_time, first_open, scale_factor):
    self.filename = filename
    self.pathname = pathname
    self.first_time = first_time
    self.first_open = first_open
    self.scale_factor = scale_factor

def create_ui():
  ctk.set_appearance_mode("dark")
  ctk.set_default_color_theme("dark-blue")

  root = ctk.CTk()
  root.geometry("750x750")
  
  file_count = 1
  logfiles = []
  labels = []

  max_files = 10

  # Logic

  def printf1():
    print("file 1")

  # utility to insure that user enters a value numeric
  def is_number(s):
      try:
        if (s==""):
          return True
        float(s)
        return True
      except ValueError:
          return False
  
  def file_explorer():
    path = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    if (path != ""):
      logfiles.append(path)
      filename = os.path.basename(path)
      labels[len(logfiles)-1].configure(text=filename, text_color="#0066bf")

  # GUI
  frame = ctk.CTkScrollableFrame(root, width=550, height=1000)
  frame.pack(pady=10, padx=10)
  frame.pack_propagate(False)

  inner_frame = ctk.CTkFrame(frame, width=500, height=70, fg_color="transparent")
  inner_frame.grid(pady=10, padx=10, column=0, row=1)
  # inner_frame.grid_propagate(False)

  path_entry = ctk.CTkEntry(frame, width=500, placeholder_text="Path to file/folder")
  path_entry.grid(pady=30, padx=10, column=0, row=0)

  fil1_btn = ctk.CTkButton(inner_frame, text=f'File {file_count}', command=file_explorer, width=70, height=50)
  fil1_btn.grid(pady=10, padx=10, column=1, row=0)

  # Create a Tcl wrapper for the validation command. It makes sure input is numeric
  vcmd = (root.register(is_number), '%P')
  sc1_btn = ctk.CTkEntry(inner_frame, width=70, height=50, validate="key", validatecommand=vcmd)
  sc1_btn.grid(pady=10, padx=10, column=2, row=0)

  file1_name_lbl = ctk.CTkLabel(inner_frame, text=f'File {file_count} Name')
  file1_name_lbl.grid(pady=10, column=3, row=0)
  labels.append(file1_name_lbl)

  file1_read_btn = ctk.CTkButton(inner_frame, text="Read", command=printf1, width=70, height=50)
  file1_read_btn.grid(pady=10, padx=10, column=4, row=0)

  # Appends a new frame for a new file entry. Allows up to 10 files
  def new_file_entry():
    nonlocal file_count, vcmd

    remove_error_messages()
    if file_count == len(logfiles):
      file_count += 1
      if (file_count <= 10):
        new_frame = ctk.CTkFrame(frame, width=500, height=70, fg_color="transparent")
        new_frame.grid(pady=10, padx=10, column=0, row=file_count)
        # inner_frame.grid_propagate(False)

        fil_btn = ctk.CTkButton(new_frame, text=f'File {file_count}', command=printf1, width=70, height=50)
        fil_btn.grid(pady=10, padx=10, column=1, row=0)


        sc_btn = ctk.CTkEntry(new_frame, width=70, height=50, validate="key", validatecommand=vcmd)
        sc_btn.grid(pady=10, padx=10, column=2, row=0)

        file_name_lbl = ctk.CTkLabel(new_frame, text=f'File {file_count} Name')
        file_name_lbl.grid(pady=10, column=3, row=0)
        labels.append(file_name_lbl)

        file_read_btn = ctk.CTkButton(new_frame, text="Read", command=file_explorer, width=70, height=50)
        file_read_btn.grid(pady=10, padx=10, column=4, row=0)

        add_file_btn = ctk.CTkButton(frame, text="Add File", command=new_file_entry if file_count < max_files else file_overflow_error, width=70, height=50)
        add_file_btn.grid(pady=10, padx=10, column=0, row=file_count+1)
      else:
        file_count = 10
    else:
      empty_file_error()

  # ERROR MESSAGES

  # Error: too many files are added
  def file_overflow_error():
    error_label = ctk.CTkLabel(frame, text="Only 10 Files permitted", text_color="red")
    error_label.grid(pady=10, column=0, row=file_count+2)

  # Error: Attempted to add new file entry when one is still empty
  def empty_file_error():
    error_label = ctk.CTkLabel(frame, text="Empty file entry", text_color="red")
    error_label.grid(pady=10, column=0, row=file_count+2)

  def remove_error_messages():
    for widget in frame.winfo_children():
      if isinstance(widget, ctk.CTkLabel) and widget["text_color"] == "red":
        widget.destroy()

  add_file_btn = ctk.CTkButton(frame, text="Add File", command=new_file_entry, width=70, height=50)
  add_file_btn.grid(pady=10, padx=10, column=0, row=2)

  # Custom close function
  def on_close():
    print("exiting")
    exit()
  #     print("exiting ", logfilename)
  #     check_file = os.path.isfile(logfilename)
  # #    print(check_file)
  # #    print(not check_file)
  #     if (not check_file):
  #         print("bye-bye")
  #         app.destroy()
  #         return
  #     now = datetime.now()
  #     midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
  #     seconds = (now - midnight).seconds
  #     print(seconds)
  #     print(first_filename)
  #     start_index = first_filename.find("hist")
  #     end_index = first_filename.find("_",start_index)
  #     rename_logfilename = first_filename[:start_index] + "log_" + str(seconds) + first_filename[end_index:]
  #     print(logfilename)
  #     print(rename_logfilename)
  #     os.rename(logfilename,rename_logfilename)
  #     app.destroy()
  
  root.protocol("WM_DELETE_WINDOW", on_close)
  root.mainloop()

create_ui()