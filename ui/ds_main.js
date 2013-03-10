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
			
			// add row separator
			if(i % 3 == 0){
				// row row row new line
				//ds.postsHtml.append('<div id="row-' + i + '" class="row-fluid">' + itemHtml + '</div>');
			}else{
				//var rowId = i - (i % 3);
				//$('#row-' + rowId).append(itemHtml);
			}
			
			
		}
		$('#posts').append("<div style='clear:both'></div>");
	});
	
	window.ds_reloader = setTimeout(drunkspotting.load_images, 5000);
	
};

drunkspotting.upload_ajax = function(){
	
	// Kill image reloading timeout
	clearTimeout(window.ds_reloader);
	
	var data = new FormData();
	
	data.append('file', $('#data')[0].files[0]);
	
	$.ajax({
		url : 'http://api.drunkspotting.com/upload_template',
		type : "POST",
		data : data,
		processData : false,
		contentType : false,
		success : function(data){
			
			// Temp
			//data.url = '/library/foo.jpg';
			
			// Init canvas
			drunkspotting.init_drawing(data.url);
			
			$('#upload-panel').hide();
			$('#edit-panel').show();
		},
		error : function (){}
	});
	
	// On upload image, hide most shit on the page until they save the drawing
	$('.page-heading img').hide();
	$('.page-heading').css({
		height : '60px',
		padding : '15px',
	});
	$('.marketing-desc').hide();
	$('.upload-btn-container').hide();
	$('#lushes-box').hide();
	$('#footer-marketing').hide();
	
};

drunkspotting.init_drawing = function(image_url){
	// set up the drawing canvas
	
	// init canvas sketch
	$('#tools_sketch').sketch();
	
	// Insert hidden image
	$('#img-loader').append( $('<img>').attr('src', image_url) );
	
	// insert background
	var context = $('#tools_sketch')[0].getContext('2d');
	var bg_context = $('#background_canvas')[0].getContext('2d');
	
	setTimeout(function(){
		var loaded_image = $('#img-loader img')[0];
		bg_context.drawImage(loaded_image, 0, 0);
	}, 250);
	
	$('#img-loader').hide();
	
};

drunkspotting.save_drawing = function(){
	// save
	
	var export_canvas_ctx = $('#export_canvas')[0].getContext('2d');
	var drawing_canvas_ctx = $('#tools_sketch')[0].getContext('2d');
	var bg_canvas_ctx = $('#background_canvas')[0].getContext('2d');
	
	// bg_canvas to export_canvas
	export_canvas_ctx.drawImage(bg_canvas_ctx.canvas, 0, 0);
	
	// drawing_canvas to export_canvas
	export_canvas_ctx.drawImage(drawing_canvas_ctx.canvas, 0, 0);
	
	// export export_canvas
	
	var img_data = $('#export_canvas')[0].toDataURL();
	
	window.export_img_data = img_data;
	
	var data = new FormData();
	
	data.append('file', img_data);
	
	$.ajax({
		url : 'http://api.drunkspotting.com/upload_picture',
		type : "POST",
		data : data,
		processData : false,
		contentType : false,
		success : function(data){
			console.log(data)
			window.response_data = data;
			
		},
		error : function (){}
	});
};

