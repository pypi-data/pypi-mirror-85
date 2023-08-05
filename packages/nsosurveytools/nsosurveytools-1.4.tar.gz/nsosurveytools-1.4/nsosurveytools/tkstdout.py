
import tkinter as tk
import tkinter.ttk  as ttk
import sys
import time
'''
window = tk.Tk()
window.title("Program GUI")
window.geometry("300x150") 
'''
'''
def RunFunc():
    print(' Running...')
    for i in range(10):    
        Txtbox.insert(tk.END, str(i))
        Txtbox.update_idletasks()
        time.sleep(0.5)
        Txtbox.delete('1.0', tk.END)
    window.geometry("600x150")
        
def ClearFunc():
    print(' Clearing...')
    Txtbox.delete('1.0', tk.END)
        

button = tk.Button( text="Run", command=RunFunc, width=10, height=2, bg="blue", fg="yellow" ).pack()
clrbutton = tk.Button( text="Clear", command=ClearFunc, width=10, height=2, bg="blue", fg="yellow" ).pack()
#buttonExit = tk.Button(root, text = "Exit",  command = window.destroy)  


Txtbox = tk.Text(window, height = 10, width = 20)


tblabel = tk.Label(window, text = "Running Status") 
tblabel.config(font = ("Courier", 10)) 


tblabel.pack()
Txtbox.pack()



window.mainloop()

'''
class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        toolbar = tk.Frame(self)
        toolbar.pack(side="top", fill="x")
        b1 = tk.Button(self, text="print to stdout", command=self.print_stdout)
        b2 = tk.Button(self, text="print to stderr", command=self.print_stderr)
        b1.pack(in_=toolbar, side="left")
        b2.pack(in_=toolbar, side="left")
        self.text = tk.Text(self, wrap="word")
        self.text.pack(side="top", fill="both", expand=True)
        self.text.tag_configure("stderr", foreground="#b22222")

        sys.stdout = TextRedirector(self.text, "stdout")
        sys.stderr = TextRedirector(self.text, "stderr")

    def print_stdout(self):
        #Illustrate that using 'print' writes to stdout
        print("this is stdout")

    def print_stderr(self):
        #Illustrate that we can write directly to stderr
        sys.stderr.write("this is stderr\n")

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")

app = ExampleApp()
app.mainloop()
