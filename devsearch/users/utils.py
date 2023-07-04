from .models import Skill, Profile
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage




def searchProfiles(request):
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    skills = Skill.objects.filter(name__icontains=search_query)
        
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills))
    
    return profiles, search_query


def paginateProfiles(request, profiles, results):
    
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)
    
    try: 
        profiles = paginator.page(page)
        
    except PageNotAnInteger:
        page=1
        profiles = paginator.page(page)
    
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
        
    return page, paginator, profiles
        


def getCustomRange(paginator, page):
    
    leftIndex = (int(page)-2)
    rigthIndex = (int(page)+3)
    
    if leftIndex < 1:
        leftIndex=1
    
    if rigthIndex > paginator.num_pages:
        rigthIndex = paginator.num_pages + 1
        
    custom_range = range(leftIndex, rigthIndex)
    
    return custom_range



