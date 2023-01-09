import json

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from vacancies.models import Vacancy


def hello(request):
    return HttpResponse("Hello WORLD")


@method_decorator(csrf_exempt, name="dispatch")
class VacancyView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()

        search_text = request.GET.get("text", None)
        if search_text:
            vacancies = vacancies.filter(text=search_text)

        response = []
        for vacancy in vacancies:
            response.append({
                "id": vacancy.id,
                "text": vacancy.text,
            })

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        vacancy_data = json.loads(request.body)

        vacancy = Vacancy()
        vacancy.text = vacancy_data["text"]

        vacancy.save()
        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text
        }, safe=False, json_dumps_params={'ensure_ascii': False}
        )


class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        # try:
        #     vacancy = Vacancy.objects.get(pk=vacancy_id)
        # except Vacancy.DoesNotExist:
        #     return JsonResponse({"error": "VACANCY NOT FOUND"}, status=404)
        vacancy = self.get_object()

        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text})
