$(function () {
    恢复盒子大小
    $('.home').width(innerWidth)

    var topSwiper = new Swiper('#topSwiper', {
        pagination: '.swiper-pagination',
        // nextButton: '.swiper-button-next',
        // prevButton: '.swiper-button-prev',
        slidesPerView: 1,
        paginationClickable: true,
        spaceBetween: 30,
        loop: true,
        autoplay: 300,
        // effect: 'coverflow',
    });
    // var swiper = new Swiper('mustbuySwiper', {
    //   slidesPerView: 3,
    //   spaceBetween: 30,
    //   pagination: {
    //     el: '.swiper-pagination',
    //     clickable: true,
    //   },
    // });
    var mustbuySwiper = new Swiper('#mustbuySwiper', {
        slidesPerView: 3,
        spaceBetween:3,
        autoplay:3000,
        loop: true,
    });
})
