import tkinter as tk
from tkinter.constants import ANCHOR, NW
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import pdb

#WINDOW
root = tk.Tk()
root.title('AIP_61047064S')
#root.geometry('928x416')
align_mode='nswe'

#FRAME
frame_width = 400
frame_height = 400
button_width = 80
pad=8
root.op=0

frame1 = tk.Frame(root,  width=frame_width, height=frame_height)
frame2 = tk.Frame(root,  width=button_width, height=frame_height)
frame3 = tk.Frame(root,  width=frame_width, height=frame_height)
frame1.grid(column=0, row=0)
frame2.grid(column=1, row=0)
frame3.grid(column=2, row=0)

heading_height=0
heading_1=tk.Label(frame1, text='Input Image', height = heading_height)
heading_2=tk.Label(frame3, text='Output Image', height = heading_height)
heading_1.grid( sticky='w')
heading_2.grid(column=0, row=0, sticky='w')

canvas_in = tk.Canvas(frame1, width = frame_width, height = frame_height, bg='gray') 
canvas_out= tk.Canvas(frame3, width = frame_width, height = frame_height, bg='gray')
canvas_in.grid( sticky=align_mode)
canvas_out.grid(column=0, row=1, sticky=align_mode)

#====MENU BUTTONS====
def open():
    """Open a file for editing."""
    filepath = askopenfilename(
    #    filetypes=[("Png Images", "*.png"), ("JPG Images", "*.jpg"), ("Bmp Images", "*.bmp"), ("Ppm Images", "*.ppm")]
    )

    if filepath!='':
        root.im_in = Image.open(filepath)

        r1= frame_width/root.im_in.width 
        r2= frame_height/root.im_in.height
        m=min(r1, r2)
        w=int(m*root.im_in.width)
        h=int(m*root.im_in.height)

        root.im_br=root.im_in.resize((w, h))
        root.im = ImageTk.PhotoImage(root.im_br)
        canvas_in.create_image((0,0), image=root.im, anchor=NW)
        canvas_out.create_image((0,0), image=root.im, anchor=NW)
        root.op=1

def save():
    if root.op==1:
     root.im_in.save("result.bmp")
    

    




#Menu frame
menu = tk.Menu(root)
#tearoff=False turn off the tearoff
filemenu = tk.Menu(menu, tearoff=False)
#add filemenu into menu 
menu.add_cascade(menu=filemenu, label='File')
#add menu
filemenu.add_command(label='Open...', command=open)
#add separate line
filemenu.add_separator()
#add save
filemenu.add_command(label='Save', command=save)
#put menu into root
root.config(menu=menu)

# ====Future BUTTONS=============
# def create_button(txt):
#      bt_1 = tk.Button(root, text=txt, bg='white')
#      bt_1['activebackground']='blue'
#      bt_1['activeforeground']='white'
# bt_1 = tk.Button(root, text='Do sth.1')
# bt_2=tk.Button(root, text='Do sth.2')
# bt_1.pack()
# bt_2.pack()
# ===============================



root.mainloop()