/**
 * Created by josh on 30/7/15.
 */

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
        console.log(prefix);

        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        console.log(formCount);
        var row = $('.dynamic-form:first').clone(true).get(0);
        console.log(row);
        $(row).removeAttr('id').insertAfter($('.dynamic-form:last')).children('.hidden').removeClass('hidden');

        $(row).children().not(':last').children().each(function() {
    	    updateElementIndex(this, prefix, formCount);
    	    $(this).val('');

        });
        $(row).children('.errorlist').remove();

        $(row).find('.delete-row').click(function() {
    	    deleteForm(this, prefix);
        });
         $('#id_'+prefix+'-'+(formCount)+'-scheduled').val('no');
        //$('#id_'+prefix+'-'+(formCount)+'-scheduled').toArray('no','yes').select('no');
        $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
        return false;
    }

    function deleteForm(btn, prefix) {
        if(parseInt($('#id_' + prefix + '-TOTAL_FORMS').val())==1)
            return false;
        $(btn).parents('.dynamic-form').remove();
        var forms = $('.dynamic-form');
        console.log(forms)
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
    	    $(forms.get(i)).children().not(':last').children().each(function() {
    	        updateElementIndex(this, prefix, i);
    	    });
        }
        return false;
    }
