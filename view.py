'''
    Thomas Vanek 
    20.01.2020
'''

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pprint
from time import gmtime, strftime

class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        print("Creating Gui...")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        
        self.chkvars = {}
        self.eventChannel = {}
        self.eventDmxValue = {}
        self.eventSeconds = {}
        self.eventDefaultTo = {}
        self.eventsecondsPerUnit = {}

        self.maskToken = tk.BooleanVar(value=True)

        self.stoplistening = False
        self.eventlist = self.controller.config.collection.eventlist
        self.startText = tk.StringVar(value='Start listening for Events')

        self.vcmd = (self.register(self.onValidate),
        '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.createGui()
        self.resizable(0,0)
        
        

    #functions

        # valid percent substitutions (from the Tk entry man page)
        # note: you only have to register the ones you need; this
        # example registers them all for illustrative purposes
        #
        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %i = index of char string to be inserted/deleted, or -1
        # %P = value of the entry if the edit is allowed
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %v = the type of validation that is currently set
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        # %W = the tk name of the widget
    def onValidate(self, d, i, P, s, S, v, V, W):
        # print("OnValidate:\n")
        # print("d='%s'" % d)
        # print("i='%s'" % i)
        # print("P='%s'" % P)
        # print("s='%s'" % s)
        # print("S='%s'" % S)
        # print("v='%s'" % v)
        # print("V='%s'" % V)
        # print("W='%s'" % W)

        entry = self.nametowidget(W)
        minval = entry.config()['from'][4]
        maxval = entry.config()['to'][4]
        # Check something
        if P is '': return True
        try:
            entered = int(P)
            return ((minval <= entered) and  (entered <= maxval))
        except ValueError:
            return False


    def getOAuthToken(self):
        self.controller.clicked_getToken()

    def btnSecPerUnitClicked(self):
        self.controller.secPerUnitHelp()


    def doStuff(self):
        tk.messagebox.showinfo("Title", "I will do stuff!")
        #self.frmAlerts.configure(state='disable')
        for child in self.frmAlerts.winfo_children():
            self.setState(child)

    def setState(self, widget, state='disabled'):
        #print type(widget)
        try:
            widget.configure(state=state)
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            self.setState(child, state=state)

    def disableAlerts(self,state='disabled'):
        self.setState(self.frmAlerts,state=state)
        self.setState(self.frmChannelconfig,state=state)

        #self.controller.doStuff()
    
    def saveSettings(self):
        self.controller.clicked_save()
    
    def startListening(self):
        #self.controller.start_listening(self.followerDmxChannel.get())
        self.controller.start_listening(stop=self.stoplistening)
    
    def changeStartButton(self):
        if self.stoplistening:
            self.stoplistening=False
            self.startText.set("Start listening for Events")
        else:
            self.stoplistening=True
            self.startText.set("Stop listening for Events")
        

    def on_exit(self):
        self.controller.on_exit()
        self.destroy()

    def cklicked_mask(self):
        if self.maskToken.get():
            self.entrOAuthToken.config(show='*')
        else:
            self.entrOAuthToken.config(show='')

    def createGui(self):

        # Create windows object
        #app = tk.Tk()

        #variables
        #self.followerDmxChannel = tk.IntVar(self,2)
        #self.followerDmxChannel = tk.IntVar(self,self.controller.config.ini['follow']['dmxchannel'])

        #channelconfig
        self.comport = tk.StringVar(value=self.controller.config.collection.data['communication']['port'])
        self.sockettoken = tk.StringVar(value=self.controller.config.collection.data['token']['sockettoken'])
        
        title="Chron-O-John's Twitch(streamlabs) DMX Alerts"
        self.title(title)

        canvas=tk.Frame(self,padx=10,pady=10)

        lblUeberschrift = tk.Label(canvas, text=title, font=('bold',16), pady=20)

        self.frmChannelconfig= tk.Frame(canvas)

        frmPortConfig = tk.Frame(self.frmChannelconfig)
        lblPort = tk.Label(frmPortConfig, text="Port of your RS485 adaptor: ")
        choices = (self.comport.get(),'COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','COM10','COM11','COM12','COM13','COM14','COM15')
        menPort = ttk.OptionMenu(frmPortConfig, self.comport, *choices)
        menPort.config(width=7)

        frmTokenConfig = tk.Frame(self.frmChannelconfig)
        lblOAuthToken = tk.Label(frmTokenConfig, text="Your Socket API Token")
        self.entrOAuthToken = ttk.Entry(frmTokenConfig, show="*", textvariable=self.sockettoken, width=70, justify='right')
        #self.entrOAuthToken = tk.Entry(frmTokenConfig, textvariable=self.sockettoken , justify='right')
        btnGetToken = tk.Button(frmTokenConfig, text="Get OAuth-Token", command=self.getOAuthToken)
        chkMask = tk.Checkbutton(frmTokenConfig, text='Mask',anchor='w',variable=self.maskToken, command=self.cklicked_mask)

        lblAlertWhen = tk.Label(canvas, text="Alert:", height=2, anchor='s')

        self.frmAlerts = tk.Frame(canvas)

        #eventlist=['follow','subscription','resub','prime_sub_gift', 'host','bits','raids','donation']
        eventlist=self.eventlist
        print(eventlist)

        frmEvent = {}
        chkEvent = {}
        spinEventChannel = {}
        lblEventDMXValue = {}
        spinEventValue = {}
        lblEventSeconds = {}
        spinEventSeconds = {}
        lblEventDefaultTo = {}
        spinEventDefaultTo = {}
        chkPerUnit={}
        btnSecPerUnit={}


        for idx,eventname in enumerate(eventlist):

            frmEvent[eventname] = tk.Frame(self.frmAlerts)
            
            # self.chkvars[eventname]= self.controller.config.data
            # print(f"Alert in config: {self.controller.config.collection.data[eventname]['alert']}") 
            # print(f"Collection data of:{eventname}")
            # pprint.pprint(self.controller.config.collection.data[eventname])^

            #set Variables
            self.chkvars[eventname]=tk.BooleanVar(value=self.controller.config.collection.data[eventname]['alert'])
            self.eventChannel[eventname] = tk.IntVar(value=self.controller.config.collection.data[eventname]['dmxchannel'])
            self.eventDmxValue[eventname] = tk.IntVar(value=self.controller.config.collection.data[eventname]['dmxvalue'])
            self.eventSeconds[eventname] = tk.DoubleVar(value=self.controller.config.collection.data[eventname]['seconds'])
            self.eventDefaultTo[eventname] = tk.IntVar(value=self.controller.config.collection.data[eventname]['default'])
            if 'secondsperunit' in self.controller.config.collection.data[eventname]:
                self.eventsecondsPerUnit[eventname] = tk.BooleanVar(value=self.controller.config.collection.data[eventname]['secondsperunit'])
                chkPerUnit[eventname] = tk.Checkbutton(frmEvent[eventname], text=f"use seconds per unit", anchor='w',variable=self.eventsecondsPerUnit[eventname])
                spinSecIncrement=0.1
                btnSecPerUnit[eventname] = tk.Button(frmEvent[eventname], text="?", width=2, command=self.btnSecPerUnitClicked)
            else:
                spinSecIncrement=1

            chkEvent[eventname] = tk.Checkbutton(frmEvent[eventname], text=f"New {eventname.replace('_',' ')} to DMX Channel",width=28, anchor='w',variable=self.chkvars[eventname])
            spinEventChannel[eventname] = tk.Spinbox(frmEvent[eventname], justify='right', from_=1, to=512, width=3, textvariable=self.eventChannel[eventname],validate="key", validatecommand=self.vcmd)
            lblEventDMXValue[eventname] = tk.Label(frmEvent[eventname], text="with value")
            spinEventValue[eventname] = tk.Spinbox(frmEvent[eventname], justify='right', from_=0, to=255, width=3, textvariable=self.eventDmxValue[eventname])
            lblEventSeconds[eventname] = tk.Label(frmEvent[eventname], text="for")
            spinEventSeconds[eventname] = tk.Spinbox(frmEvent[eventname], justify='right', from_=0, to=300, width=3,increment=spinSecIncrement, textvariable=self.eventSeconds[eventname])
            lblEventDefaultTo[eventname] = tk.Label(frmEvent[eventname], text="seconds, then set to")
            spinEventDefaultTo[eventname] = tk.Spinbox(frmEvent[eventname], justify='right', from_=0, to=255, width=3, textvariable=self.eventDefaultTo[eventname])

            #place Elements
            frmEvent[eventname].grid(row=idx, sticky='w')
            chkEvent[eventname].pack(side='left')
            spinEventChannel[eventname].pack(side='left')
            lblEventDMXValue[eventname].pack(side='left')
            spinEventValue[eventname].pack(side='left')
            lblEventSeconds[eventname].pack(side='left')
            spinEventSeconds[eventname].pack(side='left')
            lblEventDefaultTo[eventname].pack(side='left')
            spinEventDefaultTo[eventname].pack(side='left')
            if eventname in chkPerUnit:
                chkPerUnit[eventname].pack(side='left')
                btnSecPerUnit[eventname].pack(side='left')

        frmBottomButtons = tk.Frame(canvas)
        btnSaveConfig = tk.Button(frmBottomButtons, text="Save all settings",command=self.saveSettings, padx=3)
        btnDoStuff = tk.Button(frmBottomButtons, text="Do Stuff", command=self.doStuff, padx=3)
        btnStartListening = tk.Button(frmBottomButtons, textvar=self.startText, command=self.startListening, padx=3)

        #debugwindow
        frmList = tk.Frame(canvas)
        self.debugList = tk.Listbox(frmList)
        scrollbar = tk.Scrollbar(frmList, orient="vertical")
        scrollbar.config(command=self.debugList.yview)
        

        self.debugList.config(yscrollcommand=scrollbar.set)


        #pack the stuff
        canvas.pack()

        lblUeberschrift.grid(row=10)

        self.frmChannelconfig.grid(row=20, sticky='w')
        frmPortConfig.grid(row=21, sticky='w')
        frmTokenConfig.grid(row=22, sticky='w')
        lblPort.pack(side='left')
        #entrChannelname.pack(side='left')
        menPort.pack(side='left')
        lblOAuthToken.pack(side='left')
        self.entrOAuthToken.pack(side='left',padx=5)
        btnGetToken.pack(side='left')
        chkMask.pack(side='left')

        lblAlertWhen.grid(row=30, sticky='w')

        self.frmAlerts.grid(row=40, sticky='w')
        
        frmBottomButtons.grid(row=60, column=0, sticky=('w','e'), pady=4)
        btnSaveConfig.pack(side='left')
        #btnDoStuff.pack(side='left',padx=10)
        btnStartListening.pack(side='right')

        #debugtext
        frmList.grid(row=90, sticky=('n', 's', 'e', 'w'))
        scrollbar.pack(side='right',fill='y')
        self.debugList.pack(side='left',fill='both',expand=True)
        #self.debugList.grid(row=90, sticky=('n', 's', 'e', 'w'))
        #scrollbar.grid(row=90, sticky=('n', 's', 'e', 'w'))
        

    def addToList(self,text,withTime=True):
        datetime = ""
        if withTime: datetime = strftime("%H:%M:%S", gmtime()) + " - "
        self.debugList.insert(0,datetime+text)

    def updateConfigData(self):
        #self.controller.config.collection.data[eventname]
        self.controller.config.collection.data['communication']['port'] = self.comport.get()
        self.controller.config.collection.data['token']['sockettoken'] = self.sockettoken.get()

        for eventname in self.eventlist:
            self.controller.config.collection.data[eventname]['alert'] = self.chkvars[eventname].get()
            self.controller.config.collection.data[eventname]['dmxchannel'] = self.eventChannel[eventname].get()
            self.controller.config.collection.data[eventname]['dmxvalue'] = self.eventDmxValue[eventname].get()
            self.controller.config.collection.data[eventname]['seconds'] = self.eventSeconds[eventname].get()
            self.controller.config.collection.data[eventname]['default'] = self.eventDefaultTo[eventname].get()
            if 'secondsperunit' in self.controller.config.collection.data[eventname]:
                self.controller.config.collection.data[eventname]['secondsperunit'] = self.eventsecondsPerUnit[eventname].get()
        pass

        # self.chkvars = {}
        # self.eventChannel = {}
        # self.eventDmxValue = {}
        # self.eventSeconds = {}
        # self.eventDefaultTo = {}
        # self.eventsecondsPerUnit = {}

#set Variables
# self.chkvars[eventname]=tk.BooleanVar(value=self.controller.config.collection.data[eventname]['alert'])
# self.eventChannel[eventname] = tk.IntVar(value=self.controller.config.collection.data[eventname]['dmxchannel'])
# self.eventDmxValue[eventname] = tk.IntVar(value=self.controller.config.collection.data[eventname]['dmxvalue'])
# self.eventSeconds[eventname] = tk.IntVar(value=self.controller.config.collection.data[eventname]['seconds'])
# self.eventDefaultTo[eventname] = tk.IntVar(value=self.controller.config.collection.data[eventname]['default'])
# if 'secondsperunit' in self.controller.config.collection.data[eventname]:
#     self.eventsecondsPerUnit[eventname] = tk.BooleanVar(value=self.controller.config.collection.data[eventname]['secondsperunit'])
#     chkPerUnit[eventname] = tk.Checkbutton(frmEvent[eventname], text=f"use seconds per unit",width=27, anchor='w',variable=self.eventsecondsPerUnit[eventname])
