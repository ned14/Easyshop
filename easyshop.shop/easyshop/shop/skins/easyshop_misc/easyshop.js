function easyShopZoomWindow(url, w, h) {
	w = window.open(url, "Preview", "height=" + h +", width=" + w +", screenX=500, screenY=150, scrollbars=yes, resizable=yes");
	w.focus();
}

function myToggleSelect() 
{
     for (i = 0; i < document.getElementsByName("paths:list").length; i++)
     {
        var status = document.getElementsByName("paths:list")[i].checked;

        if (status == false)
        {
           var new_status = true
        }
        else 
        {
           var new_status = false               
        }
        document.getElementsByName("paths:list")[i].checked = new_status
     }
}