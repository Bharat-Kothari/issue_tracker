from itertools import izip, count
import json
import operator
import datetime

from django.core.urlresolvers import reverse_lazy, reverse
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.loader import render_to_string
from django.views.generic import View, CreateView, FormView, UpdateView, DetailView, ListView
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.db.models import Q, Sum, Count
from psycopg2.extensions import JSON

from Issue_Track import settings
from issue_tracker.form import AddStoryFormSet, AddStoryForm
from issue_tracker.models import Project, Story
from issue_tracker import form
from issue_tracker import tasks
from user_app.models import MyUser


class DashBoardView(ListView):
    """
    View of dashboard showing profile page link,
    Create project and various project in which user in involved.
    """
    template_name = "issue_tracker/dashboard.html"
    model = Project
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DashBoardView, self).get_context_data(**kwargs)
        context['filter_code'] = self.request.GET.get('id')  # To send the id in filter_code
        return context

    def get_queryset(self):
        filter_id = self.request.GET.get('id')
        project = Project.objects.filter(assigned_to=self.request.user)

        # To have different queryset for All Member Owner of project.
        if filter_id == '1':
            project = Project.objects.filter(assigned_to=self.request.user)
        if filter_id == '3':
            project = Project.objects.filter(project_manager=self.request.user)
        if filter_id == '2':
            temp = Project.objects.exclude(project_manager=self.request.user)
            project = temp.filter(assigned_to=self.request.user)
        return project


class CreateProjectView(CreateView):
    """
     View to Create Project

    """
    template_name = "issue_tracker/project/create.html"
    form_class = form.CreateProjectForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super(CreateProjectView, self).get_form_kwargs()
        kwargs['request'] = self.request  # To send request to the form
        return kwargs


class ProjectView(DetailView):
    """
    View To see project details
    Display story of that project

    """
    template_name = "issue_tracker/project/project.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        story_visible = Story.objects.filter(project_title=self.object.id, visibility=True).order_by('date')

        sch_story = story_visible.filter(scheduled='ys')
        unscheduled_story = story_visible.filter(scheduled='no')

        un_started = sch_story.filter(status='unstrtd')
        started = sch_story.exclude(status='unstrtd')

        context['started'] = started
        context['unstarted'] = un_started
        context['unsch_story'] = unscheduled_story
        return context


class ProjectUpdateView(UpdateView):
    """
    View To update the project
    """
    template_name = "issue_tracker/project/update.html"
    model = Project
    context_object_name = 'project'
    form_class = form.UpdateProjectForm

    def get_success_url(self):
        project_id = self.kwargs['pk']
        return reverse_lazy('project', kwargs={'pk': project_id})

    def get_form_kwargs(self):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['id'] = self.kwargs['pk']
        return kwargs


class AddStoryView(FormView):
    """
    View to add multiple story to the project
    """

    form_class = formset_factory(AddStoryForm, formset=AddStoryFormSet, extra=0, min_num=1)
    template_name = "issue_tracker/story/add.html"

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            stories_list = self.request.POST.get('stories')
            stories_list = json.loads(stories_list)
            for story in stories_list:
                s = Story()
                s.project_title = Project.objects.get(id=self.kwargs['pk'])
                s.email = self.request.user
                s.story_title = story['story_title']
                s.description = story['description']
                s.estimate = story['estimate']
                s.scheduled = story['scheduled']['scheduled']
                s.assignee = MyUser.objects.get(email=story['assignee']['name'])
                s.save()
            return HttpResponse(stories_list, content_type="html")
        return super(AddStoryView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            print('assignee')
            project = Project.objects.get(id=self.kwargs['pk'])
            assignees = project.assigned_to.all()
            print(assignees)
            response = [{'name': assignee.email} for assignee in assignees]
            print (response)
            print(response[1])
            return HttpResponse(json.dumps(response), content_type="application/json")
        return super(AddStoryView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AddStoryView, self).get_form_kwargs()
        kwargs['id'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AddStoryView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        for f in form:
            obj = f.save(commit=False)
            if obj.story_title:
                obj.project_title = Project.objects.get(id=self.kwargs['pk'])
                obj.email = self.request.user
                obj.save()

        return super(AddStoryView, self).form_valid(form)

    def get_success_url(self):
        project_id = self.kwargs['pk']
        return reverse('project', kwargs={'pk': project_id})


class StoryView(DetailView):
    """
    View to show story
    Have link for update story and delete story
    """
    model = Story
    template_name = "issue_tracker/story/story.html"


class UpdateStoryView(UpdateView):
    """
    view to update the story
    """
    model = Story
    template_name = "issue_tracker/story/update.html"
    form_class = form.UpdateStoryForm

    def get_form_kwargs(self):
        kwargs = super(UpdateStoryView, self).get_form_kwargs()
        kwargs['id'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        assigned = form.cleaned_data['assignee']
        result = Story.objects.filter(assignee=assigned).exists()
        if result == False:  # To send the mail to new assigned member
            subject = self.object.story_title
            message = ' You have been assigned to story'
            from_email = settings.EMAIL_HOST_USER
            to_mail = self.object.assignee.email
            send_mail(subject, message, from_email, [to_mail], fail_silently=True)
        return super(UpdateStoryView, self).form_valid(form)

    def get_success_url(self):
        project_id = self.get_object().project_title.id
        return reverse('project', kwargs={'pk': project_id})


class StoryDeleteView(View):
    """
    view to softly delete a story
    Setting visibility to false
    """

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        story = get_object_or_404(Story, pk=id)
        story.visibility = False
        story.save()
        project_id = story.project_title.id
        return HttpResponseRedirect(reverse_lazy('project', kwargs={'pk': project_id}))


class SearchStoryView(View):
    """
    View to return story of that project
    Story are filter by the keywords enter
    """
    template_name = "issue_tracker/story/search.html"

    def dispatch(self, request, *args, **kwargs):
        search_text = self.request.GET.get('search_text')
        items = search_text.split(',')  # for splitting the data separated by ','
        keywords = [a.strip() for a in items if a.strip()]  # To remove blank spaces before and after the word
        project_id = self.kwargs['pk']
        if (len(search_text) != 0) and keywords:
            story = Story.objects.filter(reduce(operator.or_, (Q(story_title__icontains=item) & Q(visibility='ys')
                                                               for item in keywords)))
            stories = story.filter(project_title_id=project_id)
            if stories:
                response = [{'story_title': story.story_title} for story in stories]
            else:
                response = [{'story_title': "No Story Found"}]
        else:
            response = [{'story_title': "Please enter search word"}]
        return HttpResponse(json.dumps(response), content_type="application/json")


class ProjectSettingView(DetailView):
    """
    View to show the different member and their story.
    Story that are started un-started and finished
    and to show unassigned story of that project
    """
    template_name = "issue_tracker/project/project_settings.html"
    model = Project

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = dict()
            initial_date = self.request.GET.get('initial_date')
            final_date = self.request.GET.get('final_date')
            context = self.story(context, initial_date, final_date)
            data = render_to_string('issue_tracker/story/table.html', context=context)
            if self.request.GET.get('mail'):
                tasks.email.delay(data, self.request.user.email)
            return HttpResponse(data, content_type="html")
        return super(ProjectSettingView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        id = self.kwargs['pk']
        context = super(ProjectSettingView, self).get_context_data(**kwargs)
        initial = (Story.objects.filter(project_title=id)).order_by('date')
        if initial:
            initial_date = initial[0].date
        else:
            initial_date = datetime.date.today()
        context = self.story(context, initial_date, datetime.date.today())

        result = render_to_string('issue_tracker/story/table.html', context=context)
        context['result'] = result
        context['init'] = initial_date
        context['final'] = datetime.date.today()
        return context
        # return self.render_to_response(context=context)

    def story(self, context, initial_date, final_date):
        id = self.kwargs['pk']
        project = Project.objects.get(id=id)
        assignees = project.assigned_to.all()
        storys = (Story.objects.filter(project_title=id, visibility='ys', date__range=(initial_date, final_date))).order_by('assignee__email')
        list = []
        i = 0
        for each in assignees:
            list.append([])
            list[i] = (storys.filter(assignee=each).exclude(status='deliv')).values('assignee__email', 'status','estimate').annotate(d=Count('assignee'),d1=Sum('estimate'))
            i += 1


        un_assigned_story = storys.filter(assignee=None)
        count_story = un_assigned_story.count()
        count_estimate = un_assigned_story.aggregate(Sum('estimate'))

        context['result']=izip(assignees, list)
        context['count_story']=count_story
        context['count_estimate']=count_estimate
        return context