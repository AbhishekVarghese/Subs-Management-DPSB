import xlrd,random,xlwt,time,sys,datetime,os
import Tkinter as Tk
from PIL import ImageTk,Image
from tkFileDialog import askopenfilename, askopenfile, asksaveasfile

# MAin drawback : only can be used in normal working days. Incase of an extra day system day will have to be changed to the day corresponding to the timetable


# at many places changes to self.history is being made but that is not at all important
# It only stores what you did after opening the program i.e. what changes you made and is a
# good tool for debugging if ever any error occurs

class Application(object) : # Changed all label items to canvas
    def __init__(self,temp) :
        
        
        print 'Starting application',str(time.strftime("%X"))
        
        self.restart_times = temp
        if self.restart_times == 0 :
            self.book_errorfree = False
            self.history = 'Started application 1st time '+str(time.strftime("%X"))+"\n"
        else :
            self.history += 'Starting application  '+str(time.strftime("%X"))+"\n"
        self.root = None # our Tk window at every time
        self.book = None # the workbook(object) to work upon (for engagement list only)
        self.saveas = None# saving the created engagement list(object not the path)
        self.skip = False # used in check_database(). The most 'error causing variable' during debugging!
        self.display_text = '' # the status  to display at the right side of the screen
        self.day = datetime.datetime.today().weekday()
        self.check_stats()        
        self.set_up_screen(500,400)
        self.start_screen()

   
        
    def restart_app(self) : # Restart the application( activates whenever we press home button or when program delibrately restarts
        self.root.destroy() # Created root will we destroyed and app will restart
        self.restart_times += 1#updating history elements and the history
        print 'restarting ',str(time.strftime("%X"))
        self.history+= 'restarting '+ str(time.strftime("%X"))+"\n"
        self.__init__(self.restart_times)

    def check_stats(self) : # Check current date/time and database
        not_selected = False
        not_save = False
        with open("Support/path.txt", "r") as textfile:
            a = textfile.readline()
            if a == '' :
                not_selected = 'Not selected'
        with open("Support/save.txt", "r") as textfile:
            b = textfile.readline()
            if b == '' :
                not_save = 'No save directory selected'
        daysofweek = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        if not not_selected :
            not_selected = a
        if not not_save :
            not_save = b
        self.display_text = "STATS \n\nDate : %s\nDay : %s\nCurrent Time : %s\n\nDatabase : \n%s\n\nSave directory :\n %s\n\n Database error free : %s"%(str(time.strftime("%x")),daysofweek[self.day],str(time.strftime("%X")),not_selected,not_save,self.book_errorfree)
        if self.restart_times == 0 :
            self.history += "Date : %s\nDay : %s\nCurrent Time : %s\nDatabase : %s\nSave directory :%s"%(str(time.strftime("%x")),daysofweek[self.day],str(time.strftime("%X")),not_selected,not_save) +"\n\n"
                
    def set_up_screen(self,width,height): # Set up root(main screen) whenever required
        self.root = Tk.Tk()
        self.root.title("Morning Job")
        # the below procedire ensures the screen stays in middle of screen and does not open at top left
        w = width
        h = height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # A blank window comes upon the screen. Now to add elements on it....

            
        
    def start_screen(self) : # Setting elements on The main screen
        
        im = Image.open("backgrounds/500x400.png")
        tkimage = ImageTk.PhotoImage(im)
        im1 = Image.open("backgrounds/exit.png")
        tkimage1 = ImageTk.PhotoImage(im1)
        im2 = Image.open("backgrounds/help.png")
        tkimage2 = ImageTk.PhotoImage(im2)
        im3 = Image.open("backgrounds/credits.png")
        tkimage3 = ImageTk.PhotoImage(im3)
        im4 = Image.open("backgrounds/history.png")
        tkimage4 = ImageTk.PhotoImage(im4)
        logo = Image.open("backgrounds/logo1.png")
        logoimage = ImageTk.PhotoImage(logo)
        # Canvas is used here. This gives a wide opportuninty to place things wherever we like.
        # Tk root() is like a hard board and canvas like a chartpaper. It is best to draw on chartpaper instead of hard board.

        can = Tk.Canvas(self.root,width = 500,height=400)#brought the chartpaper of the size of the hard board
        can.pack()#We cant draw keeping chartpaper handing in the air, so we pasted it on the hardboard. A perfect fit!!!!! : )
        Canvas_Image = can.create_image(0,0, image=tkimage, anchor="nw")# Painted a background on the chartpaper. i.e. we fitted a image of size of canvas into canvas.

        # creating all the buttons and widgets that goes into the program and pasting it on the canvas.
        # quit button
        b = Tk.Button(self.root, justify =Tk.LEFT,command = self.root.destroy)
        b.config(image=tkimage1,width="40",height="40", activebackground = "SlateGray1")
        b.place(x=430,y=340)
        # help button
        b2 = Tk.Button(self.root, justify =Tk.LEFT,command = self.show_help)
        b2.config(image=tkimage2,width="49",height="42", activebackground = "SlateGray1")
        b2.place(x=260,y=340)
        # credits! at least!!
        b3 = Tk.Button(self.root, justify =Tk.LEFT,command = self.credits_screen)
        b3.config(image=tkimage3,width="49",height="45", activebackground = "SlateGray1")
        b3.place(x=370,y=337)
        # history button
        b4 = Tk.Button(self.root, justify =Tk.LEFT,command = self.show_recent_history)
        b4.config(image=tkimage4,width="50",height="43", activebackground = "SlateGray1")
        b4.place(x=315,y=340)
        
        # the main buttons that will give access to different features of this program.
        Tk.Button(self.root, text='  Create Engagement list  ', command=self.create_list).place(x=20,y=100)
        Tk.Button(self.root, text='  Select/Change your database  ', command=self.select_database).place(x=20,y=150)
        Tk.Button(self.root, text='  Select/Change save directory  ', command=self.save_database).place(x=20,y=200)
        Tk.Button(self.root, text='  Work Load  ', command=self.work_load).place(x=20,y=250)
        Tk.Button(self.root, text='  Check the above Databse for Errors  ', command=self.check_database).place(x=270,y=270)
        
        
        # create a seperation
        can.create_line(250, 50,250, 350, fill = 'gray61',width = 0)
        can.create_line(265, 330 ,480, 330, fill = 'gray61',width = 0)
        # now after the seperation paste the text we obtained from self.status() earlier
        canvas_id = can.create_text(260,60, anchor="nw")
        can.itemconfig(canvas_id, text= self.display_text)
        canvas_id1 = can.create_text(190,10, anchor="nw")
        can.itemconfig(canvas_id1, text= "Delhi Public School, Bhilai",font = "bold",fill = "steel blue",)
        can.create_image(30,38, image=logoimage)
        self.root.mainloop() # loop until one of the button above is pressed

        # if root(the hardboard) is destroyed by pressing quit {or any other bugs (which should not be there)} then quit the application
        print 'quitting',str(time.strftime("%X"))
        
        self.history += 'quitting ' + str(time.strftime("%X"))+"\n"
        self.history += 'Times restarted = ' + str(self.restart_times)
        with open("Support/history.txt", "w") as textfile:
            textfile.write(self.history)
        if not textfile.closed :
            textfile.close()
        sys.exit()


        
    def credits_screen(self) :# Oh! its just a screen nothing much about it. If you still want to know the workings of this pirticular screen, continue..on.. : )))!!

        self.root.destroy() # destroy the root(our hardboard/can also call it our main screen) This wont let application close down because... well I dont know much about that!!.
        # updating the history
        print "Read Credits",str(time.strftime("%X"))
        self.history += "Read Credits  " + str(time.strftime("%X"))+"\n"
        #creating a new harboard after the previous one had been destroyed
        self.set_up_screen(500,400)
        # text to be displayed
        makers = """Made by :
Abhishek Varghese
Harsh Jain


Resources :

Background- yourswallpaper.com/wallpaper/3d/wallpaper-abstraction-blue-white-558.htm
icon - physweb.bgu.ac.il/COURSES/EnvelopePhysics/Images/book2.png
"""
        
        im = Image.open("backgrounds/500x400.png")
        tkimage = ImageTk.PhotoImage(im)
        can = Tk.Canvas(self.root,width = 500,height=400)#again creating a canvas(the chartpaper !
        can.pack()# pasting canvas on the root
        Canvas_Image = can.create_image(0,0, image=tkimage, anchor="nw")# background image of the canvas
        canvas_id = can.create_text(10,50, anchor="nw") # creating text element
        can.itemconfig(canvas_id, text= makers)# adding our text to the text element
        im1 = Image.open("backgrounds/home.png")
        tkimage1 = ImageTk.PhotoImage(im1)
        b = Tk.Button(self.root, justify =Tk.LEFT,command = self.restart_app)# pressing home restarts the application
        b.config(image=tkimage1,width="60",height="50", activebackground = "white")
        b.place(x=400,y=320)
        canvas_id1 = can.create_text(200,10, anchor="nw")
        can.itemconfig(canvas_id1, text= "Credits",font = "bold",fill = "steel blue",)
        self.root.mainloop()



    def show_recent_history(self) : # history panel very useful in time of debugging
        self.root.destroy() # destroy the main screen
        # No further help/comments for this section
        print "Read previous history",str(time.strftime("%X"))
        self.history += "Read previous history  "+str(time.strftime("%X"))+"\n"
        self.set_up_screen(500,400)
        
        with open("Support/history.txt", "r") as textfile:
            history = textfile.read()
        if not textfile.closed :
            textfile.close()
        
        im = Image.open("backgrounds/500x400.png")
        tkimage = ImageTk.PhotoImage(im)
        can = Tk.Canvas(self.root,width = 500,height=400)
        can.pack()
        Canvas_Image = can.create_image(0,0, image=tkimage, anchor="nw")
        canvas_id = can.create_text(10,50, anchor="nw")
        can.itemconfig(canvas_id, text= history)
        im1 = Image.open("backgrounds/home.png")
        tkimage1 = ImageTk.PhotoImage(im1)
        b = Tk.Button(self.root, justify =Tk.LEFT,command = self.restart_app)
        b.config(image=tkimage1,width="60",height="50", activebackground = "white")
        b.place(x=400,y=320)
        
        canvas_id1 = can.create_text(200,10, anchor="nw")
        can.itemconfig(canvas_id1, text= "Last opned History",font = "bold",fill = "steel blue",)
        self.root.mainloop()

    def show_help(self): # Show help if you dont know to use it
        self.root.destroy()# destroying main screen as usual
        print "Read Help",str(time.strftime("%X"))
        #----following section has already been explained ---------
        self.history += "Read Help  " + str(time.strftime("%X"))+"\n"
        self.set_up_screen(500,400)
        help_text = """Requirements : OS - Windows


Create a new fresh list of substitute teachers


Select the TimeTable of the teachers



Select the location where the list will be saved


Work Load -- """
        im = Image.open("backgrounds/500x400.png")
        tkimage = ImageTk.PhotoImage(im)
        im2 = Image.open("backgrounds/troubleshoot.png")
        tkimage2 = ImageTk.PhotoImage(im2)

        
        can = Tk.Canvas(self.root,width = 500,height=400)
        can.pack()
        Canvas_Image = can.create_image(0,0, image=tkimage, anchor="nw")
        canvas_id = can.create_text(200,45, anchor="nw")
        can.itemconfig(canvas_id, text= help_text)
        #---------------------------------------------------------------------------------
        # Creating buttons which are designed for help panel. i.e. press it as much you want!!nothing will happen.
        Tk.Button(self.root,text = 'Create Engagement List',command = None).place(x=20,y=85)
        Tk.Button(self.root,text = 'Select/Change your Database',command = None).place(x=20,y=135)
        Tk.Button(self.root,text = 'Select/Change Save Loaction',command = None).place(x=20,y=185)
        Tk.Button(self.root,text = 'Work Load',command = None).place(x=20,y=235)
        
        im1 = Image.open("backgrounds/home.png")
        tkimage1 = ImageTk.PhotoImage(im1)
        b = Tk.Button(self.root, justify =Tk.LEFT,command = self.restart_app)
        b.config(image=tkimage1,width="60",height="50", activebackground = "white")
        b.place(x=20,y=320)
        b2 = Tk.Button(self.root, justify =Tk.LEFT,command = self.troubleshoot)# best to include a trouble shoot icon in help when you cant do it in main screen
        b2.config(image=tkimage2,width="60",height="60", activebackground = "SlateGray1")
        b2.place(x=400,y=320)
        
        
        canvas_id1 = can.create_text(200,10, anchor="nw")
        can.itemconfig(canvas_id1, text= "Help",font = "bold",fill = "steel blue",)
        self.root.mainloop()
        
    def troubleshoot(self) : # shows the text for troubleshooting. It can also be viewed in notepad in support
        self.root.destroy()
        print "Read Troubleshoot",str(time.strftime("%X"))
        self.history += "Read Troubleshoot  "+str(time.strftime("%X"))+"\n"
        self.set_up_screen(500,400)
        # open the txt file containing troubleshoot text
        with open("Support/troubleshoot.txt", "r") as textfile:
            troubleshoot = textfile.read()# coply all the text to a variable
        if not textfile.closed :
            textfile.close()
        
        im = Image.open("backgrounds/500x400.png")
        tkimage = ImageTk.PhotoImage(im)
        im1 = Image.open("backgrounds/back.png")
        tkimage1 = ImageTk.PhotoImage(im1)

        
        
        can = Tk.Canvas(self.root,width = 500,height=400)
        can.pack()
        Canvas_Image = can.create_image(0,0, image=tkimage, anchor="nw")
        canvas_id = can.create_text(10,50, anchor="nw")
        can.itemconfig(canvas_id, text= troubleshoot)
        
        canvas_id1 = can.create_text(200,10, anchor="nw")
        can.itemconfig(canvas_id1, text= "Troubleshoot",font = "bold",fill = "steel blue",)
        b = Tk.Button(self.root, justify =Tk.LEFT,command = self.show_help)
        b.config(image=tkimage1,width="60",height="60", activebackground = "SlateGray1")
        b.place(x=400,y=325)
        self.root.mainloop()

        
    def open_book(self) : #Open a book(in form of object) when required. book refers to excel file
        with open("Support/path.txt", "r") as textfile:
            a = textfile.readline()
            if a == '' :
                textfile.close()
                self.select_database()
            else :
                self.book = xlrd.open_workbook(a)# store the excel object into a class variable (to use it somewhere else)
        if not textfile.closed :
            textfile.close()
        



    def save_database(self) :#select a path to save and store it in notepad to be used later
        textfile = open("Support/save.txt", "w")
        path = str(asksaveasfile(mode='w',filetypes=[("Excel files","*.xls;*.xlsx")]))# asksaveasfile is a function provided with t-kinter which makes our work easier!!
        print 'Save location changed :  ',path,str(time.strftime("%X"))
        self.history+=  'Save location changed : '+str(path)+str(time.strftime("%X"))+"\n"
        textfile.write(path[ 13:-26 ])#To delete all other useless charecters returned by asksaveas. Select only the required path
        textfile.close()
        self.root.destroy()
        self.set_up_screen(230,100)# setting a screen to make user know that a restart is required to make changes 
        can = Tk.Canvas(self.root,width = 230,height=100)
        can.pack()
        im = Image.open("backgrounds/250x200.png")
        tkimage = ImageTk.PhotoImage(im)
        Canvas_Image = can.create_image(0,0, image=tkimage, anchor="nw")
        canvas_id = can.create_text(40, 20, anchor="nw")
        
        can.itemconfig(canvas_id, text="Save Loaction has been set\n   Restarting Application")
        self.root.after(4000,self.restart_app) # who would like a instant restart ??!! At least give some time to read the message on the screen!!!!
        self.root.mainloop()
        
    def select_database(self) : #Select a database if none is selected i.e. a database path is read from notepad. asked to select sa path if no path is available in the notepad
        textfile = open("Support/path.txt", "w")
        path = askopenfilename(filetypes=[("Excel files","*.xls;*.xlsx")])# askopenfilename is a function provided with t-kinter which makes our work easier!!
        print 'Database changed :  ' ,path ,str(time.strftime("%X"))
        self.history+=   'Database changed :'+ str(path) +str(time.strftime("%X"))+ "\n"
        textfile.write(str(path))
        textfile.close()
        self.book_errorfree = False
        self.root.destroy()
        self.set_up_screen(230,100)
        can = Tk.Canvas(self.root,width = 230,height=100)
        can.pack()
        im = Image.open("backgrounds/250x200.png")
        tkimage = ImageTk.PhotoImage(im)
        Canvas_Image = can.create_image(0,0, image=tkimage, anchor="nw")
        canvas_id = can.create_text(12, 10, anchor="nw")
        
        can.itemconfig(canvas_id, text="\n A new database has been selected.\n          Restarting the Application")
        self.root.after(5000,self.restart_app)# who would like a instant restart ??!! At least give some time to read the message on the screen!!!!
        self.root.mainloop()
       

    def checkbox_list(self,sheet) :# Harsh's(see credits) brains behind it. I cant comment much on this. A funtion to select and return absent teachers.It destroys the self.root() unlike other functions so whenever use it remember not to destroy it again.
        # protocols required to set checkboxes. Creating one list for each letter of english alphabets

        # READ : If in future the list gets out of screen expand the dimentions. It will look a bit clumsy but still one can work with it.
        AL = []
        BL = []
        CL = []
        DL = []
        EL = []
        FL = []
        GL = []
        HL = []
        IL = []
        JL = []
        KL = []
        LL = []
        ML = []
        NL = []
        OL = []
        PL = []
        QL = []
        RL = []
        SL = []
        TL = []
        UL = []
        VL = []
        WL = []
        XL = []
        YL = []
        ZL = []
        for n in range (sheet.nrows) :
            temp = str(sheet.cell_value(n,0))[0].upper()
            if temp == 'A' :
                AL.append(sheet.cell_value(n,0))
            elif temp == 'B' :
                BL.append(sheet.cell_value(n,0))
            elif temp == 'C' :
                CL.append(sheet.cell_value(n,0))
            elif temp == 'D' :
                DL.append(sheet.cell_value(n,0))
            elif temp == 'E' :
                EL.append(sheet.cell_value(n,0))
            elif temp == 'F' :
                FL.append(sheet.cell_value(n,0))
            elif temp == 'G' :
                GL.append(sheet.cell_value(n,0))
            elif temp == 'H' :
                HL.append(sheet.cell_value(n,0))
            elif temp == 'I' :
                IL.append(sheet.cell_value(n,0))
            elif temp == 'J' :
                JL.append(sheet.cell_value(n,0))
            elif temp == 'K' :
                KL.append(sheet.cell_value(n,0))
            elif temp == 'L' :
                LL.append(sheet.cell_value(n,0))
            elif temp == 'M' :
                ML.append(sheet.cell_value(n,0))
            elif temp == 'N' :
                NL.append(sheet.cell_value(n,0))
            elif temp == 'O' :
                OL.append(sheet.cell_value(n,0))
            elif temp == 'P' :
                PL.append(sheet.cell_value(n,0))
            elif temp == 'Q' :
                QL.append(sheet.cell_value(n,0))
            elif temp == 'R' :
                RL.append(sheet.cell_value(n,0))
            elif temp == 'S' :
                SL.append(sheet.cell_value(n,0))
            elif temp == 'T' :
                TL.append(sheet.cell_value(n,0))
            elif temp == 'U' :
                UL.append(sheet.cell_value(n,0))
            elif temp == 'V' :
                VL.append(sheet.cell_value(n,0))
            elif temp == 'W' :
                WL.append(sheet.cell_value(n,0))
            elif temp == 'X' :
                XL.append(sheet.cell_value(n,0))
            elif temp == 'Y' :
                YL.append(sheet.cell_value(n,0))
            elif temp == 'Z' :
                ZL.append(sheet.cell_value(n,0))
            
       
        main_list = [AL,BL,CL,DL,EL,FL,GL,HL,IL,JL,KL,LL,ML,NL,OL,PL,QL,RL,SL,TL,UL,VL,WL,XL,YL,ZL]
        l = []
        
        class Checkbar(Tk.Frame):
           def __init__(self, parent=None, picks=[], side=Tk.LEFT, anchor='w'):
              Tk.Frame.__init__(self, parent)
              self.vars = []
              for pick in picks:
                 var = Tk.IntVar()
                 chk = Tk.Checkbutton(self, text=pick, variable=var)
                 chk.pack(side=side, anchor=anchor, expand=Tk.YES)
                 self.vars.append(var)
           def state(self):
              return map((lambda var: var.get()), self.vars)
        self.root.destroy()
        self.set_up_screen(1200,800)# make changes to the screen here - self.set_up_screen(width,height)   <<<<---------------------================
        im = Image.open("backgrounds/1200x950.png")
        tkimage = ImageTk.PhotoImage(im)
        myvar=Tk.Label(self.root,image = tkimage)
        myvar.place(x=0, y=0, relwidth=1, relheight=1)
        lab = Tk.Label(self.root,text = "\n\nSelect absent teachers", anchor = "w")
        lab.pack()
        
        A = Checkbar(self.root, AL)
        A.pack(side=Tk.TOP,)
        A.config(relief=Tk.GROOVE, bd=2)
        B = Checkbar(self.root, BL)
        B.pack(side=Tk.TOP,)
        B.config(relief=Tk.GROOVE, bd=2)
        C = Checkbar(self.root, CL)
        C.pack(side=Tk.TOP,)
        C.config(relief=Tk.GROOVE, bd=2)
        D = Checkbar(self.root, DL)
        D.pack(side=Tk.TOP,)
        D.config(relief=Tk.GROOVE, bd=2)
        E = Checkbar(self.root, EL)
        E.pack(side=Tk.TOP,)
        E.config(relief=Tk.GROOVE, bd=2)
        F = Checkbar(self.root, FL)
        F.pack(side=Tk.TOP,)
        F.config(relief=Tk.GROOVE, bd=2)
        G = Checkbar(self.root, GL)
        G.pack(side=Tk.TOP,)
        G.config(relief=Tk.GROOVE, bd=2)
        H = Checkbar(self.root, HL)
        H.pack(side=Tk.TOP,)
        H.config(relief=Tk.GROOVE, bd=2)
        I = Checkbar(self.root, IL)
        I.pack(side=Tk.TOP,)
        I.config(relief=Tk.GROOVE, bd=2)
        J = Checkbar(self.root, JL)
        J.pack(side=Tk.TOP,)
        J.config(relief=Tk.GROOVE, bd=2)
        K = Checkbar(self.root, KL)
        K.pack(side=Tk.TOP,)
        K.config(relief=Tk.GROOVE, bd=2)
        L = Checkbar(self.root, LL)
        L.pack(side=Tk.TOP,)
        L.config(relief=Tk.GROOVE, bd=2)
        M = Checkbar(self.root, ML)
        M.pack(side=Tk.TOP,)
        M.config(relief=Tk.GROOVE, bd=2)
        N = Checkbar(self.root, NL)
        N.pack(side=Tk.TOP,)
        N.config(relief=Tk.GROOVE, bd=2)
        O = Checkbar(self.root, OL)
        O.pack(side=Tk.TOP,)
        O.config(relief=Tk.GROOVE, bd=2)
        P = Checkbar(self.root, PL)
        P.pack(side=Tk.TOP,)
        P.config(relief=Tk.GROOVE, bd=2)
        Q = Checkbar(self.root, QL)
        Q.pack(side=Tk.TOP,)
        Q.config(relief=Tk.GROOVE, bd=2)
        R = Checkbar(self.root, RL)
        R.pack(side=Tk.TOP,)
        R.config(relief=Tk.GROOVE, bd=2)
        S = Checkbar(self.root, SL)
        S.pack(side=Tk.TOP,)
        S.config(relief=Tk.GROOVE, bd=2)
        T = Checkbar(self.root, TL)
        T.pack(side=Tk.TOP,)
        T.config(relief=Tk.GROOVE, bd=2)
        U = Checkbar(self.root, UL)
        U.pack(side=Tk.TOP,)
        U.config(relief=Tk.GROOVE, bd=2)
        V = Checkbar(self.root, VL)
        V.pack(side=Tk.TOP,)
        V.config(relief=Tk.GROOVE, bd=2)
        W = Checkbar(self.root, WL)
        W.pack(side=Tk.TOP,)
        W.config(relief=Tk.GROOVE, bd=2)
        X = Checkbar(self.root, XL)
        X.pack(side=Tk.TOP,)
        X.config(relief=Tk.GROOVE, bd=2)
        Y = Checkbar(self.root, YL)
        Y.pack(side=Tk.TOP,)
        Y.config(relief=Tk.GROOVE, bd=2)
        Z = Checkbar(self.root, ZL)
        Z.pack(side=Tk.TOP,)
        Z.config(relief=Tk.GROOVE, bd=2)
       
       
        def allstates():
          
           list1 = [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z]
           for i in range(len(list1)):
              n = list(list1[i].state())
              for j in range(len(n)):
                 if n[j] == 1:
                    l.append(main_list[i][j])
           self.root.destroy()

        im1 = Image.open("backgrounds/cancel.png")
        tkimage1 = ImageTk.PhotoImage(im1)
        
        im2 = Image.open("backgrounds/next.png")
        tkimage2 = ImageTk.PhotoImage(im2)

        b1 = Tk.Button(self.root, justify =Tk.LEFT,command = self.restart_app)
        b1.config(image=tkimage1,width="149",height="30", activebackground = "SlateGray1")
        b1.pack(side=Tk.LEFT,padx = 100)
        b2 = Tk.Button(self.root, justify =Tk.LEFT,command = allstates)
        b2.config(image=tkimage2,width="60",height="60", activebackground = "SlateGray1")
        b2.pack(side=Tk.RIGHT,padx = 100)
        
        
        self.root.mainloop()
        return l

    def create_list(self) : #Main Engagement list
        # first of all select a book if no book has been selected
        if self.book == None :
            self.open_book()# this generates a book object in self.book variable
        print self.book
        self.history+=   "book item = " + str(self.book) +"\n"
        to_write = xlwt.Workbook()# create a book object to write the created list
        to_write_sheet = to_write.add_sheet("Today's Engagement list",cell_overwrite_ok= True)# add a sheet into it
        # back to work on self.book as writing part is ready...
        sheet = self.book.sheet_by_index(self.day)# open the sheet of the book corresponding to today's day as noted by status() function
        absent_list = self.checkbox_list(sheet)# obtain list of absent teachers from checkbox() function
        main_list = []# Get ready !!!!!
        present_list = []# Setting up for the magic to happen !!!!!!!!

        '''Dont || ----DO NOT--- combine the 2 loops given below for any shorcut!!!!'''
        # creating main list of teachers in main_list and present_list together
        for n in range (0,107):
            main_list += [str(sheet.cell_value(n,0))]
            present_list += [str(sheet.cell_value(n,0))]
        # Removing the absent teachers from the present list.
        for n in absent_list :
            for n1 in present_list :
                if n==n1 :
                    
                    present_list.remove(n)
        ''' ^^^^ Better not to touch or disturb the above 2 loops ^^^^ '''
                    

        
        class Teacher(object) : # creating a class to handle the vast amount of data
             def __init__(self,n,sheet) :# basically each teacher is converted into an object and the 9 periods are stored in following variables
                 self.first = sheet.cell_value(n,1)
                 self.second = sheet.cell_value(n,2)
                 self.third =  sheet.cell_value(n,3)
                 self.fourth = sheet.cell_value(n,4)
                 self.fifth = sheet.cell_value(n,5)
                 self.sixth = sheet.cell_value(n,6)
                 self.seventh = sheet.cell_value(n,7)
                 self.eighth = sheet.cell_value(n,8)
                 self.ninth = sheet.cell_value(n,9)
        # ---------------Preparing the writing sheet to write -----------------------
        to_write_sheet.write(0,0,"Name of absent Teachers")
        to_write_sheet.write(0,1,"Period 1")
        to_write_sheet.write(0,2,"Period 2")
        to_write_sheet.write(0,3,"Period 3")
        to_write_sheet.write(0,4,"Period 4")
        to_write_sheet.write(0,5,"Period 5")
        to_write_sheet.write(0,6,"Period 6")
        to_write_sheet.write(0,7,"Period 7")
        to_write_sheet.write(0, 8,"Period 8")
        to_write_sheet.write(0,9,"Period 9")
        # -----------------The heart of the program : based on logic ----------------------

        x = 2# the row counter for writing on created eng list
        agree_list = []
        
        def make_agree_list(emf) :
                agree_list_temp = [] # list of teachers who can be given engagement
                if n + emf > 9 :
                    emf = abs(9-n)
                for n1 in present_list :
                        
                        position1 = main_list.index(n1)
                       
                        if int(sheet.cell_type(position1,n+emf)) == 0:
                            agree_list_temp += [n1]
                return agree_list_temp
            
        for absent in absent_list :
            
            position = main_list.index(absent)
            selected = Teacher(position,sheet)
            
            for n in range(1,10) : # selecting a period
                free = 6 #next 5 periods are free then add to substitute
                if int(sheet.cell_type(position,n)) != 0 : # going rowise in absent teacher to find a period to put substitution

                    if agree_list == [] :
                        free -= 1
                    agree_list = make_agree_list(free)
                    substitute = random.choice(agree_list)
                    present_list.remove(substitute)
                    if n == 1 :
                        selected.first += " : " + substitute
                    if n== 2 :
                        selected.second += " : " + substitute
                    if n== 3 :
                        selected.third += " : " + substitute
                    if n==4 :
                        selected.fourth += " : " + substitute
                    if n== 5 :
                        selected.fifth += " : " + substitute
                    if n== 6 :
                        selected.sixth += " : " + substitute
                    if n== 7 :
                        selected.seventh += " : " + substitute
                    if n== 8 :
                        selected.eighth += " : " + substitute
                    if n== 9 :
                        selected.ninth += " : " + substitute
            # write the things on the sheet prepared above
            to_write_sheet.write(x,0,absent)
            to_write_sheet.write(x,1,selected.first)
            to_write_sheet.write(x,2,selected.second)
            to_write_sheet.write(x,3,selected.third)
            to_write_sheet.write(x,4,selected.fourth)
            to_write_sheet.write(x,5,selected.fifth)
            to_write_sheet.write(x,6,selected.sixth)
            to_write_sheet.write(x,7,selected.seventh)
            to_write_sheet.write(x,8,selected.eighth)
            to_write_sheet.write(x,9,selected.ninth)
            x +=1 #increment of the row counter
        #-----------------------------------------------------------------


        # open the save.txt and see if any path had been written there to save the file if no ask for a path and save the file
        with open("Support/save.txt", "r") as textfile:
            a = textfile.readline()
            if a == '' :
                textfile.close()
                root = Tk.Tk()#Necessary to remove Tcl image5 error. i.e. create a temporary tcl window
                a = str(asksaveasfile(mode='w',filetypes=[("Excel files","*.xls;*.xlsx")]))
                a = a[13:-26]
                root.destroy()#Destroyes the temporary Tcl window after work is done
        if not textfile.closed :
            textfile.close()

        print a

        to_write.save(a)# save the created list on the path obtained
        print "Created Engagement list",str(time.strftime("%X"))
        self.history+=   "Created Engagement list  "+ str(time.strftime("%X"))+"\n"

        
        self.set_up_screen(500,400)# set up screen to show to open the file created
        can = Tk.Canvas(self.root,width = 500,height=400)
        can.pack()
        im = Image.open("backgrounds/500x400.png")
        tkimage = ImageTk.PhotoImage(im)
        Canvas_Image = can.create_image(0,0, image=tkimage, anchor="nw")
        
        
        im2 = Image.open("backgrounds/open250x250.png")# A minion after all this hulubulao is nice to see
        tkimage2 = ImageTk.PhotoImage(im2)
        canvas_id = can.create_text(100, 20, anchor="nw")
        
        can.itemconfig(canvas_id, text = "Click on the Icon below to open the preapred list" )

        b = Tk.Button(self.root, justify =Tk.LEFT,command = lambda : os.startfile(a))
        b.config(image=tkimage2,width="200",height="200", activebackground = "lavender")
        b.place(x=150,y=100)
        im12 = Image.open("backgrounds/home.png")
        tkimage12 = ImageTk.PhotoImage(im12)
        
        b12 = Tk.Button(self.root, justify =Tk.LEFT,command = self.restart_app)
        b12.config(image=tkimage12,width="60",height="50", activebackground = "white")
        b12.place(x=400,y=320)
        
        self.root.mainloop()

        
    def check_database(self): # Future errors might be based on self.skip used in this section which is used to override all the error messages
        # --------------------the code below is only based on searching indexes in an excel file-----------------------------
        if self.book == None :
            self.open_book()
        def main(database) :
            noerror = True
            
            
            def no_of_charectors(string) :
                count = 0
                for n in string :
                    if n != ' ' :
                        count += 1
                return count
            def error_msg(msg) : # message to give out the errors
                def override() :# skip all the errors
                    self.skip = True
                    print  "Error still available in the document. Error check overrided" + str(time.strftime("%X"))
                    self.history += "Error available in the document. Error check overrided " + str(time.strftime("%X"))+"\n"
                    

                def combine_funcs(*funcs):
                    def combined_func(*args, **kwargs):
                        for f in funcs:
                            f(*args, **kwargs)
                    return combined_func
                
                root1 = Tk.Toplevel()# toplevel() required as root() is already in use
                root1.attributes("-topmost", True)
                root1.title("Error")
                w1 = 230
                h1 = 100
                ws1 = root1.winfo_screenwidth()
                hs1 = root1.winfo_screenheight()
                x1 = (ws1/2) - (w1/2)
                y1 = (hs1/2) - (h1/2)
                root1.geometry('%dx%d+%d+%d' % (w1, h1, x1, y1))
                can1 = Tk.Canvas(root1,width = 230,height=100)
                can1.pack()
                im1 = Image.open("backgrounds/250x200.png")
                tkimage1 = ImageTk.PhotoImage(im1)
                Canvas_Image1 = can1.create_image(0,0, image=tkimage, anchor="nw")
                
                canvas_id1 = can1.create_text(15, 10, anchor="nw")
                can1.itemconfig(canvas_id1, text=msg)
                Tk.Button(root1, text=' OK ', command = root1.destroy).place(x=150,y=70)
                Tk.Button(root1, text='Override all errors', command = lambda : combine_funcs(root1.destroy(),override())).place(x=30,y=70)
                root1.wait_window()
                return None
            
            self.history += "Check window active  "+str(time.strftime("%X"))+"\n"
            n_sheet = database.nsheets
            if n_sheet < 5 :
                error_msg("Your Database Must have minimum 5 sheets")
                noerror = False

            if self.skip :
                self.skip = False
                return

            for index in range (n_sheet) :
                current_sheet = database.sheet_by_index(index)
                if index == 0 :
                    n_rows = current_sheet.nrows
                    n_cols = current_sheet.ncols
                else :
                    if current_sheet.nrows != n_rows :
                        error_msg("The sheet of index %s has different no. of records than the first page"%(index))
                        if self.skip :
                            return
                        noerror = False
                    if current_sheet.ncols != 10 :
                        error_msg("The sheet of index %s has  %s  no. of \n columns than the required 10 columns"%(index,current_sheet.ncols))
                        if self.skip :
                            self.skip = False
                            return
                        noerror = False

            for n in range (n_rows) :
                for index in range (n_sheet):
                    current_sheet = database.sheet_by_index(index)
                    if index == 0 :
                        value = current_sheet.cell_value(n,0)
                    else :
                        if current_sheet.cell_value(n,0) != value :
                            error_msg("The sheet of index %s has different \n value in row %s of column 0 than of first page"%(index,n))
                            noerror = False
                            if self.skip :
                                self.skip = False
                                return
            
                    
            for index in range(n_sheet) :
                current_sheet = database.sheet_by_index(index)
                for n in range (n_rows) :
                    for n1 in range (1,n_cols) :
                        temp = no_of_charectors(current_sheet.cell_value(n,n1))
                        if temp > 3 :
                            error_msg("The value of cell of row = %s col = %s \n of sheet %s is not valid "%(n,n1,index))
                            noerror = False
                            if self.skip :
                                self.skip = False
                                return 
                        
            print "Check completed. ",str(time.strftime("%X")),"noerror = ",noerror,"\n"                
            self.history +=    "Check completed. " + str(time.strftime("%X"))+"noerror = "+str(noerror) + "\n"                
            if noerror :
                self.book_errorfree =True
            
                





        self.root.destroy()
        print "Checked database",str(time.strftime("%X"))
        self.history += "Checked the database  "+str(time.strftime("%X"))+"\n"
        self.set_up_screen(500,400)
        im = Image.open("backgrounds/500x400.png")
        tkimage = ImageTk.PhotoImage(im)
        can = Tk.Canvas(self.root,width = 500,height=400)
        can.pack()
        Canvas_Image = can.create_image(0,0, image=tkimage, anchor="nw")
        canvas_id = can.create_text(60,70, anchor="nw")
        message_to_show = '''           Criteria for determining Errors :

    1) The database should contain minimum 5 sheets

    2) The no. of rows in each sheet should be same

    3) The values of cells in 1st column should be same in each sheet

    4) Invalid Entry should not be there in any cell from second column onwards

    Invalid Entry : Cell contains more than 3 proper charecters except spaces


Override : Warning!! - You can override all the errors but this wont remove any
                             error in the document and you still wont be able to access
                                                     many features of this Application! '''
        can.itemconfig(canvas_id, text= message_to_show)
        im1 = Image.open("backgrounds/home.png")
        tkimage1 = ImageTk.PhotoImage(im1)
        b = Tk.Button(self.root, justify =Tk.LEFT,command = self.restart_app)
        b.config(image=tkimage1,width="60",height="50", activebackground = "white")
        b.place(x=400,y=320)
        Tk.Button(self.root, text='  Check for errors  ', command = lambda : main(self.book)).place(x=70,y=320)
        canvas_id1 = can.create_text(160,10, anchor="nw")
        can.itemconfig(canvas_id1, text= "Checking database",font = "bold",fill = "steel blue",)
        self.root.mainloop()









# ------------------------------------Under construction --------------------------------------------------------_____________________________________-
    def add_sub_for_workload(self) :# activates when you click on add subject

        class Checkbar(Tk.Frame):
           def __init__(self, parent=None, picks=[], side=Tk.LEFT, anchor='w'):
              Tk.Frame.__init__(self, parent)
              self.vars = []
              for pick in picks:
                 var = Tk.IntVar()
                 chk = Tk.Checkbutton(self, text=pick, variable=var)
                 chk.pack(side=side, anchor=anchor, expand=Tk.YES)
                 self.vars.append(var)
           def state(self):
              return map((lambda var: var.get()), self.vars)
        

        with open("Support/subjects.txt", "r") as textfile:#just check for available subjects and store them in dictionary and a list
            a = textfile.read()
        if not textfile.closed :
            textfile.close()
        
        a = a.split()
        sub = {}# the dic has sub: abrivation pairs
        i= 0
        while i in range(len(a)) :
            if a[i+1] == ':' :
                sub[a[i]] = a[i+2]
                i += 3

        list_sub = []# The list will contain all subjects
        for i in sub :
            temp = [i+ ' (' + sub[i] + ')']
            list_sub.append(temp)


        s = ""
        def retrieve_input():#function when when activated obtains whatever is written inside the text box
            with open("Support/subjects.txt", "r") as textfile:
                a = textfile.read()
            if not textfile.closed :
                textfile.close()
            # modifing the subject name and its attributes to avoid any errors
            s = e.get().lstrip(" ").rstrip(" ")
            s1 = e1.get().lstrip(" ").rstrip(" ")
            s,s1 = list(s),list(s1)
            for n in range (len(s)) :
                if s[n] == " " :
                    s[n] = "_"
            for n in range (len(s1)) :
                if s1[n] == " " :
                    s1[n] = "_"
            
            s = ''.join(s)
            s1 = ''.join(s1)
            
            #-- modification finished--
            if s.split() != [] and s1.split() != [] :
                with open("Support/subjects.txt", "w") as textfile1:
                    textfile1.write( a+ '\n' +  s + " : " + s1)
                if not textfile1.closed :
                    textfile1.close()
            self.work_load_screen()
            
        
        self.root.destroy()
        self.set_up_screen(500,400)
        
        im = Image.open("backgrounds/500x400.png")
        tkimage = ImageTk.PhotoImage(im)
        myvar=Tk.Label(self.root,image = tkimage)
        myvar.place(x=0, y=0, relwidth=1, relheight=1)
        lab = Tk.Label(self.root,text = "\n\nAdd Subjects", anchor = "w")
        lab.pack()
        list_sub.sort()
        for i in range(len(list_sub)) :
            list_sub[i] = Checkbar(self.root, list_sub[i])
            list_sub[i].pack(side=Tk.TOP,)
            list_sub[i].config(relief=Tk.GROOVE, bd=2)
        
        label2 = Tk.Label( self.root, text="Subject Name")
        label3 = Tk.Label( self.root, text="Subject Abrivation")
        e = Tk.Entry(self.root,bd = 5)
        e1 = Tk.Entry(self.root,bd = 5)
        
        label2.pack()
        e.pack()
        label3.pack()
        e1.pack()
        b1 = Tk.Button(self.root,text = "Cancel", justify =Tk.LEFT,command = self.work_load_screen)
        b1.config(activebackground = "SlateGray1")
        b1.pack(side=Tk.LEFT,padx = 100)
        
        b2 = Tk.Button(self.root, justify =Tk.LEFT,text = "Add" ,command = retrieve_input)
        b2.config(activebackground = "SlateGray1")
        b2.pack(side=Tk.RIGHT,padx = 100)
        
        
        self.root.mainloop()
       

        
    def work_load_screen(self) : #The main work load screen. It destroys the self.root() when pressing next unlike other functions so whenever use it remember not to destroy it again
        class Checkbar(Tk.Frame):
           def __init__(self, parent=None, picks=[], side=Tk.LEFT, anchor='w'):
              Tk.Frame.__init__(self, parent)
              self.vars = []
              for pick in picks:
                 var = Tk.IntVar()
                 chk = Tk.Checkbutton(self, text=pick, variable=var)
                 chk.pack(side=side, anchor=anchor, expand=Tk.YES)
                 self.vars.append(var)
           def state(self):
              return map((lambda var: var.get()), self.vars)
        

        
        self.root.destroy()
        self.set_up_screen(500,400)
        im = Image.open("backgrounds/500x400.png")
        tkimage = ImageTk.PhotoImage(im)
        myvar=Tk.Label(self.root,image = tkimage)
        myvar.place(x=0, y=0, relwidth=1, relheight=1)
        lab = Tk.Label(self.root,text = "\n\nSelect Subjects", anchor = "w")
        lab.pack()

        with open("Support/subjects.txt", "r") as textfile:#just check for available subjects and store them in dictionary and a list
            a = textfile.read()
        if not textfile.closed :
            textfile.close()
        
        a = a.split()
        sub = {}
        i= 0
        def check(a) :
            for i in range(len(a)) :
                if a[i] == ':' :
                    print i+4 < len(a)
                    if i+4 < len(a) and (a[i + 3] != ":" or ":" in [a[n] for n in range(i+1,i+3)]):
                        return False
            else :
                return True
        if not check(a) :
            print "Unable to load Subjects. Error in ../support/subjects.txt. Correct it manually or clear its contents completely  " + str(time.strftime("%X"))
            self.history += "Unable to load Subjects. Error in ../support/subjects.txt.  " + str(time.strftime("%X"))+"\n"
            check = False
            a = []
            root1 = Tk.Toplevel()# toplevel() required as root() is already in use
            root1.attributes("-topmost", True)
            root1.title("Error")
            w1 = 230
            h1 = 100
            ws1 = root1.winfo_screenwidth()
            hs1 = root1.winfo_screenheight()
            x1 = (ws1/2) - (w1/2)
            y1 = (hs1/2) - (h1/2)
            root1.geometry('%dx%d+%d+%d' % (w1, h1, x1, y1))
            can1 = Tk.Canvas(root1,width = 230,height=100)
            can1.pack()
            im1 = Image.open("backgrounds/250x200.png")
            tkimage1 = ImageTk.PhotoImage(im1)
            Canvas_Image1 = can1.create_image(0,0, image=tkimage, anchor="nw")
                
            canvas_id1 = can1.create_text(15, 10, anchor="nw")
            can1.itemconfig(canvas_id1, text="                     !!WARNING!!\n\n                Unable to load Subjects")
            Tk.Button(root1, text=' OK ', command = root1.destroy).place(x=110,y=70)
           
            root1.wait_window()
        else :
            check = True
            
        while i in range(len(a)) :
            if i +2 < len(a) :
                if a[i+1] == ':' :
                    sub[a[i]] = a[i+2]
                    i += 3

        list_sub = []
        for i in sub :
            temp = [i+ ' (' + sub[i] + ')']
            list_sub.append(temp)

        list_sub.sort()
        main_list = list(list_sub)
        selected = []
        for i in range(len(list_sub)) :
            list_sub[i] = Checkbar(self.root, list_sub[i])
            list_sub[i].pack(side=Tk.TOP,)
            list_sub[i].config(relief=Tk.GROOVE, bd=2)

        def allstates():
           list1 = [i for i in list_sub]
           
           for i in range(len(list1)):
              n = list(list1[i].state())
              for j in range(len(n)):
                 if n[j] == 1:                  
                    selected.append(main_list[i][j])
           self.root.destroy()


        

        if check :
            
            b3 = Tk.Button(self.root,text='Add a subjects', justify =Tk.LEFT,command = self.add_sub_for_workload)
            b2 = Tk.Button(self.root, text = "Next" ,justify =Tk.LEFT,command = allstates)
        else :
            b3 = Tk.Button(self.root,text='Add a subject', justify =Tk.LEFT,command = self.add_sub_for_workload,state = Tk.DISABLED)
            b2 = Tk.Button(self.root,text = "Next" , justify =Tk.LEFT,command = allstates,state = Tk.DISABLED)
        


        b1 = Tk.Button(self.root,text = "Cancel", justify =Tk.LEFT,command = self.restart_app)
        b1.config(activebackground = "SlateGray1")
        b3.config(activebackground = "SlateGray1")
        b3.pack(side=Tk.TOP,padx = 100,pady = 50)
        b1.pack(side=Tk.LEFT,padx = 100)
        b2.config(activebackground = "SlateGray1")
        b2.pack(side=Tk.RIGHT,padx = 100)
        
        
        self.root.mainloop()
        
        return selected

    def work_load(self) :

        sub = self.work_load_screen()
        print sub
        



if __name__ == "__main__" :
    Run_Application = Application(0)#Run the program
sys.exit()










            
