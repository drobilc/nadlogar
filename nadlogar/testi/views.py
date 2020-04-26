from django.shortcuts import get_object_or_404, render

from .models import Test

def index(request):
    seznam_testov = Test.objects.all()
    return render(request, 'testi/seznam_testov.html', {'seznam_testov': seznam_testov})

def podrobnosti(request, pk: int):
    test: Test = get_object_or_404(Test, pk=pk)
    return render(request, 'testi/test.html', {'test': test, 'naloge': test.naloge.all()})
