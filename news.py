import io
import PIL
import webbrowser
from cProfile import label
from urllib.request import urlopen
from io import BytesIO
from PIL import Image,ImageTk
import requests
from tkinter import *
class NewsApp:
    def __init__(self):
        #fetch data from API: done using python module named requests
        self.data = requests.get(
            'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=eabf90a1242e41f4b43e1fb9aefeb987').json()
        #initial GUI load: we use tkinter
        self.loadgui()

        #load the 1st news item
        self.load_news_item(0)

    def loadgui(self):
        self.root = Tk()
        self.root.geometry('350x600')
        self.root.resizable(False, False)
        self.root.configure(background='black')
        self.root.title('News App')

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()
    def load_news_item(self, index):

        #clear the screen for the new news item
        self.clear()

        #code for displaying image
        try:
            img_url=self.data['articles'][index]['urlToImage']
            raw_data=urlopen(img_url).read()
            im=PIL.Image.open(io.BytesIO(raw_data)).resize((350,250))
            photo = ImageTk.PhotoImage(im)
        except: #if image fails to load
            img_url = 'https://images.wondershare.com/repairit/aticle/2021/07/resolve-images-not-showing-problem-1.jpg'
            raw_data = urlopen(img_url).read()
            im = PIL.Image.open(io.BytesIO(raw_data)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)
        label = Label(self.root, image=photo)
        label.pack()
        #code to display heading
        heading = Label(self.root,text=self.data['articles'][index]['title'],bg='black',fg='white',
                        wraplength=350,justify='center')
        heading.pack(pady=(10,20))
        heading.config(font=('verdana',15))

        #code to display details
        details = Label(self.root, text=self.data['articles'][index]['description'], bg='black', fg='white',
                        wraplength=350, justify='center')
        details.pack(pady=(2, 20))
        details.config(font=('verdana', 12))

        #code for making buttons
        frame=Frame(self.root, bg='black')
        frame.pack(expand=True, fill='both')

        if index != 0:
            prev=Button(frame,text='Prev',width=16,height=3,command=lambda: self.load_news_item(index-1))
            prev.pack(side=LEFT)

        read = Button(frame, text='Read More', width=16, height=3,command=lambda: webbrowser.open(self.data['articles'][index]['url']))
        read.pack(side=LEFT)

        if index != len(self.data['articles']) - 1:
            next = Button(frame, text='Next', width=16, height=3,command=lambda: self.load_news_item(index+1))
            next.pack(side=LEFT)

        self.root.mainloop()

    def open_link(self,url):
        webbrowser.open(url)
obj = NewsApp()