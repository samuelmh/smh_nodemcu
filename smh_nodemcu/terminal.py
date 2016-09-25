# -*- coding: utf-8 -*-


import threading

class AsyncReader(threading.Thread):

	def __init__(self, connector, func_write):
		self.connector = connector
		self.func_write = func_write
		self.working = True
		super(AsyncReader, self).__init__()

	def stop(self):
		self.working = False

	def run(self):
		while self.working:
			r = self.connector.read(self.connector.in_waiting or 1)
			if r!='':
				self.func_write(r)


class Terminal(object):

	def __init__(self, connector, func_read, func_write):
		self.connector = connector
		self.func_read = func_read
		self.func_write = func_write
		self.reader = AsyncReader(connector, func_write)


	def start(self):
		self.reader.start()
		self.func_write('\nTerminal, press CTRL-D to exit.\n\n')
		flag_exit = False
		while not flag_exit:
			try:
				msg = self.func_read()
				self.send_msg(msg)
			except Exception as e:
				flag_exit = True
				self.func_write('\n\nExiting terminal.\n')
		self.stop()

	def stop(self):
		self.reader.stop()
		self.reader.join()

	def send_msg(self, msg):
		return self.connector.write('{msg}\r\n'.format(msg=msg))


	def send_msg_then_read(self, msg):
		self.connector.reset_input_buffer()
		self.connector.reset_output_buffer()
		retval = ''
		self.send_msg(msg)
		old_timeout = self.connector.timeout
		self.connector.timeout = 2
		reading = True
		while reading:
		    r = self.connector.read(self.connector.in_waiting or 1)
		    self.connector.timeout = 0.5
		    if not r:
		        reading = False
		    else:
		        retval += r
		self.connector.timeout = old_timeout
		return retval
