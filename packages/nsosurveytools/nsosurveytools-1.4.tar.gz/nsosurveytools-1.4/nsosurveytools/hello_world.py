import tkinter as tk
import tkinter.ttk  as ttk
import sys



class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
        

def RunProg( ):
    print("Hello World")
    
    


window = tk.Tk()
window.title("Agriculture Survey")
window.geometry("400x350")

btext = tk.Text(window, width=20, height=10)
btext.pack()
btext.tag_configure("stdout", foreground="#b22222")


runButton = tk.Button( text="START", command=RunProg, width=10, height=1, bg="#80DEEA", fg="black", font=('calibre', 10, 'bold') ).pack()

sys.stdout = TextRedirector(btext, "stdout")

window.mainloop()

