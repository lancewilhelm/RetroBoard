var CHAR_SPACE = 1;
var CHAR_WIDTH = 5;
var CHAR_HEIGHT = 5;
var CHAR_COUNT = 8;
var BUF_CHAR_COUNT = 128;
var DM_WIDTH = 64;
var DM_HEIGHT = 32;
var DOT_RADIUS = 5;
var DOT_PAD = 1;
var OUT_PAD = 5;

function Display(canvas) {
	this.canvas = canvas || document.createElement("canvas");
	this.ctx = this.canvas.getContext("2d");
	this.mat = new Array(DM_WIDTH);
	for (var i = 0; i < this.mat.length; i++) {
		this.mat[i] = new Array(DM_HEIGHT)
		for (var j = 0; j < this.mat[i].length; j++) {
			this.mat[i][j] = [0, 0, 0]
		}
	}
	
	this.is_equal = function(arr1, arr2) {
		for (var i = 0, l = arr1.length; i < l; i++) {
			if (arr1[i] !== arr2[2]) {
				return false;
			};
		};
		return true;
	};

	this.set = function(x, y, v) {
		v = v || false;
		var i = x + y * DM_WIDTH;
		this.mat[i] = v;
	};
	
	this.clear = function() {
		for (var i = 0; i < this.mat.length; i++)
			this.mat[i] = false;
	};
	
	this.redraw = function() {
		var ctx = this.ctx;
		var pad = DOT_PAD * 2;
		var rad = (DOT_RADIUS+pad/2);
		this.canvas.width = (DM_WIDTH * rad * 2) + OUT_PAD*2;
		this.canvas.height = (DM_HEIGHT * rad * 2) + OUT_PAD*2;

		ctx.fillStyle = "#000";
		ctx.fillRect(0, 0, canvas.width, canvas.height);

		for (var y = 0; y < DM_HEIGHT; y++) {
			for (var x = 0; x < DM_WIDTH; x++) {
				var dx = x * rad * 2 + OUT_PAD,
					dy = y * rad * 2 + OUT_PAD;
				var idx = x + y * DM_WIDTH;
				
				ctx.fillStyle = "#222";
				ctx.beginPath();
				ctx.arc(dx + rad, dy + rad, DOT_RADIUS, 0, Math.PI * 2);
				ctx.fill();
				
				if (!this.is_equal(this.mat[x][y], [0, 0, 0])) {
					ctx.fillStyle = 'rgb('+ this.mat[x][y][0] + ','+ this.mat[x][y][1] +',' + this.mat[x][y][2] +')';
					ctx.shadowColor = 'rgb('+ this.mat[x][y][0] + ','+ this.mat[x][y][1] +',' + this.mat[x][y][2] +')';
					ctx.shadowBlur = rad + OUT_PAD;
					ctx.shadowOffsetX = 0;
					ctx.shadowOffsetY = 0;
					ctx.beginPath();
					ctx.arc(dx + rad, dy + rad, DOT_RADIUS, 0, Math.PI * 2);
					ctx.fill();
					ctx.shadowBlur = 0;
				}
			}
		}
	};
	
	this.start = function() {
		var that = this;
		this.redraw();
		const socket = new WebSocket('ws://' + location.host + '/data')
		socket.addEventListener('message', e => {
			this.mat = JSON.parse(e.data);
			this.redraw();
		})
	};
};

var canvas = document.getElementById("display");
var ctx = canvas.getContext("2d");


var d = new Display(canvas);
d.start();