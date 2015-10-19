function story()
{
    var self = this;
    self.story_title = ko.observable("Story title").extend({
        required: {
            params: true,
            message: "This is required"
        }
    });
    self.description = ko.observable("Description");
    self.assignee = ko.observable();
    self.estimate = ko.observable(0);
    self.scheduled = ko.observable();
}

function StoryFormsetViewModel(){
    var self = this;

    self.displaydiv = ko.observable(false);

    self.storys = ko.observableArray([
        new story(),
        new story()
    ]);

    self.addStory = function() {
        self.storys.push(new story())
    };

    self.removeStory = function(story) { self.storys.remove(story) };

    self.totalname = ko.computed(function() {
        var total = 0;
        for (var i = 0; i < self.storys().length; i++) {
            total += self.storys().length;
        }


        self.members = function()
        {
            var url = window.location.href;
            self.assignees = ko.observableArray();
            $.ajax({
                type: "GET",
                url: url,
                success: function searchSuccess(data)
                {
                    for(var i= 0; i< data.length;i++)
                    {
                        self.assignees.push(data[i]);
                    }
                },
                failure:console.log('no result')
            });
        };
        self.members();
        return total;
    });


    self.optionss = [
        {scheduled:'ys'},
        {scheduled:'no'}
    ];
    self.show_div = function(){
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');
        var url = window.location.href;
        $.ajax({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            type: "POST",
            url: url,
            data: {
                'stories': ko.toJSON(self.storys)
            },
            success:console.log('a')
                //window.location.replace("/home/dashboard/")
        });
    };
}

ko.applyBindings(new StoryFormsetViewModel());