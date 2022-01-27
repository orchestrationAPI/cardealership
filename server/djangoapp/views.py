import os
import json
import logging
import re
from datetime import datetime
from ratelimit import limits
import requests
from .classes.cloudrequests import CloudRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from djangoapp.restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from djangobackend.settings import BASE_DIR
from .forms import LoginForm, ReviewSubmission, SignupForm
from .models import CarDealer, CarMake, CarModel
from requests.auth import HTTPBasicAuth
# Get an instance of a logger
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()
SENTIMENT_API_KEY = "PhKqzTnoHQAPNQqJIyrUWfi6GllzUoAaKg_9WLqCu12F"
# Create your views here.

# Create an `about` view to render a static about page
# defabout(request):
# ...
GET_DEALERSHIPS_URL = "https://b2c76643.us-south.apigw.appdomain.cloud/dealership/api/dealership"
REVIEW_URL = "https://b2c76643.us-south.apigw.appdomain.cloud/getreviewbydealerid/api/review"

def header_login_form(context):
        form = LoginForm()
        context["form"] = form


def about(request):
    context = {}
    header_login_form(context)
    template = "djangoapp/about.html"
    return render(request, template, context)


def contact(request):
    context = {}
    header_login_form(context)
    template = "djangoapp/contact.html"
    return render(request, template, context)


def login_req(request):
    context = {}
    login_templ = "djangoapp/login.html"

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                logger.error("User can log in!")
                login(request, user)
                return redirect("djangoapp:index")
            else:
                logger.error("User can NOT  log in!")
                messages.error(request, "Invalid username or password!")
                context["form"] = form
                return render(request, login_templ, context)
        else:
            logger.error("Invalid input!")
            messages.error(request, "Invalid user input!")
            context["form"] = form
            return render(request, login_templ, context)
    elif request.method == "GET":
        context["form"] = LoginForm()
        return render(request, login_templ, context)


def logout_req(request):
    logout(request)
    return redirect("djangoapp:index")


def registrate_req(request):
    context = {}
    registration_templ = "djangoapp/registration.html"
    if request.method == "GET":
        logger.error(BASE_DIR)
        context["form"] = SignupForm()
        return render(request, registration_templ, context)
    elif request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                logger.error("form has been valid")
                user = form.save() 
                login(request, user)
                logger.error("User is created!")
                messages.success(request, "Succsesful registration!")
                return redirect("djangoapp:index")
            except ValidationError as err:
                logger.error(form.error_message)
        else:
                context["form"] = form
                messages.error(request, "The form is invalid")
                return render(request, registration_templ, context)

@limits(calls=15, period=900)
def get_dealerships(request):
    context = {}
    template_name = "djangoapp/index.html"
    if request.method == 'GET':
        cloud_req = CloudRequest()
        with requests.Session() as session:
            respond = get_dealers_from_cf(GET_DEALERSHIPS_URL, session, cloud_req)

            if respond.get("error"):
                messages.error(request, respond["message"])
                print(respond)
                return render(request, template_name, context)

            messages.success(request, respond["message"])
            dealerships = respond["list"]
            context["dealers"] = dealerships
            header_login_form(context)
            return render(request, template_name, context)

@limits(calls=15, period=900)
def get_dealer_details(request, dealer_id, dealer_name='this dealer'):
    context = {}
    context["dealer_name"] = dealer_name
    context["dealer_id"] = dealer_id
    template_name = "djangoapp/dealer_details.html"
    if request.method == 'GET':
        cloud_req = CloudRequest()
        with requests.Session() as session:
            auth=HTTPBasicAuth('apikey', SENTIMENT_API_KEY)
            session.auth = auth
            respond = get_dealer_reviews_from_cf(REVIEW_URL, session, cloud_req, params={'dealerId':dealer_id})

            if respond.get("error"):
                if respond["error"] == "'dealerId does not exist'":
                    messages.warning(request, "Sorry, review isn't avaible about this dealer yet, please try later or add a review.")
                    return render(request, template_name, context)
                print('ERROR', )
                messages.error(request, respond["message"])
                print(respond["error"])
                return render(request, template_name, context)

            messages.success(request, respond["message"])
            header_login_form(context)
            print('++ ',respond["list"][0].review)
            context["reviews"] = respond["list"]
            return render(request, template_name, context)

@limits(calls=15, period=900)
def add_review_view(request, dealer_id, dealer_name="this dealer"):
    context = {}
    template_name = "djangoapp/add_review.html"
    redirect_template = "djangoapp:dealer_details"
    if request.method == 'GET':
        context["dealer_name"] = dealer_name
        form = ReviewSubmission(dealer_id=dealer_id)
        print("++++",form.fields["car_description"].choices)
        context["form"] = form
        return render(request, template_name, context)
        
    elif request.method == 'POST':
        if request.user.is_authenticated:
            cloud_req = CloudRequest()
            form = ReviewSubmission(request.POST, dealer_id=dealer_id)
            if form.is_valid():
                print("The form was valid")
                with requests.Session() as session:
                        respond = form.save(session, cloud_req)
                        print(respond)
                        if respond.get("error"):
                            messages.error(request, respond["message"])
                            print(respond["error"])
                            return redirect(redirect_template, dealer_id=dealer_id, dealer_name=dealer_name)

                        #messages.success(request, respond["message"])

            else:
                context["form"] = form
                messages.error(request, "The form is invalid")
        else:
            messages.error(request,"Please, login to send your review.")
        return redirect(redirect_template, dealer_id=dealer_id, dealer_name=dealer_name)

#CarMake.objects.bulk_create([
#    CarMake(name="BMW", description="reliable brand"),
#    CarMake(name="Bugatti", description="reliable brand"),
#    CarMake(name="Ferrari", description="reliable brand"),
#    CarMake(name="Jaguar", description="reliable brand"),
#    CarMake(name="Mercedes-Benz", description="reliable brand"),
#    CarMake(name="Lamborghini", description="reliable brand"),
#    CarMake(name="Pagani", description="reliable brand"),
#    CarMake(name="Porche", description="reliable brand"),
#    CarMake(name="Fiat", description="reliable brand"),
#    CarMake(name="Lancia", description="reliable brand"),
#    CarMake(name="Dacia", description="reliable brand"),
#    CarMake(name="Fiat", description="reliable brand"),
#    CarMake(name="Nissan", description="reliable brand"),
#    CarMake(name="Opel", description="reliable brand"),
#    CarMake(name="Ford", description="reliable brand"),
#    CarMake(name="Volkswagen", description="reliable brand"),
#    CarMake(name="Volvo", description="reliable brand"),
#
#    ])
#def get_dealerships(request):
#    context = {}
#    if request.method == "GET":
#        header_login_form(context)
#        return render(request, "djangoapp/index.html", context)
#  Create a `contact` view to return a static contact page



# def contact(request):

# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list
# of dealerships




# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
