$(function(){
	
	$('#countdown').countup();
	
});

var app = {
    chars: ["dvm", "bee", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    init: function() {
        app.container = document.createElement("div");
        app.container.className = "animation-container";
        document.body.appendChild(app.container);
        window.setInterval(app.add, 100)
    },
    add: function() {
        var a = document.createElement("span");
        app.container.appendChild(a);
        app.animate(a)
    },
    animate: function(a) {
        var n = app.chars[Math.floor(Math.random() * app.chars.length)];
        var e = Math.floor(Math.random() * 15) + 1;
        var t = Math.floor(Math.random() * (50 - e * 2)) + 3;
        var o = 10 + (15 - e);
        a.style.cssText = "right:" + t + "vw; right:" + t + "vw; font-size:" + o + "px;animation-duration:" + e + "s";
        a.innerHTML = n;
        window.setTimeout(app.remove, e * 1e3, a)
    },
    remove: function(a) {
        a.parentNode.removeChild(a)
    }
};
document.addEventListener("DOMContentLoaded", app.init);