import csv
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import MealEntryForm, ProfileForm, PostForm
from .models import MealEntry, Profile, Post


def index(request):
    return render(request, "index.html")


@login_required
def timeline(request):
    query = request.GET.get("q", "").strip()
    posts = Post.objects.all()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    return render(request, "timeline.html", {"posts": posts, "query": query})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect("timeline")
    else:
        form = PostForm()
    return render(request, "post_create.html", {"form": form})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "post_detail.html", {"post": post})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "post_edit.html", {"form": form, "post": post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("timeline")
    return render(request, "post_confirm_delete.html", {"post": post})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


# ---------------- calorie ----------------
@login_required
def calorie_dashboard(request):
    today = timezone.localdate()
    start = today - timedelta(days=6)

    entries = MealEntry.objects.filter(user=request.user, date__range=[start, today])
    daily = entries.values("date").annotate(kcal_total=Sum("kcal")).order_by("date")

    profile, _ = Profile.objects.get_or_create(user=request.user)

    today_totals = entries.filter(date=today).aggregate(
        kcal=Sum("kcal"),
        protein=Sum("protein"),
        fat=Sum("fat"),
        carb=Sum("carb"),
    )

    labels = [d["date"].strftime("%m/%d") for d in daily]
    kcal_series = [int(d["kcal_total"] or 0) for d in daily]

    return render(
        request,
        "calorie/dashboard.html",
        {
            "profile": profile,
            "today": today,
            "today_totals": today_totals,
            "labels": labels,
            "kcal_series": kcal_series,
        },
    )


@login_required
def calorie_entry_list(request):
    qs = MealEntry.objects.filter(user=request.user)

    q = request.GET.get("q", "").strip()
    date_from = request.GET.get("from", "").strip()
    date_to = request.GET.get("to", "").strip()
    order = request.GET.get("order", "-date")

    if q:
        qs = qs.filter(name__icontains=q)
    if date_from:
        qs = qs.filter(date__gte=date_from)
    if date_to:
        qs = qs.filter(date__lte=date_to)

    allowed_orders = ["-date", "date", "-kcal", "kcal"]
    if order not in allowed_orders:
        order = "-date"

    qs = qs.order_by(order)

    return render(
        request,
        "calorie/entry_list.html",
        {"entries": qs, "q": q, "date_from": date_from, "date_to": date_to, "order": order},
    )


@login_required
def calorie_entry_create(request):
    if request.method == "POST":
        form = MealEntryForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect("calorie_entry_list")
    else:
        form = MealEntryForm()
    return render(request, "calorie/entry_form.html", {"form": form, "title": "add entry"})


@login_required
def calorie_entry_update(request, pk):
    obj = get_object_or_404(MealEntry, pk=pk, user=request.user)
    if request.method == "POST":
        form = MealEntryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("calorie_entry_list")
    else:
        form = MealEntryForm(instance=obj)
    return render(request, "calorie/entry_form.html", {"form": form, "title": "edit entry"})


@login_required
def calorie_entry_delete(request, pk):
    obj = get_object_or_404(MealEntry, pk=pk, user=request.user)
    if request.method == "POST":
        obj.delete()
        return redirect("calorie_entry_list")
    return render(request, "calorie/entry_delete.html", {"obj": obj})


@login_required
def calorie_settings(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("calorie_dashboard")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "calorie/settings.html", {"form": form})


@login_required
def calorie_copy_yesterday(request):
    today = timezone.localdate()
    yesterday = today - timedelta(days=1)

    y_entries = MealEntry.objects.filter(user=request.user, date=yesterday)
    for e in y_entries:
        MealEntry.objects.create(
            user=request.user,
            date=today,
            name=e.name,
            kcal=e.kcal,
            protein=e.protein,
            fat=e.fat,
            carb=e.carb,
        )
    return redirect("calorie_entry_list")


@login_required
def calorie_export_csv(request):
    qs = MealEntry.objects.filter(user=request.user).order_by("-date", "-created_at")

    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename="calorie_entries.csv"'

    w = csv.writer(resp)
    w.writerow(["date", "name", "kcal", "protein", "fat", "carb"])
    for e in qs:
        w.writerow([e.date, e.name, e.kcal, e.protein, e.fat, e.carb])

    return resp


@login_required
def calorie_api_entries(request):
    qs = MealEntry.objects.filter(user=request.user).order_by("-date", "-created_at")[:200]
    data = [
        {
            "id": e.id,
            "date": e.date.isoformat(),
            "name": e.name,
            "kcal": e.kcal,
            "protein": e.protein,
            "fat": e.fat,
            "carb": e.carb,
        }
        for e in qs
    ]
    return JsonResponse({"entries": data})
