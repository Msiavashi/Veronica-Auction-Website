// Opera 8.0+
var isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;

// Firefox 1.0+
var isFirefox = typeof InstallTrigger !== 'undefined';

// Safari 3.0+ "[object HTMLElementConstructor]"
// var isSafari = /constructor/i.test(window.HTMLElement) || (function (p) { return p.toString() === "[object SafariRemoteNotification]"; })(!window['safari'] || (typeof safari !== 'undefined' && safari.pushNotification));

// Internet Explorer 6-11
var isIE = /*@cc_on!@*/false || !!document.documentMode;

// Edge 20+
var isEdge = !isIE && !!window.StyleMedia;

// Chrome 1+
var isChrome = !!window.chrome && !!window.chrome.webstore;

// Blink engine detection
var isBlink = (isChrome || isOpera) && !!window.CSS;

function isSafari() {
	var isSafari = false;
	var ua = navigator.userAgent.toLowerCase();
	if (ua.indexOf('safari') != -1) {
	  if (ua.indexOf('chrome') > -1) {
	    isSafari = false;
	  } else {
	    isSafari = true;
	  }
	}
	return isSafari;
}

var images_path = '/static/images/products/';
var main_avatar_path = '/files/avatars/';
var avatar_path = '/static/images/avatars/';
var category_icon = '/static/images/icons/category/';
var ad_image_path = '/static/images/ads/';
var product_image_path = '/static/images/products/';

$('.close').on('click',function(event){
	event.preventDefault();
	$(this).parent().removeClass('show').addClass('hide')
});

function sleep(millisec) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > millisec){
      break;
    }
  }
}

function getFormData($form){
	var unindexed_array = $form.serializeArray();
	var indexed_array = {};
	$.map(unindexed_array, function(n, i){
		if(n['value']!=''){
			indexed_array[n['name']] = n['value'];
		}
	});
	return indexed_array;
}

function ClearifyNames(ugly_text) {
	if(ugly_text)
		return ugly_text.replace(/'/g, '').replace('[','').replace(']','').replace(' ','').split(',');
}

Date.prototype.format = function (format, utc){
    return formatDate(this, format, utc);
};

function formatDate(date, format, utc){
        var MMMM = ["\x00", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        var MMM = ["\x01", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        var dddd = ["\x02", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        var ddd = ["\x03", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        function ii(i, len) { var s = i + ""; len = len || 2; while (s.length < len) s = "0" + s; return s; }

        var y = utc ? date.getUTCFullYear() : date.getFullYear();
        format = format.replace(/(^|[^\\])yyyy+/g, "$1" + y);
        format = format.replace(/(^|[^\\])yy/g, "$1" + y.toString().substr(2, 2));
        format = format.replace(/(^|[^\\])y/g, "$1" + y);

        var M = (utc ? date.getUTCMonth() : date.getMonth()) + 1;
        format = format.replace(/(^|[^\\])MMMM+/g, "$1" + MMMM[0]);
        format = format.replace(/(^|[^\\])MMM/g, "$1" + MMM[0]);
        format = format.replace(/(^|[^\\])MM/g, "$1" + ii(M));
        format = format.replace(/(^|[^\\])M/g, "$1" + M);

        var d = utc ? date.getUTCDate() : date.getDate();
        format = format.replace(/(^|[^\\])dddd+/g, "$1" + dddd[0]);
        format = format.replace(/(^|[^\\])ddd/g, "$1" + ddd[0]);
        format = format.replace(/(^|[^\\])dd/g, "$1" + ii(d));
        format = format.replace(/(^|[^\\])d/g, "$1" + d);

        var H = utc ? date.getUTCHours() : date.getHours();
        format = format.replace(/(^|[^\\])HH+/g, "$1" + ii(H));
        format = format.replace(/(^|[^\\])H/g, "$1" + H);

        var h = H > 12 ? H - 12 : H == 0 ? 12 : H;
        format = format.replace(/(^|[^\\])hh+/g, "$1" + ii(h));
        format = format.replace(/(^|[^\\])h/g, "$1" + h);

        var m = utc ? date.getUTCMinutes() : date.getMinutes();
        format = format.replace(/(^|[^\\])mm+/g, "$1" + ii(m));
        format = format.replace(/(^|[^\\])m/g, "$1" + m);

        var s = utc ? date.getUTCSeconds() : date.getSeconds();
        format = format.replace(/(^|[^\\])ss+/g, "$1" + ii(s));
        format = format.replace(/(^|[^\\])s/g, "$1" + s);

        var f = utc ? date.getUTCMilliseconds() : date.getMilliseconds();
        format = format.replace(/(^|[^\\])fff+/g, "$1" + ii(f, 3));
        f = Math.round(f / 10);
        format = format.replace(/(^|[^\\])ff/g, "$1" + ii(f));
        f = Math.round(f / 10);
        format = format.replace(/(^|[^\\])f/g, "$1" + f);

        var T = H < 12 ? "AM" : "PM";
        format = format.replace(/(^|[^\\])TT+/g, "$1" + T);
        format = format.replace(/(^|[^\\])T/g, "$1" + T.charAt(0));

        var t = T.toLowerCase();
        format = format.replace(/(^|[^\\])tt+/g, "$1" + t);
        format = format.replace(/(^|[^\\])t/g, "$1" + t.charAt(0));

        var tz = -date.getTimezoneOffset();
        var K = utc || !tz ? "Z" : tz > 0 ? "+" : "-";
        if (!utc)
        {
            tz = Math.abs(tz);
            var tzHrs = Math.floor(tz / 60);
            var tzMin = tz % 60;
            K += ii(tzHrs) + ":" + ii(tzMin);
        }
        format = format.replace(/(^|[^\\])K/g, "$1" + K);

        var day = (utc ? date.getUTCDay() : date.getDay()) + 1;
        format = format.replace(new RegExp(dddd[0], "g"), dddd[day]);
        format = format.replace(new RegExp(ddd[0], "g"), ddd[day]);

        format = format.replace(new RegExp(MMMM[0], "g"), MMMM[M]);
        format = format.replace(new RegExp(MMM[0], "g"), MMM[M]);

        format = format.replace(/\\(.)/g, "$1");

        return format;
    };

function ToPersian( num, dontTrim ) {
	if(!num) return '۰';

	    var i = 0,

	        dontTrim = dontTrim || false,

	        num = dontTrim ? num.toString() : num.toString().trim(),
	        len = num.length,

	        res = '',
	        pos,

	        persianNumbers = typeof persianNumber == 'undefined' ?
	            ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'] :
	            persianNumbers;

	    for (; i < len; i++)
	        if (( pos = persianNumbers[num.charAt(i)] ))
	            res += pos;
	        else
	            res += num.charAt(i);

	    return res;
		}

function formatCurrency(num){
    num = num.toString().replace(/\$|\,/g, '');
    if (isNaN(num))
    {
        num = "0";
    }

    sign = (num == (num = Math.abs(num)));
    num = Math.floor(num * 100 + 0.50000000001);
    cents = num % 100;
    num = Math.floor(num / 100).toString();

    if (cents < 10)
    {
        cents = "0" + cents;
    }
    for (var i = 0; i < Math.floor((num.length - (1 + i)) / 3); i++)
    {
        num = num.substring(0, num.length - (4 * i + 3)) + ',' + num.substring(num.length - (4 * i + 3));
    }

    return (((sign) ? '' : '-') + num );
}

function triggerBigTimer() {
	if($('.deals-cowndown').length>0){
		 $(".deals-cowndown").TimeCircles({
			 fg_width: 0.01,
			 bg_width: 1.2,
			 text_size: 0.07,
			 circle_bg_color: "#ffffff",
			 time: {
				 Days: {
					 show: true,
					 text: "روز",
					 color: "#f9bc02"
				 },
				 Hours: {
					 show: true,
					 text: "ساعت",
					 color: "#f9bc02"
				 },
				 Minutes: {
					 show: true,
					 text: "دقیقه",
					 color: "#f9bc02"
				 },
				 Seconds: {
					 show: true,
					 text: "ثانیه",
					 color: "#f9bc02"
				 }
			 }
		 });
	 	}
}

function triggerFlashTimer() {
	if($('.flash-countdown').length>0){
		$(".flash-countdown").TimeCircles({
			fg_width: 0.01,
			bg_width: 1.2,
			text_size: 0.07,
			circle_bg_color: "#ffffff",
			time: {
				Days: {
					show: false,
					text: "",
					color: "#f9bc02"
				},
				Hours: {
					show: true,
					text: "",
					color: "#f9bc02"
				},
				Minutes: {
					show: true,
					text: "",
					color: "#f9bc02"
				},
				Seconds: {
					show: true,
					text: "",
					color: "#f9bc02"
				}
			}
		});
	}
}

function triggerSlider(element){
	var data = element.data();
	console.log(data);

	setTimeout(function() {

		element.owlCarousel({
			addClassActive:true,
			stopOnHover:true,
			itemsCustom:data.itemscustom,
			autoPlay:data.autoplay,
			transitionStyle:data.transition,
			beforeInit:background,
			afterAction:animated,
			navigationText:['<i class="fa fa-angle-left" aria-hidden="true"></i>','<i class="fa fa-angle-right" aria-hidden="true"></i>'],
		});
		element.find('.owl-controls').css('left',data.control+'px');

		//BxSlider
		if($('.bxslider-banner').length>0){
			$('.bxslider-banner').each(function(){
				$(this).find('.bxslider').bxSlider({
					controls:false,
					pagerCustom: $(this).find('.bx-pager')
				});
			});
		}

	}, 1000);
}

function triggerOwlcarousel() {
	console.log('here');
	if($('.wrap-item').length>0){
		$('.wrap-item').each(function(){
			var data = $(this).data();
			$(this).owlCarousel({
				addClassActive:true,
				stopOnHover:true,
				itemsCustom:data.itemscustom,
				autoPlay:data.autoplay,
				transitionStyle:data.transition,
				beforeInit:background,
				afterAction:animated,
				navigationText:['<i class="fa fa-angle-left" aria-hidden="true"></i>','<i class="fa fa-angle-right" aria-hidden="true"></i>'],
			});
			$(this).find('.owl-controls').css('left',data.control+'px');
		});
	}
}

function background(){
	$('.bg-slider .item-banner').each(function(){
		var src=$(this).find('.banner-thumb a img').attr('src');
		$(this).css('background-image','url("'+src+'")');
	});
}

function animated(){
	$('.banner-slider .owl-item').each(function(){
		var check = $(this).hasClass('active');
		if(check==true){
			$(this).find('.animated').each(function(){
				var anime = $(this).attr('data-animated');
				$(this).addClass(anime);
			});
		}else{
			$(this).find('.animated').each(function(){
				var anime = $(this).attr('data-animated');
				$(this).removeClass(anime);
			});
		}
	});
}

function triggerAvatars() {
	$('.avatarUser img').click( function(){
	    if ( $(this).hasClass('current') ) {
	    } else {
	        $('img.current').removeClass('current');
	        $(this).addClass('current');
	    }
	});
}

function triggerPaymentTable() {
	$(".fold-table tr.view").on("click", function(){
		if($(this).hasClass("open")) {
		$(this).removeClass("open").next(".fold").removeClass("open");
		} else {
		$(".fold-table tr.view").removeClass("open").next(".fold").removeClass("open");
		$(this).addClass("open").next(".fold").addClass("open");
		}
	});
}

function triggerUpDown() {
	$('.qty-product').each(function(){
	var qtyval = parseInt($(this).find('.qty-num').text(),10);
	$('.qty-up').on('click',function(event){
		event.preventDefault();
		qtyval=qtyval+1;
		$(this).prev().text(qtyval);
	});
	$('.qty-down').on('click',function(event){
		event.preventDefault();
		qtyval=qtyval-1;
		if(qtyval>1){
			$(this).next().text(qtyval);
		}else{
			qtyval=1;
			$(this).next().text(qtyval);
		}
		});
	});
 }

function triggerUpDownCart() {
	$('.detail-qty').each(function(){
		var qtyval = parseInt($(this).find('.qty-val').text(),10);
		$('.qty-up').on('click',function(event){
			event.preventDefault();
			qtyval=qtyval+1;
			$(this).prev().text(qtyval);
		});
		$('.qty-down').on('click',function(event){
			event.preventDefault();
			qtyval=qtyval-1;
			if(qtyval>1){
				$(this).next().text(qtyval);
			}else{
				qtyval=1;
				$(this).next().text(qtyval);
			}
		});
	});
}


function startLoading(e){

    $('<div class="page-loading" id="page-loading"> \
        <div class="bx-loading"> \
                <div class="spinner"><div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div></div> \
                <h3>لطفا صبر کنید ...</h3> \
            </div> \
        </div>').prependTo( $(e) );
}
function endLoading(){
    $("#page-loading").fadeOut('slow', function(){
        $(this).remove();
    });
}


function start_loading(element){
	element.style.display = "block";
}

function stop_loading(element){ //spinner handler
		element.style.display = "none";
}

loading_element = document.getElementById('myModal');
