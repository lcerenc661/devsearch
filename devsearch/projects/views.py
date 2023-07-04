from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages


from .forms import ProjecForm, ReviewForm
from .models import Project, Review, Tag
from .utils import searchProjects, getCustomRange , paginateProjects


def projects(request):
    projects, search_query = searchProjects(request)
    results = 6
    page, paginator, projects = paginateProjects(request, projects, results)
    custom_range = getCustomRange(paginator, page)
    context = {'projects':projects, 'search_query': search_query, 
                'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)


def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    reviews = projectObj.review_set.all()
    form = ReviewForm()
     
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount
        messages.success(request, 'Your review was successfully submitted')
        return redirect('project', pk=projectObj.id)
        
        
    context = {'project':projectObj, 'reviews': reviews, 'form':form}
    return render (request, 'projects/single_projects.html', context)


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjecForm
    
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(','," ").split()
        form = ProjecForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjecForm(instance=project)
    
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(','," ").split()
        
        form = ProjecForm(request.POST, request.FILES, instance=project )
        if form.is_valid():
            form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
                
            return redirect('account')
    context = {'form': form, 'project': project}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    projectObj = profile.project_set.get(id=pk)
    context = {'object':projectObj}
    if request.method == "POST":
        projectObj.delete()
        return redirect('account')
        
    return render(request, 'delete_template.html', context)