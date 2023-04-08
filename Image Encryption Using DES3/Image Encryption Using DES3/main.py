import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from Crypto.Cipher import DES3
from Crypto import Random
from PIL import ImageTk,Image

window = Tk()
window.geometry("800x600")
window.title("Image Encryption & Decryption Tool")

def selectfile():
    selectfile.file = filedialog.askopenfilename(initialdir=os.getcwd(),title='select file',filetypes=(("JPG File","*.jpeg"),("PNG File","*.png"),("ALL File","*.*")))
    img = ImageTk.PhotoImage(Image.open(selectfile.file))
    lbl.configure(image=img)
    lbl.image = img



def encrypt():

    filename=selectfile.file
    key = e_val.get()
    er1='Enter Valid key'
    if (len(key)) != 16:
        t1.delete('1.0',END)
        t1.insert(END,er1)
    else:
        success='Encryption Successful\nFile Location:'
        t1.delete('1.0',END)
        t1.insert(END,success)

        chunksize = 64 * 1024
        OutFile = filename[:-5] + "(encypted).jpeg"
        filesize = str(os.path.getsize(filename)).zfill(8)
        IV = Random.new().read(8)
        t1.insert(END,OutFile)
        encryptor = DES3.new(key, DES3.MODE_CBC, IV)
        with open(filename, 'rb') as infile:

            with open(OutFile, 'wb') as outfile:
                outfile.write(filesize.encode('utf-8'))
                outfile.write(IV)

                while True:
                    chunk = infile.read(chunksize)

                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 8 != 0:
                        chunk += b' ' * (8 - (len(chunk) % 8))
                    outfile.write(encryptor.encrypt(chunk))


def decrypt():
    file = filedialog.askopenfile(mode='r')
    if file is not None:
        filename = file.name
        key = e_val.get()
        er2 = 'Enter Valid key'
        if (len(key)) != 16:
            t1.delete('1.0', END)
            t1.insert(END, er2)

        else:
            success1 = 'Decryption Successful\nFile Location:'
            t1.delete('1.0', END)
            t1.insert(END, success1)

            chunksize = 64 * 1024

            OutFile = filename[:-15] + "(decrypted).jpeg"

            t1.insert(END,OutFile)
            with open(filename,'rb') as infile:
                filesize = int(infile.read(8))
                IV = infile.read(8)

                decryptor = DES3.new(key, DES3.MODE_CBC, IV)

                with open(OutFile,'wb') as outfile:
                    while True:
                        chunk = infile.read(chunksize)

                        if len(chunk) == 0:
                            break
                        outfile.write(decryptor.decrypt(chunk))
                    outfile.truncate(filesize)


header=Label(window,text='IMAGE ENCRYPTION TOOL',bg='blue',fg='white',height=2)
header.pack(fill=X)

intro = Label(window,text="Note : Select an Image for Encryption \nDon't select Image for Decryption \nclick on Unlock Directly",fg='grey')
intro.place(x=370,y=50)

select_btn= PhotoImage(file='select.png')
select_label = Label(image=select_btn)
b1=Button(window, image=select_btn,command=selectfile)
b1.place(x=50,y=50)

quit_btn= PhotoImage(file='close.png')
quit_label = Label(image=quit_btn)
b4=Button(window, image=quit_btn,command=window.quit)
b4.place(x=700,y=520)

key= PhotoImage(file='key.png')
key_label = Label(image=key)
key_label.place(x=350,y=200)

label2 = Label(window, text='16 digit Alphanumeric Key',fg='red')
label2.place(x=580,y=200)

e_val = StringVar()
e1 = Entry(window, textvariable=e_val)
e1.place(x=380,y=200)

lock_btn= PhotoImage(file='lock.png')
lock_label = Label(image=lock_btn)
b2=Button(window, image=lock_btn, command=encrypt, border=0)
b2.place(x=480,y=320)


unlock_btn= PhotoImage(file='unlock.png')
key_label = Label(image=unlock_btn)
b4=Button(window, image=unlock_btn, command=decrypt, border=50)
b4.place(x=580,y=320)


t1 = Text(window,fg='red',width=60,height=4)
t1.place(x=300,y=400)

lbl = Label(window)
lbl.place(x=150,y=100)


window.mainloop()
