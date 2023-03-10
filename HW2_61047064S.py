import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from matplotlib import figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pdb

#WINDOW
root = tk.Tk()
root.title('AIP_61047064S')
root.array= np.array(256)
root.op=0

def open():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Png Images", "*.png"), ("JPG Images", "*.jpg"), ("Bmp Images", "*.bmp"), ("Ppm Images", "*.ppm")]
    )

    if filepath!='':
        canvas_out.delete("all")
        root.im = Image.open(filepath)
        r1=(frame_width/root.im.width )
        r2=(frame_height/root.im.height)
        m=min(r1, r2)
        root.w=int(m*root.im.width)
        root.h=int(m*root.im.height)

        root.im_in=root.im.resize((root.w, root.h))
        root.im_in=ImageTk.PhotoImage(root.im_in) #original image
        canvas_in.create_image((frame_width/2,frame_height/2), image=root.im_in, anchor='center') #original image
        canvas_out.create_image((frame_width/2,frame_height/2), image=root.im_in, anchor='center') #original image
        root.op=1
        root.hist=0

def save():
    if root.op==1:
        im_save = ImageTk.getimage( root.im_out )
        im_save.save("result.bmp")
        if root.hist==1:
            root.p.figure.savefig('Histogram.png')
            
    
def histogram():
    """改成用BAR去畫！！"""
    if root.op==1 and root.hist==0:
        root.im_out=ImageTk.getimage(root.im_in)#original
        root.im_out=gray(root.im_out) #grayscaled
        
        f = figure.Figure(figsize=(5,4), dpi=100)
        canvas_hist = FigureCanvasTkAgg(f, master=frame3)
        canvas_hist.get_tk_widget().grid(row=1, column=2, sticky='ne')
        root.p = f.gca()
        data=np.array(root.im_out)
        hist=np.zeros(256)
        for intensity in range(256):
            A=(data==intensity)
            hist[intensity]=A.sum()
        root.p.hist(hist,density=False,bins=256,cumulative = False)

        root.p.set_title('Image Histogram') 

        root.im_out=ImageTk.PhotoImage(root.im_out) #grayscaled
        canvas_in.create_image((frame_width/2,frame_height/2), image=root.im_in, anchor='center') #original image
        canvas_out.create_image((frame_width/2,frame_height/2), image=root.im_out, anchor='center') #grayscaled
        
        #root.p.set_xlabel("grayscale value") #set label of x axis
        #root.p.set_ylabel("pixels") #set label of y axis
        #plt.xlim(0,255) #set the range of x axis
        #fig.tight_layout()
        
        canvas_hist.draw()
        root.hist=1
    

def gray(image):
    pix = image.load()
    #print(root.array)
    a= np.zeros(256)
    if len(pix[0,0])==3:#RGB
        for x in range(0,image.size[0]):  # Get the width and hight of the image for iterating over
            for y in range(0, image.size[1]):
                
                i=int(np.dot(pix[x,y],[0.2989, 0.5870, 0.1140])) #Get the RGB Value of the a pixel of an image, then do multipllication with grayscale matrix
                pix[x,y]=(i,i,i) # Set the RGB Value of the image (tuple)
                a[i]=a[i]+1 #calculate the amount of the pixels of each grayscale value
    if len(pix[0,0])==4:#RGBA
        for x in range(0,image.size[0]):  # Get the width and hight of the image for iterating over
            for y in range(0, image.size[1]):
                i=int(np.dot(pix[x,y],[0.2989, 0.5870, 0.1140,0])) #Get the RGB Value of the a pixel of an image, then do multipllication with grayscale matrix
                pix[x,y]=(i,i,i,pix[x,y][3]) # Set the RGB Value of the image (tuple)
                a[i]=a[i]+1 #calculate the amount of the pixels of each grayscale value
            
    root.array=a #save the amount of the pixels of each grayscale value
    return image  # Return the modified pixels
   


#FRAME
frame_width = 350
frame_height = 350
button_width = 60
pad=5

#input image
frame1 = tk.Frame(root, width=frame_width, height=frame_height)
frame1.grid(column=0, row=0, sticky='ns')

#for buttons
frame2 = tk.Frame(root,  bg='gray')
frame2.grid(column=1, row=0, sticky='ns')

#output image
frame3 = tk.Frame(root, width=frame_width, height=frame_height)
frame3.grid(column=2, row=0, sticky='ns')

heading_height=1

heading_1=tk.Label(frame1, text='Input Image', height = heading_height)
heading_1.grid(column=0, row=0, sticky='senw')

canvas_in = tk.Canvas(frame1, width = frame_width, height = frame_height) 
canvas_in.grid( column=0, row=1, sticky='nswe')

bt_1 = tk.Button(frame2, text='Histogram', command=histogram)
bt_1.grid(row=1,column=0,sticky="ew", padx=pad, pady=5)

heading_2=tk.Label(frame3, text='Output Image', height = heading_height)
heading_2.grid(column=0, row=0, sticky='nsew')

canvas_out= tk.Canvas(frame3, width = frame_width, height = frame_height)
canvas_out.grid(column=0, row=1, sticky='nswe')




#====MENU BUTTONS====
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


root.mainloop()