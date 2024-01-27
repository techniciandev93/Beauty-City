from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Saloon, Service, Specialist, Review


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
def profile(request):
    return render(request, 'BeautySaloon/notes.html')
