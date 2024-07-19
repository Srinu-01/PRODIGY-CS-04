import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import tkinter.messagebox as mbox

window = Tk()
window.geometry("800x600")
window.title("Encryption and Decryption")

# Global variables
global x, panelA, panelB, eimg, image_encrypted, key

panelA = None
panelB = None
x = None
eimg = None
image_encrypted = None
key = None

# Function to open an image file
def openfilename():
    filename = filedialog.askopenfilename(title='Select Image', filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    return filename

# Function to open and display selected image
def open_img():
    global x, panelA, panelB, eimg
    x = openfilename()
    if x:
        input_path_entry.delete(0, END)  # Clear the entry widget
        input_path_entry.insert(0, x)  # Insert the selected file path
        img = Image.open(x)
        eimg = img
        img = img.resize((300, 300), Image.LANCZOS)  # Resize image to display
        img = ImageTk.PhotoImage(img)
        if panelA is None:
            panelA = Label(image=img)
            panelA.image = img
            panelA.place(x=50, y=150)  # Adjust position of original image display
        else:
            panelA.configure(image=img)
            panelA.image = img
        if panelB is None:
            panelB = Label(image=img)
            panelB.image = img
            panelB.place(x=450, y=150)  # Adjust position of encrypted/decrypted image display
        else:
            panelB.configure(image=img)
            panelB.image = img
    else:
        mbox.showwarning("Warning", "No image selected.")

# Function for encryption
def en_fun(x):
    global image_encrypted, key
    image_input = cv2.imread(x, 0)
    if image_input is not None:
        (x1, y) = image_input.shape
        image_input = image_input.astype(float) / 255.0
        mu, sigma = 0, 0.1
        key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
        image_encrypted = image_input / key
        cv2.imwrite('image_encrypted.jpg', image_encrypted * 255)
        imge = Image.open('image_encrypted.jpg')
        imge = imge.resize((300, 300), Image.LANCZOS)  # Resize encrypted image to display
        imge = ImageTk.PhotoImage(imge)
        panelB.configure(image=imge)
        panelB.image = imge
        mbox.showinfo("Encrypt Status", "Image Encrypted successfully.")
    else:
        mbox.showwarning("Warning", "Failed to read image.")

# Function for decryption
def de_fun():
    global image_encrypted, key
    if image_encrypted is not None and key is not None:
        image_output = image_encrypted * key
        image_output *= 255.0
        cv2.imwrite('image_output.jpg', image_output)
        imgd = Image.open('image_output.jpg')
        imgd = imgd.resize((300, 300), Image.LANCZOS)  # Resize decrypted image to display
        imgd = ImageTk.PhotoImage(imgd)
        panelB.configure(image=imgd)
        panelB.image = imgd
        mbox.showinfo("Decrypt Status", "Image decrypted successfully.")
    else:
        mbox.showwarning("Warning", "Image not encrypted yet.")

# Label for the title
title_label = Label(window, text="Encryption and Decryption", font=("Arial", 30))
title_label.place(x=200, y=20)

# Label and Entry for selecting image
select_label = Label(window, text="Select Image: ", font=("Arial", 15))
select_label.place(x=50, y=70)

input_path_entry = Entry(window, width=50, font=("Arial", 12))
input_path_entry.place(x=180, y=75)

# Button to browse and open image
browse_button = Button(window, text="Browse", command=open_img, font=("Arial", 12))
browse_button.place(x=600, y=70)

# Buttons for Encrypt and Decrypt
encrypt_button = Button(window, text="Encrypt", command=lambda: en_fun(x), font=("Arial", 15))
encrypt_button.place(x=200, y=470)

decrypt_button = Button(window, text="Decrypt", command=de_fun, font=("Arial", 15))
decrypt_button.place(x=400, y=470)

# Label for Normal Image
normal_label = Label(window, text="Normal Image", font=("Arial", 15))
normal_label.place(x=150, y=100)

# Label for Encrypted/Decrypted Image
enc_dec_label = Label(window, text="Encrypted/Decrypted Image", font=("Arial", 15))
enc_dec_label.place(x=500, y=100)

window.mainloop()
