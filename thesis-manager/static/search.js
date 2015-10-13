$(function(){
	
	function onSearchSubmit(event){
		$("li.search-list").remove();
		var data = $(event.target).serializeArray();
		var thesis_search_api = '/api/thesis/search/';
		thesis_search_api = thesis_search_api + data[0].value;
		$("input[type=text]").val("")
		loadThesisEntries(thesis_search_api);
		
		return false;
	}
	
	$(".mysearch").submit(onSearchSubmit)
	
	function loadThesisEntries(thesis_search_api){
	$.get(thesis_search_api, {}, function(response) {
			response.data.forEach(function(t) {
				var entry_name = ('<li class=search-list> &nbsp <a href=/thesis/details/' + t.id + '>'+ t.year + ' ' + t.title + '</a> '+
				' &nbsp <p><a href=/thesis/edit/' + t.id + '>Edit</a> &nbsp <a href=/thesis/delete/' + t.id + '>Delete</a> &nbsp Created by:' + t.created_by + '</p></li>');
				$(".stls").prepend(entry_name);
			});
		});
	}
	
	//loadThesisEntries();
});
