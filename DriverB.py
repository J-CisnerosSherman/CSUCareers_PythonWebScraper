import os
import subprocess
import tkinter as tk
from tkinter import simpledialog


#import os

# Get the folder name from the user
folder_name = input("Enter the folder name: ")

# Get the user's desktop path (assuming it's on C:\)
desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
print("Desktop path ", desktop_path)
# Create the folder on the desktop
folder_path = os.path.join(desktop_path, folder_name)

try:
    os.mkdir(folder_path)
    print(f"Folder '{folder_name}' created on the desktop at: {folder_path}")
except FileExistsError:
    print(f"Folder '{folder_name}' already exists on the desktop.")
except Exception as e:
    print(f"An error occurred: {e}")
