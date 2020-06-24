import locale
import platform
import sqlite3
import time
import tkinter
import tkinter.messagebox
from sqlite3 import Error
from tkinter import *

from PIL import Image, ImageTk, ImageSequence


# from helper import checknfcuidexist


class Register_new_user(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        self.bind("<<show_frame>>", self.checkexist)

        def resize_image(event):
            global photo
            new_width = event.width
            new_height = event.height

            image = copy_of_image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(image)

            label.config(image=photo)
            label.image = photo  # avoid garbage collection

        copy_of_image = Image.open("resource_images/united_bank.png")
        photoimage = ImageTk.PhotoImage(copy_of_image)

        label = Label(self, image=photoimage)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.bind('<Configure>', resize_image)

        top_left_frame = Frame(self, relief='groove', borderwidth=2)
        top_left_frame.place(relx=1, rely=0.1, anchor=NE)
        center_frame = Frame(self, relief='raised', borderwidth=2)
        center_frame.place(relx=0.5, rely=0.75, anchor=CENTER)
        Button(top_left_frame, text='HomeMenu', bg='grey', width=14, height=1,
               command=lambda: controller.show_frame(WelcomePage)).pack()

        #############3 Function to scan new card to check if it exists

        Button(center_frame, text='RETRY', fg='white', bg='green', width=13, height=2,
               command=lambda: controller.show_frame(Register_new_user)).pack()

    def checkexist(self, event):
        import helper.checknfcuidexist
        status = helper.checknfcuidexist.get_status()
        print(f"Check if entry exists or not {status}")

        if status:
            ####################### load a form to the full names then face rec register finally a pin for the card
            toplvl = Toplevel()
            toplvl.title("Register New user")
            toplvl.iconbitmap('register.ico')
            toplvl.geometry('600x500')
            myButton = Button(toplvl, text="clieck me", fg='white', bg='black', width=12, height=2, relief=RIDGE)
            myButton.pack()
            lblFn = Label(toplvl, text="First_Name").pack()
            fnentry = Entry(toplvl, variable=first_name).pack()

        '''
           if return true do:
               1. start an sqlite transaction that only commits after all needed details have been saved.
                    a. full names be entered address and contact number
                    b. 
               2. redirect to a page that contains a form that will require filling the columns of the users table 
           else:
               1. redirect to the nfc scan page after notifying the user that the nfc card already exists or is invalid.    
           '''


class SeaofBTCapp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (
                WelcomePage, InsertATM, InsertATM2, FaceAuth, InputPin, MainMenu, Withdraw, WithdrawConfirm, Deposit,
                DepositConfirm,
                BalanceQuery, Register_new_user):  # ,PageThree,PageFour):
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

        copy_of_image = Image.open("resource_images/united_bank.png")
        photoimage = ImageTk.PhotoImage(copy_of_image)

        label = Label(self, image=photoimage)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.bind('<Configure>', resize_image)

        top_left_frame = Frame(self, relief='groove', borderwidth=2)
        top_left_frame.place(relx=1, rely=0.1, anchor=NE)
        center_frame = Frame(self, relief='raised', borderwidth=2)
        center_frame.place(relx=0.5, rely=0.75, anchor=CENTER)
        Button(top_left_frame, text='REGISTER', bg='grey', width=14, height=1,
               command=lambda: controller.show_frame(Register_new_user)).pack()
        Button(center_frame, text='ENTER', fg='white', bg='green', width=13, height=2,
               command=lambda: controller.show_frame(FaceAuth)).pack()


################################################# Start of insert card Animation#########


class InsertATM(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        self.bind("<<show_frame>>", self.onShowFrame)

        def animate(self, counter):
            canvas.itemconfig(image, image=sequence[counter])
            parent.after(250, lambda: animate(self, (counter + 1) % len(sequence)))

        canvas = Canvas(self, width=600, height=500)
        canvas.pack()
        sequence = [ImageTk.PhotoImage(img)
                    for img in ImageSequence.Iterator(
                Image.open(r'resource_images/atmswipe.gif')
            )]
        image = canvas.create_image(200, 200, image=sequence[0])
        animate(self, 1)
        label = Label(self, text="Please Swipe Atm Card to Continue...", font='times 24 bold').pack(pady=10, padx=10)

        # ############################ Run system commands to initialize and execute nfc program to read the card
        # ###################33#

        # 1 Find a code that skips the first init and does not execute the loop program
        # 2 When loop function completes and some content is saved on local disk automatically redirect to the next page

    def onShowFrame(self, event):
        if (platform.system() == "Linux"):
            import helper.Linux.FileReader
            Account_uid_compare = helper.Linux.FileReader.reader()

            # save the credentials to cardswipelogger.db for logging
            import helper.db_models.save_log_card_to_db as saver
            saver.sqltable(Account_uid_compare)

            # should save the value to memory sqlitedb for retrieval or save to local
            # file that will serve as a session.
            # time.sleep(3)
        elif (platform.system() == "Windows"):
            #  TODO: employ use of multiprocessing to ensure # Cant seem to find a work around with tkinter !!
            # the tkinter window does not hang when serial module is called

            # Read the arduino nfc card from COM and save to the file cheserem.key
            import helper.Windows.ArduinoSerialCom

            # the reader parses the cheserem.key file and extracts the main key removing unnecessary characters
            import helper.Windows.FileReader
            card_creds = helper.Windows.FileReader.format_key()
            # print(card_creds)

            # save the credentials to cardswipelogger.db for logging
            import helper.db_models.save_log_card_to_db as saver
            saver.sqltable(card_creds)
            # time.sleep(2)
            import Authenticator.cardexist as cardAuth
            status = cardAuth.get_status(card_creds)
            print(f"The results came in as {status}")

            if status:
                # messagebox = (self,)

                tkinter.messagebox.showinfo("Success", "AUTH CARD SUCCESS")
                time.sleep(1)

                command = self.controller.show_frame(FaceAuth)
            else:
                # TODO: if there is an error i need the system to play a sound for both a success and an error tone
                response = tkinter.messagebox.askyesno("Authentication",
                                                       "AUTH CARD INVALID or EXPIRED!!!! You have 1 tries left !  Do "
                                                       "you wish to RETRY ?")
                if response == 1:
                    # self.onShowFrame(event)
                    time.sleep(2)
                    command = self.controller.show_frame(InsertATM2)




                else:
                    tkinter.messagebox.showinfo("EXIT", "Thank You for Using The UnitedBank")
                    # command = self.controller.show_frame(WelcomePage)
                    self.quit()



        else:
            print("Unsupported Platform !!!!!!!!!!")

        # TODO: should show a tkinter message that if yes is selected it starts reading card
        # TODO: format the ArduinoSerialCom code to allow for true or false entry
        # TODO: The code should time out after 10 seconds of inactivity and resume on userinput from
        # a prompt

        ############### probs #########33
        # 1 ensure animation automatically resizes to fill whole page


class InsertATM2(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        self.bind("<<show_frame>>", self.onShowFrame2)

        def animate(self, counter):
            canvas.itemconfig(image, image=sequence[counter])
            parent.after(250, lambda: animate(self, (counter + 1) % len(sequence)))

        canvas = Canvas(self, width=600, height=500)
        canvas.pack()
        sequence = [ImageTk.PhotoImage(img)
                    for img in ImageSequence.Iterator(
                Image.open(r'resource_images/atmswipe.gif')
            )]
        image = canvas.create_image(200, 200, image=sequence[0])
        animate(self, 1)
        label = Label(self, text="ON LAST TRY...",background="red", font='times 24 bold').pack(pady=10, padx=10)

        # ############################ Run system commands to initialize and execute nfc program to read the card
        # ###################33#

        # 1 Find a code that skips the first init and does not execute the loop program
        # 2 When loop function completes and some content is saved on local disk automatically redirect to the next page

    def onShowFrame2(self, event):
        if (platform.system() == "Linux"):
            import helper.Linux.FileReader
            Account_uid_compare = helper.Linux.FileReader.reader()

            # save the credentials to cardswipelogger.db for logging
            import helper.db_models.save_log_card_to_db as saver
            saver.sqltable(Account_uid_compare)

            # should save the value to memory sqlitedb for retrieval or save to local
            # file that will serve as a session.
            # time.sleep(3)
        elif (platform.system() == "Windows"):
            #  TODO: employ use of multiprocessing to ensure # Cant seem to find a work around with tkinter !!
            # the tkinter window does not hang when serial module is called

            # Read the arduino nfc card from COM and save to the file cheserem.key
            time.sleep(3)
            print("Initializing the RFID READER")
            import helper.Windows.ArduinoSerialCom2

            # the reader parses the cheserem.key file and extracts the main key removing unnecessary characters
            import helper.Windows.FileReader as read_format
            card_creds2 = read_format.format_key()
            # print(card_creds)

            # save the credentials to cardswipelogger.db for logging
            import helper.db_models.save_log_card_to_db as saver
            saver.sqltable(card_creds2)
            # time.sleep(2)
            import Authenticator.cardexist as cardAuth
            status2 = cardAuth.get_status(card_creds2)
            print(f"The results came in as {status2}")

            if status2:
                # messagebox = (self,)

                tkinter.messagebox.showinfo("Success", "AUTH CARD SUCCESS")
                time.sleep(1)

                command = self.controller.show_frame(FaceAuth)
            else:
                # TODO: if there is an error i need the system to play a sound for both a success and an error tone
                tkinter.messagebox.showerror("Authentication",
                                             "AUTH CARD INVALID or EXPIRED!!!! You have 0 tries left !  Program "
                                             "Exit ?")
                self.quit()


        else:
            print("Unsupported Platform !!!!!!!!!!")

        # TODO: The code should time out after 10 seconds of inactivity and resume on userinput from
        # a prompt

        ############### probs #########33
        # 1 ensure animation automatically resizes to fill whole page

class FaceAuth(Frame):
    def __init__(self, parent, controller):
        self.controller = controller

        Frame.__init__(self, parent)
        self.bind("<<show_frame>>", self.facerec)

        def animates(self, counters):
            canvas.itemconfig(image, image=sequence[counters])
            parent.after(250, lambda: animates(self, (counters + 1) % len(sequence)))

        canvas = Canvas(self, width=400, height=400)
        canvas.pack()
        sequence = [ImageTk.PhotoImage(img)
                    for img in ImageSequence.Iterator(
                Image.open(r'resource_images/face_rec.gif')
            )]
        image = canvas.create_image(200, 200, image=sequence[0])
        animates(self, 1)
        label = Label(self, text="Position Camera Face Upward",background='green', font='times 15 bold').pack(pady=10, padx=10)

    def facerec(self, event):
        # This function performs a post request much like a form submit to a website
        # the website checks the two creds i.e. account_number from rfid secton and the user id.
        # To check for success of authentication there's need to query
        # for Authentication_user.get_Status()
        #TODO: Tkinter code sample to pass values to the successor class
        '''
        1. Create a function that is able to link to the previous predecessor
        function to retrieve the userid as assigned to the auth card
        2. import face class and pass in the arguments of the
        :param event:
        :return:
        '''
        import faces
        account = "b32344"
        id = 1
        obj = faces.Authenticate_User(account,id)
        before = obj.get__status()
        #After calling the below method once it return true it needs to exit
        obj.opencv()
        after_auth = obj.get__status()

        condition = faces.getname()
        # alobj =
        print("hello world " + str(condition))
        # should save the value to memory sqlitedb for retrieval or save to local
        # file that will serve as a session.
        if condition:
            command = self.controller.show_frame(InputPin)
        # else:
        #
        time.sleep(3)



class InputPin(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="PIN INPUT", font='times 15 bold')
        label.pack(pady=10, padx=10)

        # print("Check for incoming pin" + str(validation_pin))
        # self.ID_number = National_identity_number

        entry_1 = None
        count = 1
        passwd = StringVar

        def enternumber(x):
            global entry_1
            setval = StringVar()
            setval = str(x)
            print(setval)
            entry_1.insert(END, setval)

        def killwindow():

            command = controller.show_frame(WelcomePage)

        # #############  Function to parse for only numerical input
        # ################################################################################3
        def validate(input):
            if input.isdigit():
                return True
            elif input == "":
                return True
            else:
                return False

        def main():

            global entry_1
            global password

            password = StringVar()

            # global counter
            # counter = 0

            #############################     Work Here ###################

            def loginauth():
                #TODO: This section should check that faceauth and rfid have been passed
                #  thruogh checking the authentication database in memory that sets a boolean
                # value when auth is successful i.e rfid = true facerec=true
                # if either is false this page does not load rather it throws an error
                # and returns user to the Welcome page This is a custom implementation of
                # a session cookie.
                # In that note need to research on how session cookies are implemented
                # in web technologies. To better improve on this proj {Security}

                P = password.get()

                # pinobj = InsertATM(parent, controller)
                # compare = pinobj.return_pin()
                compare = 2323
                print(f"Within loginauth the gotten pin is {compare}")

                if P == str(compare):

                    ###############################333333333333
                    global National_id
                    # National_id = pinobj.return_id()
                    National_id = 34176984

                    print(f"Within pin compare if statement id is {National_id}")

                    # below sql query pre-saves the preset
                    # name/s retrieved from the client table in test.db through use of the National_id

                    def sqlcon():
                        try:
                            conn = sqlite3.connect('test.db')
                            return conn
                        except Error:
                            print('Connection to database failed ' + str(Error))

                    def matching_account(con):
                        mycursor = con.cursor()
                        query = "SELECT Sur_name,First_name from client WHERE National_id = " + str(National_id)
                        status = mycursor.execute(query)
                        if status:
                            global surname
                            global first_name
                            validate = mycursor.fetchone()
                            # print(validate[0])
                            surname = validate[0]
                            first_name = validate[1]

                            print(f"login debug to check retrieval of surname {surname}  and firstname {first_name} ")

                            # # Research on how to catch database errors such assurname = validate[0] TypeError:
                            # 'NoneType' object is not subscriptable

                        # else:
                        #
                        #     tkinter.messagebox.showerror("Error", "ATM Expired or Invalid ")
                        #
                        #     # Should redirect to the Welcome page
                        #
                        #     command = controller.show_frame(WelcomePage)

                    test = sqlcon()
                    matching_account(test)

                    #####     Username  ##############
                    print("surname = " + surname + " first name " + first_name)

                    #### Debug statement

                    # To be more user friendly display (' Welcome #username')

                    # Furthermore on the top left display the username
                    tkinter.messagebox.showinfo("Login", "Welcome " + surname + " " + first_name)
                    command = controller.show_frame(MainMenu)
                    password.set('')
                    # and name == 'cheseremtitus'):
                    # command = lambda: controller.show_frame(MainMenu)
                    # Redirect to FACE RECOGNITION PAGE WITHOUT BUTTON CLICK



                else:

                    print("pin incorrect")

                    response = tkinter.messagebox.askyesno("Authentication",
                                                           "PIN Incorrect!!!! You have 2  tries left !  Do you wish to continue ?")

                    if response == 1:  # and count_tries > 0:
                        # tries_counter()
                        # total_tries = count_tries
                        # print(total_tries)
                        password.set("")
                        entry_1.focus()
                    else:
                        tkinter.messagebox.showinfo("EXIT", "Thank You for Using BankAir")
                        command = controller.show_frame(WelcomePage)

            def cleartxtfield():
                global password
                new = ""
                password.set(new)

            entry_1 = Entry(self, textvariable=password, width=64, show='*')
            entry_1.place(x=200, y=100)
            entry_1.focus()

            reg = self.register(validate)
            entry_1.config(validate="key", validatecommand=(reg, '%P'))

            def getcreds():
                # check if four digit entered and is not empty
                global passwd
                passwd = password.get()
                print(f"The Credentials are {passwd}")

            def funcbackspace():
                length = len(entry_1.get())
                entry_1.delete(length - 1, 'end')

            cancel = Button(self, width=8, height=3, text="Cancel", bg="red", fg="black", command=killwindow)
            cancel.place(x=220, y=150)
            backspace = Button(self, width=8, height=3, text="Backspace", bg="red", fg="black", command=funcbackspace)
            backspace.place(x=500, y=150)

            # ----number Buttons------
            btn_numbers = []
            for i in range(10):
                btn_numbers.append(
                    Button(self, width=8, height=3, text=str(i), bd=6, command=lambda x=i: enternumber(x)))
            btn_text = 1
            for i in range(0, 3):
                for j in range(0, 3):
                    btn_numbers[btn_text].place(x=220 + j * 140, y=250 + i * 100)
                    btn_text += 1

            btn_zero = Button(self, width=15, height=2, text='0', bd=5, command=lambda x=0: enternumber(x))
            btn_zero.place(x=330, y=550)
            clear = Button(self, text="Clear", bg="green", fg="white", width=8, height=3, command=cleartxtfield)
            clear.place(x=220, y=550)
            okbtn = Button(self, text="Enter", bg="green", fg="black", width=8, height=3,
                           command=loginauth)
            okbtn.place(x=500, y=550)

        main()


class MainMenu(Frame):

    #############3 IN Main menu following requirements are necessary

    #   1. client table UserID to get national ID, account_no and names
    #   2. input_pin Account_status.account_no to get balance for check status page
    #   3. face_rec Account_changes.change_id to get amount, changed_at, flag

    # def return_Cuid(self):
    #     cuidobj = InsertATM.return_id(self)
    #     print(f'check for cuidnationalid {cuidobj}')
    #
    #     # pinobj = InsertATM(parent, controller)
    #     # compare = pinobj.return_pin()
    # def sqlcon():
    #     try:
    #         conn = sqlite3.connect('test.db')
    #         return conn
    #     except Error:
    #         print('Connection to database failed ' + str(Error))

    # def retrieve_account_status(con):
    #     global N_id
    #     idobj = InsertATM.return_id(InsertATM)
    #     N_id = idobj
    #     print(f"debug for national  id gives {idobj}")
    #     mycursor = con.cursor()
    #     query = "SELECT UserID from client where National_id=" + str(N_id)
    #     status = mycursor.execute(query)
    #
    #     if status:
    #         global Cuid
    #         validate = mycursor.fetchone()
    #         # print(validate[0])
    #         Cuid = validate[0]
    #
    #         print(f"login debug to check retrieval of userid for client which is  {Cuid}")
    #
    # test = sqlcon()
    # retrieve_account_status(test)
    #

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        frame = Frame(self, relief='raised', borderwidth=2)
        frame.pack(fill=BOTH, expand=YES)
        frame.pack_propagate(False)

        ######### Returns the Current user ID and populates the relevant
        ######### information onto the dashboard

        # Cuidobj = InputPin(parent,controller)
        # CUID = Cuidobj.return_Cuid()

        #################3 fUNCTION TO RETRIEVE ACCOUNT_NO FROM ATM SWIPE CLASS ########

        # insert_card_obj = InsertATM(parent, controller)
        # account_no_main = insert_card_obj.return_account_no()
        account_no_main = 2222
        # print(f"Within Main Menu the gotten account_no as : {account_no_main}")

        ############## Function to return values from the client to populate the Home page ######################3

        # def sqlcon():
        #     try:
        #         conn = sqlite3.connect('test.db')
        #         return conn
        #     except Error:
        #         print('Connection to database failed ' + str(Error))
        #
        # def retrieve_client_details(con):
        #     global N_id
        #     global User_ID
        #     global First_Name
        #     global Sur_Name
        #     idobj = InsertATM.return_id(InsertATM)
        #     N_id = idobj
        #     print(f"debug for national  id gives {idobj}")
        #     mycursor = con.cursor()
        #     query = "SELECT UserID,Sur_name, First_name from client where National_id=" + str(N_id)
        #     status = mycursor.execute(query)
        #
        #     if status:
        #         global Cuid
        #         validate = mycursor.fetchall()
        #         # print(validate[0])
        #         Cuid = validate[0]
        #
        #         print(f"login debug to check retrieval of userid for client which is  {Cuid}")
        #
        # test = sqlcon()
        # retrieve_client_details(test)
        ################################################### END of Function retrieve from Client table ######################

        username = Label(frame, width=51, text="username", font=("arial", 13, "bold"))
        username.place(x=300, y=22)
        user_id = Label(frame, width=15, height=3, text=f" ACC: {account_no_main}", font=("arial", 12, "bold"))
        user_id.place(x=277, y=22)

        mainLabel = Label(frame, width=20, text="Main Menu", font=("arial", 30, "bold"))
        mainLabel.place(x=200, y=70)

        Depositt = Button(frame, width=12, height=2, fg="white", bg="grey", relief=RAISED, text="Deposit",
                          command=lambda: controller.show_frame(Deposit))
        Depositt.place(x=250, y=150)
        CheckBalance = Button(frame, width=12, height=2, fg="white", bg="grey", relief=RAISED, text="Check Balance",
                              command=lambda: controller.show_frame(CheckBalance))
        CheckBalance.place(x=500, y=150)

        Withdrawal = Button(frame, width=12, height=2, fg="white", bg="grey", relief=RAISED, text="Withdrawal",
                            command=lambda: controller.show_frame(Withdraw))
        Withdrawal.place(x=250, y=200)
        FastCash = Button(frame, width=12, height=2, fg="white", bg="grey", relief=RAISED, text="Fast Cash (200)")
        FastCash.place(x=500, y=200)

        TransferMoney = Button(frame, width=12, height=2, fg="white", bg="grey", relief=RAISED,
                               text="Transfer Money")
        TransferMoney.place(x=250, y=250)

        ### * pop up showing "Thank you for using Cheserem's Atm Services" #########
        Signout = Button(frame, height=2, width=12, fg="white", bg="green", relief=RAISED, text="Sign Out",
                         command=lambda: controller.show_frame(WelcomePage))
        Signout.place(x=500, y=250)


class Withdraw(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        #
        # Hold onto a global reference for the root window
        global entry_2
        entry_2 = None
        count = 1
        amount = StringVar()

        # clear password field

        # function to input entry onto the entry
        def enternumber(x):
            global entry_2
            setval = StringVar()
            setval = str(x)
            print(setval)
            entry_2.insert(END, setval)

        def killwindow():
            pass

        # window.destroy()  # kill the root window

        def validate(
                inp):  #####Work on it so that it accepts only one dot and input starts from * LTR, and auto adds commas

            if inp.isdigit():
                return True
            elif inp == "":
                return True
            else:
                return False

        def withdrawconfirmation(inputamount):
            # loads the next page and validates the input

            pass

        def main():
            global entry_2
            global inputamount
            inputamount = StringVar()

            # pinobj = InsertATM(parent, controller)
            # compare = pinobj.return_account_no()
            # print(f"Debug to check if withdraw gets account_no {compare}")

            def cleartxtfield():
                global entry_2
                entry_2.delete(0, END)
                # inputamount.set("")

            def formattothousands():

                # ### Handle input of many points and return an error to the user or you can parse the input to only
                # allow one point to be input

                val = inputamount.get()
                f = float(val)
                print(locale.setlocale(locale.LC_ALL, ''))
                cash = locale.currency(f, grouping=True)

                inputamount.set(cash)

            entry_2 = Entry(self, textvariable=inputamount, width=64)
            entry_2.place(x=200, y=100)
            entry_2.focus()

            # isnum = lambda q:q.replace('.','',1).isdigit()
            # value = entry_1.get()
            # status = isnum(value)
            # print(status)
            rege = self.register(validate)
            entry_2.config(validate="key", validatecommand=(rege, '%P'))

            # def getcreds():
            #     # check if four digit entered and is not empty
            #     global amount
            #     amount = inputamount.get()
            #     print(amount)

            def funcbackspace():
                length = len(entry_2.get())
                entry_2.delete(length - 1, 'end')

            def goback():
                command = controller.show_frame(MainMenu)

                pass

            cancel = Button(self, width=8, height=3, text="Cancel", bg="red", fg="black", command=goback)
            cancel.place(x=220, y=150)

            clear = Button(self, text="Clear", bg="green", fg="white", width=8, height=3, command=cleartxtfield)
            clear.place(x=360, y=150)

            thousands = Button(self, width=8, height=3, text="Format", bg="red", fg="black",
                               command=formattothousands)
            thousands.place(x=600, y=150)

            backspace = Button(self, width=8, height=3, text="Backspace", bg="red", fg="black", command=funcbackspace)
            backspace.place(x=500, y=150)

            # ----number Buttons------
            btn_numbers = []
            for i in range(10):
                btn_numbers.append(
                    Button(self, width=8, height=3, text=str(i), bd=6, command=lambda x=i: enternumber(x)))
            btn_text = 1
            for i in range(0, 3):
                for j in range(0, 3):
                    btn_numbers[btn_text].place(x=220 + j * 140, y=250 + i * 100)
                    btn_text += 1

            btn_zero = Button(self, width=15, height=2, text='0', bd=5, command=lambda x=0: enternumber(x))
            btn_zero.place(x=330, y=550)

            #############################################3 Function to return amount

            """""""""
            addbutton(window, 220, 250,enterNumber)
            addbutton(window, 360, 250,enterNumber)
            addbutton(window, 500, 250,enterNumber)

            addbutton(window, 220, 350,enterNumber)
            addbutton(window, 360, 350,enterNumber)
            addbutton(window, 500, 350,enterNumber)

            addbutton(window, 220, 450,enterNumber)
            addbutton(window, 360, 450,enterNumber)
            addbutton(window, 500, 450,enterNumber)
        """

            dot = Button(self, text=".", bg="white", fg="black", width=8, height=3,
                         command=lambda x='.': enternumber(x))
            dot.place(x=500, y=550)
            okbtn = Button(self, text="Enter", bg="green", fg="black", width=12, height=6,
                           command=lambda: controller.show_frame(WithdrawConfirm))
            okbtn.place(x=600, y=500)

        """
            zero = Button(window, text="0", bg="black", fg="white", width=8, height=3)
            zero.place(x=360, y=550)
           """

        # Backspace = Button(window,text="Backspace",bg="black",fg="white",width=8,height=3)
        # Backspace.place(x=640,y=250)

        main()


class WithdrawConfirm(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # hold global reference to root window
        root = None
        lframe = None
        rframe = None
        lastbalance = None

        def addlabels(window, name, sidetopack):
            global root
            global lframe
            global rframe
            name_text = str(name)
            label = Label(window, text=name, bd=7, relief=GROOVE, height=5)
            label.pack(side=sidetopack)

        def main():
            global lastbalance
            global inputamount
            inputamount.set("")
            lastbalance = "Your Previous balance"
            prevbal = "Your Previous balance:"
            Withdrawamount = "Withdrawal amount:"
            newbalance = "Your new balance: "
            holdframe = Frame(self)
            bottom = Frame(self)
            lframe = Frame(holdframe)
            rframe = Frame(holdframe)
            addlabels(lframe, prevbal, LEFT)
            addlabels(lframe, Withdrawamount, LEFT)
            addlabels(lframe, newbalance, LEFT)
            lframe.pack(side=TOP)

            addlabels(rframe, prevbal, LEFT)
            addlabels(rframe, Withdrawamount, LEFT)
            addlabels(rframe, newbalance, LEFT)
            rframe.pack(side=BOTTOM)

            # * automatically redirect to the face recognition page for the animation and the actual 2 factor auth before money is withdrawn if
            # it fails " Authentication failed could not withdraw" Redirect to the page to confirm amount and then prompt if ready to scan face again
            ## if yes reauthenticate to a max of 5 times then terminate withdraw and return to the main menu

            Button(bottom, text="Print Reciept", fg='black', bg='green', font='times 18 bold', relief=RAISED, width=13,
                   height=2).pack(side=LEFT, padx=20)
            Button(bottom, text="Main Menu", fg='black', bg='brown', font='times 18 bold', relief=GROOVE, width=13,
                   height=2, command=lambda: controller.show_frame(MainMenu)).pack(side=LEFT, padx=20)
            bottom.pack(side=BOTTOM)

            holdframe.pack(side=TOP)

        main()


class Deposit(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Page one!!", font='times 15 bold').pack(pady=10, padx=10)
        label1 = Label(self, text="animation for the card to be inserted <event handler> [arduino]").pack()

        button1 = Button(self, text="Main Menu", command=lambda: controller.show_frame(MainMenu))
        button1.pack()

        button2 = Button(self, text="automatically redirect to Page Two when cash amount is read in",
                         command=lambda: controller.show_frame(DepositConfirm))
        button2.pack()


class DepositConfirm(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # hold global reference to root window
        root = None
        lframe = None
        rframe = None
        lastbalance = None

        def addlabels(window, name, sidetopack):
            global root
            global lframe
            global rframe
            name_text = str(name)
            label = Label(window, text=name, bd=7, relief=GROOVE, height=5)
            label.pack(side=sidetopack)

        def main():
            global lastbalance
            lastbalance = "Your Previous balance"
            prevbal = "Your Previous balance:"
            Withdrawamount = "Deposit amount:"
            newbalance = "Your new balance: "
            holdframe = Frame(self)
            bottom = Frame(self)
            lframe = Frame(holdframe)
            rframe = Frame(holdframe)
            addlabels(lframe, prevbal, LEFT)
            addlabels(lframe, Withdrawamount, LEFT)
            addlabels(lframe, newbalance, LEFT)
            lframe.pack(side=TOP)

            addlabels(rframe, prevbal, LEFT)
            addlabels(rframe, Withdrawamount, LEFT)
            addlabels(rframe, newbalance, LEFT)
            rframe.pack(side=BOTTOM)

            Button(bottom, text="Print Reciept", fg='black', bg='green', font='times 18 bold', relief=RAISED, width=13,
                   height=2).pack(side=LEFT, padx=20)
            Button(bottom, text="Main Menu", fg='black', bg='brown', font='times 18 bold', relief=GROOVE, width=13,
                   height=2, command=lambda: controller.show_frame(MainMenu)).pack(side=LEFT, padx=20)
            bottom.pack(side=BOTTOM)

            holdframe.pack(side=TOP)

        main()


class BalanceQuery(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)


# ######################################### Withdrawal Page ############################################################################
# class PageFour(Frame):
#     # def __init__(self, parent, controller):
#     #     Frame.__init__(self, parent)
#     #     # hold global reference to root window
#     #
#     # root = None
#     # lframe = None
#     # rframe = None
#     # lastbalance = None
#     #
#     #
#     #
#     # def main(self):
#     #     global lastbalance
#     #     lastbalance = "Your Previous balance"
#     #     prevbal = "Your Previous balance:"
#     #     Withdrawamount = "Withdrawal amount:"
#     #     newbalance = "Your new balance: "
#     #     holdframe = Frame(self)
#     #     lframe = Frame(holdframe)
#     #     rframe = Frame(holdframe)
#     #
#     #     def addlabels(window, name, sidetopack):
#     #         global lframe
#     #         global rframe
#     #         name_text = str(name)
#     #         label = Label(window, text=name, bd=7, relief=GROOVE, height=5)
#     #         label.pack(side=sidetopack)
#     #     addlabels(lframe, prevbal, LEFT)
#     #     addlabels(lframe, Withdrawamount, LEFT)
#     #     addlabels(lframe, newbalance, LEFT)
#     #     lframe.pack(side=TOP)
#     #
#     #     addlabels(rframe, prevbal, LEFT)
#     #     addlabels(rframe, Withdrawamount, LEFT)
#     #     addlabels(rframe, newbalance, LEFT)
#     #     rframe.pack(side=BOTTOM)
#     #
#     #     holdframe.pack(side=TOP)
#     #
#     #
#     # main()
#     pass
#





####################################################### End of Insert ATM ##################################################



####################################################### END of PIN Entry #################################################

# ########################################################### Start of Welcome Page
# ################################################


app = SeaofBTCapp()
app.mainloop()
