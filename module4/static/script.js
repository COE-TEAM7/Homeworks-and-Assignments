$(function() {
    var thesis_delete_api = '/api/thesis/delete/(.*)';
    function onFormSubmit(event) {
        var data = $(event.target).serializeArray();
        var thesis = {};
        for(var i = 0; i<data.length ; i++)
        {
            thesis[data[i].name] = data[i].value
        }
        //var list_element = $('<li>');
        // list_element.html("Title: " + thesis.thesis_title + ' Year: ' + thesis.thesis_year + ' Abstract: ' + thesis.thesis_abstract + ' Adviser: ' + thesis.thesis_adviser + ' Section: ' + thesis.thesis_section);
        // $('.thesis-list').prepend(list_element);
        $('.text_box').val('');
        $('.abstract').val('');
        $('.select').val('');

        var thesis_entry_api = '/api/thesis';
        $.post(thesis_entry_api, thesis, function(response){
            if (response.status = 'OK'){
                // list_element.html(thesis.thesis_year + ' ' +  thesis.thesis_title);
                 var entry_name = ('<li class=list>' + thesis.thesis_year + ' ' + thesis.thesis_title + ', Created by: ' + thesis.thesis_author + ' &nbsp <a href=/api/thesis/delete/' + thesis.id + '>' + 'Created by: ' + '<input class=newbtn type=button value=delete></input></a></li>');
                 $(".thesis-list").prepend(entry_name);
            }else {
                alert("ERROR");
            }
        });

        return false;
    }

    $('.create-form').submit(onFormSubmit)
    $(document).on("click", ".newbtn", deleteThesisInfo)
    $('.submit_form').click(function() {
              location.reload();

    });


    function deleteThesisInfo(event){
        $(this).parent().parent().remove();
    }

    function loadThesis2(event){
        var thesis_list_api = '/api/thesis';
        $.get(thesis_list_api, {}, function(response){
            console.log('thesis_list', response);
            response.data.forEach(function(thesis){
                var list_element = $('<li>');
                var entry_name = ('<li class=list>' + thesis.thesis_year + ' ' + thesis.thesis_title + ', Created by: ' + thesis.thesis_author);
                $(".thesis-list2").prepend(entry_name);
                })
        });
    }

    function loadThesis1(event){
        var thesis_list_api = '/api/thesis';
        $.get(thesis_list_api, {}, function(response){
            console.log('thesis_list', response);
            response.data.forEach(function(thesis){
            	var list_element = $('<li>');
        		var entry_name = ('<li class=list>' + thesis.thesis_year + ' ' + thesis.thesis_title + ', Created by: ' + thesis.thesis_author + ' &nbsp <a href=/api/thesis/delete/' + thesis.id + '><input class=newbtn type=button value=delete></input></a></li>');
                $(".thesis-list1").prepend(entry_name);
                })
        });
    }
    loadThesis1();
    loadThesis2();
});
