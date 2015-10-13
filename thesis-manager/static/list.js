$(function(){	
	function loadThesisEntries(event){
		var category = $("#category").text().split(" ")[1];
		var list_by = $("#list_by").text();
		list_item = '';
		for (var i = 0; i < list_by.length; i++)
			list_item += list_by[i].replace(" ","_");
		var thesis_detail_api = '/api/thesis/list/'+ category +'/'+ list_item;
		$.get(thesis_detail_api, {}, function(response) {
			response.data.forEach(function(t) {
				var entry_name = ('<li class=list> &nbsp <a href=/thesis/details/' + t.id + '>'+ t.year + ' ' + t.title + '</a> '+
				' &nbsp <p><a href=/thesis/edit/' + t.id + '>Edit</a> &nbsp <a href=/thesis/delete/' + t.id + '>Delete</a> &nbsp Created by:' + t.created_by + '</p></li>');
				$(".stls").prepend(entry_name);
			});
		});
		
		/**PAGINATION DAPAT**/
		//~ var numItems = items.length;
		//~ alert(numItems)
		//~ var perPage = 10;
		//~ items.slice(perPage).hide();
		//~ 
		//~ 
		//~ $(".stls").pagination({
			//~ items: numItems,
			//~ itemsOnPage: perPage,
			//~ cssStyle: 'light-theme',
			//~ onPageClick: function(pageNumber) { // this is where the magic happens
				//~ // someone changed page, lets hide/show trs appropriately
				//~ var showFrom = perPage * (pageNumber - 1);
				//~ var showTo = showFrom + perPage;
//~ 
				//~ items.hide() // first hide everything, then show for the new page
					 //~ .slice(showFrom, showTo).show();
			//~ }
		//~ });
	}
	

	
	//~ function loadIndex(){
		//~ var thesis_detail_api = '/api/thesis/index'
		//~ $.get(thesis_detail_api, {}, function(response) {
			//~ var year_now = new Date().getFullYear();
			//~ for (var yr = 2010; yr <= year_now; yr++){
				//~ var entry_name = ('<div align=center><a href=/thesis/list/year/' + yr +'>'+ yr +'</a></div><br>');
				//~ $(".index").append(entry_name);
			//~ };
			//~ response.adviser.forEach(function(adv) {
				//~ entry_name = ('<div align=center><a href=/thesis/list/adviser/' + adv + '>' + adv.split('_')[0] +' ' + adv.split('_')[1] + '</a></div><br>');
				//~ $(".index").append(entry_name);
			//~ });
			//~ response.university.forEach(function(uni) {
				//~ entry_name = ('<div align=center><a href=/thesis/list/university/' + PUP + '>' + uni + '</a></div><br>');
				//~ entry_name = ('<div align=center><a href=/thesis/list/university/PUP>PUP</a></div><br>');
				//~ $(".index").append(entry_name);
			//~ });
		//~ });
	//~ }
	function loadIndex(){
		var thesis_detail_api = '/api/thesis/index'
		$.get(thesis_detail_api, {}, function(response) {
			var year_now = new Date().getFullYear();
				$("#thesis-menu").append('<li><a href=/thesis/list/all/all>All</a></li>');
				$("#thesis-menu").append('<li role=separator class=divider></li>');	
			for (var yr = 2010; yr <= year_now; yr++){
				$("#thesis-menu").append('<li><a href=/thesis/list/year/' + yr +'>'+ yr +'</a></li>');
			};
			$("#thesis-menu").append('<li role=separator class=divider></li>');
			response.adviser.forEach(function(adv) {
				$("#thesis-menu").append('<li><a href=/thesis/list/adviser/' + adv + '>' + adv.split('_')[0] +' ' + adv.split('_')[1] + '</a></li>');
			});
			$("#thesis-menu").append('<li role=separator class=divider></li>');
			uni_display = '';
			response.university.forEach(function(uni) {
				for (var i = 0; i < uni.length; i++)
					uni_display += uni[i].replace("_"," ");
				$("#thesis-menu").append('<li><a href=/thesis/list/university/'+ uni +'>'+ 	uni_display + '</a></li>');
			});
		});
	}
	
	if ($("#category").length){
		loadThesisEntries();
	}
	if ($("#thesis-menu").length){
		loadIndex();
	}
});
