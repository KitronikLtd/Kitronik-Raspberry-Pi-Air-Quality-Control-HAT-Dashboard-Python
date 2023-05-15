var servoValue = document.getElementById("servo-value");
var servoLabel = document.getElementById("servo-label");
var redValue = document.getElementById("red-value");
var redLabel = document.getElementById("red-label");
var greenValue = document.getElementById("green-value");
var greenLabel = document.getElementById("green-label");
var blueValue = document.getElementById("blue-value");
var blueLabel = document.getElementById("blue-label");
var brightnessValue = document.getElementById("brightness-value");
var brightnessLabel = document.getElementById("brightness-label");
var red = redValue.value;
var green = greenValue.value;
var blue = blueValue.value;
setRGB();
brightnessValue.style.backgroundColor = "rgba(0, 0, 0, " + (1 - brightnessValue.value / 100) + ")";
var hpo1Value = document.getElementById("hpo1-value");
var hpo1Label = document.getElementById("hpo1-label");
var hpo2Value = document.getElementById("hpo2-value");
var hpo2Label = document.getElementById("hpo2-label");

servoValue.oninput = function() {
	servoLabel.innerHTML = "Servo Angle: " + this.value;
}

redValue.oninput = function() {
	redLabel.innerHTML = "Red: " + this.value;
	red = this.value;
	setRGB();
}

greenValue.oninput = function() {
	greenLabel.innerHTML = "Green: " + this.value;
	green = this.value;
	setRGB();
}

blueValue.oninput = function() {
	blueLabel.innerHTML = "Blue: " + this.value;
	blue = this.value;
	setRGB();
}

brightnessValue.oninput = function() {
	brightnessLabel.innerHTML = "Brightness: " + this.value;
	brightnessValue.style.backgroundColor = "rgba(0, 0, 0, " + (1 - this.value / 100) + ")";
}

function setRGB() {
	redValue.style.backgroundColor = "rgb(" + red + ", " + green + ", " + blue + ")";
	greenValue.style.backgroundColor = "rgb(" + red + ","  + green + "," + blue + ")";
	blueValue.style.backgroundColor = "rgb(" + red + ", " + green + ", " + blue + ")";
}

hpo1Value.oninput = function() {
	hpo1Label.innerHTML = "HPO 1: " + this.value;
}

hpo2Value.oninput = function() {
	hpo2Label.innerHTML = "HPO 2: " + this.value;
}
