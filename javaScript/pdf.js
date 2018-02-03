function myLoadSlide() {
    console.log("loaded");
    var target = document.getElementsByClassName("slide")[0];
    var title  = target.hasAttribute("data-title") ? target.getAttribute("data-title"):"";
    document.getElementById("slideTitle").innerHTML= title;
    
}
