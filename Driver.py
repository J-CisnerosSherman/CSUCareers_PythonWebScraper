import os
import subprocess
import tkinter as tk
from tkinter import simpledialog




# Create a tkinter root window (it won't be displayed)
root = tk.Tk()
root.withdraw()  # Hide the root window



# Use simpledialog to get user input

folder_name = simpledialog.askstring("User Input", "Enter name of folder ")
days_num = simpledialog.askstring("User Input", "How many days ago do you want to search?")
folder_path = simpledialog.askstring("User Input", "Enter the path to desktop:")                 #C:\Users\User\Desktop



# Display the user's input
if folder_name and days_num and folder_path:
    print("You entered:", folder_name)
    print("You entered:", days_num)
    print("You entered:", folder_path)
else:
    print("No input provided.")


# Check if the folder exists
if not os.path.exists(os.path.join(folder_path, folder_name)):
    # If it doesn't exist, create it
    os.makedirs(os.path.join(folder_path, folder_name))






# Close the root window (optional)
root.destroy()

