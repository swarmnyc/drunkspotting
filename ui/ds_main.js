var drunkspotting = {};

drunkspotting.load_images = function(){
	
	var ds = {};
	
	$.get('http://api.drunkspotting.com/pictures/latest/12', function(data){
	
		ds.template = $('#template-listing').html();
		ds.postsHtml = $('#posts');
		
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
			
			// wat
			if(i % 3 == 0){
				ds.postsHtml.append('<div id="row-' + i + '" class="row-fluid">' + itemHtml + '</div>');
			}else{
				var rowId = i - (i % 3);
				$('#row-' + rowId).append(itemHtml);
			}
			
		}
	});
	
	setTimeout(drunkspotting.load_images, 5000);
	
}

