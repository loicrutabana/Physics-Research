# Author Loïc Rutabana, developing code by Dr. Dejongh

from datetime import datetime
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
import os
import random
import array as arr
from typing import Callable

# TODO: Add a button to remove a file entry
# TODO: Add a button to clear all file entries
# TODO: Remember the last file path used
# TODO: Add a button to add a folder
# TODO: Make it possible to change a file entry
# TODO: Add labels letting the user knowing when convertion is done


teal = "#008080"


class LogFile:
  """
  A log file object for the logfiles array. Makes it easier to get the file attributes
  """
  def __init__(self, filename, pathname, first_time, first_open, scale_factor, outputfile, checked: str="off"):
    self.filename = filename
    self.pathname = pathname
    self.first_time = first_time
    self.first_open = first_open
    self.scale_factor = scale_factor
    self.outputfile = outputfile
    self.checked = checked


def create_ui():
  """
  Creates the UI though it slowly developed into also holding the logic

  ### Returns:
    `None`
  """
  ctk.set_appearance_mode("dark")
  ctk.set_default_color_theme("dark-blue")

  root = ctk.CTk()
  root.geometry("900x750")
  
  max_files = 10

  file_count = 0
  logfiles = []
  labels = []
  spectrums = [[] for _ in range(max_files)]


  # First frame to hold the file entries
  frame = ctk.CTkScrollableFrame(root, width=1000, height=1000)
  frame.pack(pady=70, padx=70)
  frame.pack_propagate(True)
  
  def find_scale_factor_rough(j: int) -> str:
    """
    Utility function to find the scale factor of a given file entry number before a logfile
    object is created. It scans the entry widgets to find the user inputted scale factor

    Parameters:
      j (`int`) : The index of the file entry. This is used to find the file in the logfiles array

    Returns:
      `float` : The scale factor of the file entry
    """

    i = j + 2 #idk why this works but it does
    frame_name = f'!ctkframe{i}' if i != 1 else '!ctkframe'
    frame_in_question = frame.children.get(frame_name)
    val = frame_in_question.children.get("!ctkentry").get()
    return val
  
  
  
  def find_scale_factor(i: int) -> float:
    """
    Simplifed version of the above function. If the logfile object hasn't been created than
    it will use `find_scale_factor_rough` to find the scale factor.

    Parameters:
      i (`int`) : The index of the file entry. This is used to find the file in the logfiles array

    Returns:
      `float` : The scale factor of the file entry
    """

    if (len(logfiles) <= i):
      val = find_scale_factor_rough(i)
      if val == "" or "scale factor" in val:
        return 1.0
      if val[0] == '-':
        return float('-' + val[1:len(val)])
      elif val[0] == '.':
        return float('0' + val[0:len(val)])
      return val
    return float(logfiles[i-1].scale_factor)
  
  def find_checked_status_rough(i: int) -> str:
    """
    Utility function to find the checked status of a given file entry number before a logfile
    object is created. It scans the entry widgets to find the user inputted checked status
    """

    i = i + 2
    frame_name = f'!ctkframe{i}' if i != 1 else '!ctkframe'
    frame_in_question = frame.children.get(frame_name)
    val = frame_in_question.children.get("!ctkcheckbox").get()
    return val
  
  def find_checked_status(i: int) -> str:
    """
    Simplifed version of the above function. If the logfile object hasn't been created than
    it will use `find_checked_status_rough` to find the checked status.
    """

    if (len(logfiles) <= i):
      return find_checked_status_rough(i)
    return logfiles[i-1].checked
    
  def scale_factor_validator(val: str, 
                             i: int) -> bool:
      """
      Utility to insure that user enters a value numeric (decimcal)
      The parameter the index of the file entry. This is used to find the file in the logfiles array

      Parameters:
        ref (`int`) : The index of the file entry. This is used to find the file in the logfiles array

      Returns:
        `bool` : True if the value is numeric and false otherwise
      """
      
      if (val=="" or "scale factor" in val or val=="-" or val=="."):
          return True
      try:
        num = float(val)
        if (len(logfiles) > int(i)):
          logfiles[int(i)].scale_factor = num
        return True
      except ValueError:
        return False
      
  def load_last_folder_path():
    try:
        with open("config.json", "r") as config_file:
            data = json.load(config_file)
            return data.get("last_folder_path", "")
    except FileNotFoundError:
        return ""
  
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
    
    path = filedialog.askopenfilename(initialdir = load_last_folder_path, title = "Select file", filetypes = (("dat files","*.dat"),("all files","*.*")))
    if (path != ""):
      filename = os.path.basename(path)
      log_file = LogFile(filename, os.path.dirname(path), True, True, find_scale_factor(i), find_checked_status(i))
      logfiles.append(log_file)
      labels[len(logfiles)-1].configure(text=filename, text_color="#0066bf")


  # The frame to hold the first file entry
  inner_frame = ctk.CTkFrame(frame, width=500, height=70, fg_color="transparent")
  inner_frame.grid(pady=10, padx=10, column=0, row=1)
  inner_frame.grid_propagate(True)

  # Reference to the scale factor entry
  ref = None

  # Create a Tcl wrapper for the validation command. It makes sure input is numeric
  vcmd = (root.register(scale_factor_validator), '%P', ref)
  
  def read(i: int) -> int:
    """
    This method reads the file and stores the values in the spectrums array
    Such that the write function below can write the values to a file
    This code essentially moves the cursor to the thirs line, reads the 10
    space separated number and stores them in the spectrums array. It does this
    on each line until it reaches the last line which may have less than 10 numbers
    On that line it does the same as it has for the other lines but it multiplies 
    the numbers by the scale factor before appending them to the spectrums array.

    Parameters:
      i (`int`) : The index of the file entry. This is used to find the file in the logfiles array

    Returns:
      `None`
    """
    if (len(logfiles) < i + 1):
      #TODO handle this case
      file_not_found_error()
      return -1

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

    # Loop over each line, updating the spectrum array accordingly multiplying by the scale factor
    for k in range(number_full_lines):
      line = inputfile.readline().strip()
      spectrum.extend(int(x) * scale_factor for x in line.split(" "))
    
    # Append the values on the last line, multplying them with the scale factors
    line = inputfile.readline().strip()
    spectrum.extend(int(x) * scale_factor for x in line.split(" "))
      
    spectrums.insert(i, spectrum)
    inputfile.close()
    return 0

  
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

  def unique_identifier_popup() -> str or int:
    result = ''

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
      nonlocal result
      remove_error_message()
      result = entry.get()
      if (len(entry.get()) < 4 and len(entry.get())!= 0):
        invalid_identifier()
      else:
        popup_root.destroy()
    
    def cancel():
      nonlocal result
      popup_root.destroy()
      result = -1
    
    def invalid_identifier():
      error_label = ctk.CTkLabel(popup, text="Identifier must be atleast 4 digits long", text_color="red")
      error_label.grid(pady=10, column=0, row=3, columnspan=2)

    def remove_error_message():
      for widget in popup.winfo_children():
        if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == "red":
          widget.destroy()
    
    popup_root.protocol("WM_DELETE_WINDOW", lambda: cancel())
    popup_root.wait_window()
    return result
  
  def write(i) -> None:
    """
    This method writes the values in the spectrums array to a file
    It does so in the form \"`<index>`: `<value>`\".

    **Edit**: I've modified this code to be able to write from multiple files. It does this by checking
    all files that are checked, reading them individually using the read() method and adding up their
    results and writing that on the outputfile
  
    Parameters:
      i (`int`) : The index of the file entry. This is used to find the file in the logfiles array
  
    Returns:
      `None`
    """
    nonlocal logfiles, spectrums
    
    checked_spectrums= []
    for j in range(len(logfiles)):
      if (logfiles[j].checked == "on"): 
        if (read(j) == -1):
          return
        checked_spectrums.append(spectrums[j])
    if (read(i) == -1):
      return
    checked_spectrums.append(spectrums[i])
    num_lines = 0
    with open(logfiles[i].pathname + "/" + logfiles[i].filename, 'r') as f:
      while f.readline():
        num_lines += 1
    is_new = False
    pop_ans = False
    
    # The unique identifier inputed by the user
    identifier = unique_identifier_popup()
    if (identifier == -1):
      return
    input_filename = logfiles[i].filename
    start_index = input_filename.find("hist")
    end_index = input_filename.find("_",start_index)
    outputfilename = "results\\" + input_filename[:start_index] + "o_" + identifier + input_filename[end_index:]
    filename = f"{os.getcwd()}\\{outputfilename}"

    logfiles[i].outputfile = outputfilename

    if (os.path.exists(filename) == False):
      is_new = True
    else:
      pop_ans = overwrite_popup()
    
    if (is_new or pop_ans): # -> Check this
      with open(filename, 'w') as f:
        print(f'Writing to {outputfilename}')
        for j in range(num_lines):
          val = 0
          for k in range(len(checked_spectrums)):
            # sub_list  = checked_spectrums[k]
            # sub_val = sub_list[j]
            # val += int(sub_val)
            val = sum(s[j] for s in checked_spectrums)
            f.write(f'{++j} {val}\n')
        convertion_complete()
        checked_files = []
        for j in range(len(logfiles)):
          if (logfiles[j].checked == "on"): 
            if (read(j) == -1):
              return
            checked_files.append(logfiles[j])
        create_log(logfiles[i], checked_files, identifier)
    else:
      print(f'Not writing to {filename}')
  
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

        fil_btn = ctk.CTkButton(new_frame, text="Upload", command=lambda i=file_count: file_explorer(i-1), width=70, height=50)
        fil_btn.grid(pady=10, padx=10, column=1, row=0)

        sc_entry = ctk.CTkEntry(new_frame, width=100, height=50, validate="key",
                                validatecommand=(root.register(scale_factor_validator), '%P', file_count-1), placeholder_text=f'scale factor {file_count}')
        sc_entry.grid(pady=10, padx=10, column=2, row=0)

        file_name_lbl = ctk.CTkLabel(new_frame, text=f'File {file_count} Name')
        file_name_lbl.grid(pady=10, column=3, row=0)
        labels.append(file_name_lbl)

        file_write_btn = ctk.CTkButton(new_frame, text="Convert", command=lambda i=file_count: write(i-1), width=70, height=50)
        file_write_btn.grid(pady=10, padx=10, column=5, row=0)

        add_file_btn = ctk.CTkButton(frame, text="Add File", command=new_file_entry if file_count < max_files else file_overflow_error, width=70, height=50)
        add_file_btn.grid(pady=10, padx=10, column=0, row=file_count+1)

        check_var = ctk.StringVar(value="off")
        def on_check(i: int, string: str, write_btn: ctk.CTkButton, upload_btn: ctk.CTkButton) -> None:
          write_btn.configure(state='normal' if check_var.get() == 'off' else 'disabled')
          upload_btn.configure()
          # Set checked to true in log file object if created
          if (len(logfiles) == i):
            state = check_var.get()
            logfiles[i-1].checked = "on" if state == 'on' else "off"

        checkbox = ctk.CTkCheckBox(new_frame, text="",
                                   command=lambda write_btn=file_write_btn, upload_btn=fil_btn, str_var=check_var.get(), i=file_count: on_check(i, str_var, write_btn, upload_btn),
                                   variable=check_var, onvalue="on", offvalue="off")
        checkbox.grid(pady=10, padx=10, column=6, row=0)
        
      else:
        file_count = 10
    else:
      empty_file_error()

  def print_logfiles() -> None:
    """
    Prints the logfiles array to the console. Used for debugging

    Returns:
      `None`
    """
    for i in range(len(logfiles)):
      print(f'File {i+1}: {logfiles[i].filename} {logfiles[i].scale_factor} {logfiles[i].checked}')

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

  # Non Error Messages

  def convertion_complete() -> None:
    """
    Tells the user that the convertion is complete.
    Message goes away after 3 seconds

    Returns:
      `None`
    """

    msg_label = ctk.CTkLabel(frame, text="Convertion Complete", text_color=teal)
    msg_label.grid(pady=10, column=0, row=file_count+2)
    root.after(3000, lambda: msg_label.destroy())

  def on_reset() -> None:
    # Make it destroy root, end the create_ui function, and call create_ui again
    nonlocal root, file_count, logfiles, labels, spectrums
    root.destroy()
    file_count = 0
    logfiles = []
    labels = []
    spectrums = [[] for _ in range(max_files)]
    create_ui()

  img = Image.open("assets/images/bomb.png")
  icon = CTkImage(light_image=img, size=(30, 30))
  reset_btn = ctk.CTkButton(frame, image=icon, text="", command=on_reset, width=30, height=30)
  reset_btn.grid(pady=30, padx=10, column=0, row=0, sticky='w')

  def create_log(logfile: LogFile, extras, identifier: str) -> None:
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds

    start_index = logfile.filename.find("hist")
    end_index = logfile.filename.find("_",start_index)
    log_name = logfile.filename[:start_index] + "log_" + identifier + str(seconds) + logfile.filename[end_index:]
    with open(f'logs/{log_name}', 'w') as f:
      f.write(f'{str(datetime.now())}\n')
      if logfile.first_open:
        f.write('Opened for the first time\n')
      if len(extras) != 0:
        f.write('Added files:\n')
        for e in extras:
          f.write(f'\t{e.filename} at scale factor {e.scale_factor}\n')
      f.write(f'Selected file {logfile.pathname}\n')
      f.write(f'Scale Factor: {logfile.scale_factor}\n')
      f.write(f'Wrote to {logfile.outputfile}\n')
      


  def on_close() -> None:
    """
    This method is called when the user closes the window. It closes the window and renames the log file
    to include the number of seconds since midnight
    """

    nonlocal root
    root.destroy()
    print_logfiles()
    exit()
  #     app.destroy()
    
  new_file_entry()
  
  root.protocol("WM_DELETE_WINDOW", on_close)
  root.mainloop()

create_ui() 