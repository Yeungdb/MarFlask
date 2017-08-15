#!/usr/bin/env python

# An example of the effect of windowing on spectrum 
# of two input sine waves. marsyas_util.py contain 
# helper functions for the compact syntax 
# for specifying Marsyas networks. This 
# example also illustrate how Marsyas and matplotlib 
# can interact 
import MarsyasFlask
from pylab import *
import sys
from matplotlib import pyplot
from marsyas import *
from marsyas_util import *
import json
import itertools
import collections
import yaml
# The compact syntax for network specification is based 
# on recursive specifying the network. The syntax is 
# [name of composite pareant, [comma separated list of children]] 

spec = ["Series/MySystem",
  	       [["Fanout/additive",
	["SineSource/src1", "SineSource/src2"]],
	"Sum/sum",
                ["Fanout/analyzers",
                      [["Series/branch1",
		       ["Spectrum/spk",
                        "PowerSpectrum/pspk",
                        "Gain/gain"]],
		["Series/branch2",
			["Windowing/win",
                         "Spectrum/spk",
                         "PowerSpectrum/pspk",
                         "Gain/gain"]],
		["Series/branch3",
			["Windowing/win",
                         "Spectrum/spk",
                         "PowerSpectrum/pspk",
                         "Gain/gain"]]]]]]

####################
SERVERLOCATION = "127.0.0.1:5000"
client = MarsyasFlask.MarsyasClient(SERVERLOCATION)


# The create function (defined in marsyas_util) takes 
# as input the network specification and return 
# the actual network that can be used for processing
client.initNet(spec)


# We can now create top-level controls for easier 
# access to what we need. These provide the 
# "client" interface to the functionality of the 
# network. For example we will have shorter 
# control names for the frequency controls of the sinusoids. 

data = {}
data['dest'] = "Fanout/additive/SineSource/src1/mrs_real/frequency"
data['mrs_type'] = "mrs_real/frequency1"

data = json.dumps(data)
data = yaml.safe_load(data)
dest = str(data['dest'])
mrs_type = str(data['mrs_type'])
print dest, mrs_type
# make top level controls for the frequencies of the two oscillators 
client.linkctrl(dest, mrs_type)
client.linkctrl("Fanout/additive/SineSource/src2/mrs_real/frequency", 
                "mrs_real/frequency2");

# You can link two or more controls to the same top-level control, so
# the same control will change parameters for multiple controls in the
# network. For example map all spectrum types to the same top level control 

client.linkctrl(
    "Fanout/analyzers/Series/branch1/PowerSpectrum/pspk/mrs_string/spectrumType",
    "mrs_string/spectrumType")
client.linkctrl(
    "Fanout/analyzers/Series/branch2/PowerSpectrum/pspk/mrs_string/spectrumType","mrs_string/spectrumType")

client.linkctrl(
    "Fanout/analyzers/Series/branch3/PowerSpectrum/pspk/mrs_string/spectrumType","mrs_string/spectrumType")

# make top level controls for accessing the 3 spectrums 
client.linkctrl("Fanout/analyzers/Series/branch1/PowerSpectrum/pspk/mrs_realvec/processedData","mrs_realvec/spectrum1")
client.linkctrl("Fanout/analyzers/Series/branch2/PowerSpectrum/pspk/mrs_realvec/processedData","mrs_realvec/spectrum2")
client.linkctrl("Fanout/analyzers/Series/branch3/PowerSpectrum/pspk/mrs_realvec/processedData","mrs_realvec/spectrum3")

# Now, we will setup our analyzers in each analyzer branch.  In
# branch1, we have no window, hence it is a rectangular-shaped window.
# In branch2, we will have a hamming window, which is the default
# (hence it does not have to be changed) In branch3, we will have a
# hann window, which is set below:
client.updatectrl("Fanout/analyzers/Series/branch3/Windowing/win/mrs_string/type", "Hann");

# Using the getControl() method, we access the controls of the 
# different for a the components in the network
# The following commands will set that we want our output for 
# the spectrumTupe (remember, we linked that to all three spectral 
# analyzers above!). This is an alternative syntax for setting 
# control to the syntax above for setting the window type 

client.funcgetctrl("mrs_string/spectrumType", "setValue_string", MethodVar="decibels", MethodVarType="str", IsReturn="False", IsTick="False")

# We are doing something similar here. Note that this is equivalent to
# using the client.updatectrl() method properly,
# but it might save you some work later. After you have executed this, uncomment the last two lines of this block and
# see what the output is like!

client.funcgetctrl("mrs_real/frequency1", "setValue_real", MethodVar=1500.0, MethodVarType='float', IsReturn='False')
client.funcgetctrl("mrs_real/frequency2", "setValue_real", MethodVar=3000.0, MethodVarType='float', IsReturn='False')
client.updatectrl("mrs_real/frequency1", 2000.0);
client.updatectrl("mrs_real/frequency2", 4000.0);


outData1 = client.funcgetctrl("mrs_realvec/spectrum1", "to_realvec", IsReturn = 'True', IsTick='True')
outData2 = client.funcgetctrl("mrs_realvec/spectrum2", "to_realvec", IsReturn = 'True', IsTick='True')
outData3 = client.funcgetctrl("mrs_realvec/spectrum3", "to_realvec", IsReturn = 'True', IsTick='True')

outData1 = str(outData1).split("\n")
outData2 = str(outData2).split("\n")
outData3 = str(outData3).split("\n")

# These commands below are for plotting.
plot(linspace(0,11050, 257),outData1, label="Rectangular")
plot(linspace(0,11050, 257),outData2, label="Hamming")
plot(linspace(0,11050, 257),outData3, label="Hanning")

xlabel("Frequency (Hz)")
ylabel("Magnitude (dB)");
suptitle("Marsyas windowing demo through Flask");
legend()

# save .svg and .ps versions of the figure 
savefig('windowing-Flask.svg')
savefig('windowing-Flask.ps')
savefig('windowing-Flask.png')

show()

# Try drawing the network we are running
# When you are finished, go to phone.py to continue the tutorial.
