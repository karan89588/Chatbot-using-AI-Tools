import tkinter as tk
from predict_response import get_response

window=tk.Tk()
window.title('ChatBot')
window.resizable(0,0)
window.geometry('500x600')


def on_enter(event):
    send()

def clear():
    lab3.configure(state='normal')
    lab3.delete("1.0",tk.END)
    lab3.configure(cursor='arrow',state='disable')


lab1=tk.Label(window,bg='lightblue',text='Welcome',font='System 14')
lab1.place(relwidth=1,relheight=0.08,rely=0.009)

lab2=tk.Label(window,bg='grey')
lab2.place(relwidth=1,relheight=0.008,rely=0.09)

lab3=tk.Text(window,bg='lightgreen')
lab3.place(relwidth=1,relheight=0.8,rely=0.1)
lab3.configure(cursor='arrow',state='disable')

scroll=tk.Scrollbar(lab3)
scroll.place(relheight=1,relx=0.97)
scroll.configure(command=lab3.yview)

lab4=tk.Label(window)
lab4.place(relwidth=1,relheight=0.1,rely=0.9)

input=tk.Entry(lab4,font='System 11',bg='lightpink')
input.insert(0,'Enter your query here.')
input.place(relwidth=0.7,relheight=0.8)
input.bind('<Return>',on_enter)

quit=['quit','exit','bye','byebye','good night','leave now']

def send():
    if input.get()=='':
        return
    if input.get().lower() in quit:
        window.quit() 
    lab3.configure(state='normal')
    lab3.insert(tk.END,'You >>> '+input.get()+'\n')
    lab3.insert(tk.END,'Merry >>> '+get_response(input.get())+'\n\n')
    lab3.configure(cursor='arrow',state='disable')
    input.delete(0,tk.END)
    lab3.see(tk.END)


btn1=tk.Button(lab4,bg='grey',text='Send',command=send)
btn1.place(relx=0.72,relheight=0.8,relwidth=0.1)

btn2=tk.Button(lab4,text='Clear',bg='grey',command=clear)
btn2.place(relheight=0.8,relwidth=0.1,relx=0.85)



if __name__=='__main__':
    window.mainloop()