from django.shortcuts import redirect, render
from django.views import View

class inicio(View):
    def get(self, request):
        return render(request, 'inicio.html')