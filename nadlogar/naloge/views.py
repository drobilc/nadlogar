from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
import uuid

from .models import Test, Naloga
from .generatorji.latex_generator import LatexGenerator

def index(request):
    seznam_testov = Test.objects.all()
    return render(request, 'testi/seznam_testov.html', {'seznam_testov': seznam_testov})

def podrobnosti(request, pk: int):
    test: Test = get_object_or_404(Test, pk=pk)
    return render(request, 'testi/test.html', {'test': test, 'naloge': test.naloge.all()})

def test_pdf(request, pk: int):
    test: Test = get_object_or_404(Test, pk=pk)

    random_name = uuid.uuid4()

    dokument = LatexGenerator.generate_latex(test)
    dokument.generate_pdf(settings.MEDIA_ROOT + str(random_name), clean=True, clean_tex=True)

    return redirect(settings.MEDIA_URL + str(random_name) + '.pdf')