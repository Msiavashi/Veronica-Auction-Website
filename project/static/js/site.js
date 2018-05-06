$('.close').on('click',function(){
	$(this).parent().removeClass('show').addClass('hide')
});

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

// $.getJSON( "{{url_for('categories')}}", function( data ) {
// 	$.each( data[0], function( key, val ) {
// 		console.log(val.name);
// 		item = '<li><a href="#"><img alt="" src="{{url_for("static",filename="'+val.icon+'")}}"><span>'+val.name+'</span></a></li>';
// 		$('.list-cat-icon').append(item);
// 		$('.list-category-toggle').append(item);
// 	});
// });
