// Look at https://www.html5rocks.com/en/tutorials/canvas/performance/
// for information on how to float multiple canvases.
// I think that when I decide to draw the bicycles, I'll draw them all
// on separate canvases, that way it is easy to add/delete them without
// affecting the other drawings.

console.log('Testing out my javascript');

var canvas = document.querySelector('canvas');
console.log(canvas);

canvas.width = canvas.clientWidth;
canvas.height = (canvas.width * innerHeight / innerWidth) | 0; //canvas.clientHeight;

var c = canvas.getContext('2d');

var x = 100;
var y = 50;
var width = 100;
var height = 20;
c.fillStyle = 'rgba(255, 0, 0, 0.5)'
c.fillRect(x, y, width, height);
c.fillStyle = 'rgba(0, 0, 255, 0.5)'
c.fillRect(150, 60, width, height)

// Need to figure out how to move the 'zero' coordinate of the canvas

// Line
var sizeWidth = canvas.width;
var sizeHeight = canvas.height;
var scaleWidth = sizeWidth/100;
var scaleHeight = sizeHeight/100;
var size = { width: sizeWidth, height: sizeHeight };
console.log(size);
var scale = { width: scaleWidth, height: scaleHeight };
console.log(scale);

// circle
c.beginPath();
c.arc(0, 0, 20, 0, 2*Math.PI);
c.strokeStyle = "orange"
c.stroke();

// lines!
c.beginPath();
c.moveTo(0, 0)
c.lineTo(0, sizeHeight/2);
c.lineTo(sizeWidth/2, 0);
c.lineTo(sizeWidth, sizeHeight/2);
c.lineTo(sizeWidth/2, sizeHeight);
c.lineTo(0, sizeHeight/2);
c.strokeStyle = "blue"
c.stroke();


// Math.random();
// window.innerWidth;
// window.innerHeight;


// So many circles!
var centerX = 10;
var centerY = 20;
for (var i = 0; i <= 10; i++) {
	c.beginPath();
	c.arc(centerX + i*20, centerY + i*5, 25 + i*2, 0, 2 * Math.PI);
	c.stroke();
}

var x = (Math.random() * sizeWidth) | 0;
var y = (Math.random() * sizeHeight) | 0;
var maxDx = 500;
var maxDy = 500;
var dx = (Math.random() * maxDx) - 0.5 * maxDx;
var dy = (Math.random() * maxDy) - 0.5 * maxDy;
var radius = (Math.random() * 30) | 0;

console.log(innerWidth)
console.log(sizeWidth)

var lastRender = Date.now();
function animate() {
	requestAnimationFrame(animate);
	now = Date.now();
	var deltaT = (now - lastRender) * 1e-3;
	lastRender = now;
	c.clearRect(0, 0, sizeWidth, sizeHeight);

	c.beginPath();
	c.arc(x | 0, y | 0, radius, 0, 2 * Math.PI);
	c.strokeStyle = 'blue'
	c.stroke();

	if (x + radius > sizeWidth || x - radius < 0) {
		dx = -dx;
		console.log({x_pos: x|0, y_pos: y|0, dx: dx, dy: dy})
	}

	if (y + radius > sizeHeight || y - radius < 0) {
		dy = -dy;
		console.log({x_pos: x|0, y_pos: y|0, dx: dx, dy: dy})
	}

	x += dx * deltaT;
	y += dy * deltaT;
	
	//console.log({x_pos: x, y_pos: y})
	console.log("FPS: " + 1/deltaT)
}

animate()
