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

    $('.date_button').click(function(event) {

        var initial_date = $('.initial_date').val();
        var final_date = $('.final_date').val();
        var x = document.getElementById("project_id").value;
        dates = {"initial_date":initial_date, "final_date":final_date};
        if (!initial_date)
            alert("select initial date")
        else
        if(!final_date)
        alert("select final date")
        else
        if(initial_date>final_date)
        alert("initial date should be smaller than final")
	    $.ajax({
		        type: "GET",
		        url: "http://localhost:8000/home/project/settings/"+x+"/",
		        data: dates,
                success: searchStory

		        });
	});
});

function searchStory(data){
    $('.story_table').empty();
    $('.story_table').html(data);
}
function searchSuccess(data) {
            $('#search-results').html('');
            $.each(data, function(index, element) {
            $('#search-results').append("<li>" +element['story_title']+"</li>");
            console.log("hello");
            console.log(element['story_title']);

        });
}

$(function () {
        $('.add-row').click(function() {
    	    return addForm(this, 'form');
        });
        $('.delete-row').click(function() {
    	    return deleteForm(this, 'form');
        })
    });



function updateElementIndex(el, prefix, ndx) {
		var id_regex = new RegExp('(' + prefix + '-\\d+)');
		var replacement = prefix + '-' + ndx;
		if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
		if (el.id) el.id = el.id.replace(id_regex, replacement);
		if (el.name) el.name = el.name.replace(id_regex, replacement);
	}

    function addForm(btn, prefix) {
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        var row = $('.dynamic-form:first').clone(true).get(0);
        $(row).removeAttr('id').insertAfter($('.dynamic-form:last')).children('.hidden').removeClass('hidden');
        $(row).children().not(':last').children().each(function() {
    	    updateElementIndex(this, prefix, formCount);
    	    $(this).val('');
        });
        $(row).find('.delete-row').click(function() {
    	    deleteForm(this, prefix);
        });
        $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
        return false;
    }

    function deleteForm(btn, prefix) {
        $(btn).parents('.dynamic-form').remove();
        var forms = $('.dynamic-form');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
    	    $(forms.get(i)).children().not(':last').children().each(function() {
    	        updateElementIndex(this, prefix, i);
    	    });
        }
        return false;
    }


