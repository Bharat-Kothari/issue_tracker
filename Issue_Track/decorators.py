from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404

from issue_tracker.models import Project, Story

# To check user is already logged in.


def login_check(f):
    def check_authentication(request, *args):
        if request.user.is_authenticated():
            return redirect(reverse_lazy('dashboard'))
        else:
            return f(request)

    return check_authentication


# To check user has logged in.


def logout_check(f):
    def check_authentication(request, *args, **kwargs):
        if request.user.is_authenticated():
            return f(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    return check_authentication


# To check a login member is member of that project


def project_member_check(f):
    def check_authentication(request, *args, **kwargs):
        if request.user.is_authenticated():
            if get_object_or_404(Project, pk=kwargs['pk'], assigned_to=request.user):
                return f(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    return check_authentication


# To check that a project which is being updated,is updated by the Project manager


def project_update_check(f):
    def check_authentication(request, *args, **kwargs):
        if request.user.is_authenticated():
            if get_object_or_404(Project, pk=kwargs['pk'], project_manager=request.user):
                return f(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    return check_authentication


# To check a logged in user is  member of that project of which he is viewing the story


def story_view_check(f):
    def check_authentication(request, *args, **kwargs):
        if request.user.is_authenticated():
            if Story.objects.filter(id=kwargs['pk']).exists():
                story = Story.objects.get(id=kwargs['pk'])
                if story.visibility:
                    project = story.project_title
                    temp = project.assigned_to.all()
                    if temp.filter(email=request.user.email):
                        return f(request, *args, **kwargs)
                    else:
                        raise Http404
                else:
                    raise Http404
            else:
                raise Http404
        else:
            return redirect(reverse('login'))

    return check_authentication
