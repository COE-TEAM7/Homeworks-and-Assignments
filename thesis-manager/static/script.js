$(function(){	
	var thesis_entry_api = '/api/thesis';
	var thesis_edit_api = '/api/thesis/edit';
	//~ var thesis_delete_api = '/api/thesis/delete/(.*)';
	//~ var thesis_search_api = '/api/thesis/search/(.*)';
    function onFormSubmit(event){
		var data = $(event.target).serializeArray();
		var thesis = {};
		var a = 0;
		for(var i = 0; i<data.length ; i++)
		{
			if (data[i].name === 'members'){
				thesis[data[i].name + a] = data[i].value;
				a = a + 1;
			}
			else {
				thesis[data[i].name] = data[i].value;
			}
		}
		$.post(thesis_entry_api, thesis, function(){
				//~ $("input[type=text], [type=number], textarea").val("")
		});
		//~ $.post(thesis_entry_api, thesis, function(response){
			//~ if (response.status = 'OK') {
				//~ var entry_name = ('<li class=list>' + response.data.year + ' ' + response.data.title + '. Created by:' + response.data.created_by + 
				//~ ' &nbsp <a href=/api/thesis/delete/' + response.data.id + '><input class=newbtn type=button value=Delete></input></a> '+
				//~ ' &nbsp <a href=/api/thesis/details/' + response.data.id + '><input class=newbtn type=button value=View Details></input></a> '+
				//~ ' &nbsp <a href=/thesis/edit/' + response.data.id + '><input class=newbtn type=button value=Edit></input></a></li>');
				//~ $(".stls").prepend(entry_name);
				//~ $("input[type=text], [type=number], textarea").val("")
			//~ } else {
				//~ alert("ERROR");
			//~ }
		//~ })
		return false;
	}
	//~ 
	//~ function deleteStudentInfo(event){
		//~ $(this).parent().parent().remove();
	//~ }
	//~ 
	//~ $(document).on("click", ".newbtn", deleteStudentInfo)
	$("#create_thesis").submit(onFormSubmit)
	
	function loadEntries(event){
		var thesis_detail_api = '/api/thesis/form'
		$.get(thesis_detail_api, {}, function(response) {
			//~ $('#select_year').append($('<option selected disabled/>').text('Select a year').val(''));
			//~ $('#select_section').append($('<option selected disabled/>').text('Section').val(''));
			//~ $('#select_adviser').append($('<option selected disabled/>').text('Select the adviser').val(''));
			//~ $('#select_members').append($('<option selected disabled/>').text('Select the proponents').val(''));
			//~ $('#select_dept').append($('<option selected disabled/>').text('Select a department').val(''));
			//~ $('#select_coll').append($('<option selected disabled/>').text('Select a college').val(''));
			//~ $('#select_univ').append($('<option selected disabled/>').text('Select a university').val(''));
			var year_now = new Date().getFullYear();
			for (var yr = 2010; yr <= year_now; yr++){
				$('#select_year').append($('<option />').text(yr).val(yr));
			}
			for (var sec = 1; sec <= 5; sec++){
				$('#select_section').append($('<option />').text(sec).val(sec));
			}
			response.advisers.forEach(function(adv) {
				$('#select_adviser').append($('<option />').text(adv.adviser_name).val(adv.adviser_id));
				$('#select_members').append($('<option />').text(adv.adviser_name).val(adv.adviser_id));
				});
			response.students.forEach(function(stud) {
				$('#select_members').append($('<option />').text(stud.student_name).val(stud.student_id));
				});
			response.departments.forEach(function(d) {
				$('#select_dept').append($('<option />').text(d.dept_name).val(d.dept_id));
				});
			response.colleges.forEach(function(coll) {
				$('#select_coll').append($('<option />').text(coll.coll_name).val(coll.coll_id));
				});
			response.universities.forEach(function(univ) {
				$('#select_univ').append($('<option />').text(univ.univ_name).val(univ.univ_id));
				});
				
			$(".chosen-select").chosen({no_results_text: "None found!"});
		});
		
	}
	
	loadEntries();
});
