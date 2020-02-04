'''
    Thomas Vanek 
    20.01.2020
    verion 0.1
'''

from model import Model
from view import View
from configHandler import ConfigHandler
#import logging as lg
import socketio
import threading
import webbrowser as webbrowser
import serial

import tkinter as tk

class Controller:
    def __init__(self):
        super().__init__()

        #self.url = "https://sockets.streamlabs.com/socket.io/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkYwNzBBNUZDQjhDN0UxQzY5MDEwIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiNDMyMjk0NDg2In0.RCu48_ocKe_4nSmz1ZniDT0rB-ezIX1TJh5cpRSLz1g"

        #lg.basicConfig(level=lg.ERROR)


        self.config = ConfigHandler()
        self.model = Model(self)
        self.view = View(self)
        self.sio = socketio.Client()
        

        

    def main(self):
        print("In Main Controller")
        self.view.mainloop()

    def secPerUnitHelp(self):
        tk.messagebox.showinfo("Help", "Seconds per Unit means:\n\nThe actual ammount of seconds an alert is beeing send to the specified DMX channel is multiplied by the ammount of Bits/Currency (whole $/€ - not cents)\n\nFor example: Alert is set to 0.2 seconds and someone sent 30 Bits.\n\nDuration of alert is 0.2 seconds * 30 = 6 seconds")
    
    def doStuff(self):
        #print(self.config.ini['follow']['dmxchannel'])
        self.dmxstartstop()
        #self.startSocketListener()
        pass


    def dmxstartstop(self):
        #print("contr - dmxstartstop called")
        self.model.dmxstartstop(frequency=20)

    def start_listening(self,stop=False):
        #print(f"contr - startlistening called")
        self.view.updateConfigData()
        if stop==False:
            try:
                self.model.dmxstartstop(frequency=20,port=self.config.collection.data['communication']['port'])
                self.startSocketListener()
                self.view.disableAlerts(state='disabled')
                self.view.changeStartButton()
                self.view.addToList("Started listening...")
            except serial.serialutil.SerialException as e:
                tk.messagebox.showerror("Error",str(e))
            except BaseException as ex:
                tk.messagebox.showerror("Error",str(ex))

        else:
            self.view.disableAlerts(state='normal')
            self.sio.disconnect()
            self.model.dmxstartstop(onlystop=True)
            self.view.changeStartButton()
            self.view.addToList("Stopped listeneing...")

    def clicked_save(self):
        self.view.updateConfigData()
        self.config.saveData()
        tk.messagebox.showinfo("Save...", "Settings saved")
    
    def clicked_getToken(self):
        message = ("In order to get the token do the following:\n\n\n"
        " - Go to Streamlabs Dashboard -> Settings -> API Settings\n  (Browser should open automatically afer you've clicked yes)\n\n"
        " - Go to \"API Settings\"\n\n"
        " - Copy the Socket API Token (the longer one) into the textfield left to the Button you've just clicked\n\n"
        "ATTENTION: Be absolutely sure that the token is correct, as it is not checked for now.\n"
        "If the Socket API Token is not correct you will NOT receive any events!\n\n"
        "Continue with opening you Browser?")

        MsgBox = tk.messagebox.askquestion ('Get API Token',message)
        if MsgBox == 'yes':
            webbrowser.open('https://streamlabs.com/dashboard/#/settings/api-settings', new=1)

    def on_exit(self):
        self.model.dmxstartstop(onlystop=True)
        self.sio.disconnect()
        print("exiting....")

    ###########
    # Websocket stuff
    ###########w
    def startSocketListener(self):
        url_prefix= 'https://sockets.streamlabs.com/socket.io/?token='
        url_with_token= url_prefix + self.config.collection.data['token']['sockettoken']
        self.sio.on('event', self.message_handler)
        # self.wst = threading.Thread(target=self.sio.connect(url_with_token))
        # self.wst.daemon = True
        # self.wst.start()
        self.sio.connect(url_with_token)
        
    #when socket.io message "event" is received (defined with sio.on 'eventname')
    def message_handler(self,msg):
        #print('Received message, type= ',msg['type'])
        self.view.addToList('Received message, type: '+msg['type'])
        self.model.got_message(msg,self.config.collection.eventlist)

        

if __name__ == '__main__':
    print("Started...")
    dmxApp=Controller ()
    dmxApp.main()