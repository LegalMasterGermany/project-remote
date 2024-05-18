from tkinter import *
from PIL import Image, ImageTk

def close_window(event):
    event.widget.quit()

def jumpscare(uuid):
    root = Tk()
    root.attributes('-fullscreen', True)
    root.configure(background='black')  

    root.focus_force()
    root.lift()
    root.attributes('-topmost', True)

    image_path = "jumpscare.jpg"  
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    label = Label(root, image=photo, bg='black') 
    label.image = photo
    label.pack(expand=True, fill=BOTH)

    root.bind("<Button-1>", close_window)
    root.bind("<Key>", close_window)
    root.mainloop()

def init_jumpscare(uuid):
    jumpscare(uuid)


