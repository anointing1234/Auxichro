;(function($){

$(document).ready(function(){

//========== HEADER ACTIVE STRATS ============= //
function initHeaderSticky() {
  var windowOn = $(window);
  windowOn.on('scroll', function () {
    var scroll = windowOn.scrollTop();
    if (scroll < 100) {
      $(".vl-header-area").removeClass("header-sticky");
    } else {
      $(".vl-header-area").addClass("header-sticky");
    }
  });
}
initHeaderSticky();
//========== HEADER ACTIVE ENDS ============= //

//========== MOBILE MENU STARTS ============= //
function initOffcanvasMenu() {
  var vlMenuWrap = $('.vl-mobile-menu-active > ul').clone();
  var vlSideMenu = $('.vl-offcanvas-menu nav');
  vlSideMenu.append(vlMenuWrap);

  if ($(vlSideMenu).find('.sub-menu, .vl-mega-menu').length !== 0) {
    $(vlSideMenu).find('.sub-menu, .vl-mega-menu').parent().append('<button class="vl-menu-close"><i class="fas fa-chevron-right"></i></button>');
  }

  var sideMenuList = $('.vl-offcanvas-menu nav > ul > li button.vl-menu-close, .vl-offcanvas-menu nav > ul li.has-dropdown > a');
  $(sideMenuList).on('click', function (e) {
    e.preventDefault();
    if (!$(this).parent().hasClass('active')) {
      $(this).parent().addClass('active');
      $(this).siblings('.sub-menu, .vl-mega-menu').slideDown();
    } else {
      $(this).siblings('.sub-menu, .vl-mega-menu').slideUp();
      $(this).parent().removeClass('active');
    }
  });

  $(".vl-offcanvas-toggle").on('click', function () {
    $(".vl-offcanvas").addClass("vl-offcanvas-open");
    $(".vl-offcanvas-overlay").addClass("vl-offcanvas-overlay-open");
  });

  $(".vl-offcanvas-close-toggle, .vl-offcanvas-overlay").on('click', function () {
    $(".vl-offcanvas").removeClass("vl-offcanvas-open");
    $(".vl-offcanvas-overlay").removeClass("vl-offcanvas-overlay-open");
  });
}

initOffcanvasMenu();
//========== MOBILE MENU ENDS ============= //

//========== SIDEBAR/SEARCH AREA ============= //
function initHeaderSearchPopup() {
  $(".header-search-btn").on("click", function (e) {
    e.preventDefault();
    $(".header-search-form-wrapper").addClass("open");
    $('.header-search-form-wrapper input[type="search"]').focus();
    $('.body-overlay').addClass('active');
  });

  $(".tx-search-close").on("click", function (e) {
    e.preventDefault();
    $(".header-search-form-wrapper").removeClass("open");
    $("body").removeClass("active");
    $('.body-overlay').removeClass('active');
  });
}
initHeaderSearchPopup();
//========== SIDEBAR/SEARCH AREA ============= //

//========== PAGE PROGRESS STARTS ============= // 
function initScrollProgress() {
  var progressPath = document.querySelector(".progress-wrap path");
  if (!progressPath) return;
  var pathLength = progressPath.getTotalLength();
  progressPath.style.transition = progressPath.style.WebkitTransition = "none";
  progressPath.style.strokeDasharray = pathLength + " " + pathLength;
  progressPath.style.strokeDashoffset = pathLength;
  progressPath.getBoundingClientRect();
  progressPath.style.transition = progressPath.style.WebkitTransition = "stroke-dashoffset 10ms linear";
  var updateProgress = function () {
    var scroll = $(window).scrollTop();
    var height = $(document).height() - $(window).height();
    var progress = pathLength - (scroll * pathLength) / height;
    progressPath.style.strokeDashoffset = progress;
  };
  updateProgress();
  $(window).on('scroll', updateProgress);
  var offset = 50;
  var duration = 550;
  $(window).on("scroll", function () {
    if ($(this).scrollTop() > offset) {
      $(".progress-wrap").addClass("active-progress");
    } else {
      $(".progress-wrap").removeClass("active-progress");
    }
  });
  $(".progress-wrap").on("click", function (event) {
    event.preventDefault();
    $("html, body").animate({ scrollTop: 0 }, duration);
    return false;
  });
}
initScrollProgress();
//========== PAGE PROGRESS STARTS ============= // 

//========== VIDEO POPUP STARTS ============= //
function initYoutubePopup() {
  var youtubePopup = $(".popup-youtube");
  if (youtubePopup.length > 0) {
    youtubePopup.magnificPopup({
      type: "iframe",
    });
  }
}
initYoutubePopup();
//========== VIDEO POPUP ENDS ============= //
AOS.init;
AOS.init({disable: 'mobile'});

//========== NICE SELECT ============= //
$('select').niceSelect();

//========== CASE IMAGE ============= //
function initHoverActive() {
  $('.cs_hover_active').hover(function () {
    $(this).addClass('active').siblings().removeClass('active');
  });
}
initHoverActive();

});
//========== COUNTER UP============= //
function initCounterUp() {
  const ucounter = $('.counter');
  if (ucounter.length > 0) {
    ucounter.countUp();
  }
}
initCounterUp();
//========== TESTIMONIAL AREA ============= //

// SLIDER //
$(".testimonial-single-slider").slick({
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows: true,
  prevArrow: $(".testimonial-prev-arrow"),
  nextArrow: $(".testimonial-next-arrow"),
  loop: true,
  autoplay:true,
  autoplayTimeout:500,
});

// SLIDER //
$(".testimonial-single-slider3").slick({
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows: true,
  prevArrow: $(".prev-arrow"),
  nextArrow: $(".next-arrow"),
  loop: true,
  autoplay:true,
  autoplayTimeout:500,
});

// SLIDER //
$('.team-single-slider').owlCarousel({
  loop:true,
  margin:30,
  nav:true,
  dots:true,
  items:10,
  navText:["<i class='fa-solid fa-angle-left'></i>" , "<i class='fa-solid fa-angle-right'></i>"],
  autoplay:true,
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:2,
      },
      1000:{
          items:3,
      }
  }
});

// SLIDER //
$('.team-single-slider2').owlCarousel({
  loop:true,
  margin:30,
  nav:true,
  dots:false,
  items:10,
  navText:["<i class='fa-solid fa-angle-left'></i>" , "<i class='fa-solid fa-angle-right'></i>"],
  autoplay:true,
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:2,
      },
      1000:{
          items:3,
      }
  }
});

// SLIDER //
$('.service-single-slider').owlCarousel({
  loop:true,
  margin:30,
  nav:true,
  dots:true,
  items:10,
  navText:["<i class='fa-solid fa-angle-left'></i>" , "<i class='fa-solid fa-angle-right'></i>"],
  autoplay:true,
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:2,
      },
      1000:{
          items:3,
      }
  }
});

// SLIDER //
$('.testimonial-single-slider2').owlCarousel({
  loop:true,
  margin:30,
  nav:true,
  dots:true,
  items:10,
  navText:["<i class='fa-solid fa-angle-left'></i>" , "<i class='fa-solid fa-angle-right'></i>"],
  autoplay:true,
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:2,
      },
      1000:{
          items:2,
      }
  }
});

// SLIDER //
$(".hero-main-slider").slick({
  autoplay:true,
  autoplaySpeed:2000,
  speed:1500,
  slidesToShow:1,
  slidesToScroll:1,
  pauseOnHover:false,
  dots:false,
  arrows:true,
  pauseOnDotsHover:true,
  cssEase:'linear',
  fade:true,
  draggable:true,
  prevArrow: $(".testimonial-prev-arrow"),
  nextArrow: $(".testimonial-next-arrow"), 
}); 


// SLIDER //
$('.team-box-slider').owlCarousel({
  loop:true,
  margin:30,
  nav:true,
  dots:true,
  items:10,
  navText:["<i class='fa-solid fa-angle-left'></i>" , "<i class='fa-solid fa-angle-right'></i>"],
  autoplay:true,
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:2,
      },
      1000:{
          items:4,
      }
  }
});

// SLIDER //
$('.team4-slider-area').owlCarousel({
  loop:true,
  margin:30,
  nav:false,
  dots:true,
  items:10,
  autoplay:true,
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:2,
      },
      1000:{
          items:4,
      }
  }
});

// SLIDER //
$('.service4-slider-area').owlCarousel({
  loop:true,
  margin:30,
  nav:false,
  dots:true,
  items:10,
  autoplay:true,
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:2,
      },
      1000:{
          items:4,
      }
  }
});

// SLIDER //
$('.testimonial4-slider-area').owlCarousel({
  loop:true,
  margin:30,
  nav:false,
  dots:true,
  items:10,
  autoplay:true,
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:2,
      },
      1000:{
          items:3,
      }
  }
});

// SLIDER //
$('.shop-single-slider').owlCarousel({
  loop:true,
  margin:30,
  nav:true,
  dots:false,
  items:10,
  autoplay:true,
  navText:["<i class='fa-solid fa-angle-left'></i>" , "<i class='fa-solid fa-angle-right'></i>"],
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:2,
      },
      1000:{
          items:4,
      }
  }
});

// SLIDER //
$('.blog-slider-area').owlCarousel({
  loop:true,
  margin:30,
  nav:true,
  dots:false,
  items:10,
  autoplay:true,
  navText:["<i class='fa-solid fa-angle-left'></i>" , "<i class='fa-solid fa-angle-right'></i>"],
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:2,
      },
      1000:{
          items:3,
      }
  }
});

// SLIDER //
$('.testimonial7-slider-boxarea').owlCarousel({
  loop:true,
  margin:30,
  nav:true,
  dots:false,
  fade:true,
  items:10,
  autoplay:true,
  navText:["<i class='fa-solid fa-angle-left'></i>" , "<i class='fa-solid fa-angle-right'></i>"],
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:1,
      },
      1000:{
          items:1,
      }
  }
});

// SLIDER //
$('.team-slide-widget').owlCarousel({
  loop:true,
  margin:30,
  nav:false,
  dots:true,
  fade:true,
  items:10,
  autoplay:true,
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:2,
      },
      1000:{
          items:4,
      }
  }
});

// SLIDER //
$(".testimonial8-imges").slick({
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows: false,
  autoplay:true,
  autoplaySpeed:2000,
  loop: true,
  focusOnSelect: true,
  vertical:false,
  asNavFor: ".testimonial-content-slider",
  infinite: true,
  fade:true,
});

$(".testimonial-content-slider").slick({
  slidesToShow: 1,
  slidesToScroll: 1,
  asNavFor: ".testimonial8-imges",
  dots: false,
  arrows: true,
  centerMode: false,
  focusOnSelect: true,
  loop: true,
  autoplay:true,
  autoplaySpeed:2000,
  prevArrow: $(".testimonial-prev-arrow"),
  nextArrow: $(".testimonial-next-arrow"), 
});

// SLIDER //
$('.hero8-images-area').owlCarousel({
  loop:true,
  margin:30,
  nav:true,
  dots:false,
  navText:["<i class='fa-solid fa-angle-left'></i>" , "<i class='fa-solid fa-angle-right'></i>"],
  fade:true,
  items:10,
  animateOut: 'fadeOut',
  animateIn: 'fadeIn',
  autoplay:true,
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:1,
      },
      1000:{
          items:1,
      }
  }
});

// SLIDER //
$('.team6-slider-widget').owlCarousel({
  loop:true,
  margin:30,
  nav:true,
  dots:false,
  navText:["<i class='fa-solid fa-arrow-left'></i>" , "<i class='fa-solid fa-arrow-right'></i>"],
  fade:true,
  items:10,
  autoplay:true,
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:2,
      },
      1000:{
          items:4,
      }
  }
});

// SLIDER //
$('.testimonial8-widgetarea ').owlCarousel({
  loop:true,
  margin:30,
  nav:true,
  dots:false,
  navText:["<i class='fa-solid fa-arrow-left'></i>" , "<i class='fa-solid fa-arrow-right'></i>"],
  fade:true,
  items:10,
  autoplay:true,
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:1,
      },
      1000:{
          items:1,
      }
  }
});

// SLIDER //
$('.case-slider-area').owlCarousel({
  loop:true,
  margin:30,
  nav:true,
  dots:false,
  navText:["<i class='fa-solid fa-arrow-left'></i>" , "<i class='fa-solid fa-arrow-right'></i>"],
  fade:true,
  items:10,
  autoplay:true,
  smartSpeed:2000,
  autoplayTimeout:3000,
  responsiveClass:true,
  responsive:{
      0:{
          items:1,
      },
      600:{
          items:2,
      },
      1000:{
          items:3,
      }
  }
});
//========== PRELOADER ============= //
function initPreloader() {
  $(window).on("load", function () {
    setTimeout(function () {
      $(".cs_preloader").fadeToggle();
    }, 200);
  });
}
initPreloader();


})(jQuery);


//========== GSAP AREA ============= //
function initTextAnimation() {
  if ($('.text-anime-style-1').length) {
    let staggerAmount = 0.05,
        translateXValue = 0,
        delayValue = 0.5,
        animatedTextElements = document.querySelectorAll('.text-anime-style-1');

    animatedTextElements.forEach((element) => {
      let animationSplitText = new SplitText(element, { type: "chars, words" });
      gsap.from(animationSplitText.words, {
        duration: 1,
        delay: delayValue,
        x: 20,
        autoAlpha: 0,
        stagger: staggerAmount,
        scrollTrigger: { trigger: element, start: "top 85%" },
      });
    });
  }
}
initTextAnimation();

function initTextAnimationStyle2() {
  if ($('.text-anime-style-2').length) {
    let staggerAmount = 0.05,
        translateXValue = 20,
        delayValue = 0.5,
        easeType = "power2.out",
        animatedTextElements = document.querySelectorAll('.text-anime-style-2');

    animatedTextElements.forEach((element) => {
      let animationSplitText = new SplitText(element, { type: "chars, words" });
      gsap.from(animationSplitText.chars, {
        duration: 1,
        delay: delayValue,
        x: translateXValue,
        autoAlpha: 0,
        stagger: staggerAmount,
        ease: easeType,
        scrollTrigger: { trigger: element, start: "top 85%" },
      });
    });
  }
}

initTextAnimationStyle2();

function initTextAnimationStyle3() {
  if ($('.text-anime-style-3').length) {
    let animatedTextElements = document.querySelectorAll('.text-anime-style-3');

    animatedTextElements.forEach((element) => {
      if (element.animation) {
        element.animation.progress(1).kill();
        element.split.revert();
      }
      element.split = new SplitText(element, {
        type: "lines,words,chars",
        linesClass: "split-line",
      });
      gsap.set(element, { perspective: 400 });
      gsap.set(element.split.chars, { opacity: 0, x: "50" });
      element.animation = gsap.to(element.split.chars, {
        scrollTrigger: { trigger: element, start: "top 90%" },
        x: "0",
        y: "0",
        rotateX: "0",
        opacity: 1,
        duration: 1,
        ease: Back.easeOut,
        stagger: 0.02,
      });
    });
  }
}
initTextAnimationStyle3();


function initRevealAnimation() {
  if ($('.reveal').length) {
    gsap.registerPlugin(ScrollTrigger);

    let revealContainers = document.querySelectorAll(".reveal");

    revealContainers.forEach((container) => {
      let image = container.querySelector("img");
      
      let tl = gsap.timeline({
        scrollTrigger: {
          trigger: container,
          toggleActions: "play none none none",
        }
      });
      tl.set(container, { autoAlpha: 1 });
      tl.from(container, 1.5, { xPercent: -100, ease: Power2.out });
      tl.from(image, 1.5, { xPercent: 100, scale: 1.3, delay: -1.5, ease: Power2.out });
    });
  }
}

initRevealAnimation();



//========== FILTER IMAGE ============= //
jQuery(document).ready(function($){
  var dragging = false,
      scrolling = false,
      resizing = false;
  
  var imageComparisonContainers = $('.cd-image-container');

  checkPosition(imageComparisonContainers);

  $(window).on('scroll', function(){
      if( !scrolling) {
          scrolling = true;
          requestAnimationFrame(function(){ checkPosition(imageComparisonContainers); });
      }
  });

  imageComparisonContainers.each(function(){
      var container = $(this);
      drags(container.find('.cd-handle'), container.find('.cd-resize-img'), container, 
           container.find('.cd-image-label[data-type="original"]'), 
           container.find('.cd-image-label[data-type="modified"]'));
  });

  $(window).on('resize', function(){
      if( !resizing) {
          resizing = true;
          requestAnimationFrame(function(){ checkLabel(imageComparisonContainers); });
      }
  });

  function checkPosition(container) {
      container.each(function(){
          var actualContainer = $(this);
          if( $(window).scrollTop() + $(window).height() * 0.5 > actualContainer.offset().top) {
              actualContainer.addClass('is-visible');
          }
      });
      scrolling = false;
  }

  function checkLabel(container) {
      container.each(function(){
          var actual = $(this);
          updateLabel(actual.find('.cd-image-label[data-type="modified"]'), actual.find('.cd-resize-img'), 'left');
          updateLabel(actual.find('.cd-image-label[data-type="original"]'), actual.find('.cd-resize-img'), 'right');
      });
      resizing = false;
  }

  function drags(dragElement, resizeElement, container, labelContainer, labelResizeElement) {
      dragElement.on("mousedown vmousedown", function(e) {
          dragElement.addClass('draggable1');
          resizeElement.addClass('resizable1');

          var dragWidth = dragElement.outerWidth(),
              xPosition = dragElement.offset().left + dragWidth - e.pageX,
              containerOffset = container.offset().left,
              containerWidth = container.outerWidth(),
              minLeft = containerOffset + 10,
              maxLeft = containerOffset + containerWidth - dragWidth - 10;
          dragElement.parents().on("mousemove vmousemove", function(e) {
              if( !dragging) {
                  dragging = true;
                  requestAnimationFrame(function(){ animateDraggedHandle(e, xPosition, dragWidth, minLeft, maxLeft, containerOffset, containerWidth, resizeElement, labelContainer, labelResizeElement); });
              }
          }).on("mouseup vmouseup", function(e){
              dragElement.removeClass('draggable1');
              resizeElement.removeClass('resizable1');
          });
          e.preventDefault();
      }).on("mouseup vmouseup", function(e) {
          dragElement.removeClass('draggable1');
          resizeElement.removeClass('resizable1');
      });
  }

  function animateDraggedHandle(e, xPosition, dragWidth, minLeft, maxLeft, containerOffset, containerWidth, resizeElement, labelContainer, labelResizeElement) {
      var leftValue = e.pageX + xPosition - dragWidth;   
      leftValue = Math.max(minLeft, Math.min(leftValue, maxLeft));

      var widthValue = (leftValue + dragWidth / 2 - containerOffset) * 100 / containerWidth + '%';
      $('.draggable1').css('left', widthValue);
      $('.resizable1').css('width', widthValue);
      updateLabel(labelResizeElement, resizeElement, 'left');
      updateLabel(labelContainer, resizeElement, 'right');

      dragging = false;
  }

  function updateLabel(label, resizeElement, position) {
      if(position === 'left') {
          (label.offset().left + label.outerWidth() < resizeElement.offset().left + resizeElement.outerWidth()) ? label.removeClass('is-hidden') : label.addClass('is-hidden');
      } else {
          (label.offset().left > resizeElement.offset().left + resizeElement.outerWidth()) ? label.removeClass('is-hidden') : label.addClass('is-hidden');
      }
  }
});
