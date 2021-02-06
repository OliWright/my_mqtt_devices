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

import paho.mqtt.client as mqtt

codes = {
	"A1" : "0x807FD827",
	"A2" : "0x807F40BF",
	"A3" : "0x807F48B7",
	"A4" : "0x807F708F",
	
	"B1" : "0x807F7887",
	"B2" : "0x807F50AF",
	"B3" : "0x807F08F7",
	"B4" : "0x807FF00F",
	
	"Power" : "0x807FF807",
	"2CH"   : "0x807F58A7",
	"5.1CH" : "0x807FB04F",
	"Adv"   : "0x807F8877",
	"ARC"   : "0x807FA05F",
	"SPDIF" : "0x807FA05F",
}

inputs = [ "Off", "Sky", "Switch", "PS3", "PS4" ]

class HdmiSwitch():
	def __init__(self, base_topic, device_name, ir_gateway):
		self.device_name = device_name
		self.base_topic = base_topic + "/hdmiswitch"
		self.subscribe_topic = self.base_topic + "/#"
		self.remote_topic = self.base_topic + "/remote"
		self.set_state_a_topic = self.base_topic + "/set-state-a"
		self.set_state_b_topic = self.base_topic + "/set-state-b"
		self.status_topic = self.base_topic + "/status"
		self.ir_gateway = ir_gateway
		self.output_states = [0,0]
		
	def publish_status(self, client):
		global inputs
		json = '{{"outputA":"{outputA}", "outputB":"{outputB}"}}'.format(outputA = inputs[self.output_states[0]], outputB = inputs[self.output_states[1]])
		client.publish(self.base_topic + "/status", payload = json, retain = True)

	def send_remote(self, command):
		global codes
		hex = codes.get(command, None)
		if hex is None:
			print("Unknown command: " + command)
			return
		self.ir_gateway.enqueue(self.device_name, command, "NEC", 32, hex)
		
	def set_state(self, client, output_idx, input_name):
		global inputs
		input_idx = inputs.index(input_name)
		output_letter = 'A'
		if self.output_states[output_idx] != input_idx:
			self.output_states[output_idx] = input_idx

			if output_idx == 1:
				output_letter = 'B'
			if input_idx == 0:
				# Off
				if (self.output_states[0] == 0) and (self.output_states[1] == 0):
					# Both outputs are off. So we can switch the HDMI switch off too
					pass
			else:
				self.send_remote(output_letter + str(input_idx))

			if (self.output_states[0] != 0) and (self.output_states[1] == 0):
				# Output A is being used, but Output B isn't.
				# We need to make sure Output B is set to a different input
				# or else we get HDMI problems
				if self.output_states[0] == 3:
					self.send_remote('B2')
				else:
					self.send_remote('B3')

			self.publish_status(client)

	def on_message(self, client, userdata, msg, payload):
		if msg.topic == self.remote_topic:
			self.send_remote(client, payload)
		elif msg.topic == self.set_state_a_topic:
			self.set_state(client, 0, payload)
		elif msg.topic == self.set_state_b_topic:
			self.set_state(client, 1, payload)
		elif msg.topic == self.status_topic:
			pass
		else:
			print("Unknown topic: " + msg.topic)
		
	def on_connect(self, client, userdata, flags, rc):
		self.publish_status(client)
