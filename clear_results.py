import os

filepath = os.getcwd() + '/results/'

# Clear results folder
for filename in os.listdir(filepath):
    file_path = os.path.join(filepath, filename)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
    except Exception as e:
        print(e)

filepath = os.getcwd() + '/logs/'

# Clear results folder
for filename in os.listdir(filepath):
    file_path = os.path.join(filepath, filename)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
    except Exception as e:
        print(e)