from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
from KitronikAirQualityControlHAT import *
from time import sleep
import csv

# Initialise the Flask web app
app = Flask(__name__)

# Initialise our HAT sensors
bme688 = KitronikBME688()
oled = KitronikOLED(flipScreen=False)
adc0 = KitronikADC(0)
adc1 = KitronikADC(1)
adc2 = KitronikADC(2)
servo = KitronikServo()
zipleds = KitronikZIPLEDs()
hpo1 = KitronikHighPowerOut(1, True)
hpo2 = KitronikHighPowerOut(2, True)

# Creates connection with the sensor data database
def get_database_connection():
	conn = sqlite3.connect('database.db')
	conn.row_factory = sqlite3.Row
	return conn

# Retrieves the most recent BME688 data
def get_bme688_data():
	conn = get_database_connection()
	# Read the most recent BME688 values
	temperature = conn.execute('SELECT sensorValue, created FROM sensorData WHERE sensorType="Temperature" ORDER BY id DESC;').fetchone()
	pressure = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="Pressure" ORDER BY id DESC;').fetchone()
	humidity = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="Humidity" ORDER BY id DESC;').fetchone()
	eCO2 = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="eCO2" ORDER BY id DESC;').fetchone()
	airQualityPercent = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="AirQualityPercent" ORDER BY id DESC;').fetchone()
	airQualityScore = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="AirQualityScore" ORDER BY id DESC;').fetchone()
	conn.close()
	# Set default values if none in the database
	if temperature is None:
		temperature = ["No data", "No data"]
	if pressure is None:
		pressure = ["No data"]
	if humidity is None:
		humidity = ["No data"]
	if eCO2 is None:
		eCO2 = ["No data"]
	if airQualityPercent is None:
		airQualityPercent = ["No data"]
	if airQualityScore is None:
		airQualityScore = ["No data"]
	return (temperature[1], temperature[0], pressure[0], humidity[0], eCO2[0], airQualityPercent[0], airQualityScore[0])

# Retrieves all the BME688 data
def get_all_bme688_data():
	conn = get_database_connection()
	# Read all the BME688 values
	temperature = conn.execute('SELECT sensorValue, created FROM sensorData WHERE sensorType="Temperature" ORDER BY id DESC;').fetchall()
	pressure = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="Pressure" ORDER BY id DESC;').fetchall()
	humidity = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="Humidity" ORDER BY id DESC;').fetchall()
	eCO2 = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="eCO2" ORDER BY id DESC;').fetchall()
	airQualityPercent = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="AirQualityPercent" ORDER BY id DESC;').fetchall()
	airQualityScore = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="AirQualityScore" ORDER BY id DESC;').fetchall()
	conn.close()
	bme688_data = []
	# Order the data as: created, temperature, pressure, humidity, eCO2, airQualityPercent, airQualityScore
	for i in range(len(temperature)):
		temp = []
		temp.append(temperature[i][1])
		temp.append(temperature[i][0])
		temp.append(pressure[i][0])
		temp.append(humidity[i][0])
		temp.append(eCO2[i][0])
		temp.append(airQualityPercent[i][0])
		temp.append(airQualityScore[i][0])
		bme688_data.append(temp)
	return bme688_data

# Adds the most recent BME688 data
def add_bme688_data(bme688):
	bme688.measureData()
	sleep(1)
	temperature = bme688.readTemperature()
	pressure = bme688.readPressure()
	humidity = bme688.readHumidity()
	eCO2 = bme688.readeCO2()
	airQualityPercent = bme688.getAirQualityPercent()
	airQualityScore = bme688.getAirQualityScore()
	conn = get_database_connection()
	# Add the most recent BME688 values
	conn.execute("INSERT INTO sensorData (sensorType, sensorValue) VALUES (?, ?)", ("Temperature", temperature))
	conn.execute("INSERT INTO sensorData (sensorType, sensorValue) VALUES (?, ?)", ("Pressure", pressure))
	conn.execute("INSERT INTO sensorData (sensorType, sensorValue) VALUES (?, ?)", ("Humidity", humidity))
	conn.execute("INSERT INTO sensorData (sensorType, sensorValue) VALUES (?, ?)", ("eCO2", eCO2))
	conn.execute("INSERT INTO sensorData (sensorType, sensorValue) VALUES (?, ?)", ("AirQualityPercent", airQualityPercent))
	conn.execute("INSERT INTO sensorData (sensorType, sensorValue) VALUES (?, ?)", ("AirQualityScore", airQualityScore))
	conn.commit()
	conn.close()

# Retrieves the most recent ADC data
def get_adc_data():
	conn = get_database_connection()
	# Read the most recent ADC values
	adc0 = conn.execute('SELECT sensorValue, created FROM sensorData WHERE sensorType="ADC0" ORDER BY id DESC;').fetchone()
	adc1 = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="ADC1" ORDER BY id DESC;').fetchone()
	adc2 = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="ADC2" ORDER BY id DESC;').fetchone()
	conn.close()
	# Set default values if none in the database
	if adc0 is None:
		adc0 = ["No data", "No data"]
	if adc1 is None:
		adc1 = ["No data"]
	if adc2 is None:
		adc2 = ["No data"]
	return (adc0[1], adc0[0], adc1[0], adc2[0])

# Retrieves all the ADC data
def get_all_adc_data():
	conn = get_database_connection()
	# Read all the ADC values
	adc0 = conn.execute('SELECT sensorValue, created FROM sensorData WHERE sensorType="ADC0" ORDER BY id DESC;').fetchall()
	adc1 = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="ADC1" ORDER BY id DESC;').fetchall()
	adc2 = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="ADC2" ORDER BY id DESC;').fetchall()
	conn.close()
	adc_data = []
	# Order the data as: created, adc0, adc1, adc2, adc3
	for i in range(len(adc0)):
		temp = []
		temp.append(adc0[i][1])
		temp.append(adc0[i][0])
		temp.append(adc1[i][0])
		temp.append(adc2[i][0])
		adc_data.append(temp)
	return adc_data

# Adds the most recent ADC data
def add_adc_data(adc0, adc1, adc2):
	conn = get_database_connection()
	# Add the most recent ADC values
	conn.execute("INSERT INTO sensorData (sensorType, sensorValue) VALUES (?, ?)", ("ADC0", adc0.read()))
	conn.execute("INSERT INTO sensorData (sensorType, sensorValue) VALUES (?, ?)", ("ADC1", adc1.read()))
	conn.execute("INSERT INTO sensorData (sensorType, sensorValue) VALUES (?, ?)", ("ADC2", adc2.read()))
	conn.commit()
	conn.close()

# Retrieves the most recent Servo data
def get_servo_data():
	conn = get_database_connection()
	# Read the most recent Servo values
	servo = conn.execute('SELECT sensorValue, created FROM sensorData WHERE sensorType="Servo" ORDER BY id DESC;').fetchone()
	conn.close()
	# Set default values if none in the database
	if servo is None:
		servo = ["90", "No data"]
	return (servo[1], servo[0])

# Retrieves all the Servo data
def get_all_servo_data():
	conn = get_database_connection()
	# Read all the Servo values
	servo = conn.execute('SELECT sensorValue, created FROM sensorData WHERE sensorType="Servo" ORDER BY id DESC;').fetchall()
	conn.close()
	servo_data = []
	# Order the data as: created, servo
	for i in range(len(servo)):
		temp = []
		temp.append(servo[i][1])
		temp.append(servo[i][0])
		servo_data.append(temp)
	return servo_data

# Adds the most recent Servo data
def add_servo_data(servo_value):
	conn = get_database_connection()
	# Add the most recent Servo values
	conn.execute("INSERT INTO sensorData (sensorType, sensorValue) VALUES (?, ?)", ("Servo", servo_value))
	conn.commit()
	conn.close()

# Retrieves the most recent ZIPLED data
def get_zipleds_data():
	conn = get_database_connection()
	# Read the most recent ZIPLED values
	zipleds = conn.execute('SELECT sensorValue, created FROM sensorData WHERE sensorType="ZIPLEDs" ORDER BY id DESC;').fetchone()
	conn.close()
	# Set default values if none in the database
	if zipleds is None:
		zipleds = ["128,128,128,50", "No data"]
	data = zipleds[0].split(",")
	return (zipleds[1], data[0], data[1], data[2], data[3])

# Retrieves all the ZIPLED data
def get_all_zipleds_data():
	conn = get_database_connection()
	# Read all the ZIPLED values
	zipleds = conn.execute('SELECT sensorValue, created FROM sensorData WHERE sensorType="ZIPLEDs" ORDER BY id DESC;').fetchall()
	conn.close()
	zipleds_data = []
	# Order the data as: created, red, green, blue, brightness
	for i in range(len(zipleds)):
		temp = []
		temp.append(zipleds[i][1])
		data = zipleds[i][0].split(",")
		temp.append(data[0])
		temp.append(data[1])
		temp.append(data[2])
		temp.append(data[3])
		zipleds_data.append(temp)
	return zipleds_data

# Adds the most recent ZIPLED data
def add_zipleds_data(zipleds_value):
	conn = get_database_connection()
	# Add the most recent ZIPLED values
	conn.execute("INSERT INTO sensorData (sensorType, sensorValue) VALUES (?, ?)", ("ZIPLEDs", zipleds_value))
	conn.commit()
	conn.close()

# Retrieves the most recent High Power Out data
def get_hpo_data():
	conn = get_database_connection()
	# Read the most recent High Power Out values
	hpo1 = conn.execute('SELECT sensorValue, created FROM sensorData WHERE sensorType="HPO1" ORDER BY id DESC;').fetchone()
	hpo2 = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="HPO2" ORDER BY id DESC;').fetchone()
	conn.close()
	# Set default values if none in the database
	if hpo1 is None:
		hpo1 = ["0", "No data"]
	if hpo2 is None:
		hpo2 = ["0", "No data"]
	return (hpo1[1], hpo1[0], hpo2[0])

# Retrieves all the High Power Out data
def get_all_hpo_data():
	conn = get_database_connection()
	# Read all the High Power Out values
	hpo1 = conn.execute('SELECT sensorValue, created FROM sensorData WHERE sensorType="HPO1" ORDER BY id DESC;').fetchall()
	hpo2 = conn.execute('SELECT sensorValue FROM sensorData WHERE sensorType="HPO2" ORDER BY id DESC;').fetchall()
	conn.close()
	hpo_data = []
	# Order the data as: created, hpo1, hpo2
	for i in range(len(hpo1)):
		temp = []
		temp.append(hpo1[i][1])
		temp.append(hpo1[i][0])
		temp.append(hpo2[i][0])
		hpo_data.append(temp)
	return hpo_data

# Adds the most recent High Power Out data
def add_hpo_data(hpo1_value, hpo2_value):
	conn = get_database_connection()
	# Add the most recent High Power Out values
	conn.execute("INSERT INTO sensorData (sensorType, sensorValue) VALUES (?, ?)", ("HPO1", hpo1_value))
	conn.execute("INSERT INTO sensorData (sensorType, sensorValue) VALUES (?, ?)", ("HPO2", hpo2_value))
	conn.commit()
	conn.close()

# Calculate BME688 sensor baselines
bme688.calcBaselines(oled)
# Read and save the BME688 sensor values
add_bme688_data(bme688)
print("Finished baselines")

# Load the kitronik-logo.jpg image onto the OLED display
oled.image = Image.open("images/kitronik-logo.jpg")
# Convert the image to greyscale on the OLED display
oled.image = oled.image.convert('1')
# Resize the image to fit on the OLED display
oled.image = oled.image.resize((128, 64))
# Invert the colours of the image (black to white, white to black)
oled.invert(1)
# Update the OLED display with the changes
oled.show()

# Reset the servo to previous values
servo.start()
servo.changeAngle(int(get_servo_data()[1]))

# Reset the ZIPLEDs to previous values
zipleds_data = get_zipleds_data()
zipleds.setBrightness(int(zipleds_data[4]))
zipleds.fill((int(zipleds_data[1]), int(zipleds_data[2]), int(zipleds_data[3])))

# Reset the high power out to previous values
hpo_data = get_hpo_data()
hpo1.changeDutyCycle(int(hpo_data[1]))
hpo1.start()
hpo2.changeDutyCycle(int(hpo_data[2]))
hpo2.start()

# Render the home control page
@app.route('/')
def home():
	# Render the dashboard with most recent HAT values
    return render_template('home.html',
		bme688=get_bme688_data(),
		adc=get_adc_data(),
		servo=get_servo_data(),
		zipleds=get_zipleds_data(),
		hpo=get_hpo_data())

# Read the most recent BME688 values
@app.route('/bme688/measureData', methods=['POST'])
def bme688_measureData():
	if request.method == 'POST':
		# When form submitted, update the BME688 values
		add_bme688_data(bme688)
	return redirect(url_for('home'))

# Render the BME688 data page
@app.route('/bme688')
def bme688_data():
	bme688_data = get_all_bme688_data()
	# Render the BME688 data with all values
	return render_template('bme688.html', bme688_data=bme688_data)

# Read the most recent ADC values
@app.route('/adc/measureData', methods=['POST'])
def adc_measureData():
	if request.method == 'POST':
		# When form submitted, update the ADC values
		add_adc_data(adc0, adc1, adc2)
	return redirect(url_for('home'))

# Render the ADC data page
@app.route('/adc')
def adc_data():
	adc_data = get_all_adc_data()
	# Render the ADC data with all values
	return render_template('adc.html', adc_data=adc_data)

# Update the Servo values
@app.route('/servo/set', methods=['POST'])
def servo_set():
	if request.method == 'POST':
		# When form submitted, update the Servo values
		servo_value = int(request.form['servo-value'])
		servo.changeAngle(servo_value)
		add_servo_data(servo_value)
	return redirect(url_for('home'))

# Render the Servo data page
@app.route('/servo')
def servo_data():
	servo_data = get_all_servo_data()
	# Render the Servo data with all values
	return render_template('servo.html', servo_data=servo_data)

# Update the ZIPLED values
@app.route('/zipleds/set', methods=['POST'])
def zipleds_set():
	if request.method == 'POST':
		# When form submitted, update the ZIPLED values
		red_value = request.form['red-value']
		green_value = request.form['green-value']
		blue_value = request.form['blue-value']
		brightness_value = request.form['brightness-value']
		zipleds.setBrightness(int(brightness_value))
		zipleds.fill((int(red_value), int(green_value), int(blue_value)))
		zipleds_value = red_value + "," + green_value + "," + blue_value + "," + brightness_value
		add_zipleds_data(zipleds_value)
	return redirect(url_for('home'))

# Render the ZIPLEDs data page
@app.route('/zipleds')
def zipleds_data():
	zipleds_data = get_all_zipleds_data()
	# Render the ZIPLED data with all values
	return render_template('zipleds.html', zipleds_data=zipleds_data)

# Update the High Power Out values to On
@app.route('/hpo/set', methods=['POST'])
def hpo_set():
	if request.method == 'POST':
		# When form submitted, update the High Power Out values
		hpo1_value = request.form['hpo1-value']
		hpo2_value = request.form['hpo2-value']
		hpo1.changeDutyCycle(int(hpo1_value))
		hpo2.changeDutyCycle(int(hpo2_value))
		add_hpo_data(hpo1_value, hpo2_value)
	return redirect(url_for('home'))

# Render the High Power Out data page
@app.route('/hpo')
def hpo_data():
	hpo_data = get_all_hpo_data()
	# Render the High Power Out data with all values
	return render_template('hpo.html', hpo_data=hpo_data)

# Download all the HAT data on the user's computer
@app.route('/download/all')
def download_all_data():
	conn = get_database_connection()
	curs = conn.cursor()
	curs.execute('SELECT * FROM sensorData ORDER BY id DESC;')
	# Write all the HAT data to a CSV file
	with open('static/hat-data.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow([i[0] for i in curs.description])
		writer.writerows(curs)
	conn.close()
	# Send all the HAT data in a CSV file to the user
	return send_file('static/hat-data.csv', as_attachment=True)

# Download all the BME688 data on the user's computer
@app.route('/download/bme688')
def download_bme688_data():
	bme688_data = get_all_bme688_data()
	# Write all the BME688 data to a CSV file
	with open('static/bme688-data.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["Time", "Temperature", "Pressure", "Humidity", "eCO2", "AirQualityPercent", "AirQualityScore"])
		writer.writerows(bme688_data)
	# Send all the BME688 data in a CSV file to the user
	return send_file('static/bme688-data.csv', as_attachment=True)

# Start the Flask web app
app.run(host="0.0.0.0", port=5000, debug=False)
