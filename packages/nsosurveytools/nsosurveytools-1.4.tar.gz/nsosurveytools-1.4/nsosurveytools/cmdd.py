import tkinter as tk
import tkinter.ttk  as ttk



def GapLabel(window,size):
    GapLabel = tk.Label(window, text = '', font=('calibre', size, 'bold')).pack(side = 'top')

def progress(window):
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
     
    progressInfo = tk.Label(ProgressFrame, text='0 %') # Progress Label
     
    # Use the grid manager
    progressInfo.grid(row=0, column=0)
    progress_bar.grid(row=0, column=1)
    ProgressFrame.pack()



window = tk.Tk()
window.title("Program GUI")
window.geometry("300x150") 

progress(window)

window.mainloop()

import pandas  as pd
RandomTable = pd.read_pickle('RandomTable.pkl')

RandomTable.max().max()


