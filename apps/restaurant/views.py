from django.core import serializers
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from django.http import JsonResponse

from .forms import OrderForm
from .models import Hall, Table
from .tasks import send_comment_notification


class HallList(ListView):
    model = Hall
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HallList, self).get_context_data(**kwargs)
        context['halls'] = Hall.objects.all()
        return context


class HallDetail(DetailView):
    model = Hall
    slug_field = 'hall_slug'
    slug_url_kwarg = 'hall_slug'
    template_name = 'hall.html'

    def get_context_data(self, **kwargs):
        context = super(HallDetail, self).get_context_data(**kwargs)
        context['form'] = OrderForm(initial={'hall': self.object.pk, 'table': self.object.pk})
        context['tables'] = Table.objects.filter(hall=self.object.pk)
        return context


def check_free_table(request):
    if request.is_ajax and request.method == 'GET':
        date = request.GET.get('date')
        tab = Table.objects.filter(order_table__date=date)
        ser_instance = serializers.serialize('json', tab)
        return JsonResponse({'tables': ser_instance}, status=200, safe=False)
    else:
        return JsonResponse({'errors': ""}, status=400)


def reserve_table(request):
    if request.is_ajax and request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [instance, ])

            mail_subject = "Спасибо за заказ!"
            message = render_to_string('new_order_table.txt', {
                'hall': instance.hall.name,
                'table_number': instance.table.number,
                'date_order': instance.date
            })
            to_email = form.cleaned_data.get('email')
            send_comment_notification.delay(mail_subject, message, to_email)

            return JsonResponse({'instance': ser_instance}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": ""}, status=400)
