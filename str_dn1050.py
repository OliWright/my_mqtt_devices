# MIT License
#
# Copyright (c) 2020 Oli Wright <oli.wright.github@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from ir_gateway import GenericIRDevice

zone1_config = {
    "SendIREvenIfSameState" : True,
	"ProtocolName" : "SONY",
	"StateRemoteCodes" : {
		"Off"      : "PowerOff",
		"SAT-CATV" : "SAT-CATV",
		"SA-CD"    : "SA-CD",
		"BD-DVD"   : "BD-DVD",
		"Game"     : "Game",
		"TV"       : "TV",
	},
	"RemoteCodes" : [
		{
			"Bits" : 15,
			"Codes" : {
                "PowerOff"  : "0x7A0C",
				"SAT-CATV"  : "0x600D",
				"Game"      : "0x1F0C",
				"SA-CD"     : "0x520C",
				"TV"        : "0x2B0C",
			}
		},
		{
			"Bits" : 20,
			"Codes" : {
				"BD-DVD"   : "0x68114",
			}
		},
	]
}

zone2_config = {
	"ProtocolName" : "SONY",
	"StateRemoteCodes" : {
		"Off"      : "PowerOff",
		"SAT-CATV" : "SAT-CATV",
		"SA-CD"    : "SA-CD",
		"BD-DVD"   : "BD-DVD",
		"Game"     : "Game",
	},
	"RemoteCodes" : [
		{
			"Bits" : 15,
			"Codes" : {
				"SAT-CATV"  : "0x600D",
				"Game"      : "0x1F0C",
				"SA-CD"     : "0x520C",
			}
		},
		{
			"Bits" : 20,
			"Codes" : {
				"BD-DVD"   : "0x68114",
			}
		},
	]
}

class Zone1(GenericIRDevice):
	def __init__(self, base_topic, short_name, device_name, input_friendly_names, ir_gateway):
		global config
		GenericIRDevice.__init__(self, base_topic, short_name, device_name, zone1_config, input_friendly_names, ir_gateway)

class Zone2(GenericIRDevice):
	def __init__(self, base_topic, short_name, device_name, input_friendly_names, ir_gateway):
		global config
		GenericIRDevice.__init__(self, base_topic, short_name, device_name, zone2_config, input_friendly_names, ir_gateway)
	
