import os
import sys
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import ttk
from PIL import Image, ImageTk

sys.path.append(os.path.join(os.getcwd(), 'src'))

import cv2


def encrypt(messege_img, dummy_img):
    m_image = cv2.imread(messege_img)   # messege image
    d_image = cv2.imread(dummy_img)     # dummy image
    dim = m_image.shape[:2][::-1]
    image_mod2 = cv2.resize(d_image, dim, interpolation=cv2.INTER_CUBIC)
    bgr_img = ((image_mod2 // 16) * 16) + (m_image // 16)
    b, g, r = cv2.split(bgr_img)
    rgb_img = cv2.merge((r, g, b))
    en_img = Image.fromarray(rgb_img)
    return en_img


def decrypt(en_img):
    e_img = cv2.imread(en_img)
    bgr_img = (e_img % 16) * 16
    b, g, r = cv2.split(bgr_img)
    rgb_img = cv2.merge((r, g, b))
    de_img = Image.fromarray(rgb_img)
    return de_img


m_image = None
d_image = None
e_image = None
s_image = None


def resize_image(event, img, label):
    n_w = event.width
    n_h = event.height
    image = img.resize((n_w, n_h))
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo


def open_files(label):
    global m_image
    global d_image
    global e_image
    dialog_box1 = filedialog.askopenfilename(
        initialdir='images/', title='Select a file',
        filetypes=(('jpg files', '*.jpg'), ('png files', '*.png'),
                   ('all files', '*.*')))
    if not dialog_box1:
        return
    temp_img = Image.open(dialog_box1)
    img = temp_img.resize((label.winfo_width(), label.winfo_height()))
    img1 = ImageTk.PhotoImage(img)
    label.config(image=img1)
    label.image = img1
    label.bind('<Configure>', lambda event,
               img=img.copy(), label=label: resize_image(event, img, label))
    if label == label_up:
        m_image = dialog_box1
    elif label == label_down:
        d_image = dialog_box1
    else:
        e_image = dialog_box1
    return None


def generate_image(label):
    global s_image
    if label == label_right:
        if m_image is None or d_image is None:
            print('Make sure both of the images are selected')
            return
        else:
            en_img = encrypt(m_image, d_image)
    else:
        if e_image is None:
            print('Make sure the image is delected')
            return
        else:
            en_img = decrypt(e_image)
    img = en_img.resize((label.winfo_width(), label.winfo_height()))
    s_image = en_img
    img1 = ImageTk.PhotoImage(img)
    label.config(image=img1)
    label.image = img1
    label.bind('<Configure>', lambda event,
               img=img.copy(), label=label: resize_image(event, img, label))
    return


def save_image():
    if s_image is None:
        print('Press the generate image button to generate an image')
        return
    filename = filedialog.asksaveasfile(mode='w', defaultextension='.png',
                                        filetypes=(('png files', '*.png'),
                                                   ('all files', '*.*')))
    if not filename:
        return
    s_image.save(filename.name)


# Root
root = tk.Tk()
root.title(string='Stegacrypt')
root.iconbitmap('src//icon.ico')
root.geometry('700x500')

bg_image = Image.open('src//bg_image.jpg')
imgtk = ImageTk.PhotoImage(bg_image)


# Tabs
notebook = ttk.Notebook(root)
notebook.place(relx=0, rely=0, relheight=1, relwidth=1)


# Encrypt Frame
en_frame = tk.Frame(notebook, highlightthickness=2)
en_frame.config(highlightbackground='#7c5692', highlightcolor='#7c5692')
en_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

b_label = tk.Label(en_frame, image=imgtk)
b_label.bind('<Configure>', lambda event,
             img=bg_image.copy(), label=b_label: resize_image(event, img, label))
b_label.place(relx=0, rely=0, relwidth=1, relheight=1)


# Upper Frame(Encrypt Frame)
frame_up = tk.Frame(en_frame, bd=5, bg='#7c5692')
frame_up.place(relx=0.05, rely=0.05, relheight=0.4, relwidth=0.4)

button_up = tk.Button(frame_up, text='Choose Image', font=(
    'times', 10), justify='center', pady=0.2, bg='#b4f6ff', relief='flat',
    fg='#424242', command=lambda: open_files(label_up))
button_up.place(relx=0.25, rely=0.925, relheight=0.08, relwidth=0.5)

label_up = tk.Label(frame_up, bd=10, bg='#c3b4df',
                    text='Hidden Image', fg='#424242')
label_up.place(relx=0.01, rely=0.01, relheight=0.9, relwidth=0.98)


# Lower Frame(Encrypt Frame)
frame_down = tk.Frame(en_frame, bd=5, bg='#7c5692')
frame_down.place(relx=0.05, rely=0.55, relheight=0.4, relwidth=0.4)

button_down = tk.Button(frame_down, text='Choose Image',
                        font=('times', 10), justify='center', pady=0.2,
                        bg='#b4f6ff', relief='flat', fg='#424242',
                        command=lambda: open_files(label_down))
button_down.place(relx=0.25, rely=0.925, relheight=0.08, relwidth=0.5)

label_down = tk.Label(frame_down, bd=10, bg='#c3b4df',
                      text='Dummy Image', fg='#424242')
label_down.place(relx=0.01, rely=0.01, relheight=0.9, relwidth=0.98)

# Side Frame(Encrypt Frame)
frame_right = tk.Frame(en_frame, bd=5, bg='#7c5692')
frame_right.place(relx=0.55, rely=0.3, relheight=0.4, relwidth=0.4)

button_right_save = tk.Button(
    frame_right, text='Save Image', font=('times', 10), justify='center',
    pady=0.2, bg='#b4f6ff', relief='flat', fg='#424242', command=save_image)
button_right_save.place(relx=0.5, rely=0.925, relheight=0.08,
                        relwidth=0.480)

button_right_generate = tk.Button(
    frame_right, text='Generate Image', font=('times', 10), justify='center',
    pady=0.2, bg='#b4f6ff', relief='flat', fg='#424242',
    command=lambda: generate_image(label_right))
button_right_generate.place(relx=0.01, rely=0.925,
                            relheight=0.08, relwidth=0.480)

label_right = tk.Label(frame_right, bd=10, bg='#c3b4df',
                       text='Modified Image', fg='#424242')
label_right.place(relx=0.01, rely=0.01, relheight=0.9, relwidth=0.98)

notebook.add(en_frame, text='Encrypt')


# Decrypt Frame
de_frame = tk.Frame(notebook, highlightthickness=2)
de_frame.config(highlightbackground='#7c5692', highlightcolor='#7c5692')
de_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

b_label = tk.Label(de_frame, image=imgtk)
b_label.bind('<Configure>', lambda event,
             img=bg_image.copy(), label=b_label: resize_image(event, img, label))
b_label.place(relx=0, rely=0, relwidth=1, relheight=1)


# Left Frame(Decrypt Frame)
frame_dleft = tk.Frame(de_frame, bd=5, bg='#7c5692')
frame_dleft.place(relx=0.05, rely=0.3, relheight=0.4, relwidth=0.4)

button_dleft = tk.Button(frame_dleft, text='Choose Image',
                         font=('times', 10), justify='center', pady=0.2,
                         bg='#b4f6ff', relief='flat', fg='#424242',
                         command=lambda: open_files(label_dleft))
button_dleft.place(relx=0.25, rely=0.925, relheight=0.08, relwidth=0.5)

label_dleft = tk.Label(frame_dleft, bd=10, bg='#c3b4df',
                       text='Modified Image', fg='#424242')
label_dleft.place(relx=0.01, rely=0.01, relheight=0.9, relwidth=0.98)


# Right Frame(Decrypt Frame)
frame_dright = tk.Frame(de_frame, bd=5, bg='#7c5692')
frame_dright.place(relx=0.55, rely=0.3, relheight=0.4, relwidth=0.4)

button_dright_generate = tk.Button(
    frame_dright, text='Generate Image', font=('times', 10), justify='center',
    pady=0.2, bg='#b4f6ff', relief='flat', fg='#424242',
    command=lambda: generate_image(label_dright))
button_dright_generate.place(relx=0.01, rely=0.925,
                             relheight=0.08, relwidth=0.480)

button_dright_save = tk.Button(
    frame_dright, text='Save Image', font=('times', 10), justify='center',
    pady=0.2, bg='#b4f6ff', relief='flat', fg='#424242', command=save_image)
button_dright_save.place(relx=0.5, rely=0.925, relheight=0.08,
                         relwidth=0.480)

label_dright = tk.Label(frame_dright, bd=10, bg='#c3b4df',
                        text='Hidden Image', fg='#424242')
label_dright.place(relx=0.01, rely=0.01, relheight=0.9, relwidth=0.98)

notebook.add(de_frame, text='Decrypt')


root.mainloop()
