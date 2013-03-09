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
	
	setTimeout(drunkspotting.load_images, 5000);
	
};

drunkspotting.upload_ajax = function(){
	var data = new FormData();
	
	data.append('file', $('#data')[0].files[0]);
	$.ajax({
		url : 'http://api.drunkspotting.com/upload_template',
		type : "POST",
		data : data,
		processData : false,
		contentType : false,
		success : function(data){
			$('#tools_sketch').attr('style', "background: url("+data.url+");");
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


