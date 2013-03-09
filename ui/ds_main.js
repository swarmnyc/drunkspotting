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
			
			
			//$('#posts').append(itemHtml);
			
			// wat
			if(i % 3 == 0){
				// row row row new line
				ds.postsHtml.append('<tr id="row-' + i + '" class="row-fluid">' + itemHtml + '</tr>');
			}else{
				var rowId = i - (i % 3);
				$('#row-' + rowId).append(itemHtml);
			}
			
		}
	});
	
	setTimeout(drunkspotting.load_images, 5000);
	
}

