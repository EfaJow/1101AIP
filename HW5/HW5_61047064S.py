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
        filetypes=[("Images", "*.png *.jpg *.bmp *.ppm")]
    )

    if filepath!='':
        clearhist()
        canvas_out.delete("all")
        root.im = Image.open(filepath)
        r1=(root.im_size/root.im.width)
        r2=(root.im_size/root.im.height)
        m=max(r1, r2)
        if r1>=r2:
            root.w=int(root.im_size)
            root.h=int(m*root.im.height+0.5)
        else:
            root.w=int(m*root.im.width+0.5)
            root.h=int(root.im_size)    

        root.im_in=root.im.resize((root.w, root.h))#scale in original ratio
        root.im_in=root.im_in.crop((int(root.w/2)-root.im_size/2,int(root.h/2)-root.im_size/2,int(root.w/2)+root.im_size/2,int(root.h/2)+root.im_size/2))
        root.im_in=ImageTk.PhotoImage(root.im_in) #original image
        root.im_out=root.im_in
        canvas_in.create_image((frame_width/2,frame_height/2), image=root.im_in, anchor='center') #original image
        canvas_out.create_image((frame_width/2,frame_height/2), image=root.im_out, anchor='center') #original image
        root.op=1
        root.hist=0
        root.gray=0

def save():
    if root.op==1:
        im_save = ImageTk.getimage( root.im_out )
        im_save.save("result.bmp")
        if root.hist==1:
            root.p.figure.savefig('Histogram.png')

def showresult():
    
    root.im_out = ImageTk.PhotoImage(root.im_out) #processed
    canvas_in.create_image((frame_width/2,frame_height/2), image=root.im_in, anchor='center') #original image
    canvas_out.create_image((frame_width/2,frame_height/2), image=root.im_out, anchor='center') #processed


def grayhistogram():
    if root.op==1:
        clearhist()
        root.im_out = ImageTk.getimage(root.im_in)#original
        root.im_out = gray(root.im_out) #grayscaled
        pixels = getpixelvalue(root.im_out)
        histogram(pixels,"Grayscale Value",'out')
        showresult()
        

def getpixelvalue(image):
    pixels=[pixel for pixel in image.getdata()]
    return pixels

def histogram(pixels,title,in_out):

    f = figure.Figure(figsize=(4,2), dpi=100)
    if in_out=='out':
        root.canvas_hist = FigureCanvasTkAgg(f, master=frame4)
    else:
        root.canvas_hist = FigureCanvasTkAgg(f, master=frame5)
    root.canvas_hist.get_tk_widget().grid(row=1, column=0, sticky='ne')
    root.p = f.gca()

    root.p.hist(pixels,bins=300)
    root.p.set_title(title) 
    
    root.canvas_hist.draw()
    root.hist=1

def clearhist():
    for widget in frame4.winfo_children():
        widget.destroy()
    for widget in frame5.winfo_children():
        widget.destroy()

    root.hist=0

def gray(image):
    image=image.convert('L')
    return image  # Return the modified pixels

def scalevalue(v):
    root.scale=v       
        
def GaussianPop():
    if root.op==1 and root.pop==0:
        
        root.scale=0
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
        scale=tk.Scale(frame1 , from_=0, to=20, orient='horizontal', 
        tickinterval=10, resolution=1, showvalue=True, command=scalevalue)
        scale.grid(row=2, column=0, sticky='we')
        bt_ok=tk.Button(frame2, text='OK', command=lambda:newWindow.destroy() or GWN())
        bt_ok.grid(row=0,column=0)

        bt_cancel=tk.Button(frame2, text='Cancel', command=newWindow.destroy)
        bt_cancel.grid(row=0,column=1)

def GWN():
    clearhist()
    root.im_out=ImageTk.getimage(root.im_in)#original
    root.im_out=gray(root.im_out)#gray
    array=GaussianNoise(root.scale)
    showresult()    
    histogram(array,"Gaussian Noise",'out')
    
def GaussianNoise(sigma):
    width, height = root.im_out.size
    g = root.im_out.load()
    list=[]

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


            g[i,2*j]=inrange(g[i,2*j]+z1)
            g[i,2*j+1]=inrange(g[i,2*j+1]+z2)
            

    return list

def float2int(float):
    if (float>=0):
        return int(float+0.5)
    if (float<0):
        return int(float-0.5)
 
def inrange(v):
    if (v < 0):
        v=0
    if(v>255):
        v=255
    return v

def Wavelet():
    if root.op== 1:
        clearhist()
        root.im_out=gray(ImageTk.getimage(root.im_in)) #grayscaled
        g= root.im_out.load()
        wid,hei=root.im_out.size
        w= np.zeros((wid,hei))
        for N in range(0,3):#do wavelet 3 times
            wid= int(wid/2) # 256=512/2  128=512/2^2  64=512/2^3 
            hei=int(hei/2)
            for i in range(0,wid):  #width 256=512/2  128=512/2^2  64=512/2^3 
                for j in range(0,hei): #height 256=512/2  128=512/2^2  64=512/2^3
                    x= 2*i 
                    y= 2*j 
                    w[i][j]         =inrange( LL(g[x,y],g[x+1,y],g[x,y+1],g[x+1,y+1]) )
                    w[i+wid][j]     =inrange( HL(g[x,y],g[x+1,y],g[x,y+1],g[x+1,y+1]) )
                    w[i][j+hei]     =inrange( LH(g[x,y],g[x+1,y],g[x,y+1],g[x+1,y+1]) )
                    w[i+wid][j+hei] =inrange( HH(g[x,y],g[x+1,y],g[x,y+1],g[x+1,y+1]) )

            for i in range(0,int(root.im_size)):#width
                for j in range(0,int(root.im_size)):#height
                    g[i,j]=int(w[i][j])

        showresult()

def Equalization():
     if root.op== 1:
        clearhist()
        root.im_in=gray(ImageTk.getimage(root.im_in)) #grayscale input
        pixels_in= getpixelvalue(root.im_in)
        root.im_in=ImageTk.PhotoImage(root.im_in)
        root.im_out=gray(ImageTk.getimage(root.im_in)) #grayscaled
        pic= root.im_out.load()
        H= np.zeros(256)
        H_c=np.zeros(256)
        T=np.zeros(256)
        g_min=0

        for i in range(0, root.im_size):
            for j in range(0, root.im_size):
                H[pic[i,j]]=H[pic[i,j]]+1
       
        for g in range(0,256):
            if H[g]>0: 
                g_min==g
                break
        
        H_c[0]=H[0]
        for g in range(1,256):
            H_c[g]=H_c[g-1]+H[g] 
        H_min=H_c[g_min]

        for g in range(0,256):
            T[g]=int(255*(H_c[g] - H_min)/(root.im_size*root.im_size - H_min) + 0.5)

        
        for i in range(0, root.im_size):
            for j in range(0, root.im_size):
                pic[i,j]=int(T[pic[i,j]])
        pixels_out= getpixelvalue(root.im_out)
        histogram(pixels_in,"Grayscale Value",'in')
        histogram(pixels_out,"Grayscale Value",'out')
        showresult()


                
def LL(A,B,C,D):
    X=int(((A+B)+(C+D))/4+0.5)
    return X

def HL(A,B,C,D):
    X=int(((A-B)+(C-D))/4+0.5)
    return X

def LH(A,B,C,D):
    X=int(((A+B)-(C+D))/4+0.5)
    return X

def HH(A,B,C,D):
    X=int(((A-B)-(C-D))/4+0.5)
    return X




# #POPUP
# pop=tk.Tk()


#WINDOW
root = tk.Tk()
root.title('AIP_61047064S')
#root.array= np.array(256)
root.op=0
root.pop=0
root.scale=float(0)
root.im_size=512


#FRAME
frame_width = root.im_size
frame_height = root.im_size
button_width = 60
pad=5

#input image
frame1 = tk.Frame(root, width=frame_width, height=frame_height)
frame1.grid(row=0, column=0, sticky='ns',padx=5,pady=5)

#for buttons
frame2 = tk.Frame(root)
frame2.grid(row=0, column=2, sticky='ew',padx=5,pady=5)

#output image
frame3 = tk.Frame(root, width=frame_width, height=frame_height)
frame3.grid(row=0, column=1, sticky='ns',padx=5,pady=5)

frame4= tk.Frame(root)
frame4.grid(row=1,column=1, sticky='ns')

frame5= tk.Frame(root)
frame5.grid(row=1, column=0, sticky= 'ns')

heading_height=2

heading_In=tk.Label(frame1, text='Input Image', height = heading_height)
heading_In.grid(row=0, column=0, sticky='senw')

canvas_in = tk.Canvas(frame1, width = frame_width, height = frame_height) 
canvas_in.grid(row=1, column=0, sticky='nswe')

heading_1=tk.Label(frame2, text='HW2', height = 1)
heading_1.grid(row=0, column=0, sticky='w')
bt_1 = tk.Button(frame2, text='Grayscale Histogram', command=grayhistogram)
bt_1.grid(row=0, column=1,sticky="ew", pady=5)

heading_2=tk.Label(frame2, text='HW3', height = 1)
heading_2.grid(row=1, column=0, sticky='w')
bt_2 = tk.Button(frame2, text='Gaussian White Noise', command=GaussianPop)
bt_2.grid(row=1, column=1,sticky="ew", pady=5)

heading_3=tk.Label(frame2, text='HW4', height = 1)
heading_3.grid(row=2, column=0, sticky='w')
bt_3 = tk.Button(frame2, text='Wavelet Transform', command=Wavelet)
bt_3.grid(row=2, column=1,sticky="ew", pady=5)

heading_4=tk.Label(frame2, text='HW5', height = 1)
heading_4.grid(row=3, column=0, sticky='w')
bt_4 = tk.Button(frame2, text='Histogram Equalization', command=Equalization)
bt_4.grid(row=3, column=1,sticky="ew", pady=5)

heading_Out=tk.Label(frame3, text='Output Image', height = heading_height)
heading_Out.grid(row=0, column=0, sticky='nsew')

canvas_out= tk.Canvas(frame3, width = frame_width, height = frame_height)
canvas_out.grid(row=1, column=0, sticky='nswe')



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