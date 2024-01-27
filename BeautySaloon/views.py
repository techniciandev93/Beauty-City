from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ReviewTextForm
from .models import Saloon, Service, Specialist, Review, Order
from .services import monthly_payment_stats, registered_users_stats


def index(request):
    saloons = [
        {
            'name': saloon.name,
            'address': saloon.address,
            'image': request.build_absolute_uri(saloon.image.url),
        }
        for saloon in Saloon.objects.all()
    ]

    services = [
        {
            'name': service.name,
            'price': service.price,
            'image': request.build_absolute_uri(service.image.url),
        } for service in Service.objects.all()
    ]

    specialists = [
        {
            'name': specialist.name,
            'speciality': specialist.speciality,
            'experience': specialist.experience,
            'review': specialist.reviews.count(),
            'image': request.build_absolute_uri(specialist.image.url),
        } for specialist in Specialist.objects.all()
    ]

    reviews = [
        {
            'client': review.client.phone_number,
            'rating': review.rating,
            'text': review.text,
            'date': review.date
        } for review in Review.objects.all()
    ]

    return render(
        request,
        'BeautySaloon/index.html',
        context={
            'saloons': saloons,
            'services': services,
            'specialists': specialists,
            'reviews': reviews
        }
    )


@login_required
def create_review(request, order_id):
    order = get_object_or_404(Order, id=order_id, client=request.user, review__isnull=True)

    if request.method == 'POST':
        form = ReviewTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            review = Review.objects.create(
                client=request.user,
                specialist=order.specialist,
                text=text,
            )
            order.review = review
            order.save()
            return redirect('profile')
    else:
        form = ReviewTextForm()
    return render(request, 'BeautySaloon/review.html', {'form': form, 'orderid': order.id})


@login_required
def profile(request):
    if request.user.is_superuser:
        total_payment_this_month = monthly_payment_stats()
        users_registered_this_month, total_users_registered_this_year, total_users = registered_users_stats()
        return render(request, 'BeautySaloon/admin.html', context={
            'total_payment_this_month': total_payment_this_month,
            'users_registered_this_month': users_registered_this_month,
            'total_users_registered_this_year': total_users_registered_this_year,
            'total_users': total_users
        })
    orders = Order.objects.prefetch_related('client', 'saloon', 'service', 'specialist').all()
    total_unpaid_orders = request.user.calculate_total_unpaid_orders
    return render(request, 'BeautySaloon/notes.html',
                  context={'orders': orders, 'total_unpaid_orders': total_unpaid_orders})


def get_saloons(request):
    saloons = [{
        'id': saloon.id,
        'name': saloon.name,
        'address': saloon.address
    }
        for saloon in Saloon.objects.all()
    ]
    return render(
        request,
        'BeautySaloon/select_saloon.html',
        context={
            'saloons': saloons
        })


def get_services(request):
    if request.method == 'POST':
        saloon_id = request.POST.get('selected_saloon')
        saloon = Saloon.objects.get(id=saloon_id)
        services = {
            category['category__name']:
                [
                    {
                        'id': service.id,
                        'name': service.name,
                        'price': service.price
                    } for service in saloon.service.filter(category__id=category['category__id'])
                ]
            for category in saloon.service.values('category__id', 'category__name').distinct()
        }

        return render(
            request,
            'BeautySaloon/select_service.html',
            context={
                'services': services
            })
    else:
        pass


def get_masters(request):
    if request.method == 'POST':
        saloon_id = request.POST.get('selected_service')
        print(request.POST)
        print(saloon_id)
        return render(
            request,
            'BeautySaloon/select_master.html')
