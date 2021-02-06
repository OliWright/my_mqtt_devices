#
# My local configuration for mqtt_devices
#

import mqtt_devices
import ir_gateway
from mqtt_sky import Sky
from hdmi_switch import HdmiSwitch
from lounge_tv import LoungeTV
import str_dn1050
from mqtt_fishtank_lights import CelestialController
from mqtt_fishtank_lights import ColourTable
from mqtt_fishtank_lights import LegacyFishtankLights
from mqtt_fishtank_lights import FishtankLights

# ESP32 OpenMQTTGateway in the lounge behind the TV
lounge_ir_gateway = ir_gateway.IRGateway("home/lounge")

# Up 2F0
# Down AF0
# Left 2D0
# Right CD0
# Select A70
# Back 62E9
# Home 70
# Previous 1EE9
# Next 5EE9
# 0 {"value":70385940827918,"protocol":5,"bits":48,"hex":"0x400401000F0E","protocol_name":"PANASONIC","raw":}
# 1 0x400401000F8E
# 2 4F4E
# 3 CFCE
# 4 2F2E
# 5 AFAE
# 6 6F6E
# 7 EFEE
# 8 1F1E
# 9 9F9E


# Configuration for the decoder part of the lounge IRGateway to translate
# obscure IR codes into more readable MQTT messages
lounge_ir_decoder_config = {
	"RC6": {
		"0xC800F0400" : {
			"topic" : "home/lounge/av-state",
			"payload" : "Off",
			"retain" : True
		},
		"0xC800F8401" : {
			"topic" : "home/lounge/av-state",
			"payload" : "Sky",
			"retain" : True
		},
		"0xC800F0402" : {
			"topic" : "home/lounge/av-state",
			"payload" : "Chromecast",
			"retain" : True
		},
		"0xC800F8406" : {
			"topic" : "home/lounge/av-state",
			"payload" : "PS3",
			"retain" : True
		},
		"0xC800F0407" : {
			"topic" : "home/lounge/av-state",
			"payload" : "PS4",
			"retain" : True
		},
		"0xC800F8403" : {
			"topic" : "home/lounge/av-state",
			"payload" : "Switch",
			"retain" : True
		},
		"0xC800F0404" : {
			"topic" : "home/lounge/av-state",
			"payload" : "Raspberry Pi",
			"retain" : True
		},
		"0xC800F8405" : {
			"topic" : "home/lounge/av-state",
			"payload" : "External",
			"retain" : True
		},
		# "a" : {
				# "topic" : "home/dining-room/av-state",
				# "payload" : "Off",
				# "retain" : True
		# },
		"0xC800F8408" : {
			"topic" : "home/dining-room/av-state",
			"payload" : "Sky",
			"retain" : True
		},
		"0xC800F8409" : {
			"topic" : "home/dining-room/av-state",
			"payload" : "PS3",
			"retain" : True
		},
		"0xC800F841D" : {
			"topic" : "home/dining-room/av-state",
			"payload" : "PS4",
			"retain" : True
		},
		"0xC800F841C" : {
			"topic" : "home/dining-room/av-state",
			"payload" : "Switch",
			"retain" : True
		},
	},
	"SONY" : {
		# Translate the media control codes into MQTT remote control commands
		"0x2CE9" : [ {
			"topic" : "home/lounge/sky/remote",
			"payload" : "play",
			},{
			"topic" : "home/lounge/webos-button",
			"payload" : "PLAY",
			}
		],
		"0x4CE9" : [ {
			"topic" : "home/lounge/sky/remote",
			"payload" : "pause",
			},{
			"topic" : "home/lounge/webos-button",
			"payload" : "PAUSE",
			}
		],
		"0xCE9" : [ {
			"topic" : "home/lounge/sky/remote",
			"payload" : "stop",
			},{
			"topic" : "home/lounge/webos-control",
			"payload" : "Stop",
			}
		],
		"0x6CE9" : [ {
			"topic" : "home/lounge/sky/remote",
			"payload" : "rewind",
			},{
			"topic" : "home/lounge/webos-button",
			"payload" : "LEFT",
			}
		],
		"0x1CE9" : [ {
			"topic" : "home/lounge/sky/remote",
			"payload" : "FastForward",
			},{
			"topic" : "home/lounge/webos-button",
			"payload" : "RIGHT",
			}
		],
		"0x2F0" : {
			"topic" : "home/lounge/webos-button",
			"payload" : "UP",
		},
		"0xAF0" : {
			"topic" : "home/lounge/webos-button",
			"payload" : "DOWN",
		},
		"0x2D0" : {
			"topic" : "home/lounge/webos-button",
			"payload" : "LEFT",
		},
		"0xCD0" : {
			"topic" : "home/lounge/webos-button",
			"payload" : "RIGHT",
		},
		"0xA70" : {
			"topic" : "home/lounge/webos-button",
			"payload" : "ENTER",
		},
		"0x62E9" : {
			"topic" : "home/lounge/webos-button",
			"payload" : "BACK",
		},
		"0x70" : {
			"topic" : "home/lounge/webos-button",
			"payload" : "MENU",
		},
		"0x5EE9" : {
			"topic" : "home/lounge/webos-control",
			"payload" : "Next",
		},
		"0x1EE9" : {
			"topic" : "home/lounge/webos-control",
			"payload" : "Previous",
		},
	},
}

amp_input_friendly_names = {
	"SAT-CATV" : "HDMI Switch",
	"SA-CD"    : "Raspberry Pi",
}

playroom_colour_table = ColourTable("playroom_colour_table", 255)
playroom1_colour_table = ColourTable("playroom1_colour_table")
lounge_colour_table = ColourTable("lounge_colour_table")
celestial_controller = CelestialController()

# We must declare this array of devices for mqtt_devices
devices = [
	lounge_ir_gateway,
	# Custom module for the HDMI switch under the TV in the lounge.
	HdmiSwitch("home/lounge", "Lounge HDMI switch", lounge_ir_gateway),
	# TV in the lounge, controlled by the IR gateway
	LoungeTV("home/lounge", lounge_ir_gateway),
	# SKY+ HD box controlled by remote-control commands sent over IP
	Sky("home/lounge", "192.168.100.65"),
	# Two-zone amp for the audio in the lounge and in the kitchen
	# Effectively two separate devices.
	str_dn1050.Zone1("home/lounge", "amp", "Amp Zone1", amp_input_friendly_names, lounge_ir_gateway),
	str_dn1050.Zone2("home/kitchen", "amp", "Amp Zone2", amp_input_friendly_names, lounge_ir_gateway),
	# IRDecoder to translate obtuse IR commands coming from the gateway
	# into more readable MQTT messages
	ir_gateway.IRDecoder("home/lounge", lounge_ir_decoder_config),
	# Controller to keep the sun and moon tables up to date
	celestial_controller,
	# Fishtank lights
	LegacyFishtankLights("home/fishtank-lights", "Playroom", playroom_colour_table, celestial_controller.sun, celestial_controller.moon),
	FishtankLights("home/fishtank-lights", "Lounge", "home/lounge/fishtank-lights", lounge_colour_table, celestial_controller.sun, celestial_controller.moon),
	FishtankLights("home/fishtank-lights", "Playroom1", "home/playroom/fishtank-lights1", playroom1_colour_table, celestial_controller.sun, celestial_controller.moon),
]

from secret import mqtt_broker_credentials
# Credentials to allow connection to our MQTT broker
#mqtt_broker_credentials = {
#	"User" : "<mqtt user name>",
#	"Password" : "<mqtt password>",
#	"IP" : "<mqtt ip address>",
#	"Port" : <mqtt port>
#}

# Run the whole thing...
mqtt_devices.Run(devices, mqtt_broker_credentials)
