from tkinter import *

from PIL import Image, ImageTk


class Readcard(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        self.bind("<<show_frame>>", self.readnfc)

    def readnfc(self, event):
        from helper.Linux import ReadNFC
        value = ReadNFC.getvalue()

        ## if card is new and valid redirect to
        ''' 
        1. Query the card_auth to check for existence of new probe card
        2. if it exists tkinter.messagebox.yesorno if yes probe for new card if no redirect to home page
        
        '''
        ############# SQL commands to check for existence of the probe uid ############
        # should return a boolean value.

        command = self.controller.show_frame()


class WelcomePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def resize_image(event):
            global photo
            new_width = event.width
            new_height = event.height

            image = copy_of_image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(image)

            label.config(image=photo)
            label.image = photo  # avoid garbage collection

        copy_of_image = Image.open("/root/unitedbank.jpeg")
        photoimage = ImageTk.PhotoImage(copy_of_image)

        label = Label(self, image=photoimage)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.bind('<Configure>', resize_image)

        top_left_frame = Frame(self, relief='groove', borderwidth=2)
        top_left_frame.place(relx=1, rely=0.1, anchor=NE)
        center_frame = Frame(self, relief='raised', borderwidth=2)
        center_frame.place(relx=0.5, rely=0.75, anchor=CENTER)
        Button(top_left_frame, text='REGISTER', bg='blue', width=14, height=1,
               command=lambda: controller.show_frame(Readcard)).pack()
        Button(center_frame, text='ENTER', fg='white', bg='green', width=13, height=2,
               command=lambda: controller.show_frame(Readcard)).pack()


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (Readcard, WelcomePage):  # ,PageThree,PageFour):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(WelcomePage)

    # def show_frame(self, cont):
    #     frame = self.frames[cont]
    #     frame.tkraise()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.update()
        frame.event_generate("<<show_frame>>")


app = App()

app = mainloop()
