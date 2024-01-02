# Author Loïc Rutabana, developing code by Dr. Dejongh

from tkinter import filedialog
import tkinter as tk
import customtkinter as ctk
import os
import array as arr

# TODO: Add a button to remove a file entry
# TODO: Add a button to clear all file entries
# TODO: Remember the last file path used
# TODO: Add a button to add a folder
# TODO: Make it possible to change a file entry
# TODO: A comments to method

# A log file object for the logfiles array. Makes it easier to get the file attributes
class LogFile:
  def __init__(self, filename, pathname, first_time, first_open):
    self.filename = filename
    self.pathname = pathname
    self.first_time = first_time
    self.first_open = first_open

# Creates the UI though it slowly developed into also holding the logic
def create_ui():
  ctk.set_appearance_mode("dark")
  ctk.set_default_color_theme("dark-blue")

  root = ctk.CTk()
  root.geometry("750x750")
  
  max_files = 10

  file_count = 1
  logfiles = []
  labels = []
  spectrums = [[] for _ in range(max_files)]


  # GUI
  frame = ctk.CTkScrollableFrame(root, width=1000, height=1000)
  frame.pack(pady=70, padx=70)
  frame.pack_propagate(True)

  # LOGIC

   # Returns true if the string contains the substring
  # def contains(str, sub):
  #   return str.find(sub) != -1
  
  # Utility function to find the scale factor of a given file entry number
  def find_scale_factor(j) -> float:
    i = j + 1
    frame_name = f'!ctkframe{i}' if i != 1 else '!ctkframe'
    frame_in_question = frame.children.get(frame_name)
    # placeholder_text = frame_in_question.children.get("!ctkentry").cget("placeholder_text")
    val = frame_in_question.children.get("!ctkentry").get()
    if val == "" or "scale factor" in val:
      return 1.0
    if val == "-":
      return -1.0
    return float(val)
  
  # Simplifed version of the above function. It takes the file entry number as a parameter
  # Hope to use it in the future with cleaner version of code
  def find_scale_factor_new(i) -> int:
    return logfiles[i-1].scale_factor
  
  #  Utility function to set a scale factor of a given file entry number
  def set_scale_factor(i, val):
    frame_name = f'!ctkframe{i}' if i != 1 else '!ctkframe'
    frame_in_question = frame.children.get(frame_name)
    frame_in_question.children.get("!ctkentry").delete(0, "end")
    frame_in_question.children.get("!ctkentry").insert(0, val)

  # Simplifed version of the above function. It takes the file entry number as a parameter
  def set_scale_factor_new(i, val):
    logfiles[i-1].scale_factor = val
    
  # Utility to insure that user enters a value numeric (decimcal)
  # The parameter the index of the file entry
  def scale_factor_validator(ref) -> bool:
      sc = str(find_scale_factor(ref))
      try:
        if (sc=="" or "scale factor" in sc or sc=='-'):
          return True
        float(sc)
        return True
      except ValueError:
          return False
  
  # Opens a file explorer and adds the selected file to the logfiles array
  def file_explorer() -> None:
    path = filedialog.askopenfilename(initialdir = "/Users/rutab/Desktop/Workspace/Physics-Research/", title = "Select file",filetypes = (("dat files","*.dat"),("all files","*.*")))
    if (path != ""):
      filename = os.path.basename(path)
      log_file = LogFile(filename, os.path.dirname(path), True, True)
      logfiles.append(log_file)
      labels[len(logfiles)-1].configure(text=filename, text_color="#0066bf")


  # The frame to hold the first file entry
  inner_frame = ctk.CTkFrame(frame, width=500, height=70, fg_color="transparent")
  inner_frame.grid(pady=10, padx=10, column=0, row=1)
  inner_frame.grid_propagate(True)

  # The text entry for the path to the file/folder
  path_entry = ctk.CTkEntry(frame, width=500, placeholder_text="Path to file/folder")
  path_entry.grid(pady=30, padx=10, column=0, row=0)

  # The button to open the file explorer to add a file
  fil1_btn = ctk.CTkButton(inner_frame, text=f'File {file_count}', command=lambda: file_explorer(), width=70, height=50)
  fil1_btn.grid(pady=10, padx=10, column=1, row=0)

  # Reference to the scale factor entry
  ref = None

  # Create a Tcl wrapper for the validation command. It makes sure input is numeric
  vcmd = (root.register(scale_factor_validator), '%P', ref)

  # The scale factor entry. It runs the validation command on each key press with the paramaters
  # specified in the vcmd tuple. P is the value of the entry, C is the reference to the entry
  sc1_entry = ctk.CTkEntry(inner_frame, width=100, height=50, validate="key",
                         validatecommand=lambda: scale_factor_validator(0), 
                         placeholder_text="scale factor 1")
  sc1_entry.grid(pady=10, padx=10, column=2, row=0)

  # The label to hold the name of the file
  file1_name_lbl = ctk.CTkLabel(inner_frame, text=f'File {file_count} Name')
  file1_name_lbl.grid(pady=10, column=3, row=0)
  labels.append(file1_name_lbl)

  # This method reads the file and stores the values in the spectrums array
  # Such that the write function below can write the values to a file
  def read(i) -> None:
    # Check if it's the first time the file is being read
    # TODO: Handle this case

    # Log message indicating the file is being read
    print("Reading file for the first time")

    if (len(logfiles) < i + 1):
      #TODO handle this case
      file_not_found_error()
      return

    filename = logfiles[i].pathname + "/" + logfiles[i].filename
    scale_factor = find_scale_factor(i)
    spectrum = []

    inputfile = open(filename, 'r')
    firstline = inputfile.readline()
    line = inputfile.readline()
    file_channel_count = int(line)
    number_full_lines = file_channel_count // 10 # Integer division. It truncates to always get an integer
    remainder = file_channel_count % 10

    # Loop over each file, updating the spectrum array accordingly
    for i in range(number_full_lines):
      line = inputfile.readline().strip()
      spectrum.extend(line.split(" "))
    
    # Append the values on the last line, multplying them with the scale factors
    line = inputfile.readline().strip()
    spectrum.extend(float(x) * scale_factor for x in line.split(" "))
      
    spectrums.insert(i, spectrum)
    inputfile.close()

  def new_popup() -> bool:
    overwrite_root = tk.Toplevel(background="#1a1a1a", height=350, width=350)
    overwrite_root.title("Overwrite File")
    overwrite_root.grab_set()

    popup = ctk.CTkFrame(overwrite_root, width=300, height=300)

    text = ctk.CTkLabel(popup, text="Are you sure you want to overwrite the file?")
    yes = ctk.CTkButton(popup, text="Yes", command=lambda: chose_yes())
    no = ctk.CTkButton(popup, text="No", command=lambda: chose_no())

    popup.pack(pady=10, padx=10)
    text.grid(pady=10, padx=10, column=0, row=0)
    yes.grid(pady=10, padx=10, column=0, row=1)
    no.grid(pady=10, padx=10, column=1, row=1)

    result = tk.BooleanVar()

    def chose_yes():
        overwrite_root.destroy()
        result.set(True)

    def chose_no():
        overwrite_root.destroy()
        result.set(False)

    overwrite_root.wait_window()
    return result.get()


  def write(i) -> None:
    read(i)
    is_new = False
    pop_ans = False
    filename = "C:/Users/rutab/Desktop/Workspace/Physics-Research/Loïc's Log.txt"
    short_name = "Loïc's Log"
    spectrum = spectrums[i-1]
    if (os.path.exists(filename) == False):
      is_new = True
    else:
      pop_ans = new_popup()
    
    if (is_new or pop_ans):
      with open(filename, 'w') as f:
        print(f'Writing to {filename}')
        for i in range(len(spectrum)):
          f.write(f'{++i}: {spectrum[i]}\n')
    else:
      print(f'Not writing to {filename}')


  fil1_write_btn = ctk.CTkButton(inner_frame, text="Convert", command=lambda: write(0), width=70, height=50)
  fil1_write_btn.grid(pady=10, padx=10, column=5, row=0)

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

        sc_entry = ctk.CTkEntry(new_frame, width=100, height=50, validate="key",
                                validatecommand=lambda i=file_count: scale_factor_validator(i-1), placeholder_text=f'scale factor {file_count}')
        sc_entry.grid(pady=10, padx=10, column=2, row=0)

        file_name_lbl = ctk.CTkLabel(new_frame, text=f'File {file_count} Name')
        file_name_lbl.grid(pady=10, column=3, row=0)
        labels.append(file_name_lbl)

        fil1_write_btn = ctk.CTkButton(new_frame, text="Convert", command=lambda i=file_count: write(i-1), width=70, height=50)
        fil1_write_btn.grid(pady=10, padx=10, column=5, row=0)

        add_file_btn = ctk.CTkButton(frame, text="Add File", command=new_file_entry if file_count < max_files else file_overflow_error, width=70, height=50)
        add_file_btn.grid(pady=10, padx=10, column=0, row=file_count+1)
      else:
        file_count = 10
    else:
      empty_file_error()

  # ERROR MESSAGES

  # Error: too many files are added
  def file_overflow_error():
    error_label = ctk.CTkLabel(frame, text="Only 10 Files Permitted", text_color="red")
    error_label.grid(pady=10, column=0, row=file_count+2)

  # Error: Attempted to add new file entry when one is still empty
  def empty_file_error():
    error_label = ctk.CTkLabel(frame, text="Empty File Entry", text_color="red")
    error_label.grid(pady=10, column=0, row=file_count+2)

  # Error: Attempted to read a file that doesn't exist
  def file_not_found_error():
    error_label = ctk.CTkLabel(frame, text="No File Selected", text_color="red")
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
    print(find_scale_factor(0))
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