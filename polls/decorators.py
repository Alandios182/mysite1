from django.http import HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
from functools import wraps
from .models import QuestionUser
from django.core.cache import cache

def Timer(max_votes, minutes):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            cache_key = f'user_last_vote_{user.id}'

            # Verifica si el usuario ha votado en alguna pregunta en los últimos 'minutes' minutos
            last_votes = QuestionUser.objects.filter(user=user, fecha__gte=timezone.now() - timezone.timedelta(minutes=minutes))

            if last_votes.count() >= max_votes:
                # Agrega un enlace para volver al índice
                index_url = reverse("index")
                error_message = f"Ya haz votado en una pregunta {max_votes} vez, espera {minutes} minutos. <a href='{index_url}'>Volver al índice</a>"
                return HttpResponseForbidden(error_message)

            # Registra el momento del voto actual en la caché
            cache.set(cache_key, timezone.now(), 300)  # 300 segundos = 5 minutos

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator