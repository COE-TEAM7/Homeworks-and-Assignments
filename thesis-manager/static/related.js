$(function(){
	//~ function loadThesisEntries(event){
		//~ var data = $(event.target).serializeArray();
		//~ var thesis_search_api = '/api/thesis/related/';
		//~ var thesis_id = $("p.temp").text()
		//~ thesis_search_api = thesis_search_api + thesis_id;
		//~ $.get(thesis_search_api, {}, function(response) {
				//~ response.data.forEach(function(t) {
					//~ var entry_name = ('<li class=list>' + t.year + ' ' + t.title + '. Created by:' + t.created_by + 
					//~ ' &nbsp <a href=/thesis/details/' + t.id + '><input class=newbtn type=button value=Detail></input></a> '+
					//~ ' &nbsp <a href=/thesis/edit/' + t.id + '><input class=newbtn type=button value=Edit></input></a></li>');
					//~ $(".stls").prepend(entry_name);
				//~ });
			//~ });
		//~ }
		//~ 
	//~ $(document).ready(loadThesisEntries);
	
	function loadThesisEntries(event){
			var thesis_search_api = '/api/thesis/related/';
			var thesis = $(document).val({{thesis_id}});
			thesis_search_api = thesis_search_api + thesis;
			alert(thesis)
			$.get(thesis_search_api, {}, function(response) {
					response.data.forEach(function(t) {
						var entry_name = ('<li class=list>' + t.year + ' ' + t.title + '. Created by:' + t.created_by + 
						' &nbsp <a href=/thesis/details/' + t.id + '><input class=newbtn type=button value=Detail></input></a> '+
						' &nbsp <a href=/thesis/edit/' + t.id + '><input class=newbtn type=button value=Edit></input></a></li>');
						$(".stls").prepend(entry_name);
					});
				});
			}
			
		$(document).ready(loadThesisEntries);
});
