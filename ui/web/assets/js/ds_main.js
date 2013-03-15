$(document).ready(function(){
	jQuery.support.cors = true;
	$('#upload').bind('click', function(e){
		e.preventDefault();
		$('#data').click();
	});
	$('#data').bind('change', function(){
		if($('#data').val() != ''){
			if(typeof $('#data')[0].files[0] == 'object' && $('#data')[0].files[0].size <= 2097152){
				drunkspotting.upload_ajax();
			}
			else {
				drunkspotting.error_show('Your file is too large! Trying something smaller. (that\'s what she said)');
			}
		}
	});
	drunkspotting.load_images();
	
	
	// Fixes for IE Ajax loading
	if ($.browser.msie && $.browser.version == '7.0') {
	    $.ajaxSetup({ xhr: function() {
	        return XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("MSXML2.XMLHTTP");
	    }
	    });
	}
	$.ajaxTransport("+*", function(options, originalOptions, jqXHR) {
        if ($.browser.msie && window.XDomainRequest) {
            var xdr;
            return {
                send: function(headers, completeCallback) {
                    // Use Microsoft XDR
                    xdr = new XDomainRequest();
                    xdr.open("get", options.url);
                    xdr.onload = function() {
                        if (this.contentType.match(/\/xml/)) {
                            var dom = new ActiveXObject("Microsoft.XMLDOM");
                            dom.async = false;
                            dom.loadXML(this.responseText);
                            completeCallback(200, "success", [dom]);
                        } else {
                        	completeCallback(200, "success", [this.responseText]);
                        }
                    };
                    xdr.ontimeout = function() {completeCallback(408, "error", ["The request timed out."]);};
                    xdr.onerror = function() {completeCallback(404, "error", ["The requested resource could not be found."]);};
                    xdr.onprogress = function(){};
                    xdr.send();
                },
                abort: function() {if (xdr) xdr.abort();}
            };
        }
    });
});

var drunkspotting = {img:new Image()};

drunkspotting.load_images = function(){
	var ds = {};
	
	
	$.ajax({
		url:'/api/pictures/latest/12',
		type: "GET",
		dataType: 'JSON',
		success: function(data){
			console.log('success');
			ds.template = $('#template-listing').html();
			ds.postsHtml = $('#posts');
			ds.postsLoadingHtml = $('#posts_loading');
			
			// Clear list on refresh
			$('#posts').html('');
			
			var temp, itemHtml;
			window.data = data;
			
			// For each ds image, append html
			for(var i = 0; i < data.length; i++){
				temp = ds.template;
				
				//itemHtml = temp.replace('{{title}}', data[i].description);
				itemHtml = temp.replace('{{src_link}}', data[i].url);
				itemHtml = itemHtml.replace('{{src}}', data[i].url);
				
				$('#posts').append(itemHtml);
			}
			$('#posts').append("<div style='clear:both'></div>");
		},
		error: function(obj,stat,err){
			console.log(stat, err);
		}
	});
	
	// window.ds_reloader = setTimeout(drunkspotting.load_images, 5000);
};

drunkspotting.upload_ajax = function(){
	drunkspotting.loading_start();
	// Kill image reloading timeout
	clearTimeout(window.ds_reloader);
	
	var data = new FormData();
	
	data.append('file', $('#data')[0].files[0]);
	
	$.ajax({
	url : '/api/upload_template',
	type : "POST",
	data : data,
	dataType: 'JSON',
	processData : false,
	contentType : false,
	success : function(data){
		// Init canvas
		var newUrl = data.url.replace('http://drunkspotting.blob.core.windows.net/', 'http://drunkspotting.com/');
		drunkspotting.init_drawing(newUrl);
		$(document.body).addClass('edit');
	},
	error : function (){}
	});
};

$(window).resize(function(){
	//Resize canvas when window is resized
	drunkspotting.fix_canvas();
});

drunkspotting.fix_canvas = function(){
	//Resize canvas
	
	//Get widths and heights for processing
	var canvasWidth, canvasHeight;
	$('#sketch').css('width', '100%');
	var maxWidth = $('#sketch').width()-22;
	$('#sketch').css('width', 'auto');
	var maxHeight = $(document.body).height() - $('#tools').outerHeight()-12;
	var imgWidth = parseInt($('#sketch').attr('img_width'));
	var imgHeight = parseInt($('#sketch').attr('img_height'));
	
	//Use width as base
	if(imgWidth/imgHeight >= maxWidth/maxHeight){
		if((maxWidth/imgWidth) * imgHeight >= maxHeight){
			canvasHeight = maxHeight;
			canvasWidth = (maxHeight/imgHeight) * imgHeight
		}
		else {
			canvasHeight = (maxWidth/imgWidth) * imgHeight;
			canvasWidth = maxWidth;
		}
	}
	//Use height as base
	else {
		if((maxHeight/imgHeight) * imgWidth >= maxWidth){
			canvasWidth = maxWidth;
			canvasHeight = (maxWidth/imgWidth) * imgWidth;
		}
		else {
			canvasWidth = (maxHeight/imgHeight) * imgWidth;
			canvasHeight = maxHeight;
		}
	}
	
	//Set canvas size
	$('#sketch')[0].width = Math.floor(canvasWidth);
	$('#sketch')[0].height = Math.floor(canvasHeight);
	drunkspotting.loading_stop();
}

drunkspotting.init_drawing = function(image_url){

	// Set up buttons
	$('#button_save').unbind('click').bind('click', function(e){
		e.preventDefault();
		drunkspotting.save_drawing();
	});
	$('#button_cancel').unbind('click').bind('click', function(e){
		e.preventDefault();
		drunkspotting.cancel_drawing();
	});
	
	// Reset canvas background
	$('#sketch').css('background-image', 'none');
	
	// set up the drawing canvas
	drunkspotting.img = new Image();
	$(drunkspotting.img).on('load', function () {
		$('#sketch').attr('img_width', this.width);
		$('#sketch').attr('img_height', this.height);
		$('#sketch').css('background-image', 'url(' + this.src + ')');
		drunkspotting.fix_canvas();
	});
	drunkspotting.img.src = image_url;
	$('#sketch').sketch();
	$('#sketch').sketch().actions = new Array();
	$('#sketch').sketch().redraw();
	
	
	// Set up color selector
	var colorpopup = $('<div id="color_popup"/>');
	colorpopup.appendTo('#tools').hide();
	$.each(['#ff0000', '#ff8000', '#ffff00', '#80ff00', '#00ff00', '#00ff80', '#00ffff', '#0080ff', '#0000ff', '#8000ff', '#ff00ff', '#ff0080', '#000000', '#808080', '#ffffff'], function() {
		var link = $('<a href="#sketch" data-color="' + this + '"><span style="background: ' + this + ';"></span></a>');
		link.unbind('click').bind('click', function(){
			$('#my_color span').css('background-color',$(this).find('span').css('background-color'));
			$('#color_popup').fadeOut(250);
		});
		colorpopup.append(link);
	});
	$('#my_color').unbind('click').bind('click', function(){
		$('#size_popup').fadeOut(250);
		$('#color_popup').fadeIn(500);
	});
	$('#my_color span').css('background-color','#000000');
	
	//Set up size selector
	var sizepopup = $('<div id="size_popup"/>');
	sizepopup.appendTo('#tools').hide();
	$.each([2, 6, 10, 16, 20], function() {
		var link = $('<a href="#sketch" data-size="' + this + '" class="size_'+this+'"><span></span></a>');
		link.unbind('click').bind('click', function(){
			$('#my_size').attr('data-size', $(this).attr('data-size'));
			$('#size_popup').fadeOut(250);
		});
		sizepopup.append(link);
	});
    $('#my_size').unbind('click').bind('click', function(){
		$('#color_popup').fadeOut(250);
		$('#size_popup').fadeIn(500);
	});
	$('#my_size span').attr('data-size', '6');
};

drunkspotting.error_show = function(msg){
	drunkspotting.loading_stop();
	var cover = $('<div id="cover"/>');
	cover.appendTo(document.body);
	cover.fadeIn(250);
	var error = $('<div class="error">'+msg+'</div>');
	cover.append(error);
	error.css({
		'margin-top':(error.outerHeight()/2)*-1,
		'margin-left':(error.outerWidth()/2)*-1
	});
	cover.on('click', function(){
		drunkspotting.error_hide();
	});
}
drunkspotting.error_hide = function(){
	$('#canvas').fadeOut(250, function(){
		$('#canvas').remove();
	})
}

drunkspotting.loading_start = function () {
	drunkspotting.error_hide();
	var loading = $('<div id="loading"><img src="/assets/img/loading.gif"/></div>');
	loading.appendTo(document.body);
	loading.fadeIn(250);
};

drunkspotting.loading_stop = function () {
	$('#loading').fadeOut(250, function(){
		$('#loading').remove();
	})
};

drunkspotting.cancel_drawing = function(){
	$(document.body).removeClass('edit');
}

drunkspotting.save_drawing = function(){
	// save
	drunkspotting.loading_start();
	var imageData = $('#sketch')[0].toDataURL();
	
	$.ajax({
	url : '/upload',
	type : "POST",
	data : drunkspotting.img.src + ':endurl:' + imageData,
	processData : false,
	contentType : false,
	beforeSend : function () {
	  $('#button_save').attr('disabled','disabled');
	},
	success : function(data) {
		if (data.id) {
			$(document.body).removeClass('edit');
			drunkspotting.load_images();
			drunkspotting.loading_stop();
		}
	},
	error : function (){}
	});
};

