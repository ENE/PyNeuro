from PyNeuro.PyNeuro import PyNeuro
from PyNeuro.PyNeuro import MWM2_Status

pn = PyNeuro()

def connected_callback():
    print(PyNeuro.status_def[MWM2_Status.CONNECTED].description)

def fitting1_callback():
    print(PyNeuro.status_def[MWM2_Status.FITTING1].description)

def fitting2_callback():
    print(PyNeuro.status_def[MWM2_Status.FITTING2].description)

def fitting3_callback():
    print(PyNeuro.status_def[MWM2_Status.FITTING3].description)

def nosignal_callback():
    print(PyNeuro.status_def[MWM2_Status.NOSIGNAL].description)

pn.set_highlevel_status_callback(MWM2_Status.CONNECTED, connected_callback)
pn.set_highlevel_status_callback(MWM2_Status.FITTING1, fitting1_callback)
pn.set_highlevel_status_callback(MWM2_Status.FITTING2, fitting2_callback)
pn.set_highlevel_status_callback(MWM2_Status.FITTING3, fitting3_callback)
pn.set_highlevel_status_callback(MWM2_Status.NOSIGNAL, nosignal_callback)

pn.connect()
pn.start()