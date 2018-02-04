// Wait for impress.js to be initialized
document.addEventListener( "impress:init", function( event ) {

    // Getting API from event data.
    // So you don't event need to know what is the id of the root element
    // or anything. `impress:init` event data gives you everything you
    // need to control the presentation that was just initialized.
    var api = event.detail.api;
    // Delegated handler for clicking on the links to presentation steps
    document.addEventListener( "click", function( event ) {
	
	var element = event.target;
	// console.log("clicked "+element)
	if (element.hasAttribute("data-target")) {
	    target = element.getAttribute("data-target")
	    // console.log(target)
            // If it's a link to presentation step, target this step
            if ( target && target[ 0 ] === "#" ) {
		target = document.getElementById( target.slice( 1 ) );
            }
	    // console.log("jump to "+target.tagName);
	    if ( api.goto( target ) ) {
		event.stopImmediatePropagation();
		event.preventDefault();
	    }
	}
    }, false );
});

// Actions to take when we enter a slide
document.addEventListener( "impress:stepenter", function(event) {
    console.log("stepenter");
    target=event.target;
    // start videos
    if (target.getElementsByTagName("video").length > 0) {
        // Start the video on enter
        var vids = target.getElementsByTagName("video");
        var i = 0;
        for (i=0;i<vids.length;i++) {
            vids.item(i).play();
        }
    }
    // load titles
    var title = target.hasAttribute("data-title") ? target.getAttribute("data-title"):"";
    var sTitle = target.hasAttribute("data-subtitle") ? target.getAttribute("data-subtitle"):"";
    var number = target.hasAttribute("data-number") ? target.getAttribute("data-number"):"";
    document.getElementById("slideTitle").innerHTML= title;
    document.getElementById("slideSubTitle").innerHTML= sTitle;
    document.getElementById("slideNumber").innerHTML= number;
    if (target.hasAttribute("data-links")) makeLinks(target.getAttribute("data-links",target));
    // console.log(target.getAttribute("data-links"))
})


// Actions to take when we leave a slide
document.addEventListener( "impress:stepleave", function(event) {
    // console.log("stepleave");
    target=event.target;
    // pause videos
    if (target.getElementsByTagName("video").length > 0) {
        // Start the video on enter
        var vids = target.getElementsByTagName("video");
        var i = 0;
        for (i=0;i<vids.length;i++) {
            vids.item(i).pause();
        }
    }
    // remove titles
    document.getElementById("slideTitle").innerHTML= "";
    // console.log("done")
})
	
function makeLinks(links,slide) {
    console.log("link : "+links);
    var slideBB = target.getBoundingClientRect();
    var O      = new Vector(slideBB.x,slideBB.y);
    for (let pair of links.split(",")) {
	var elts   = pair.split(":");
	var line = document.getElementById(elts[0])
	var src = document.getElementById(elts[1].split(";")[0])
	var srcBB  = src.getBoundingClientRect();
	var srcAnc = elts[1].split(";")[1];
	var trg = document.getElementById(elts[2].split(";")[0])
	var trgBB  = trg.getBoundingClientRect();
	var trgAnc = elts[2].split(";")[1];

	P1 = new Vector(0.5*(srcBB.left+srcBB.right),0.5*(srcBB.bottom+srcBB.top));
	var dx = 0.6*srcBB.width;
	var dy = 0.6*srcBB.height;
	switch (srcAnc) {
	case "n":
	    P1.subtract(new Vector(0,dy));
	    break;
	case "e":
	    P1.add(new Vector(dx,0));
	    break;
	case "s":
	    P1.add(new Vector(0,dy));
	    break;
	case "w":
	    P1.subtract(new Vector(dx,0));
	}
	P2 = new Vector(0.5*(trgBB.left+trgBB.right),0.5*(trgBB.bottom+trgBB.top));
	dx = 0.6*trgBB.width;
	dy = 0.6*trgBB.height;
	switch (trgAnc) {
	case "n":
	    P2.subtract(new Vector(0,dy));
	    break;
	case "e":
	    P2.add(new Vector(dx,0));
	    break;
	case "s":
	    P2.add(new Vector(0,dy));
	    break;
	case "w":
	    P2.subtract(new Vector(dx,0));
	}
	
	var arrow = document.getElementById("svg-"+target.getAttribute("data-name"));
	line.setAttribute("d",arrowString(O,P1,P2,10,5));
	line.setAttribute("stroke", "black");  
	line.setAttribute("stroke-width", 10);  
	line.setAttribute("fill", "black");  
    }
}

function arrowString(O,P1,P2,l,w) {
    dP = Vector.subtract(P2,P1).normalize();
    nP = Vector.rotate(dP,0.5*Math.PI);
    // P1.subtract(O).add(Vector.multiply(dP,20));
    // P2.subtract(O).subtract(Vector.multiply(dP,20));
    P1.subtract(O);
    P2.subtract(O);
    P3 = Vector.subtract(P2,Vector.multiply(dP,l));
    P4 = Vector.add(P3,Vector.multiply(nP,w));
    P5 = Vector.subtract(P3,Vector.multiply(nP,w));
    
    var Pt = new Vector(P2.x,P2.y);
    var d = "M"+P1.x+" "+P1.y;
    d+= "L "+P3.x+" "+P3.y;
    d+= "L "+P4.x+" "+P4.y;
    d+= "L "+P2.x+" "+P2.y;
    d+= "L "+P5.x+" "+P5.y;
    d+= "L "+P3.x+" "+P3.y;
    
    console.log(d);

    return d;
}
