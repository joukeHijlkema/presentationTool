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
    var number = target.hasAttribute("data-title") ? target.getAttribute("data-number"):"";
    document.getElementById("slideTitle").innerHTML= title;
    document.getElementById("slideSubTitle").innerHTML= sTitle;
    document.getElementById("slideNumber").innerHTML= number;
    // console.log("done")
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
	
