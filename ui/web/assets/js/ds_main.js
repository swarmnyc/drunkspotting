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

      // Init canvas
      var newUrl = data.url.replace('http://drunkspotting.blob.core.windows.net/', 'http://drunkspotting.com/');
      drunkspotting.init_drawing(newUrl);

      $('#upload-panel').hide();
      $('#edit-panel').show();
    },
    error : function (){}
  });
  
  // On upload image, hide most shit on the page until they save the drawing
  $('.page-heading img').hide();
  $('.page-heading').css({
    height : '60px',
    padding : '15px'
  });
  $('.marketing-desc').hide();
  $('.upload-btn-container').hide();
  $('#lushes-box').hide();
  $('#footer-marketing').hide();
};

drunkspotting.init_drawing = function(image_url){
  $('#buton_save').click(function (e) {
    drunkspotting.save_drawing();

    return false;
  });

  // set up the drawing canvas
  window.image = $('<img />').attr('src', image_url);

  $('#tools_sketch').css('background-image', 'url(' + image_url + ')');

  $.each(['#f00', '#ff0', '#0f0', '#0ff', '#00f', '#f0f', '#000', '#fff'], function() {
      $('#edit-panel .tools').append("<a href='#tools_sketch' data-color='" + this + "' style='width: 10px; background: " + this + ";'>" + this + "</a>");
    });
    $.each([3, 5, 10, 15], function() {
      $('#edit-panel .tools').append("<a href='#tools_sketch' data-size='" + this + "' style='background: #ccc'>" + this + "</a> ");
    });

  $('#tools_sketch')[0].height = window.image[0].height;
  $('#tools_sketch')[0].width = window.image[0].width;

  $('#tools_sketch').sketch();
};

drunkspotting.save_drawing = function(){
  // save
  var imageData = $('#tools_sketch')[0].toDataURL();

  $.ajax({
    url : '/upload',
    type : "POST",
    data : {canvas: imageData, imageUrl: window.image[0].src},
    processData : true,
    contentType : true,
    success : function(data) {
      console.log(data);
      window.response_data = data;
    },
    error : function (){}
  });
};

