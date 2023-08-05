
import tkinter as tk
import tkinter.ttk  as ttk
import time

window = tk.Tk()
window.title("Agriculture Survey")
window.geometry("400x350") 

separator = ttk.Separator(window, orient='horizontal')
inputFrame = tk.Frame(window)

#radVal = tk.StringVar(window, "1")  # Tkinter string variable 
radVal = tk.StringVar(window, '0')  # Tkinter string variable 
prg = tk.IntVar(window, 1)
singleVar=tk.StringVar() 
stratumVar=tk.StringVar() 
osVar=tk.StringVar() 

programs = {" Input Excel File   " : "1", 
            " Selection          " : "2", 
            " Check SubDivisions " : "3"  } 


def GapLabel(window,size):
    GapLabel = tk.Label(window, text = '', font=('calibre', size, 'bold')).pack(side = 'top')

def RunProg():
    currentProgram = list(programs.keys())[int(radVal.get())-1]
    print('Running ...',list(programs.keys())[int(radVal.get())-1])
    statusLabel['text'] = 'Running... '+currentProgram
    
    cwindow = tk.Tk()
    cwindow.title("Agriculture Survey : "+currentProgram)
    cwindow.geometry("550x650")  
    
    ### Add Progress bar
    Progressbar(cwindow, barname='Loading...', UpInterval=50)
    ### Add Text Box to show Program Status
    Txtbox = tk.Text(cwindow,  width = 400, height = 500)
    Txtbox.pack()
  
    cwindow.mainloop()


    
def Progressbar(window, barname='', UpInterval=5):
    global progressInfo
    GapLabel(window,10)
    style = ttk.Style(window)
    ProgressFrame = tk.Frame(window)
    style.layout('text.Horizontal.TProgressbar',
                 [('Horizontal.Progressbar.trough',
                   {'children': [('Horizontal.Progressbar.pbar',
                                  {'side': 'left', 'sticky': 'ns'})],
                    'sticky': 'nswe'}),
                  ('Horizontal.Progressbar.label', {'sticky': ''})])
                  # , lightcolor=None, bordercolo=None, darkcolor=None
    style.configure('text.Horizontal.TProgressbar', text='0 %')
    
    progress_bar = ttk.Progressbar(ProgressFrame, style='text.Horizontal.TProgressbar', orient="horizontal",mode="determinate", maximum=100, value=0)
     
    label_info = tk.Label(ProgressFrame, text=barname) # Progress Label
     
    # Use the grid manager
    label_info.grid(row=0, column=0)
    progress_bar.grid(row=0, column=1)
    ProgressFrame.pack()
    # Necessary, as the master object needs to draw the progressbar widget
    # Otherwise, it will not be visible on the screen
    window.update()
     
    progress_bar['value'] = 0
    window.update()
     
    while progress_bar['value'] < 100:
        progress_bar['value'] += UpInterval
        style.configure('text.Horizontal.TProgressbar', text='{:g} %'.format(progress_bar['value']))
        label_info['text']=progress_bar['value']
        
        
        window.update() # Keep updating the master object to redraw the progress bar
        time.sleep(0.5)    
    

def radioSelection():
    selection = "You selected the option " + str(radVal.get())
    currentProgram = list(programs.keys())[int(radVal.get())-1]
    print('Selected:',radVal.get(),currentProgram)
    statusLabel['text'] = defaultLabel+currentProgram
    enterData()


def enterData():
    global inputFrame
    if int(radVal.get()):
        print('Removing Frame...')
        inputFrame.destroy()
        #inputFrame.grid_forget()
    inputFrame = tk.Frame(window)
    name_entry_row=0; name_entry_col=1 # Excel FileName
    if int(radVal.get()) < 3:
        mainlabel = 'Excel Filename: '
        name_entry = tk.Entry(inputFrame, width=25, textvariable=singleVar,font=('calibre',10,'normal'))
       
    else:
        mainlabel = 'Enter SubDivisions of a Plot: ' 
        name_entry = tk.Text(inputFrame, height = 6, width = 10)
        name_entry_row=1; name_entry_col=0 # Excel FileName
        
    name_label = tk.Label(inputFrame, text = mainlabel, font=('calibre', 10, 'bold'))    
    name_label.grid(row=0,column=0) 
    name_entry.grid(row=name_entry_row,column=name_entry_col)
    
    ## Entry for Stratum, OS
    if int(radVal.get()) < 3 :
        stratum_label = tk.Label(inputFrame, text = 'Enter Stratum: ', font=('calibre', 10, 'bold'))   
        stratum_entry = tk.Entry(inputFrame, width=10, textvariable=stratumVar,font=('calibre',10,'normal')) 
        os_label = tk.Label(inputFrame, text = 'Order of Selection: ', font=('calibre', 10, 'bold'))   
        os_entry = tk.Entry(inputFrame,  width=10, textvariable=osVar,font=('calibre',10,'normal')) 

        stratum_label.grid(row=1,column=0) 
        stratum_entry.grid(row=1,column=1)
        os_label.grid(row=2,column=0) 
        os_entry.grid(row=2,column=1)
    inputFrame.pack()




defaultLabel='Selected : '
programSelection=tk.StringVar()
programSelection.set(defaultLabel)
#label = tk.Label(window, text="Selected Program : ", textvariable=programSelection).pack(side = 'top',  ipady = 5)

GapLabel(window,4) # After Radio Button
statusLabel = tk.Label(window, text = defaultLabel+list(programs.keys())[0])
statusLabel.pack(side = 'top',  ipady = 5)
#label1.place(x=0, y=0)




style = ttk.Style(window) 
style.configure("TRadiobutton", # background = "light green",  foreground = "red"
                font = ("arial", 11, "bold")) 
## Radio Buttons
RadioFrame = tk.Frame(window)
for (name, value) in programs.items(): 
    #tk.Radiobutton(window, text = name, variable = programSel, value = value).pack() 
    ttk.Radiobutton(RadioFrame, command=radioSelection, text = name, variable = radVal, value = value).pack(side = 'top', anchor = 'w',  ipady = 5)
RadioFrame.pack()    

## Line Separator
separator.pack(side='top', fill='x')



## Run Button
runButton = tk.Button( text="START", command=RunProg, width=10, height=1, bg="#80DEEA", fg="black", font=('calibre', 10, 'bold') )
runButton.pack(side = 'top', ipadx = 5,  ipady = 10)
runButton.place(bordermode=tk.OUTSIDE,  x=150, y=305 )


GapLabel(window,10)
enterData()
window.mainloop()


#entry = tk.Entry(fg="yellow", bg="blue", width=50)

