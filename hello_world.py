import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from PIL import ImageTk, Image

root = Tk()
root.geometry("1280x720")
root.title('Image Mosaic Creator')
content = Frame(root)


def select_file(x, existing=True):
    filetypes = (
        ('Image files', ['*.jpg', '*.png', '*.gif', '*.jpeg']),
        ('All files', '*.*')
    )

    if existing:
        filename = filedialog.askopenfilename(
            title = 'Open a file',
            initialdir='/',
            filetypes=filetypes
        )
    else:
        filename = filedialog.asksaveasfilename(
            title = "Select file to save to",
            initialdir='/'
        )

    x.set(filename)

def select_folder(x):
    folder = filedialog.askdirectory(
        title = 'Select tile folder',
        initialdir='/',
    )
    
    x.set(folder)

def update_image(*args):
    # Get the updated image filename from the StringVar
    image_filename = img_file.get()
    
    # Open and resize the image
    image = Image.open(image_filename)
    image_width, image_height = image.size

    screen_width = root.winfo_width()
    screen_height = root.winfo_height()

    max_width = int(.75 * screen_width)
    max_height = int(.90 * screen_height)
    scale_factor = min(max_width / image_width, max_height / image_height)

    new_width = int(image_width * scale_factor)
    new_height = int(image_height * scale_factor)
    image = image.resize((new_width, new_height))  # Adjust the size as needed
    
    # Convert the image to Tkinter PhotoImage format
    photo = ImageTk.PhotoImage(image)
    
    # Update the image displayed in the label
    label.config(image=photo)
    label.image = photo  # Keep a reference to avoid garbage collection issues

    
#layout objects
img_file = StringVar()
open_button = Button(content, text='Open a main image', command=lambda: select_file(img_file))
open_button.grid(column=0,row=0, )
img_file.set("Image path will show here...")
img_file.trace("w", update_image)

file_text = Entry(content, textvariable=img_file)
file_text.config(state='readonly')
file_text.grid(column=0, row=1, )

tile_folder = StringVar()
folder_button = Button(content, text='Select tile folder', command=lambda: select_folder(tile_folder))
folder_button.grid(column=0,row=2, )

tile_folder.set("Tile folder will show here...")
folder_text = Entry(content)
folder_text.config(state='readonly', textvariable=tile_folder)
folder_text.grid(column=0, row=3, )

subgrid = Frame(content)
subgrid.grid(column=0, row=4, )

mod_colors = BooleanVar()
mod_colors_box = Checkbutton(subgrid, text="Tile color modification", variable=mod_colors)
mod_colors_box.grid(column=0,row=0)

tile_res_label = Label(subgrid, text="Tile Res: ")
tile_res_label.grid(column=0,row=1)

tile_res = StringVar()
tile_res_box = Entry(subgrid, textvariable=tile_res)
tile_res_box.grid(column=1,row=1)

dup_thresh_label = Label(subgrid, text="Duplicates allowed: ")
dup_thresh_label.grid(column=0,row=2)

dup_thresh = StringVar()
dup_thresh_box = Entry(subgrid, textvariable=tile_res)
dup_thresh_box.grid(column=1,row=2)

scale_label = Label(subgrid, text="Scaling Factor: ")
scale_label.grid(column=0,row=3)

scale_factor = StringVar()
scale_box = Entry(subgrid, textvariable=scale_factor)
scale_box.grid(column=1,row=3)

output_dir = StringVar()
output_dir.set("Output filepath/name")
output_dir_button = Button(subgrid, text="Select output filedir", command=lambda: select_file(output_dir, existing=False))
output_dir_button.grid(column=0,row=5)
output_dir_box = Entry(subgrid, state='readonly', textvariable=output_dir)
output_dir_box.grid(column=1, row=5)

render_button = Button(content, text="Render", command=None)
render_button.grid(column=0,row=6)

label = Label(content)
label.grid(column=1, row=0, rowspan=7, columnspan=7)

content.grid()
root.mainloop()