from django.contrib.auth import login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from users.forms import ProfileModelForm
from users.models import Profile, Category


# Create your views here.


def user_list(request, cats=None):
    cat_menu = Category.objects.all()
    search_query = request.GET.get('search', '')

    if search_query:
        users = Profile.objects.filter(Q(username__icontains=search_query) | Q(phone__icontains=search_query))

    elif cats:
        users = Profile.objects.filter(category__slug=cats)

    else:
        users = Profile.objects.all()

    p = Paginator(users, 6)
    page = request.GET.get('page')

    try:
        page_obj = p.get_page(page)
    except PageNotAnInteger:
        page_obj = p.page(1)

    except EmptyPage:
        page_obj = p.page(p.num_pages)

    context = {
        'users': users,
        'page_obj': page_obj,
        'cat_menu': cat_menu,
        # 'category_users': category_users

    }
    return render(request, 'users/user-list.html', context)


def user_details(request, pk):
    user = Profile.objects.filter(id=pk).first()
    context = {
        'user': user
    }
    return render(request, 'users/user-details.html', context)


def user_add(request):
    form = ProfileModelForm()

    if request.method == 'POST':
        form = ProfileModelForm(request.POST, request.FILES)
        # email = form.cleaned_data['email']
        # password = form.cleaned_data['password']

        if form.is_valid():
            form.save()

            return redirect('user_list')

    context = {
        'form': form,
        'action': 'Add'
    }
    return render(request, 'users/user-add.html', context)


def user_delete(request, pk):
    user = Profile.objects.get(pk=pk)
    if user:
        user.delete()
    return redirect('user_list')


def user_update(request, pk):
    user = Profile.objects.filter(id=pk).first()
    form = ProfileModelForm(instance=user)

    if request.method == 'POST':
        form = ProfileModelForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')

    context = {
        'form': form,
        'action': 'Update'
    }
    return render(request, 'users/user-update.html', context)

#
# def category(request, cats):
#     category_users = Profile.objects.filter(category__slug=cats)
#
#     return render(request, 'users/categories.html', {'cats': cats.title(), 'category_users': category_users})
