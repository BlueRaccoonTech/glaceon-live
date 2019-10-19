document.addEventListener('DOMContentLoaded', function() {
if (shaka.log) {
	shaka.log.setLevel(shaka.log.Level.V1);
}
var video = document.getElementById("video");
var script = document.createElement("script");
script.src = "/"+streamer+".js";
window.video = video;
document.head.appendChild(script);
var mount = document.getElementById("shaka-mount-point");
var player = new shaka.Player(video);
var ui = new shaka.ui.Overlay(player, mount, video, {
	addSeekBar: false,
	controlPanelElements: ['spacer', 'mute', 'volume', 'fullscreen', 'overflow_menu'],
	overflowMenuButtons: ['quality', 'picture_in_picture']
});
var controls = ui.getControls();
window.ui = ui;
window.player = player;
window.controls = controls;
player.addEventListener("error", console.error);
controls.addEventListener("error", console.error);
player.configure({
});
player.load("/hls/"+streamer+".m3u8").then(function() {
	video.play();
	console.log("Loaded!");
}).catch(function(e) {
	if (e.code === 1001) {
		if (e.data[1] === 404) {
			return
		}
	}
	console.error(e);
});
});
function onResize() {
	var streamOnly = document.body.classList.contains("stream-only");
	if ((window.innerWidth/(window.innerHeight-(streamOnly ? 0 : 100))) < (16/9) || (!streamOnly && window.innerWidth < 960)) {
		document.body.classList.remove("wide");
		document.body.classList.add("tall");
	} else if (((window.innerWidth-(streamOnly ? 0 : 300))/window.innerHeight) > (16/9)) {
		document.body.classList.add("wide");
		document.body.classList.remove("tall");
	} else {
		document.body.classList.remove("wide");
		document.body.classList.remove("tall");
	}
}
window.addEventListener('resize', onResize);
document.addEventListener('DOMContentLoaded', onResize);
