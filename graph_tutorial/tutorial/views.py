from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from tutorial.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from tutorial.graph_helper import get_user, get_calendar_events
import dateutil

def initialize_context(request):
    context = {}
    error = request.session.pop("flash_error", None)

    if error != None:
        context["errors"] = []
        context["errors"].append(error)

    context["user"] = request.session.get("user", {"is_authenticated": False})
    return context


def home(request):
    context = initialize_context(request)

    return render(
        request,
        "tutorial/home.html",
        context
    )

def sign_in(request):
    """
    The sign in function
    """
    sign_in_url, state = get_sign_in_url()
    request.session["auth_state"] = state
    return HttpResponseRedirect(sign_in_url)


def callback(request):
    """
    Signin Callback Response
    """
    expected_state = request.session.pop("auth_state", "")
    token = get_token_from_code(request.get_full_path(), expected_state)
    user = get_user(token)
    store_token(request, token)
    store_user(request, user)    
    return HttpResponseRedirect(reverse("home"))


def sign_out(request):
    """
    Sign out user
    """
    remove_user_and_token(request)
    return HttpResponseRedirect(reverse("home"))


def calendar(request):
    """
    Get the calendat events for the user
    """
    context = initialize_context(request)
    token = get_token(request)
    events = get_calendar_events(token)

    if events:
        for event in events["value"]:
            event["start"]["datetime"] = dateutil.parser.parse(event["start"]["dateTime"])
            event["end"]["dateTime"] = dateutil.parser.parse(event["end"]["dateTime"])        
        context["events"] = events["value"]    
    
    return render(
        request, 
        "tutorial/calendar.html", 
        context
    )
