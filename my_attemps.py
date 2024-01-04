# Author Loïc Rutabana, developing code by Dr. Dejongh

from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
import os
import random
import array as arr

# TODO: Add a button to remove a file entry
# TODO: Add a button to clear all file entries
# TODO: Remember the last file path used
# TODO: Add a button to add a folder
# TODO: Make it possible to change a file entry
# TODO: Add labels letting the user knowing when convertion is done


class LogFile:
  """
  A log file object for the logfiles array. Makes it easier to get the file attributes
  """
  def __init__(self, filename, pathname, first_time, first_open, scale_factor=1.0):
    self.filename = filename
    self.pathname = pathname
    self.first_time = first_time
    self.first_open = first_open
    self.scale_factor = scale_factor


def create_ui():
  """
  Creates the UI though it slowly developed into also holding the logic

  ### Returns:
    `None`
  """
  ctk.set_appearance_mode("dark")
  ctk.set_default_color_theme("dark-blue")

  root = ctk.CTk()
  root.geometry("800x750")
  
  max_files = 10

  file_count = 1
  logfiles = []
  labels = []
  spectrums = [[] for _ in range(max_files)]


  # First frame to hold the file entries
  frame = ctk.CTkScrollableFrame(root, width=1000, height=1000)
  frame.pack(pady=70, padx=70)
  frame.pack_propagate(True)

  
  def find_scale_factor_rough(j: int) -> float:
    """
    Utility function to find the scale factor of a given file entry number before a logfile
    object is created. It scans the entry widgets to find the user inputted scale factor

    Parameters:
      j (`int`) : The index of the file entry. This is used to find the file in the logfiles array

    Returns:
      `float` : The scale factor of the file entry
    """

    i = j + 1
    frame_name = f'!ctkframe{i}' if i != 1 else '!ctkframe'
    frame_in_question = frame.children.get(frame_name)
    val = frame_in_question.children.get("!ctkentry").get()
    if val == "" or "scale factor" in val:
      return 1.0
    if val == "-":
      return -1.0
    return float(val)
  
  
  
  def find_scale_factor(i: int) -> int:
    """
    Simplifed version of the above function. If the logfile object hasn't been created than
    it will use `find_scale_factor_rough` to find the scale factor.

    Parameters:
      i (`int`) : The index of the file entry. This is used to find the file in the logfiles array

    Returns:
      `float` : The scale factor of the file entry
    """

    if (len(logfiles) < i + 1):
      return find_scale_factor_rough(i)
    return logfiles[i-1].scale_factor
    
  def scale_factor_validator(ref: int) -> bool:
      """
      Utility to insure that user enters a value numeric (decimcal)
      The parameter the index of the file entry. This is used to find the file in the logfiles array

      Parameters:
        ref (`int`) : The index of the file entry. This is used to find the file in the logfiles array

      Returns:
        `bool` : True if the value is numeric and false otherwise
      """

      sc = str(find_scale_factor(ref))
      try:
        if (sc=="" or "scale factor" in sc or sc=='-'):
          return True
        float(sc)
        return True
      except ValueError:
          return False
  
  def file_explorer(i: int) -> None:
    """
    Opens a file explorer and adds the selected file to the logfiles array
    and updates the UI accordingly. It also creates a logfile object for the file
    and adds it to the logfiles array. On top of that it also creates a label
    to hold the name of the file and adds it to the labels array

    Parameters:
      i (`int`) : The index of the file entry. This is used to find the file in the logfiles array

    Returns:
      `None`
    """

    path = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select file",filetypes = (("dat files","*.dat"),("all files","*.*")))
    if (path != ""):
      filename = os.path.basename(path)
      log_file = LogFile(filename, os.path.dirname(path), True, True, find_scale_factor(i))
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
  fil1_btn = ctk.CTkButton(inner_frame, text=f'File {file_count}', command=lambda: file_explorer(0), width=70, height=50)
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

  
  def read(i) -> None:
    """
    This method reads the file and stores the values in the spectrums array
    Such that the write function below can write the values to a file
    This code essentially moves the cursor to the thirs line, reads the 10
    space separated number and stores them in the spectrums array. It does this
    on each line until it reaches the last line which may have less than 10 numbers
    On that line it does the same as it has for the other lines but it multiplies 
    the numbers by the scale factor before appending them to the spectrums array

    Parameters:
      i (`int`) : The index of the file entry. This is used to find the file in the logfiles array

    Returns:
      `None`
    """
    if (len(logfiles) < i + 1):
      #TODO handle this case
      file_not_found_error()
      return

    # Get the file name and path
    filename = logfiles[i].pathname + "/" + logfiles[i].filename
    scale_factor = find_scale_factor(i)
    spectrum = []

    inputfile = open(filename, 'r')
    firstline = inputfile.readline() # Did not need to store results in variable but this moves cursor to next line
    line = inputfile.readline()
    file_channel_count = int(line)
    number_full_lines = file_channel_count // 10 # Integer division. It truncates to always get an integer
    remainder = file_channel_count % 10 # Did not need this but Pr. Dejongh used it so I did too

    # Loop over each file, updating the spectrum array accordingly
    for i in range(number_full_lines):
      line = inputfile.readline().strip()
      spectrum.extend(line.split(" "))
    
    # Append the values on the last line, multplying them with the scale factors
    line = inputfile.readline().strip()
    spectrum.extend(float(x) * scale_factor for x in line.split(" "))
      
    spectrums.insert(i, spectrum)
    inputfile.close()

  
  def overwrite_popup() -> bool:
    """  
    This method is a pop up that asks the user if they want to overwrite the file
    It returns true if the user wants to overwrite the file and false otherwise

    Returns:
      `bool` : True if the user wants to overwrite the file and false otherwise
    """

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

  def unique_identifier_popup() -> str:
    popup_root = tk.Toplevel(background="#1a1a1a")
    popup_root.title("Unique Identifier")
    popup_root.grab_set()

    outter_frame = ctk.CTkFrame(popup_root, width=300, height=300)
    outter_frame.pack_propagate(False)

    popup = ctk.CTkFrame(outter_frame, width=300, height=300)
    popup.pack_propagate(False)

    text = ctk.CTkLabel(popup, text="Enter a unique identifier", font=("Helvetica", 16))
    entry = ctk.CTkEntry(popup, width=150, height=50, placeholder_text="Unique Identifier")
    img = Image.open("assets/images/exchange.png")
    icon = CTkImage(light_image=img, size=(40, 40))
    randomizer = ctk.CTkButton(popup, image=icon, text="", command=lambda: randomize(), width=60)
    ok = ctk.CTkButton(popup, text="OK", command=lambda: submit(), width=200)
    img.close()

    outter_frame.pack(pady=10, padx=10)
    popup.grid(pady=10, padx=10, column=0, row=0)
    text.grid(pady=10, padx=10, column=0, row=0, columnspan=2)
    entry.grid(pady=10, padx=10, column=0, row=1)
    randomizer.grid(pady=10, padx=10, column=1, row=1)
    ok.grid(pady=10, padx=10, column=0, row=2, columnspan=2)

    def randomize():
      width = outter_frame.winfo_width()
      height = outter_frame.winfo_height()
      indentifier = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
      entry.delete(0, tk.END)
      entry.insert(0, indentifier)

    def submit():
      remove_error_message()
      result = tk.StringVar()
      if (len(entry.get()) < 4):
        invalid_identifier()
      else:
        return result.get()
    
    def invalid_identifier():
      error_label = ctk.CTkLabel(popup, text="Identifier must be atleast 4 digits long", text_color="red")
      error_label.grid(pady=10, column=0, row=3, columnspan=2)

    def remove_error_message():
      for widget in popup.winfo_children():
        if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == "red":
          widget.destroy()

    popup_root.wait_window()
  
  def write(i) -> None:
    """
    This method writes the values in the spectrums array to a file
    It does so in the form \"`<index>`: `<value>`\".
  
    Parameters:
      i (`int`) : The index of the file entry. This is used to find the file in the logfiles array
  
    Returns:
      `None`
    """
    read(i)
    is_new = False
    pop_ans = False
    
    # The unique identifier inputed by the user
    identifier = unique_identifier_popup()
    if (len(identifier) < 4):
      return
    input_filename = logfiles[i].filename
    start_index = input_filename.find("hist")
    end_index = input_filename.find("_",start_index)
    outputfilename = input_filename[:start_index] + "o_" + identifier + input_filename[end_index:]
    filename = os.getcwd() + "/" + outputfilename
    spectrum = spectrums[i-1]
    if (os.path.exists(filename) == False):
      is_new = True
    else:
      pop_ans = overwrite_popup()
    
    if (is_new or pop_ans):
      with open(filename, 'w') as f:
        print(f'Writing to {outputfilename}')
        for i in range(len(spectrum)):
          f.write(f'{++i}: {spectrum[i]}\n')
    else:
      print(f'Not writing to {filename}')


  fil1_write_btn = ctk.CTkButton(inner_frame, text="Convert", command=lambda: write(0), width=70, height=50)
  fil1_write_btn.grid(pady=10, padx=10, column=5, row=0)

  
  def new_file_entry() -> None:
    """
    Appends a new frame for a new file entry. Allows up to `max_files` (an int variable declared at the top) files

    Returns:
      `None`
    """
    nonlocal file_count, vcmd

    remove_error_messages()
    if file_count == len(logfiles):
      file_count += 1
      if (file_count <= 10):
        new_frame = ctk.CTkFrame(frame, width=500, height=70, fg_color="transparent")
        new_frame.grid(pady=10, padx=10, column=0, row=file_count)
        # inner_frame.grid_propagate(False)

        fil_btn = ctk.CTkButton(new_frame, text=f'File {file_count}', command=lambda i=file_count: file_explorer(i-1), width=70, height=50)
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

  def file_overflow_error() -> None:
    """
    Error: too many files are added. This is called when the user tries to add more than `max_files` files

    Returns:
      `None`
    """

    error_label = ctk.CTkLabel(frame, text="Only 10 Files Permitted", text_color="red")
    error_label.grid(pady=10, column=0, row=file_count+2)

  def empty_file_error() -> None:
   """
   Error: Attempted to add new file entry when one is still empty.
   This is called when the user tries to add a new file entry when one is still empty

    Returns:
      `None`
   """
   error_label = ctk.CTkLabel(frame, text="Empty File Entry", text_color="red")
   error_label.grid(pady=10, column=0, row=file_count+2)

  def file_not_found_error() -> None:
   """
   Error: Attempted to read a file that doesn't exist
   """
   
   error_label = ctk.CTkLabel(frame, text="No File Selected", text_color="red")
   error_label.grid(pady=10, column=0, row=file_count+2)

  def remove_error_messages():
    """
    Removes all error messages from the UI. This is called when the user adds a new file entry

    Returns:
      `None`
    """

    for widget in frame.winfo_children():
      if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == "red":
        widget.destroy()

  add_file_btn = ctk.CTkButton(frame, text="Add File", command=new_file_entry, width=70, height=50)
  add_file_btn.grid(pady=10, padx=10, column=0, row=2)

  def on_close() -> None:
    """
    This method is called when the user closes the window. It closes the window and renames the log file
    to include the number of seconds since midnight
    """

    nonlocal root
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