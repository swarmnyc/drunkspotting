var drunkspotting = {};

drunkspotting.load_images = function(){
  var ds = {};

  $.get('http://api.drunkspotting.com/pictures/latest/12', function(data){

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
    url : 'http://api.drunkspotting.com/upload_template',
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
      
      drunkspotting.loading_stop();
    },
    error : function (){}
  });
};

$(window).resize(function(){
	drunkspotting.fix_canvas();
});

drunkspotting.fix_canvas = function(){
	var canvasWidth, canvasHeight;
	$('#sketch').css('width', '100%');
	var maxWidth = $('#sketch').width()-22;
	$('#sketch').css('width', 'auto');
	var maxHeight = $(document.body).height() - $('#tools').outerHeight()-12;
	var imgWidth = parseInt($('#sketch').attr('img_width'));
	var imgHeight = parseInt($('#sketch').attr('img_height'));
	if(imgWidth/imgHeight >= maxWidth/maxHeight){
		//use width as base
		if((maxWidth/imgWidth) * imgHeight >= maxHeight){
			canvasHeight = maxHeight;
			canvasWidth = (maxHeight/imgHeight) * imgHeight
		}
		else {
			canvasHeight = (maxWidth/imgWidth) * imgHeight;
			canvasWidth = maxWidth;
		}
	}
	else {
		//use height as base
		if((maxHeight/imgHeight) * imgWidth >= maxWidth){
			canvasWidth = maxWidth;
			canvasHeight = (maxWidth/imgWidth) * imgWidth;
		}
		else {
			canvasWidth = (maxHeight/imgHeight) * imgWidth;
			canvasHeight = maxHeight;
		}
	}
	
	$('#sketch')[0].width = Math.floor(canvasWidth);
	$('#sketch')[0].height = Math.floor(canvasHeight);
	
	$('#sketch').sketch();
}

drunkspotting.init_drawing = function(image_url){

  // set up the drawing canvas
  window.image = $('<img />');
  window.image.on('load', function () {
    $('#sketch').attr('img_width', window.image[0].width);
    $('#sketch').attr('img_height', window.image[0].height);
    $('#sketch').css('background-image', 'url(' + window.image[0].src + ')');
    drunkspotting.fix_canvas();
  });
  window.image.attr('src', image_url);
  
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

drunkspotting.loading_start = function () {
  var loading = $('<div id="loading"><img src="/assets/img/loading.gif"/></div>');
  loading.appendTo(document.body);
  loading.fadeIn(250);
};

drunkspotting.loading_stop = function () {
  $('#loading').fadeOut(500, function(){
	  $('#loading').remove();
  })
};

drunkspotting.save_drawing = function(){
  // save
  drunkspotting.loading_start();
  var imageData = $('#sketch')[0].toDataURL();

  $.ajax({
    url : '/upload',
    type : "POST",
    data : window.image[0].src + ':endurl:' + imageData,
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

