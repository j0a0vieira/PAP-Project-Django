var vContinue = document.getElementById("continue"),
    vLogin = document.getElementById("login");

vContinue.addEventListener("click", function() {
   document.body.className += ' denied';
}, false);

var pfx = ["webkit", "moz", "MS", "o", ""];
function PrefixedEvent(element, type, callback) {
  for (var p = 0; p < pfx.length; p++) {
    if (!pfx[p]) type = type.toLowerCase();
    element.addEventListener(pfx[p]+type, callback, false);
  }
}

PrefixedEvent(vLogin, "AnimationEnd", function () {
  document.body.className = '';
});
