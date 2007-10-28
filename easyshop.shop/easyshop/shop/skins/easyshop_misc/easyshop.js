function easyShopZoomWindow(url, w, h) {
	w = window.open(url, "Preview", "height=" + h +", width=" + w +", screenX=500, screenY=150, scrollbars=yes, resizable=yes");
	w.focus();
}