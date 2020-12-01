import time
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata

run_count = 0
ADAFRUIT_IO_USERNAME = "Andreastest1"
ADAFRUIT_IO_KEY = "aio_YPax67KATYezU1hAHXlOFPhKTZ3O"


aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

board = pyfirmata.Arduino('COM4')

it = pyfirmata.util.Iterator(board)
it.start()

digital_output = board.get_pin('d:13:o')
analog_input = board.get_pin('a:0:i')


try:
	digital = aio.feeds('digital')
	print('Done')
except RequestError:
	feed = Feed(name='digital')
	digital = aio.create_feed(feed)
	print('Feed Error')

print(digital)

while True:
	print('Sending count:', run_count)
	aio.send_data('counter', run_count)
	aio.send_data('chart', analog_input.read())
	run_count += 1

	data = aio.receive(digital.key)

	print('Data: ', data.value)

	if data.value == "ON":
		digital_output.write(True)
	else:
		digital_output.write(False)

	time.sleep(2)