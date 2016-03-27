var waypoint = new Waypoint({
  element: document.getElementById('skilled'),
  handler: function(direction) {
    console.log('activated');
    var progress = setInterval(function () {
      var $bar = $('.bar');
      console.log($bar.width());
      if (($(window).width() > 650 && $(window).width() < 1000) || $(window).width() > 1250) {

      if ($bar.width() >= 600) {
          clearInterval(progress);
          $('.progress').removeClass('active');
      } else {
          $bar.width($bar.width() + 60);
      }
      if (($bar.width() / 6) > 100) {
        $bar.text(100 + "%");
      } else {
        $bar.text(Math.round($bar.width() / 6) + "%");
      };
    } else {
      $('.maintainer').width(300);
      if ($bar.width() >= 300) {
          clearInterval(progress);
          $('.progress').removeClass('active');
      } else {
          $bar.width($bar.width() + 30);
      }
      if (($bar.width() / 3) > 100) {
        $bar.text(100 + "%");
      } else {
        $bar.text(Math.round($bar.width() / 3) + "%");
      };
    };
    }, 600);
    offset: 5500
   }
 });

$(window).resize(function() {
  if (($(window).width() > 650 && $(window).width() < 1000) || $(window).width() > 1250) {
  $('.maintainer').width(600);
  } else {
    $('.maintainer').width(300);
  };
  var $bar = $('.bar');
  $bar.width(0);
  var waypoint = new Waypoint({
    element: document.getElementById('skilled'),
    handler: function(direction) {
      console.log('activated');
      var progress = setInterval(function () {
        var $bar = $('.bar');
        console.log($bar.width());
        if (($(window).width() > 650 && $(window).width() < 1000) || $(window).width() > 1250) {

        if ($bar.width() >= 600) {
            clearInterval(progress);
            $('.progress').removeClass('active');
        } else {
            $bar.width($bar.width() + 120);
        }
        if (($bar.width() / 6) > 100) {
          $bar.text(100 + "%");
        } else {
          $bar.text(Math.round($bar.width() / 6) + "%");
        };
      } else {
        $('.maintainer').width(300);
        if ($bar.width() >= 300) {
            clearInterval(progress);
            $('.progress').removeClass('active');
        } else {
            $bar.width($bar.width() + 60);
        }
        if (($bar.width() / 3) > 100) {
          $bar.text(100 + "%");
        } else {
          $bar.text(Math.round($bar.width() / 3) + "%");
        };
      };
      }, 600);
      offset: 5500
     }
   });
  console.log('resized');
});