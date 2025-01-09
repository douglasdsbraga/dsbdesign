$('#clientes').owlCarousel({
    loop:true,
    margin: 30,
    // autoWidth:true,
    responsiveClass:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        740:{
            items:2
        },
        1170:{
            items:3,
            loop:false
        }
    }
});
// var caroucelEventosSlide = $('#caroucelSliderEventos');
// caroucelEventosSlide.owlCarousel();
// // Custom Navigation Events
// $(".ctaEventos-next").click(function(){
//     caroucelEventosSlide.trigger('next.owl.carousel');

// })
// $(".ctaEventos-prev").click(function(){
//     caroucelEventosSlide.trigger('prev.owl.carousel');
// })

$('#iniciativas').owlCarousel({
    loop:true,
    margin: 30,
    // autoWidth:true,
    responsiveClass:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        740:{
            items:1
        },
        1170:{
            items:2,
            loop:false
        }
    }
});
