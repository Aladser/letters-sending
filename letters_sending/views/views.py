from django.db.models import Count
from django.views.generic import ListView
from letters_sending.models import Attempt, LettersSending


class AttemptListView(ListView):
    """LIST"""

    model = Attempt
    template_name = "attempt_list.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.order_by('letters_sending').values('letters_sending', 'response').annotate(count=Count('id'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['header'] = "статистика отправки"

        for attempt in context['object_list']:
            sending = LettersSending.objects.get(pk=attempt['letters_sending'])
            attempt['message'] = sending.message
            attempt['status'] = sending.status

        return context
