$(function(){
	$('#search-button').click(function(event) {
        alert('try');
        $('#search-results').html('<img id="loader-img" alt="" src="/media/images/loading_spinner.gif" width="100" height="100" />');

        event.preventDefault();
        var search_text = $('#search').val();
        var x = document.getElementById("project_id").value;
        console.log(x);
	    $.ajax({
		        type: "GET",
		        url: "http://localhost:8000/home/search/story/"+x+"/",
		        data: "search_text="+search_text,
                dataType: 'json',
                success: searchSuccess

		        });
	});

    $('#clear-button').click(function(){
        $('#search-results').hide();
    });
});

function searchSuccess(data) {
    console.log(data);

    var len = data.length;
    console.log(len);


            $('#search-results').html('');
            $.each(data, function(index, element) {
            $('#search-results').append("<li>" +element['story_title']+"</li>");
            console.log("hello");
            console.log(element['story_title']);

        });
}



