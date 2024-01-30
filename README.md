### Hope College Physics Research: 
## Data Format Converter
This repository stores scripts meant to chaange the format data received from the particle accelerator is presented.
So far, there are only 2 scripts, *kmax_ascii_twocol_no_head.py* written by **Dr. Paul DeYoung** who currently sits as 
the chair of the physics department at Hope College and *my_attemps.py* written by **Loïc Rutabana**, a senior here in
the Computer Science department. *my_attemps.py* is meant to be an improvement on *kmax_ascii_twocol_no_head.py*

Using:
 * `Python` Version 3.11.7
 * `TKinter`
 * `CustomTkinter`

![Alt text](assets/images/image.png)
Above is a screenshot of *my_attemps.py*. 

## HOW TO USE
To convert a file, click on _Upload_ button and select your file. If you want to change your scale factor (the number by which all data points will be mutliplied) you can do so by typing it on the text box labeled scale factor, though you don't have to since it defaults to one. When clicking convert, you may be prompted type in a unique identifier. This is because you may have already created a log file with that same name and the unique identifier will be added to the name of the converted file and log file to prevent overwritinng the previous convertion and log files. You can also click on the button in that popup to generate a random unique identifier.
You may want to add multiple files together and convert them into one file. You can do this by checking the check box next to the convert button. This will prevent you from converting that file and will add this file to which ever file you chose to convert. You can always add a new file entry to convert more files (independently or by adding them to each other) by clicking the _Add file_ button.