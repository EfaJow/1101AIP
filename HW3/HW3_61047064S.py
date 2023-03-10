import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from matplotlib import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random


def open():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Png Images", "*.png"), ("JPG Images", "*.jpg"), ("Bmp Images", "*.bmp"), ("Ppm Images", "*.ppm")]
    )

    if filepath!='':
        canvas_out.delete("all")
        root.im = Image.open(filepath)
        r1=(frame_width/root.im.width)
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
        root.gray=0

def save():
    if root.op==1:
        im_save = ImageTk.getimage( root.im_out )
        im_save.save("result.bmp")
        if root.hist==1:
            root.p.figure.savefig('Histogram.png')

# def grayhistogram():
#     if root.op==1:
#         root.im_out=ImageTk.getimage(root.im_in)#original
#         root.im_out=gray(root.im_out) #grayscaled
#         root.im_out=ImageTk.PhotoImage(root.im_out) #grayscaled
#         canvas_in.create_image((frame_width/2,frame_height/2), image=root.im_in, anchor='center') #original image
#         canvas_out.create_image((frame_width/2,frame_height/2), image=root.im_out, anchor='center') #grayscaled
#         histogram(0,256)
    
def histogram(arr,title):

    f = figure.Figure(figsize=(5,4), dpi=100)
    canvas_hist = FigureCanvasTkAgg(f, master=frame3)
    canvas_hist.get_tk_widget().grid(row=1, column=2, sticky='ne')
    root.p = f.gca()

    root.p.hist(arr,bins=300)
    root.p.set_title(title) 
    
    canvas_hist.draw()
    root.hist=1
    

def gray(image):
    pix = image.load()
    #print(root.array)

    if len(pix[0,0])==3:#RGB
        for x in range(0,image.size[0]):  # Get the width and hight of the image for iterating over
            for y in range(0, image.size[1]):
                i=int(np.dot(pix[x,y],[0.2989, 0.5870, 0.1140])) #Get the RGB Value of the a pixel of an image, then do multipllication with grayscale matrix
                pix[x,y]=(i,i,i) # Set the RGB Value of the image (tuple)
               
    if len(pix[0,0])==4:#RGBA
        for x in range(0,image.size[0]):  # Get the width and hight of the image for iterating over
            for y in range(0, image.size[1]):
                i=int(np.dot(pix[x,y],[0.2989, 0.5870, 0.1140,0])) 
                #Get the RGB Value of the a pixel of an image, then do multipllication with grayscale matrix
                pix[x,y]=(i,i,i,pix[x,y][3]) # Set the RGB Value of the image (tuple)
              
    #root.gray=1
    return image  # Return the modified pixels
   

def scalevalue(v):
    root.scale=v       
        
def GaussianPop():
    if root.op==1 and root.pop==0:
        root.scale=0
        #root.pop=1
        newWindow = tk.Toplevel()
        newWindow.wm_title("Gaussian White Noise")

        #for buttons
        frame1 = tk.Frame(newWindow)
        frame1.grid(row=0, column=0, sticky='we')

        #output image
        frame2 = tk.Frame(newWindow)
        frame2.grid(row=1, column=0,  sticky='e')
        
        l = tk.Label(frame1, text="Please input the value of standard deviation of Gaussian Noise:")
        l.grid(row=0, column=0)
        scale=tk.Scale(frame1, label='Value', from_=0, to=20, orient='horizontal', 
        tickinterval=10, resolution=1, showvalue=True, command=scalevalue)
        scale.grid(row=2, column=0, sticky='we')
        bt_ok=tk.Button(frame2, text='OK', command=lambda:newWindow.destroy() or GWN())
        bt_ok.grid(row=0,column=0)

        bt_cancel=tk.Button(frame2, text='Cancel', command=newWindow.destroy)
        bt_cancel.grid(row=0,column=1)

def GWN():
    root.im_out=ImageTk.getimage(root.im_in)#original
    root.im_out=gray(root.im_out)#gray
    array=GaussianNoise(root.scale)
    root.im_out=ImageTk.PhotoImage(root.im_out) #grayscaled
    canvas_in.create_image((frame_width/2,frame_height/2), image=root.im_in, anchor='center') #original image
    canvas_out.create_image((frame_width/2,frame_height/2), image=root.im_out, anchor='center') #grayscaled & gaussian noise
    histogram(array,"Gaussian Noise")
    
def GaussianNoise(sigma):
    width, height = root.im_out.size
    g = root.im_out.load()
    list=[]
    #a = np.zeros(width*height)
    #f0=np.zeros((width, height))
    for i in range(0,int(width)):
        for j in range(0,int(height/2)):

            gamma= random.random()
            phi= random.random()

            z1= float(sigma) *np.cos(2 *np.pi * phi) * np.sqrt((-2) * np.log(gamma))
            z1= float2int(z1)

            z2= float(sigma) *np.sin(2 *np.pi *phi) *np.sqrt((-2) *np.log(gamma))
            z2=float2int(z2)

            list.append(z1)
            list.append(z2)

            if len(g[0,0])==3:#RGB
                g[i,2*j]=tuple(inrange(np.add(g[i,2*j],(z1,z1,z1))))
                g[i,2*j+1]=tuple(inrange(np.add(g[i,2*j+1],(z2,z2,z2))))
            
            if len(g[0,0])==4:
                g[i,2*j]=tuple(inrange(np.add(g[i,2*j],(z1,z1,z1,0))))
                g[i,2*j+1]=tuple(inrange(np.add(g[i,2*j+1],(z2,z2,z2,0))))

    return list

def float2int(float):
    if (float>=0):
        return int(float+0.5)
    if (float<0):
        return int(float-0.5)

            
def inrange(f0):
    for i in range(0,3):
        if (f0[i] < 0):
           f0[i]=0
        if(f0[i]>255):
            f0[i]=255
    return f0



# #POPUP
# pop=tk.Tk()


#WINDOW
root = tk.Tk()
root.title('AIP_61047064S')
root.array= np.array(256)
root.op=0
root.pop=0
root.scale=float(0)


#FRAME
frame_width = 360
frame_height = 360
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

#bt_1 = tk.Button(frame2, text='Histogram', command=grayhistogram)
#bt_1.grid(row=1,column=0,sticky="ew", padx=pad, pady=5)

bt_2 = tk.Button(frame2, text='Gaussian White Noise', command=GaussianPop)
bt_2.grid(row=2,column=0,sticky="ew", padx=pad, pady=5)

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