$(function(){
	$('#search-button').click(function(event) {
        $('#search-results').html('<img id="loader-img" alt="" src="/media/images/loading_spinner.gif" width="100" height="100" />');

        event.preventDefault();
        var search_text = $('#search').val();
        var x = document.getElementById("project_id").value;
        $.ajax({
		        type: "GET",
		        url: "/home/search/story/"+x+"/",
		        data: "search_text="+search_text,
                dataType: 'json',
                success: searchSuccess

		        });
	});

    $('#clear-button').click(function(){
        $('#search-results').hide();
    });

    function callajax(flag_mail){
        $('.error-message').html("");


        var initial_date = $('.initial_date').val();
        var final_date = $('.final_date').val();
        var x = document.getElementById("project_id").value;
        if(flag_mail)
            dates = {"initial_date":initial_date, "final_date":final_date,"mail":"send_mail"};
        else

            dates = {"initial_date":initial_date, "final_date":final_date};
        if(initial_date>final_date)
        {$('.error-message').html("initial date should be smaller than final date");
        return false}
	    $.ajax({
		        type: "GET",
		        url: "/home/project/settings/"+x+"/",
		        data: dates,
                success: searchStory

		        });

    }
    $('.date_button').click(function(event) {
        callajax(false)
		        });

    $('.send_mail').click(function(event) {
        callajax(true)
                });
});

function searchStory(data){
    $('.story_table').empty();
    $('.story_table').html(data);
}

function searchSuccess(data)
{
    $('#search-results').html('');
    $('#search-results').html("<h3> Searched Storys :-</h3>")

    $.each(data, function(index, element)
    {
            $('#search-results').append("<li>" +element['story_title']+"</li>");
    });
}


