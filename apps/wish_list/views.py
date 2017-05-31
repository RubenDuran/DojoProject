from django.shortcuts import render, redirect
from django.contrib import messages
from . models import User, Item, Wishlist
import bcrypt


def main(request):
    return redirect('/main')


def index(request):
    return render(request, 'wish_list/index.html')


def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    user = User.objects.get(pk=user_id)
    items = Item.objects.all()
    my_wishlist = Wishlist.objects.filter(user__pk=user_id)
    others_wishlist = Wishlist.objects.all().exclude(user=user_id)

    wishlist = []
    for wish in my_wishlist:
        wishlist.append(wish.item.prod_name)

    context = {
        'user': user,
        'items': items,
        'my_wishlist': my_wishlist,
        'others_wishlist': others_wishlist,
        'wishlist': wishlist,
    }
    return render(request, 'wish_list/dashboard.html', context)


def register(request):
    if request.method == 'POST':
        errors = User.objects.validate(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            messages.success(request, 'Successfully registered!')
            hashed = bcrypt.hashpw(
                request.POST['pw'].encode(), bcrypt.gensalt())

            User.objects.create(name=request.POST['name'], username=request.POST[
                                'username'], password=hashed, created_at='NOW()', updated_at='NOW()', date_hired=request.POST['date_hired'])
            username = request.POST["username"]
            user_details = User.objects.filter(username=username)
            user = user_details[0]
            request.session['user_id'] = user.id
            return redirect('/dashboard')
    return redirect('/')


def login(request):
    if request.method == 'POST':
        errors = User.objects.signin(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            messages.success(request, 'Successfully logged in!')
            username = request.POST["username"]
            user_details = User.objects.filter(username=username)
            user = user_details[0]
            request.session['user_id'] = user.id
            return redirect('/dashboard')
        return redirect('/')


def logout(request):
    del request.session['user_id']
    return redirect('/')


def add_wish(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    user = User.objects.get(pk=user_id)
    item_id = id
    item = Item.objects.get(pk=item_id)

    Wishlist.objects.create(user=user, item=item)
    return redirect('/dashboard')


def delete(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    user = User.objects.get(pk=user_id)
    item_id = id
    item = Item.objects.get(pk=item_id)

    Wishlist.objects.filter(user=user, item=item).delete()
    Item.objects.filter(pk=item_id).delete()
    return redirect('/dashboard')


def remove(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    user = User.objects.get(pk=user_id)
    item_id = id
    item = Item.objects.get(pk=item_id)

    Wishlist.objects.filter(user=user, item=item).delete()
    return redirect('/dashboard')


def add(request):
    if request.method == 'POST':
        errors = Item.objects.validate(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            user_id = request.session.get('user_id')
            if not user_id:
                return redirect('/')
            user = User.objects.get(pk=user_id)
            prod_name = request.POST['prod_name']
            try:
                item = Item.objects.get(prod_name=prod_name)
            except:
                item = Item.objects.create(
                    prod_name=prod_name, user=user, created_at='NOW()', updated_at='NOW()')

            messages.success(request, 'Successfully Added Item')

            Wishlist.objects.create(
                user=user, item=item, created_at='NOW()', updated_at='NOW()')
            return redirect('/dashboard')


def create(request):
    return render(request, 'wish_list/add_item.html')


def item(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    item_id = id
    item = Item.objects.get(pk=item_id)
    user = User.objects.get(pk=user_id)
    item_wishlist = Wishlist.objects.filter(item__pk=item_id)
    # others_wishlist = Wishlist.objects.all().exclude(user__pk=user_id)

    print item_wishlist
    for name in item_wishlist:
        print name.user.name

    context = {
        'user': user,
        'item': item.prod_name,
        'item_wishlist': item_wishlist,
    }
    return render(request, 'wish_list/item.html', context)
