
jQuery(document).ready(function() {

	// Events
    $(".eventFX").on("click", function(){
        $(".caroucelEvents").toggleClass("showEvents");
    });


});


// Controle de elemtnos da interface
var controleElemen = true;
jQuery(window).scroll(function() {
	if(jQuery(window).width() > 250){

		if(jQuery(window).scrollTop() > 1){
			if(controleElemen){
				controleElemen = false;
                jQuery(".useScroll").addClass('hideUseScroll');
			}
		}else if(jQuery(window).scrollTop() < 1){
			controleElemen = true;
            jQuery(".useScroll").removeClass('hideUseScroll');;
		}

	}
	else {
        jQuery(".audioPlayerBox").removeClass('noScroll');
	}
});
