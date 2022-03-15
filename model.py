'''
    Thomas Vanek 
    20.01.2020
'''
from dmx import Dmx
import time
import queue
import threading

class Model:

    def __init__(self,controller):
        super().__init__()
        self.controller = controller
        #self.dmx = Dmx(daemon=True, frequency=1)


    def dmxstartstop(self,frequency=1, onlystop=False, port='COM3'):
        print(f"model - dmxstartstop called with port: {port}")
        print(hasattr(self,'dmx'))

        if not hasattr(self,'dmx'):
            if onlystop:
                return
            else:
                self.dmx = Dmx(daemon=True, frequency=frequency,COM=port)
                self.dmx_worker = self.Dmx_Worker(self.dmx)

        if self.dmx.is_alive():
            self.dmx_worker.stop()
            self.dmx.stop()
            del self.dmx
            del self.dmx_worker
        elif not onlystop:
            self.dmx.start()
            self.dmx_worker.start()

    def got_message(self,msg,eventlist):
        #eventlist=('follow','subscription','resub','prime_sub_gift', 'host','bits','raids','donation')
        print('Received message: ', msg)
        msgtype = msg['type']
        if msgtype in eventlist:
            # self.chkvars[eventname]=tk.BooleanVar(value=self.controller.config.collection.data[eventname]['alert'])
            # self.eventChannel[eventname] = tk.IntVar(value=self.controller.config.collection.data[eventname]['dmxchannel'])
            # self.eventDmxValue[eventname] = tk.IntVar(value=self.controller.config.collection.data[eventname]['dmxvalue'])
            # self.eventSeconds[eventname] = tk.DoubleVar(value=self.controller.config.collection.data[eventname]['seconds'])
            # self.eventDefaultTo[eventname] = tk.IntVar(value=self.controller.config.collection.data[eventname]['default'])
            print(f"Found known event-type: {msgtype}")
            if self.controller.config.collection.data[msgtype]['alert']:
                dmx_settings = {}
                dmx_settings['channel'] = self.controller.config.collection.data[msgtype]['dmxchannel']
                dmx_settings['value'] = self.controller.config.collection.data[msgtype]['dmxvalue']
                dmx_settings['seconds'] = self.controller.config.collection.data[msgtype]['seconds']
                dmx_settings['fallback'] = self.controller.config.collection.data[msgtype]['default']
                if 'secondsperunit' in (self.controller.config.collection.data[msgtype]):
                    if self.controller.config.collection.data[msgtype]['secondsperunit']:
                        dmx_settings['multiplier'] = msg['message'][0]['amount']
                    else:
                        dmx_settings['multiplier'] = 1
                else:
                    dmx_settings['multiplier'] = 1
                pass
            self.controller.view.addToList(f"Setting DMX-Channel {dmx_settings['channel']} to {dmx_settings['value']} for {dmx_settings['seconds']}*{dmx_settings['multiplier']} = {float(dmx_settings['seconds'])*float(dmx_settings['multiplier'])} seconds, then back to {dmx_settings['fallback']}")
            self.dmx_worker.q.put(dmx_settings)

        else:
            print(f"Unknown event-type: {msg['type']}")
            self.controller.view.addToList(f"Unknown event-type: {msg['type']}")

    # async def do_dmx(self,channel,value,seconds,fallback,multiplier=1):
    #     self.dmx.set_data(channel,value)
    #     asyncio.sleep(seconds*multiplier)
    #     self.dmx.set_data(channel,fallback)
    #     pass

    
    class Dmx_Worker(threading.Thread):
        
        def __init__(self,dmx,*args,runSemaphore=True,**kwargs):
            super().__init__(*args,**kwargs)
            self.dmx = dmx
            self.q = queue.Queue()
            self.runSemaphore = runSemaphore

        def run(self):
            print("DMX_WORKER started")
            while True:
                item = self.q.get()
                if item == None: break #exit when queue receives item with value NONE from stop() function
                print(f'New Worker Item: {item}')
                self.dmx.set_data(item['channel'],item['value'])
                time.sleep(float(item['seconds']) * float(item['multiplier']))
                self.dmx.set_data(item['channel'],item['fallback'])
        
        def stop(self):
            print("Worker stop called")
            self.q.put(None)
