from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Idea, DevTool, IdeaStar
from .forms import IdeaForm, DevToolForm

def idea_list(request):
    sort = request.GET.get("sort", "latest")

    if sort == "old":
        ideas = Idea.objects.all().order_by("created_at")

    elif sort == "name":
        ideas = Idea.objects.all().order_by("title")

    elif sort == "interest":
        ideas = Idea.objects.all().order_by("-interest")

    elif sort == "star":
        ideas = Idea.objects.annotate(star_count=Count("ideastar")).order_by("-star_count", "-created_at")
        
    else:   
        ideas = Idea.objects.all().order_by("-created_at")

    if request.user.is_authenticated:
        starred_ids = IdeaStar.objects.filter(user=request.user).values_list("idea_id", flat=True)
    else:
        starred_ids = []

    context = {
        "ideas": ideas,
        "sort": sort,
        "starred_ids": starred_ids,
    }

    return render(request, "ideas/idea_list.html", context)
    
def idea_create(request):

    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES)

        if form.is_valid():
            idea = form.save()
            return redirect("ideas:idea_detail", idea_id=idea.id)

        context = {
            "form": form,
        }
        return render(request, "ideas/idea_form.html", context)

    else:
        form = IdeaForm()

        context = {
            "form": form,
        }
        return render(request, "ideas/idea_form.html", context)

def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    if request.user.is_authenticated:
        is_starred = IdeaStar.objects.filter(user=request.user, idea=idea).exists()
    else:
        is_starred = False

    context = {
        "idea": idea,
        "is_starred": is_starred,
    }

    return render(request, "ideas/idea_detail.html", context)

def idea_update(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)


    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES, instance=idea)

        if form.is_valid():
            idea = form.save()
            return redirect("ideas:idea_detail", idea_id=idea.id)

        context = {
            "form": form,
            "idea": idea,
        }
        return render(request, "ideas/idea_form.html", context)


    else:
        form = IdeaForm(instance=idea)

        context = {
            "form": form,
            "idea": idea,
        }
        return render(request, "ideas/idea_form.html", context)


def idea_delete(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    if request.method == "POST":
        idea.delete()
        return redirect("ideas:idea_list")

    context = {
        "idea": idea,
    }

    return render(request, "ideas/idea_confirm_delete.html", context)

def devtool_list(request):
    devtools = DevTool.objects.all()

    context = {
        "devtools": devtools,
    }

    return render(request, "ideas/devtool_list.html", context)


def devtool_create(request):
    
    if request.method == "POST":
        form = DevToolForm(request.POST)

        if form.is_valid():
            devtool = form.save()
            return redirect("ideas:devtool_detail", devtool_id=devtool.id)

        context = {
            "form": form,
        }
        return render(request, "ideas/devtool_form.html", context)


    else:
        form = DevToolForm()

        context = {
            "form": form,
        }
        return render(request, "ideas/devtool_form.html", context)

def devtool_detail(request, devtool_id):
    devtool = get_object_or_404(DevTool, id=devtool_id)

    ideas = devtool.ideas.all()

    context = {
        "devtool": devtool,
        "ideas": ideas,
    }

    return render(request, "ideas/devtool_detail.html", context)

def devtool_update(request, devtool_id):
    devtool = get_object_or_404(DevTool, id=devtool_id)

    if request.method == "POST":
        form = DevToolForm(request.POST, instance=devtool)

        if form.is_valid():
            devtool = form.save()
            return redirect("ideas:devtool_detail", devtool_id=devtool.id)

        context = {
            "form": form,
            "devtool": devtool,
        }
        return render(request, "ideas/devtool_form.html", context)


    else:
        form = DevToolForm(instance=devtool)

        context = {
            "form": form,
            "devtool": devtool,
        }
        return render(request, "ideas/devtool_form.html", context)


def devtool_delete(request, devtool_id):
    devtool = get_object_or_404(DevTool, id=devtool_id)

    if request.method == "POST":
        devtool.delete()
        return redirect("ideas:devtool_list")

    context = {
        "devtool": devtool,
    }

    return render(request, "ideas/devtool_confirm_delete.html", context)

def idea_interest(request, idea_id, direction):
    idea = get_object_or_404(Idea, id=idea_id)

    if direction == "plus":
        idea.interest += 1
    elif direction == "minus":
        idea.interest -= 1

    idea.save()

    return redirect("ideas:idea_list")

@login_required(login_url="/admin/login/")
def idea_star_toggle(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    star = IdeaStar.objects.filter(user=request.user, idea=idea)

    if star.exists():
        star.delete()

    else:
        IdeaStar.objects.create(user=request.user, idea=idea)

    next_url = request.GET.get("next", "ideas:idea_list")
    return redirect(next_url)