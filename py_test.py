from __future__ import print_function

import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers
import time

# To test add path: set SOAPY_SDR_PLUGIN_PATH=C:\Users\DMITRII\SoapyICR8600\build\x64\Release;

#enumerate devices
results = SoapySDR.Device.enumerate()
for result in results: print(result)

#create device instance
#args can be user defined or from the enumeration result
args = dict(driver="icr8600")
sdr = SoapySDR.Device(args)

#query device info
print("Antennas:", sdr.listAntennas(SOAPY_SDR_RX, 0))
print("Gains:", sdr.listGains(SOAPY_SDR_RX, 0))
freqs = sdr.getFrequencyRange(SOAPY_SDR_RX, 0)
for freqRange in freqs: print(freqRange)

#apply settings
sdr.setSampleRate(SOAPY_SDR_RX, 0, 240000)
sdr.setFrequency(SOAPY_SDR_RX, 0, 102100000)

#setup a stream (complex floats)
rxStream = sdr.setupStream(SOAPY_SDR_RX, "CS16")
sdr.activateStream(rxStream) #start streaming

time.sleep(2.0)

#create a re-usable buffer for rx samples
buff = numpy.array([0]*1024, numpy.complex64)

#receive some samples
for i in range(20):
    sr = sdr.readStream(rxStream, [buff], len(buff))
    print("Rec:", sr.ret, buff[:4]) #num samples or error code
    # print(sr.flags) #flags set by receive operation
    # print(sr.timeNs) #timestamp for receive buffer

#shutdown the stream
sdr.deactivateStream(rxStream) #stop streaming
sdr.closeStream(rxStream)
