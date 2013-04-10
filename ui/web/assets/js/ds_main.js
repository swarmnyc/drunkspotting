var drunkspotting = {img:new Image()};
var disqus_shortname = 'drunkspotting';
var disqus_identifier;
var disqus_url;

jQuery(document).ready(function(){
	jQuery.support.cors = true;
	jQuery('#upload').bind('click', function(e){
		e.preventDefault();
		jQuery('#data').click();
	});
	jQuery('#data').bind('change', function(){
		if(jQuery('#data').val() !== ''){
			if(typeof jQuery('#data')[0].files[0] == 'object' && jQuery('#data')[0].files[0].size <= 2097152){
				drunkspotting.upload_ajax();
			}
			else {
				drunkspotting.error_show('Your file is too large! Trying something smaller. (that\'s what she said)');
			}
		}
	});
	drunkspotting.load_images();
	
	// Fixes for IE Ajax loading
	if (jQuery.browser.msie && jQuery.browser.version == '7.0') {
	    jQuery.ajaxSetup({ xhr: function() {
	        return XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("MSXML2.XMLHTTP");
	    }
	    });
	}
	jQuery.ajaxTransport("+*", function(options, originalOptions, jqXHR) {
        if (jQuery.browser.msie && window.XDomainRequest) {
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
    if(jQuery('#post').length > 0){
    	var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
		dsq.src = 'http://' + disqus_shortname + '.disqus.com/count.js';
		jQuery('head').append(dsq);
		drunkspotting.load_comments(jQuery('#post .item'), jQuery('#post .item').attr('id'), jQuery('#spot_url').attr('href'));
    }
});

drunkspotting.load_comments = function(el, id, url){	
	jQuery('.comments').hide();
	el.find('.comments').show();
	el.find('.comments').empty();
	if (window.DISQUS) {
		jQuery('#disqus_thread').appendTo(el.find('.comments'));
		DISQUS.reset({
			reload: true,
			config: function () {
				this.page.identifier = id;
				this.page.url = url;
			}
		});
		
	} else {
		jQuery('<div id="disqus_thread"></div>').appendTo(el.find('.comments'));
		disqus_identifier = id; //set the identifier argument
		disqus_url = url; //set the permalink argument
		
		//append the Disqus embed script to HTML
		var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
		dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
		jQuery('head').append(dsq);		
	}
};

drunkspotting.load_images = function(){
	var ds = {};
	
	jQuery.ajax({
		url:'http://drunkspotting.com/api/pictures/latest/12',
		type: "GET",
		dataType: 'JSON',
		success: function(data){
			jQuery('#posts').empty();
			// For each ds image, append html
			
			for(var i = 0; i < data.length; i++){
				var comment_count = 0;
				var template = jQuery('#template-listing').html();
				var regex = new RegExp('{id}', 'g');
				template = template.replace(regex, data[i].id);
				regex = new RegExp('{src}', 'g');
				template = template.replace(regex, data[i].url);
				regex = new RegExp('{comment_count}', 'g');
				template = template.replace(regex, comment_count);
				template = jQuery(template);
				var comment_link = template.find('.comment_count');
				comment_link.attr('href', comment_link.attr('href')+'#disqus_thread');
				
				comment_link.on('click', function(e){
			    	e.preventDefault();
			    	drunkspotting.load_comments(jQuery(this).parents('.item'), jQuery(this).parents('.item').attr('id'), jQuery(this).attr('href'));
			    });
			    template.find('.comments').hide();
				jQuery('#posts').append(template);
				
				template.find('img').last().load(function(){
					drunkspotting.resizeImg(jQuery(this));
				});
			}
			var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
			dsq.src = 'http://' + disqus_shortname + '.disqus.com/count.js';
			jQuery('head').append(dsq);
			jQuery('#posts').append('<div style="clear:both"></div>');
			jQuery('#posts img').last().load(function(){
				jQuery(window).trigger('resize');
			});
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
	
	data.append('file', jQuery('#data')[0].files[0]);
	
	jQuery.ajax({
	url : '/upload/template',
	type : "POST",
	data : data,
	dataType: 'JSON',
	processData : false,
	contentType : false,
	success : function(data){
		// Init canvas
		var newUrl = data.url.replace('http://drunkspotting.blob.core.windows.net/', 'http://drunkspotting.com/');
		drunkspotting.init_drawing(newUrl);
	},
	error : function (){}
	});
};

drunkspotting.resizeImg = function(obj){
	/*if(obj.width() > obj.height()){
		obj.css({
			'width':'auto',
			'height':'100%',
			'position':'absolute',
			'top':'0'
		});
		obj.css({'left':(obj.width()-obj.height())/-2});
	}*/
};

jQuery(window).resize(function(){
	//Resize canvas when window is resized
	drunkspotting.fix_canvas();
});

drunkspotting.fix_canvas = function(){
	//Resize canvas
	
	//Get widths and heights for processing
	var canvasWidth, canvasHeight;
	jQuery('#sketch').css('width', '100%');
	var maxWidth = jQuery('#sketch').width()-22;
	jQuery('#sketch').css('width', 'auto');
	var maxHeight = jQuery(document.body).height() - jQuery('#tools').outerHeight()-12;
	var imgWidth = parseInt(jQuery('#sketch').attr('img_width'));
	var imgHeight = parseInt(jQuery('#sketch').attr('img_height'));
	
	//Use width as base
	if(imgWidth/imgHeight >= maxWidth/maxHeight){
		if((maxWidth/imgWidth) * imgHeight >= maxHeight){
			canvasHeight = maxHeight;
			canvasWidth = (maxHeight/imgHeight) * imgHeight;
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
	jQuery('#sketch')[0].width = Math.floor(canvasWidth);
	jQuery('#sketch')[0].height = Math.floor(canvasHeight);
	drunkspotting.loading_stop();
};

drunkspotting.init_drawing = function(image_url){
	jQuery(document.body).addClass('edit');
	// Set up buttons
	jQuery('#button_save').unbind('click').bind('click', function(e){
		e.preventDefault();
		drunkspotting.save_drawing();
	});
	jQuery('#button_cancel').unbind('click').bind('click', function(e){
		e.preventDefault();
		drunkspotting.cancel_drawing();
	});
	
	// Reset canvas background
	jQuery('#sketch').css('background-image', 'none');
	
	// set up the drawing canvas
	drunkspotting.img = new Image();
	jQuery(drunkspotting.img).on('load', function () {
		jQuery('#sketch').attr('img_width', this.width);
		jQuery('#sketch').attr('img_height', this.height);
		jQuery('#sketch').css('background-image', 'url(' + this.src + ')');
		drunkspotting.fix_canvas();
	});
	drunkspotting.img.src = image_url;
	jQuery('#sketch').sketch();
	jQuery('#sketch').sketch().actions = new Array();
	jQuery('#sketch').sketch().redraw();
	
	
	// Set up color selector
	var colorpopup = jQuery('<div id="color_popup"/>');
	colorpopup.appendTo('#tools').hide();
	jQuery.each(['#ff0000', '#ff8000', '#ffff00', '#80ff00', '#00ff00', '#00ff80', '#00ffff', '#0080ff', '#0000ff', '#8000ff', '#ff00ff', '#ff0080', '#000000', '#808080', '#ffffff'], function() {
		var link = jQuery('<a href="#sketch" data-color="' + this + '"><span style="background: ' + this + ';"></span></a>');
		link.unbind('click').bind('click', function(){
			jQuery('#my_color span').css('background-color',jQuery(this).find('span').css('background-color'));
			jQuery('#color_popup').fadeOut(250);
		});
		colorpopup.append(link);
	});
	jQuery('#my_color').unbind('click').bind('click', function(){
		jQuery('#size_popup').fadeOut(250);
		jQuery('#color_popup').fadeIn(500);
	});
	jQuery('#my_color span').css('background-color','#000000');
	
	//Set up size selector
	var sizepopup = jQuery('<div id="size_popup"/>');
	sizepopup.appendTo('#tools').hide();
	jQuery.each([2, 6, 10, 16, 20], function() {
		var link = jQuery('<a href="#sketch" data-size="' + this + '" class="size_'+this+'"><span></span></a>');
		link.unbind('click').bind('click', function(){
			jQuery('#my_size').attr('data-size', jQuery(this).attr('data-size'));
			jQuery('#size_popup').fadeOut(250);
		});
		sizepopup.append(link);
	});
    jQuery('#my_size').unbind('click').bind('click', function(){
		jQuery('#color_popup').fadeOut(250);
		jQuery('#size_popup').fadeIn(500);
	});
	jQuery('#my_size span').attr('data-size', '6');
};

drunkspotting.error_show = function(msg){
	drunkspotting.loading_stop();
	var cover = jQuery('<div id="cover"/>');
	cover.appendTo(document.body);
	cover.fadeIn(250);
	var error = jQuery('<div class="error">'+msg+'</div>');
	cover.append(error);
	error.css({
		'margin-top':(error.outerHeight()/2)*-1,
		'margin-left':(error.outerWidth()/2)*-1
	});
	cover.on('click', function(){
		drunkspotting.error_hide();
	});
};

drunkspotting.error_hide = function(){
	jQuery('#cover').fadeOut(250, function(){
		jQuery('#cover').remove();
	});
};

drunkspotting.loading_start = function () {
	drunkspotting.error_hide();
	var loading = jQuery('<div id="loading"><img src="/assets/img/loading.gif"/></div>');
	loading.appendTo(document.body);
	loading.fadeIn(250);
};

drunkspotting.loading_stop = function () {
	jQuery('#loading').fadeOut(250, function(){
		jQuery('#loading').remove();
	});
};

drunkspotting.cancel_drawing = function(){
	jQuery(document.body).removeClass('edit');
};

drunkspotting.save_drawing = function(){
	// save
	drunkspotting.loading_start();
	var imageData = jQuery('#sketch')[0].toDataURL();
	
	jQuery.ajax({
	url : '/upload/picture',
	type : "POST",
	data : drunkspotting.img.src + ':endurl:' + imageData,
	processData : false,
	contentType : false,
	beforeSend : function () {
	  jQuery('#button_save').attr('disabled','disabled');
	},
	success : function(data) {
		if (data.id) {
			jQuery(document.body).removeClass('edit');
			drunkspotting.load_images();
			drunkspotting.loading_stop();
		}
	},
	error : function (){}
	});
};

