from django.shortcuts import render
from django.http import HttpResponse

from ...nlp.Stanley import Stanley as Director

def screenwrite(request):
    genres = ['western']
    characters = ['bob', 'bobby', 'bobra', 'bobert']
    source = '../../nlp/markov_models'    
    director = Director(genres, characters, source)
    director.direct()
    return HttpResponse('ok')
