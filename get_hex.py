import cv2
from PIL import Image, ImageEnhance, ImageTk
from numpy import asarray
import tkinter as tk
from multiprocessing.pool import ThreadPool

root = tk.Tk()   
root.grid()   
canvas = tk.Canvas(root)      
canvas.pack()   

label = tk.Label(root, text="E", anchor=tk.S)
label.pack()

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
result, image = cam.read()

pool = ThreadPool(processes=2)

def get_aver_color(img):

    enhancer = ImageEnhance.Brightness(img) 
    enhancer.enhance(2)
    
    pixels = asarray(enhancer.image)
    
    aver = 0
    r = 0
    g = 0
    b = 0
    for grid in pixels:
        for row in grid:
            aver += 1
            r += row[0] 
            g += row[1]
            b += row[2]
    
    r = r / aver
    g = g / aver
    b = b / aver
    
    hex = '#%02x%02x%02x' % (r.astype(int), g.astype(int), b.astype(int))
    return hex

while True:
    result, image = cam.read()
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(image)
    
    
    #img = img.resize((width, 128))
    
    get_color_t = pool.apply_async(get_aver_color, [img])
    
    img = ImageTk.PhotoImage(img)
    canvas.create_image(20, 20, image=img, anchor=tk.CENTER) 
    hex = get_color_t.get()
    label.config(text=hex)
    
    root['background'] = hex
    #label.config(text=get_color_t.get())
    root.update_idletasks()
    root.update()

