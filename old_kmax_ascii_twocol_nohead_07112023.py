#based on guizero_py27.py from May 27, 2023
import math
import array as arr
import os.path
import os
from datetime import datetime
from guizero import App, Text, PushButton, TextBox, Combo, Box
#spectrum will be truncated of padded
# utility to insure that user enters a value numeric
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#set the scale factor to be something other than 1.0
def set_scale():
    global scale_factor
    scale_factor = 1.
    if(is_number(text_box_scale.value)):
#        print(float(text_box_scale.value))
        scale_factor = float(text_box_scale.value)
        text_box.value = "scale factor changed"
        append_to_log("scale_factor set to " + str(scale_factor))
#        logfile.write("scale_factor set to " + str(scale_factor) + "\n")
    else:
        append_to_log("Scale_factor not numeric. Set to " + str(scale_factor))
        text_box.value = "Scale_factor not numeric. Set to  " + str(scale_factor)

#use button to exit gui
def exit():
    print("exiting ", logfilename)
    check_file = os.path.isfile(logfilename)
#    print(check_file)
#    print(not check_file)
    if (not check_file):
        print("bye-bye")
        app.destroy()
        return
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds
    print(seconds)
    print(first_filename)
    start_index = first_filename.find("hist")
    end_index = first_filename.find("_",start_index)
    rename_logfilename = first_filename[:start_index] + "log_" + str(seconds) + first_filename[end_index:]
    print(logfilename)
    print(rename_logfilename)
    os.rename(logfilename,rename_logfilename)
    app.destroy()

# unimplimented feature to scale channel number    
#def set_intercept():
#   if(is_number(text_box_intercept.value)):
#        print(float(text_box_intercept.value))
#        text_box.value = ""
#    else:
#        text_box.value = "intercept is not numeric"
#def set_slope():
#    if(is_number(text_box_slope.value)):
#        print(float(text_box_slope.value))
#        text_box.value = ""
#    else:
#        text_box.value = "slope is not numeric"

def read_data():
    global first_time
    global file_channel_count
    global spectrum
    global insert_at_index
    global first_filename
    inputfile = open(filename,"r")
    theline = inputfile.readline()
    if first_time:
        #    logfilename = filename[:start_index] + "logfile_" + filename[start_index:]
        start_index = filename.find("hist")
#        logfile.write("first time read " + filename + "\n")
        append_to_log("first time read " + filename)
        first_filename = filename
        spectrum = arr.array('d', [])
        theline = inputfile.readline()
        file_channel_count=int(theline)
        number_full_lines = file_channel_count / 10
        remainder = file_channel_count % 10
        count = 0
        while count < number_full_lines-1: #loop over full lines
            index_old = 0 #character index within the line 0 to whatever
            index = 0 # index of number in line 0 to 9
            theline = inputfile.readline()
#            print(theline)
            while index < 10:
                index_new = theline.find(" ",index_old)
                number = int(theline[index_old:index_new])
#                print(number)
                spectrum.append(number)
                index_old = index_new+1
                index = index + 1
            count = count + 1
        theline = inputfile.readline() #read the last line
#        print(theline)
        index_old = 0
        index = 0
        while index < remainder:
            index_new = theline.find(" ",index_old)
            number = int(theline[index_old:index_new]) * scale_factor
#            print(number)
            spectrum.append(number)
            index_old = index_new+1
            index = index + 1
        inputfile.close()
        first_time = False
        text_box.value = "First file read successfully"
    else:
        append_to_log(" read " + filename + " with scale_factor = " + str(scale_factor))
        theline = inputfile.readline()
        print(theline)
        temp_file_channel_count = int(theline)
        if file_channel_count != temp_file_channel_count:
            print ("channel counts don't match")
            app.error("channel count","CAN NOT ADD DIFFERENT SIZE FILES")
        else:
            number_full_lines = file_channel_count / 10
            remainder = file_channel_count % 10
            count = 0
            insert_at_index = 0
            while count < number_full_lines-1: #loop over full lines
                index_old = 0 #character index within the line 0 to whatever
                index = 0 # index of number in line 0 to 9
                theline = inputfile.readline()
                while index < 10:
                    index_new = theline.find(" ",index_old)
                    number = int(theline[index_old:index_new])
                    spectrum[insert_at_index] = scale_factor*number + spectrum[insert_at_index]
                    insert_at_index = insert_at_index + 1
                    index_old = index_new+1
                    index = index + 1
                count = count + 1
            theline = inputfile.readline() #read the last line
            index_old = 0
            index = 0
            while index < remainder:
                index_new = theline.find(" ",index_old)
                number = int(theline[index_old:index_new])
                spectrum[insert_at_index] = scale_factor*number + spectrum[insert_at_index]
                insert_at_index = insert_at_index + 1
                index_old = index_new+1
                index = index + 1
            text_box.value = "File added/subtracted successfully"
        inputfile.close()
        first_time = False
    inputfile.close()

#open, write, close log file - only way to keep possibility of writing intermidiate files
def append_to_log(logstring):
    logfile = open(logfilename,"a")
    logfile.write(logstring + "\n")
    logfile.close()

# start doing things - get a file name!    
def get_filename():
    global filename
    global logfile
    global logfilename
    global first_open
    filename = app.select_file(folder=pathname)
    print(filename)
    start_index = filename.find("hist")
    text2.value = filename[start_index:]
    text_box.value = "selected file is " + filename
#    start_index = filename.find("hist")
    if first_open:
        logfilename = filename[:filename.find("hist")] + "logfile.txt"
        print (logfilename)
        logfile = open(logfilename,"w")
        now = datetime.now()
        logfile.write(str(now)+"\n")
        logfile.write("selected file " + filename + "\n")
        logfile.close()
        first_open = False
    else:
        append_to_log("selected file " + filename + "\n")

#set the default path for finding input files    
def get_pathname():
    global pathname
    pathname = app.select_folder()
    print(pathname)
    text_box.value = "selected path is " + pathname
#    append_to_log("selected path " + filename)
    if first_open:
        logfilename = pathname + "logfile.txt"
        print (logfilename)
        logfile = open(logfilename,"w")
        now = datetime.now()
        logfile.write(str(now)+"\n")
        logfile.write("Default pathname set to " + pathname + "\n")
        logfile.close()
        first_open = False
    else:
        append_to_log("Default pathname set to  " + pathname + "\n")
    text_box.value = "Default path set to " + pathname


# write out the current spectrum - does not rename log file or signal end of program.  More files can be added
#only writes if file does NOT already exist
def write_file():
    get_ident()
    start_index = first_filename.find("hist")
    end_index = first_filename.find("_",start_index)
    outputfilename = first_filename[:start_index] + "o_" + ident + first_filename[end_index:]
    print(outputfilename)
    check_file = os.path.isfile(outputfilename)
#    print(check_file)
    if check_file:
        overwrite_question()
        if overwrite == False:
            return
    outputfile = open(outputfilename,'w')
#    print("output file opened")
    index = 0
    for entry in spectrum:
        outputfile.write(str(index+1) + "  " + str(spectrum[index]) + "\n")
        index = index + 1
    outputfile.close()
    append_to_log("wrote " + outputfilename)
    text_box.value = "Current spectrum written to file"

# utility to get string to identify output file    
def get_ident():
    global ident
    ident = app.question("out id","Enter output identifier")
    
# untility file to query user about overwriting an existing file
def overwrite_question ():
    global overwrite
    overwrite = app.yesno("overwrite existing", " Do you want to overwrite?")

# let the main part of the program begin!
#global logfilename
logfilename = " "
scale_factor = 1.
app = App(width=600,height=200)
pathname = "."
first_time = True
first_open = True
title_box1 = Box(app, width="fill", align="top")
title_box2 = Box(app, width="fill", align="top")
title_box3 = Box(app, width="fill", align="top")
title_box4 = Box(app, width="fill", align="top")
title_box5 = Box(app, width="fill", align="bottom")
text = Text(title_box1,text="Always use the EXIT button to close out.\n Use negative and non-unity scale factors with care.\n Uncertainies will be incorrect")
text2 = Text(title_box2,text="Currently selected file")
button3 = PushButton(title_box3, command=get_pathname, text="Get pathname",align="left")
button2 = PushButton(title_box3, command=get_filename, text="Get filename",align="left")
button = PushButton(title_box3, command=read_data, text="read data",align="left")
text_box_scale = TextBox(title_box3, text='scale factor',command=set_scale,align="left")
button4 = PushButton(title_box3, command=write_file, text="Write file",align="right")
button5 = PushButton(title_box5, command=exit, text="Exit Now",align="right")
#button6 = PushButton(app, command=get_pathname, text="junk")
#file_name = Text(app)
text_box = TextBox(title_box4, text='', width="fill")

#text_box_intercept = TextBox(app, text='intercept', command=set_intercept)
#text_box_slope = TextBox(app, text='slope', command=set_slope)
app.display()
#app.destroy()
#print("goodbye")
#uncomment this if you want to close python from the command window -MAY NOT WRITE OUT THE LOG FILE?
#input('Press ENTER to exit the program')
