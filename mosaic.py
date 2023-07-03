import tkinter as tk
from PIL import Image, ImageTk
import os
import enum
import glob
import pandas as pd
import numpy as np
from scipy import spatial
from scipy import stats as st
import math as m

def list_tiles(tiles):
    '''
    Inputs:
    tiles - filepath where emojis/tile imgs are stored, use * in folder containing imgs
    
    Output:
    list of tiles
    '''
    tile_list = []
    for file in glob.glob(tiles):
        tile_list.append(file)
    
    return tile_list

def get_res(source, scaling_factor, tile_res):
    '''
    Inputs:
    source - filepath of base image
    scaling_factor - resolution of tiles (default 2). calculated as source res / scaling factor
    tile_res - int of width/height of tiles (assumes square).
    
    Output:
    new_res - tuple of tile resolution of main image
    output_res - tuple of pixel resolution of output image
    '''
    photo = Image.open(source)
    photo = photo.convert("RGB")
    
    res = photo.size
    #calculate the resolution of individual tiles on source
    new_res = tuple([int(x / scaling_factor) for x in res])
    
    #calculate the output resolution (in pixels) given tile res
    output_res = tuple([int((x * tile_res) / scaling_factor) for x in res])
    
    return new_res, output_res

def modify_colors(tile_list, tile_res, scale=0.2, step=0.05):
    '''
    Inputs:
    tile_list - list of tile filepaths
    tile_res - int, size of tiles
    scale - float between 0.01, 0.99 - magnitude of color changing
    step - step between 1-scale, 1+scale
    
    Output:
    tile_imgs - list of images that have had colors altered.
    '''
    
    tile_imgs = []
    color_var = np.arange(1-scale,1+scale,step)
    for filepath in tile_list:
        tile = Image.open(filepath)
        tile = tile.convert("RGB")
        tile = tile.resize(tuple([tile_res,tile_res]))
        tile = np.array(tile)
        
        for color_mod in color_var:
            for i in range(len(np.array(tile)[1][1])):
                tile_img = tile
                tile_img[...,i] = np.clip(tile_img[...,i]*color_mod, 0, 255)
                tile_img = Image.fromarray(tile_img.astype(np.uint8))
                tile_imgs.append(tile_img)

    return tile_imgs


def calc_avg_color(tile_imgs):
    '''
    Inputs:
    tile_imgs - list of images
    
    Output:
    colors - list of mean colors for each tile
    '''
    
    colors = []
    for img in tile_imgs:
        mean_color = np.array(img).mean(axis=0).mean(axis=0)
        colors.append(mean_color)

    return colors

def calc_tiles(source, colors, new_res, dup_threshold):
    '''
    
    '''
    #create KDtree from colors
    tree = spatial.KDTree(colors)
    
    #pixelate source photo to num of tiles we'll have
    photo = Image.open(source)
    photo = photo.convert("RGB")
    resized_photo = photo.resize(new_res)
    
    #empty integer array to store indices of tiles
    closest_tiles = np.zeros((resized_photo.size), dtype=np.uint32)
    
    #create set to store used tiles
    imgs_used = set()
    for i in range(new_res[0]):
        for j in range(new_res[1]):
            pixel = resized_photo.getpixel((i,j))
            closest = tree.query(pixel, k=dup_threshold)
            
            if dup_threshold == 0:
                closest_tiles[i,j] = closest[1]
                
            else:
                for x in range(len(closest[1].tolist())):
                    if closest[1][x] not in imgs_used:
                        closest_tiles[i,j] = closest[1][x]
                        imgs_used.add(closest[1][x])
                        break
                    #if all matches used up, pick a random out of the 25% most matching tiles    
                    if x == (len(closest[1].tolist())-1):
                        y = np.random.randint(1,int(x/4))
                        closest_tiles[i,j] = closest[1][y]
                        imgs_used.add(closest[1][y])
                        break

def assemble_tiles(closest_tiles, output_res, new_res, tile_res, tile_imgs, output_filepath):
    output = Image.new("RGB", output_res)
    
    for i in range(new_res[0]):
        for j in range(new_res[1]):
            x, y = i*tile_res, j*tile_res
            index = closest_tiles[i,j]
            output.paste(tile_imgs[index],(x,y))
    
    output.save(output_filepath)

def make_mosaic(source, tiles, scaling_factor=2, dup_threshold=0, tile_res=100, mod_colors=False, output_filepath="mosaic.jpg"):
    '''
    Inputs:
    source - filepath of base image
    tiles - filepath where emojis/tile imgs are stored, use * in folder containing imgs
    scaling_factor - resolution of tiles (default 2). calculated as source res / scaling factor
    dup_threshold - how many times a tile can be used before removed from options. 0=inf
    tile_res - pixel resolution of tiles in output image (higher = more detailed but bigger files).
    output_filepath - filepath to store saved mosaic.
    
    Output:
    mosaic - jpg file saved to output_filepath
    '''
    print("Generating tile list...")
    tile_list = list_tiles(tiles)
    
    print("Generating canvas resolution...")
    new_res, output_res = get_res(source, scaling_factor, tile_res)
    print(f"Output res: {output_res}")
    print(f"New res: {new_res}")
    
    print("Compiling tile arrays to list...")
    if mod_colors:
        tile_imgs = modify_colors(tile_list, tile_res, scale=0.2, step=0.05)
    else:
        tile_imgs = modify_colors(tile_list, tile_res, scale=0, step=0)
    
    print("Calculating average tile colors...")
    colors = calc_avg_color(tile_imgs)
    
    print("Calculating nearest neighbors to base image...")
    closest_tiles = calc_tiles(source, colors, new_res, dup_threshold)
    
    print("Assembling tiles on canvas and saving...")
    assemble_tiles(closest_tiles, output_res, new_res, tile_res, tile_imgs, output_filepath)
    
    print("Done!")                    

    return closest_tiles

if __name__ == '__main__':
    #define vars inline for now:
    source = "/mnt/c/Users/brend/OneDrive/Pictures/Screenshots/"
    tiles = "C:/Users/brendo/Desktop/argo_emojis/src.har.d/emoji.slack-edge.com/TJVP90F4L/*/*"
    scaling_factor = 2
    dup_threshold = 20
    tile_res = 30
    mod_colors = True
    output_filepath="mosaic_test4.jpg"

    root = tk.Tk()

    # Add a label
    tk.Label(root, text="Enter parameter: ").grid(row=0)

    # Add a text entry box
    entry = tk.Entry(root)
    entry.grid(row=0, column=1)
    entry.trace_add("write", lambda *args: update_image())

    # Placeholder for image
    label_img = tk.Label(root)
    label_img.grid(row=2, columnspan=2)

    # Function to update the image
    def update_image():
        param = entry.get()
        img = make_mosaic(param) # define function
        img = img.resize((700, 700), Image.ANTIALIAS) # resizing so it fits in the GUI, you can change the size or remove this line
        img_tk = ImageTk.PhotoImage(img)
        label_img.config(image=img_tk)
        label_img.image = img_tk # keep a reference to the image to prevent garbage collection

    # Add a button, tied to the update_image function
    button = tk.Button(root, text="Update Image", command=update_image)
    button.grid(row=1, columnspan=2)

    root.mainloop()