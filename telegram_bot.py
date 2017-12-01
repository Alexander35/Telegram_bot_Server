from general_server_client import GeneralServer
from protobuf_asset import msg_pb2
import telebot

class TelegramBot(GeneralServer):
	"""This is server is waiting for any messages and 
	send it to a telegram bot"""
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		# self.initialize()

	def on_initialize(self):
		try:
			self.telegram_bot = telebot.TeleBot(self.get_config('TELEGRAMBOT', 'token'))
			self.chat_id = self.get_config('TELEGRAMBOT', 'chat_id')
		except Exception as exc:
			self.logger.error('Telegram bot initializing error {}'.format(exc))
		try:	
			super().start()
		except Exception as exc:
			self.logger.error('Cannot start a server {}'.format(exc))		

	def prepare_msg(self, raw_data):
		Msg = msg_pb2.Msg()
		Msg.ParseFromString(raw_data)
		return Msg	

	def on_fetch(self, msg):
		Msg = self.prepare_msg(msg)
		self.telegram_bot.send_message(self.chat_id, '{}\n{}\n{}\n'.format(Msg.title, Msg.text, Msg.tagline))

	# def on_daemonize(self):
	# 	self.on_initialize()	

def main():
	TB = TelegramBot()

if __name__ == '__main__':
	main()			