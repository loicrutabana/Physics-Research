# Author Loïc Rutabana, developing code by Dr. Dejongh

from tkinter import filedialog
import customtkinter as ctk
import os
import array as arr

# TODO: Add a button to remove a file entry
# TODO: Add a button to clear all file entries
# TODO: Remember the last file path used
# TODO: Add a button to add a folder
# TODO: Make it possible to change a file entry
# TODO: A comments to method


class LogFile:
  def __init__(self, filename, pathname, first_time, first_open):
    self.filename = filename
    self.pathname = pathname
    self.first_time = first_time
    self.first_open = first_open

def create_ui():
  ctk.set_appearance_mode("dark")
  ctk.set_default_color_theme("dark-blue")

  root = ctk.CTk()
  root.geometry("750x750")
  
  file_count = 1
  logfiles = []
  labels = []

  max_files = 10

  # GUI
  frame = ctk.CTkScrollableFrame(root, width=1000, height=1000)
  frame.pack(pady=70, padx=70)
  frame.pack_propagate(True)

  # LOGIC

   # Returns true if the string contains the substring
  def contains(str, sub):
    return str.find(sub) != -1
  
  # Utility function to find the scale factor of a given file entry number
  def find_scale_factor(i):
    frame_name = f'!ctkframe{i}' if i != 1 else '!ctkframe'
    frame_in_question = frame.children.get(frame_name)
    placeholder_text = frame_in_question.children.get("!ctkentry").cget("placeholder_text")
    val = frame_in_question.children.get("!ctkentry").get()
    print(f'placeholder_text: {placeholder_text}, val: {val}')
    if val == "" or contains(val, "scale factor"):
      return 1
    if val == "-":
      return -1
    return val
  
  #  Utility function to set a scale factor of a given file entry number
  def set_scale_factor(i, val):
    frame_name = f'!ctkframe{i}' if i != 1 else '!ctkframe'
    frame_in_question = frame.children.get(frame_name)
    frame_in_question.children.get("!ctkentry").delete(0, "end")
    frame_in_question.children.get("!ctkentry").insert(0, val)
    
  # utility to insure that user enters a value numeric (decimcal)
  def scale_factor_validator(s):
      try:
        if (s=="" or contains(s, "scale factor") or s=='-'):
          return True
        float(s)
        return True
      except ValueError:
          return False
  
  def file_explorer():
    path = filedialog.askopenfilename(initialdir = "/Users/rutab/Desktop/Workspace/Physics-Research/", title = "Select file",filetypes = (("dat files","*.dat"),("all files","*.*")))
    if (path != ""):
      logfiles.append(path)
      filename = os.path.basename(path)
      log_file = LogFile(filename, os.path.dirname(path), True, True)
      labels[len(logfiles)-1].configure(text=filename, text_color="#0066bf")

  inner_frame = ctk.CTkFrame(frame, width=500, height=70, fg_color="transparent")
  inner_frame.grid(pady=10, padx=10, column=0, row=1)
  inner_frame.grid_propagate(True)

  path_entry = ctk.CTkEntry(frame, width=500, placeholder_text="Path to file/folder")
  path_entry.grid(pady=30, padx=10, column=0, row=0)

  fil1_btn = ctk.CTkButton(inner_frame, text=f'File {file_count}', command=file_explorer, width=70, height=50)
  fil1_btn.grid(pady=10, padx=10, column=1, row=0)

  # Create a Tcl wrapper for the validation command. It makes sure input is numeric
  vcmd = (root.register(scale_factor_validator), '%P')
  sc1_entry = ctk.CTkEntry(inner_frame, width=100, height=50, validate="key", validatecommand=vcmd, placeholder_text="scale factor 1")
  sc1_entry.grid(pady=10, padx=10, column=2, row=0)

  file1_name_lbl = ctk.CTkLabel(inner_frame, text=f'File {file_count} Name')
  file1_name_lbl.grid(pady=10, column=3, row=0)
  labels.append(file1_name_lbl)

  # Reads file (Only handles unsiged integers)
  def read(filename):
    # Check if it's the first time the file is being read
    # TODO: Handle this case

    # Log message indicating the file is being read
    print("Reading file for the first time")

    # Initialize spectrum array
    spectrum = arr.array('I', [])
    # Open the file
    # Initialize vairables file_channel_count , number_full_lines and remainder

    # Loop over each file, updating the spectrum array accordingly

    # Handle the remainder

    # Print out the spectrum array


  file1_read_btn = ctk.CTkButton(inner_frame, text="Read", command=read, width=70, height=50)
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

        fil_btn = ctk.CTkButton(new_frame, text=f'File {file_count}', command=file_explorer, width=70, height=50)
        fil_btn.grid(pady=10, padx=10, column=1, row=0)

        sc_entry = ctk.CTkEntry(new_frame, width=70, height=50, validate="key", validatecommand=vcmd, placeholder_text=f'scale factor {file_count}')
        sc_entry.grid(pady=10, padx=10, column=2, row=0)

        file_name_lbl = ctk.CTkLabel(new_frame, text=f'File {file_count} Name')
        file_name_lbl.grid(pady=10, column=3, row=0)
        labels.append(file_name_lbl)

        file_read_btn = ctk.CTkButton(new_frame, text="Read", command=read, width=70, height=50)
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
      if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == "red":
        widget.destroy()

  add_file_btn = ctk.CTkButton(frame, text="Add File", command=new_file_entry, width=70, height=50)
  add_file_btn.grid(pady=10, padx=10, column=0, row=2)

  # Custom close function
  def on_close():
    nonlocal root
    print("exiting")
    print(find_scale_factor(1))
    root.destroy()
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