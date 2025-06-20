from django.shortcuts import render

from Pages.models import GemtenPage

def testing():
    pages = GemtenPage.objects.all()
    print('&&&'*30)
    print(pages)
    print()
    return True
