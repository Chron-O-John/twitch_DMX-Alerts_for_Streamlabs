import configparser
import pprint



class ConfigHandler():
    
    def __init__(self,filename='dmxSettings.ini'):
        super().__init__()
        self.filename = filename
        self.ini = configparser.ConfigParser()
        self.ini.read(self.filename)
        self.eventlist=('follow','subscription','resub','prime_sub_gift', 'host','bits','raids','donation')
        self.collection = ConfigCollection(self.ini,self.eventlist)
    
    # def saveSettings(self):
    #     with open(self.filename, 'w') as configfile:
    #         self.ini.write(configfile)

    def getCollection(self):
        return(self.collection)
    
    def saveData(self):
        for section in self.collection.data:
            #print(f'--- {section} ---')
            for option in self.collection.data[section]:
                #print(f'{option}: {self.collection.data[section][option]}')
                self.ini.set(section,option,str(self.collection.data[section][option]))
                with open(self.filename, 'w') as configfile:
                    self.ini.write(configfile)

class ConfigCollection():
    def __init__(self,configparser,eventlist):
        super().__init__() 
        self.ini = configparser
        self.data = {}
        self.eventlist=eventlist
        self.populateCollection(eventlist)

    def populateCollection(self,eventlist):

        self.data['token']={'sockettoken': self.ini.get('token','sockettoken')}
        self.data['communication']={'port': self.ini.get('communication','port')}

        self.eventList=eventlist

        #all the common alert-settings
        for section in self.eventList:
            self.data[section]= {'dmxchannel': self.ini.getint(section,'dmxchannel'),
            'dmxvalue': self.ini.getint(section,'dmxvalue'),
            'seconds': self.ini.getfloat(section,'seconds'),
            'default': self.ini.getint(section,'default'),
            'alert' : self.ini.getboolean(section,'alert')}
        
        #special settings
        self.data['bits']['secondsperunit']=self.ini.getboolean('bits','secondsperunit')
        self.data['donation']['secondsperunit']=self.ini.getboolean('donation','secondsperunit')
        # print("Populated data with:")
        # pprint.pprint(self.data)

    
if __name__ == '__main__':
    config = ConfigHandler("dmxSettings.ini")
    # config.ini['follow']['dmxchannel']=str(1)
    # config.saveSettings()
    # testlist = config.ini.sections()
    # print(testlist)
    # for x in config.ini.sections():
    #     print(f"Section: {x}")
    #     print(config.ini.items(x))
    coll=config.getCollection().data
    #print(coll['token']['sockettoken'])
    #print(coll['test'])
    pprint.pprint(coll)