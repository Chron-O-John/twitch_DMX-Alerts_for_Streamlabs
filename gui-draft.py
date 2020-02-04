import tkinter as tk
from tkinter import messagebox


class DMXApp(tk.Tk):
    #functions
    def getOAuthToken(self):
        messagebox.showinfo("Title", "a Tk MessageBox")


    def doStuff(self):
        messagebox.showinfo("Title", "I did stuff!")

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        # Create windows object
        app = tk.Tk()

        #variables
        #channelconfig
        ChannelName = tk.StringVar(value='Krogmann')
        OAuthToken = tk.StringVar(value='Press Button to get Token')

        CheckTime = tk.IntVar(value=1)
        #for Follower alert
        Alertwhenfollower = tk.IntVar(value=1)
        FollowerDMXChannel = tk.IntVar(value=1)
        FollowerDMXValue = tk.IntVar(value=255)
        FollowerDMXSeconds = tk.IntVar(value=5)
        FollowerDMXDefault = tk.IntVar(value=0)
        #for Subscriber alert
        AlertwhenSubscriber = tk.IntVar(value=1)
        SubscriberDMXChannel = tk.IntVar(value=1)
        SubscriberDMXValue = tk.IntVar(value=255)
        SubscriberDMXSeconds = tk.IntVar(value=5)
        SubscriberDMXDefault = tk.IntVar(value=0)

        app.title("Chron-O-John's Twitch DMX Alerts")

        canvas=tk.Frame(app,padx=10,pady=10)

        lblUeberschrift = tk.Label(canvas, text="Twitch DMX Alerts", font=('bold',16), pady=20)

        frmChannelconfig= tk.Frame(canvas)
        lblChannelname = tk.Label(frmChannelconfig, text="Channelname")
        entrChannelname = tk.Entry(frmChannelconfig, textvariable=ChannelName, justify='right')
        lblOAuthToken = tk.Label(frmChannelconfig, text="OAuth-Token")
        entrOAuthToken = tk.Entry(frmChannelconfig, textvariable=OAuthToken, justify='right')
        btnGetToken = tk.Button(frmChannelconfig, text="Get OAuth-Token", command=self.getOAuthToken)

        lblAlertWhen = tk.Label(canvas, text="Alert:", height=2, anchor='s')

        frmAlerts = tk.Frame(canvas)
        #Follower Line
        frmFollower = tk.Frame(frmAlerts)
        chkFollower = tk.Checkbutton(frmFollower, text="New Follower to DMX Channel",width=25, anchor='w', variable=Alertwhenfollower)
        spinFollowerChannel = tk.Spinbox(frmFollower, justify='right', from_=1, to=512, width=3, textvariable=FollowerDMXChannel)
        lblFollowerDMXValue = tk.Label(frmFollower, text="with value")
        spinFollowerValue = tk.Spinbox(frmFollower, justify='right', from_=0, to=255, width=3, textvariable=FollowerDMXValue)
        lblFollowerSeconds = tk.Label(frmFollower, text="for")
        spinFollowerSeconds = tk.Spinbox(frmFollower, justify='right', from_=0, to=300, width=3, textvariable=FollowerDMXSeconds)
        lblFollowerDefaultTo = tk.Label(frmFollower, text="seconds, then default to")
        spinFollowerDefaultTo = tk.Spinbox(frmFollower, justify='right', from_=0, to=255, width=3, textvariable=FollowerDMXDefault)

        #subscriber line
        frmSubscriber = tk.Frame(frmAlerts)
        chkSubscriber = tk.Checkbutton(frmSubscriber, text="New Subscriber to DMX Channel", width=25,anchor='w', variable=AlertwhenSubscriber)
        spinSubscriberChannel = tk.Spinbox(frmSubscriber, justify='right', from_=1, to=512, width=3, textvariable=SubscriberDMXChannel)
        lblSubscriberDMXValue = tk.Label(frmSubscriber, text="with value")
        spinSubscriberValue = tk.Spinbox(frmSubscriber, justify='right', from_=0, to=255, width=3, textvariable=SubscriberDMXValue)
        lblSubscriberSeconds = tk.Label(frmSubscriber, text="for")
        spinSubscriberSeconds = tk.Spinbox(frmSubscriber, justify='right', from_=0, to=300, width=3, textvariable=SubscriberDMXSeconds)
        lblSubscriberDefaultTo = tk.Label(frmSubscriber, text="seconds, then default to")
        spinSubscriberDefaultTo = tk.Spinbox(frmSubscriber, justify='right', from_=0, to=255, width=3, textvariable=SubscriberDMXDefault)

        frmCheckTime = tk.Frame(canvas, pady=5)
        lblChecktime = tk.Label(frmCheckTime,text='Check for new Followers/Subscribery every ')
        spinCheckTime = tk.Spinbox(frmCheckTime, justify='right', from_=0, to=60, width=2, textvariable=CheckTime)
        lblCheckTimeAfter = tk.Label(frmCheckTime,text=' seconds')

        btnSaveConfig = tk.Button(canvas, text="Save all settings") #toDo: addd Command
        btnDoStuff = tk.Button(canvas, text="Do Stuff", command=self.doStuff)

        #debugwindow
        debugList = tk.Listbox(canvas)

        #pack the stuff
        canvas.pack()

        lblUeberschrift.grid(row=10)

        frmChannelconfig.grid(row=20, sticky='w')
        lblChannelname.pack(side='left')
        entrChannelname.pack(side='left')
        lblOAuthToken.pack(side='left')
        entrOAuthToken.pack(side='left')
        btnGetToken.pack(side='left')

        lblAlertWhen.grid(row=30, sticky='w')

        frmAlerts.grid(row=40, sticky='w')
        #follower Line
        frmFollower.grid(row=0)
        chkFollower.pack(side='left')
        spinFollowerChannel.pack(side='left')
        lblFollowerDMXValue.pack(side='left')
        spinFollowerValue.pack(side='left')
        lblFollowerSeconds.pack(side='left')
        spinFollowerSeconds.pack(side='left')
        lblFollowerDefaultTo.pack(side='left')
        spinFollowerDefaultTo.pack(side='left')
        #subscriber Line
        frmSubscriber.grid(row=1)
        chkSubscriber.pack(side='left')
        spinSubscriberChannel.pack(side='left')
        lblSubscriberDMXValue.pack(side='left')
        spinSubscriberValue.pack(side='left')
        lblSubscriberSeconds.pack(side='left')
        spinSubscriberSeconds.pack(side='left')
        lblSubscriberDefaultTo.pack(side='left')
        spinSubscriberDefaultTo.pack(side='left')

        #checktime
        frmCheckTime.grid(row=50, column=0, sticky='w')
        lblChecktime.pack(side='left')
        spinCheckTime.pack(side='left')
        lblCheckTimeAfter.pack(side='left')

        btnSaveConfig.grid(row=60, column=0, sticky='w')
        btnDoStuff.grid(row=61, column=0, sticky='w')

        #debugtext
        debugList.grid(row=90, sticky=('n', 's', 'e', 'w'))

