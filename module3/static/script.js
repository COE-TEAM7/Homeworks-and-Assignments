$(function() {
    function onFormSubmit(event) {
        var data = $(event.target).serializeArray();
        var thesis = {};
        for (var i = 0; i < data.length; i++) {
            var key = data[i].name;
            var value = data[i].value;
            thesis[key] = value
        }
        var list_element = $('<li>');
        list_element.html("Title: " + thesis.thesis_title + ' Year: ' + thesis.thesis_year + ' Abstract: ' + thesis.thesis_abstract + ' Adviser: ' + thesis.thesis_adviser + ' Section: ' + thesis.thesis_section);
        $('.thesis-list').prepend(list_element);
        $('.text_box').val('');
        $('.abstract').val('');
        $('.select').val('');

        var thesis_entry_api = '/api/thesis';
        $.post(thesis_entry_api, thesis, function(response){
            if (response.status = 'OK'){
                list_element.html(thesis.thesis_year + ' ' +  thesis.thesis_title);
            }
        });

        return false;
    }
    $('.create-form').submit(onFormSubmit)

    function loadThesis(event){
        var thesis_list_api = '/api/thesis';
        $.get(thesis_list_api, {}, function(response){
            console.log('thesis_list', response);
            response.data.forEach(function(thesis){
            	var list_element = $('<li>');
        		list_element.html(thesis.thesis_year + ' ' + thesis.thesis_title);
        		$('.thesis-list').prepend(list_element);
                })
        });
    }
    loadThesis();
});
