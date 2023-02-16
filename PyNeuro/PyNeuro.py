"""
@Author Zach Wang
@Date 2021.9.27
@Version 1.2.1
"""
import json
from telnetlib import Telnet
from threading import Thread
from collections import namedtuple
from collections import OrderedDict

# Define a namedtuple
Status = namedtuple("Status", ["description", "icon"])

class MWM2_Status(Status):
    CONNECTED = "connected"
    FITTING1  = "st_fitting1"
    FITTING2  = "st_fitting2"
    FITTING3  = "st_fitting3"
    NOSIGNAL  = "nosignal"

class PyNeuro:
    """
    This is a NeuroPy-like library, to get data from the Mindwave Mobile 2,
    a EEG device manufactured by Neurosky.

    Initialising:

        object1 = PyNeuro()

    After initialising , if required the callbacks must be set. Then using
    the start() method the library will start fetching data from headset:
    
        object1.start()
    
    Similarly, the close() method can be called to stop fetching data:
    
        object1.close()

    Requirements:
    
      - Telnet
      - ThinkGear Connector

    """

    status_def = OrderedDict()
    status_def[MWM2_Status.CONNECTED] = MWM2_Status("Conectado! Sinal de qualidade ótima","icons/connected_v1.png")
    status_def [MWM2_Status.FITTING1] = MWM2_Status("Sintonizando headset... (fase 1 de 3)","icons/connecting1_v1.png")
    status_def [MWM2_Status.FITTING2] = MWM2_Status("Sintonizando headset... (fase 2 de 3)","icons/connecting2_v1.png")
    status_def [MWM2_Status.FITTING3] = MWM2_Status("Sintonizando headset... (fase 3 de 3)","icons/connecting3_v1.png")
    status_def [MWM2_Status.NOSIGNAL] = MWM2_Status("Desconectado, sem qualquer sinal","icons/nosignal_v1.png")

    '''TODO translation support
    [PyNeuro] Connecting TCP Socket Host...
    [PyNeuro] Scanning device..
    [PyNeuro] Fitting Device..
    [PyNeuro] Successfully Connected ..
    [PyNeuro] Connection lost, trying to reconnect..
    '''

    status_def_at = list(status_def.values())

    '''
    To get object a Status containing utility strings:

        print(PyNeuro.status[MWM2_Status.FITTING1])  # or

    Or by an ordered index:

        print(PyNeuro.status_at[1])  # 0-4 (the 5 values)

    '''

    __attention = 0
    __meditation = 0
    __blinkStrength = 0
    __status = "NotConnected"

    __delta = 0
    __theta = 0
    __lowAlpha = 0
    __highAlpha = 0
    __lowBeta = 0
    __highBeta = 0
    __lowGamma = 0
    __highGamma = 0

    __attention_records = []
    __meditation_records = []
    __blinkStrength_records = []

    __packetsReceived = 0
    __telnet = None

    __attention__callbacks = []
    __meditation__callbacks = []
    __blinkStrength__callbacks = []

    __delta__callbacks = []
    __theta__callbacks = []
    __lowAlpha__callbacks = []
    __highAlpha__callbacks = []
    __lowBeta__callbacks = []
    __highBeta__callbacks = []
    __lowGamma__callbacks = []
    __highGamma__callbacks = []

    '''Changing status callbacks'''
    __connect__callbacks = []
    __disconnect__callbacks = []
    #TODO? scanning
    #TODO? fitting

    callBacksDictionary = {}  # keep a track of all callbacks

    def __init__(self):
        self.__parserThread = None
        self.__threadRun = False
        self.__connected = False

    def connect(self):
        """
        Connect the TCP socket via Telnet.
        """
        try:
            if self.__telnet is None:
                self.__telnet = Telnet('localhost', 13854)
                self.__telnet.write(b'{"enableRawOutput": true, "format": "Json"}');
                print("[PyNeuro] Connecting TCP Socket Host...")
        except ConnectionRefusedError as cre:
            print("[PyNeuro]", cre.strerror)
            print("[PyNeuro]", "Perhaps the ThinkGear Connect (TGC) is not running")

    def disconnect(self):
        """
        Disconnect the TCP socket.
        """
        if self.__telnet is not None:
            self.__telnet.close()
            print("[PyNeuro] Disconnect TCP Socket.")

        for callback in self.__disconnect__callbacks:
            callback()

    def start(self):
        """
        Start Service.
        :return:
        """

        self.__parserThread = Thread(target=self.__packetParser, args=())
        self.__threadRun = True
        self.__parserThread.start()

    def close(self):
        """
        Close Service.
        :return:
        """
        self.__threadRun = False
        self.__parserThread.join()

    def __packetParser(self):
        try:
            while True:
                line = self.__telnet.read_until(b'\r');
                if len(line) > 20:
                    try:
                        raw_str = (str(line).rstrip("\\r'").lstrip("b'"))
                        data = json.loads(raw_str)
                        if "status" in data.keys():
                            if self.__status != data["status"]:
                                self.__status = data["status"]
                                if data["status"] == "scanning":
                                    print("[PyNeuro] Scanning device..")
                                else:
                                    print("[PyNeuro] Connection lost, trying to reconnect..")
                        else:
                            if "eSense" in data.keys():
                                #print(data["eegPower"])
                                if data["eSense"]["attention"] + data["eSense"]["meditation"] == 0:
                                    if self.__status != "fitting":
                                        self.__status = "fitting"
                                        print("[PyNeuro] Fitting Device..")

                                else:
                                    if self.__status != "connected":
                                        self.__status = "connected"
                                        for callback in self.__connect__callbacks:
                                            callback()
                                        print("[PyNeuro] Successfully Connected ..")
                                    self.attention = data["eSense"]["attention"]
                                    self.meditation = data["eSense"]["meditation"]
                                    self.theta = data['eegPower']['theta']
                                    self.delta = data['eegPower']['delta']
                                    self.lowAlpha = data['eegPower']['lowAlpha']
                                    self.highAlpha = data['eegPower']['highAlpha']
                                    self.lowBeta = data['eegPower']['lowBeta']
                                    self.highBeta = data['eegPower']['highBeta']
                                    self.lowGamma = data['eegPower']['lowGamma']
                                    self.highGamma = data['eegPower']['highGamma']
                                    self.__attention_records.append(data["eSense"]["attention"])
                                    self.__attention_records.append(data["eSense"]["meditation"])
                            elif "blinkStrength" in data.keys():
                                self.blinkStrength = data["blinkStrength"]
                                self.__blinkStrength_records.append(data["blinkStrength"])
                    except:
                        print("[PyNeuro] error")
        except:
            print("[PyNeuro] Stop Packet Parser")

    def set_connect_callback(self, callback):
        """
        Set callback function on connect
        :param callback: function()
        """

        self.__connect__callbacks.append(callback)

    def set_attention_callback(self, callback):
        """
        Set callback function of attention value
        :param callback: function(attention: int)
        """

        self.__attention__callbacks.append(callback)

    def set_meditation_callback(self, callback):
        """
        Set callback function of meditation value
        :param callback: function(meditation: int)
        """

        self.__meditation__callbacks.append(callback)

    def set_blinkStrength_callback(self, callback):
        """
        Set callback function of blinkStrength value
        :param callback: function(blinkStrength: int)
        """

        self.__blinkStrength__callbacks.append(callback)

    def set_delta_callback(self, callback):

        self.__delta__callbacks.append(callback)

    def set_theta_callback(self, callback):

        self.__theta__callbacks.append(callback)

    def set_lowAlpha_callback(self, callback):

        self.__lowAlpha__callbacks.append(callback)

    def set_highAlpha_callback(self, callback):

        self.__highAlpha__callbacks.append(callback)

    def set_lowBeta_callback(self, callback):

        self.__lowBeta__callbacks.append(callback)

    def set_highBeta_callback(self, callback):

        self.__highBeta__callbacks.append(callback)

    def set_lowGamma_callback(self, callback):

        self.__lowGamma__callbacks.append(callback)

    def set_highGamma_callback(self, callback):

        self.__highGamma__callbacks.append(callback)


    # attention
    @property
    def attention(self):
        """Get value for attention"""
        return self.__attention

    @attention.setter
    def attention(self, value):
        self.__attention = value
        # if callback has been set, execute the function
        if len(self.__attention__callbacks) != 0:
            for callback in self.__attention__callbacks:
                callback(self.__attention)

    # meditation
    @property
    def meditation(self):
        """Get value for meditation"""
        return self.__meditation

    @meditation.setter
    def meditation(self, value):
        self.__meditation = value
        # if callback has been set, execute the function
        if len(self.__meditation__callbacks) != 0:
            for callback in self.__meditation__callbacks:
                callback(self.__meditation)

    # blinkStrength
    @property
    def blinkStrength(self):
        """Get value for blinkStrength"""
        return self.__blinkStrength

    @blinkStrength.setter
    def blinkStrength(self, value):
        self.__blinkStrength = value
        # if callback has been set, execute the function
        for callback in self.__blinkStrength__callbacks:
            callback(self.__blinkStrength)

    @property
    def delta(self):
        """Get value for delta"""
        return self.__delta

    @delta.setter
    def delta(self, value):
        self.__delta = value
        # if callback has been set, execute the function
        for callback in self.__delta__callbacks:
            callback(self.__delta)

    @property
    def theta(self):
        """Get value for theta"""
        return self.__theta

    @theta.setter
    def theta(self, value):
        self.__theta = value
        # if callback has been set, execute the function
        for callback in self.__theta__callbacks:
            callback(self.__theta)

        # lowBeta
        # lowAlpha

    @property
    def lowAlpha(self):
        """Get value for lowAlpha"""
        return self.__lowAlpha

    @lowAlpha.setter
    def lowAlpha(self, value):
        self.__lowAlpha = value
        # if callback has been set, execute the function
        for callback in self.__lowAlpha__callbacks:
            callback(self.__lowAlpha)

    # highAlpha
    @property
    def highAlpha(self):
        """Get value for highAlpha"""
        return self.__highAlpha

    @highAlpha.setter
    def highAlpha(self, value):
        self.__highAlpha = value
        # if callback has been set, execute the function
        for callback in self.__highAlpha__callbacks:
            callback(self.__highAlpha)

    @property
    def lowBeta(self):
        """Get value for lowBeta"""
        return self.__lowBeta

    @lowBeta.setter
    def lowBeta(self, value):
        self.__lowBeta = value
        # if callback has been set, execute the function
        for callback in self.__lowBeta__callbacks:
            callback(self.__lowBeta)

    # highBeta
    @property
    def highBeta(self):
        """Get value for highBeta"""
        return self.__highBeta

    @highBeta.setter
    def highBeta(self, value):
        self.__highBeta = value
        # if callback has been set, execute the function
        for callback in self.__highBeta__callbacks:
            callback(self.__highBeta)

    # lowGamma
    @property
    def lowGamma(self):
        """Get value for lowGamma"""
        return self.__lowGamma

    @lowGamma.setter
    def lowGamma(self, value):
        self.__lowGamma = value
        # if callback has been set, execute the function
        for callback in self.__lowGamma__callbacks:
            callback(self.__lowGamma)

    # highGamma
    @property
    def highGamma(self):
        """Get value for midGamma"""
        return self.__highGamma

    @highGamma.setter
    def highGamma(self, value):
        self.__highGamma = value
        # if callback has been set, execute the function
        for callback in self.__highGamma__callbacks:
            callback(self.__highGamma)

    # status
    @property
    def status(self):
        """Get status"""
        return self.__status