import json
from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View

from users.models import CustomUser
from .forms import ReviewTextForm, OrderForm, ConsultationRequestForm
from .models import Saloon, Service, Specialist, Review, Order, Advertising, ConsultationRequest

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
    consultation_request_form = ConsultationRequestForm()

    return render(
        request,
        'BeautySaloon/index.html',
        context={
            'saloons': saloons,
            'services': services,
            'specialists': specialists,
            'reviews': reviews,
            'consultation_request_form': consultation_request_form
        }
    )


class ConsultationRequestView(View):
    template_name = 'BeautySaloon/index.html'

    def post(self, request):
        consultation_request_form = ConsultationRequestForm(request.POST)
        if consultation_request_form.is_valid():
            name = consultation_request_form.cleaned_data['name']
            phone_number = consultation_request_form.cleaned_data['phone_number']
            question = consultation_request_form.cleaned_data['question']
            ConsultationRequest.objects.create(name=name, phone_number=phone_number, question=question)
            return redirect('index')
        return render(request, self.template_name, {'consultation_request_form': consultation_request_form})


def advertising(request, slug):
    advertising_instance = Advertising.objects.get(slug=slug)
    advertising_instance.adv_counter += 1
    advertising_instance.save()
    return redirect('index')


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
    orders = Order.objects.prefetch_related('client', 'saloon', 'service', 'specialist').filter(client=request.user)
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
        request.session['selected_saloon'] = saloon_id
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
        return redirect('index')


def get_masters(request):
    if request.method == 'POST':
        service_id = request.POST.get('selected_service')
        request.session['selected_service'] = service_id
        specialists = [{
            'id': specialist.id,
            'name': specialist.name,
            'speciality': specialist.speciality,
            'image': request.build_absolute_uri(specialist.image.url)
        } for specialist
            in Specialist.objects.filter(
                saloon_id=request.session['selected_saloon'],
                service_category__services__id=service_id
            )
        ]

        return render(
            request,
            'BeautySaloon/select_master.html',
            context={
                'specialists': specialists
            }
        )
    else:
        return redirect('index')


def get_date(request):
    if request.method == 'POST':
        specialist_id = request.POST.get('selected_specialist')
        request.session['selected_specialist'] = specialist_id
        return render(
            request,
            'BeautySaloon/select_date.html', )
    else:
        return redirect('index')


def get_time(request):
    if request.method == 'POST':
        full_date = json.loads(request.POST.get('selected_date'))
        year = int(full_date['year'])
        month = int(full_date['month'])
        date = int(full_date['date'])

        selected_date = datetime(year, month + 1, date, tzinfo=timezone.get_current_timezone())

        request.session['selected_date'] = full_date

        specialist = Specialist.objects.get(id=request.session.get('selected_specialist'))

        start_work_time = selected_date.replace(hour=specialist.start_work_time.hour,
                                                minute=specialist.start_work_time.minute, second=0, microsecond=0,
                                                tzinfo=timezone.get_current_timezone())
        end_work_time = selected_date.replace(hour=specialist.end_work_time.hour,
                                              minute=specialist.end_work_time.minute, second=0, microsecond=0,
                                              tzinfo=timezone.get_current_timezone())

        all_time = [start_work_time + timedelta(minutes=x) for x in
                    range(0, (end_work_time - start_work_time).seconds // 60, 30)]

        busy_time = [slot.astimezone(timezone.get_current_timezone()) for slot in Order.objects.filter(
            specialist=specialist, ).values_list('appointment_time', flat=True)]
        free_time = [slot for slot in all_time if slot not in busy_time]

        morning = [slot.time() for slot in free_time if
                   start_work_time <= slot < start_work_time.replace(hour=12, minute=0)]
        day = [slot.time() for slot in free_time if
               start_work_time.replace(hour=12, minute=0) <= slot < start_work_time.replace(hour=17, minute=0)]
        evening = [slot.time() for slot in free_time if
                   start_work_time.replace(hour=17, minute=0) <= slot < end_work_time]

        return render(
            request,
            'BeautySaloon/select_time.html',
            context={
                'morning': morning,
                'day': day,
                'evening': evening,
            }
        )
    else:
        return redirect('index')


def create_order(request):
    if request.method == 'POST':
        meeting_time = json.loads(request.POST.get('selected_time'))
        selected_time = meeting_time.get('time')
        request.session['selected_time'] = selected_time
        order = Order.objects.last()
        if order:
            order_num = order.id + 1
        else:
            order_num = 1
        saloon = Saloon.objects.get(id=request.session.get('selected_saloon'))
        saloon_name = saloon.name
        saloon_address = saloon.address
        service = Service.objects.get(id=request.session.get('selected_service'))
        service_name = service.name
        service_price = service.price
        specialist = Specialist.objects.get(id=request.session.get('selected_specialist'))
        specialist_name = specialist.name
        specialist_image = request.build_absolute_uri(specialist.image.url)
        date = request.session.get('selected_date')
        year = int(date['year'])
        month = int(date['month'])
        date = int(date['date'])

        meeting_date = datetime(year, month + 1, date).date()
        time = selected_time

        order = {
            'order_num': order_num,
            'saloon_name': saloon_name,
            'saloon_address': saloon_address,
            'service_name': service_name,
            'service_price': service_price,
            'specialist_name': specialist_name,
            'specialist_image': specialist_image,
            'meeting_date': meeting_date,
            'time': time

        }
        return render(
            request,
            'BeautySaloon/serviceFinally.html',
            context=order
        )


def place_order(request):
    if request.method == 'POST':
        user_details = OrderForm(request.POST)
        if user_details.is_valid():
            user_name = request.POST.get('fname')
            user_phone_number = request.POST.get('tel')
            client, created = CustomUser.objects.get_or_create(
                phone_number=user_phone_number,
            )
            client.first_name = user_name
            client.save()
            user_question = request.POST.get('contactsTextarea')
            saloon = Saloon.objects.get(id=request.session.get('selected_saloon'))
            service = Service.objects.get(id=request.session.get('selected_service'))
            service_price = service.price
            specialist = Specialist.objects.get(id=request.session.get('selected_specialist'))
            date = request.session.get('selected_date')
            year = int(date['year'])
            month = int(date['month'])
            date = int(date['date'])
            hour, minute = request.session.get('selected_time').split(':')
            meeting_date_time = datetime(year, month + 1, date, hour=int(hour), minute=int(minute),
                                         )
            new_order = Order.objects.create(
                client=client,
                saloon=saloon,
                service=service,
                specialist=specialist,
                appointment_time=meeting_date_time,
                end_appointment_time=meeting_date_time + timedelta(minutes=30),
                price=service_price,
            )
            if user_question:
                new_order.question = user_question
                new_order.save()

    return redirect('index')
