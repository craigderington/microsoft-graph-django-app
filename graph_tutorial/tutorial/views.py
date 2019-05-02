from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.


def initialize_context(request):
    context = {}
    error = request.session.pop('flash_error', None)

    if error != None:
        context['errors'] = []
        context['errors'].append(error)

    context['user'] = request.session.get('user', {'is_authenticated': False})
    return context


def home(request):
    context = initialize_context(request)

    return render(
        request,
        'tutorial/home.html',
       context
   )

