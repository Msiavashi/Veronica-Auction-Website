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
