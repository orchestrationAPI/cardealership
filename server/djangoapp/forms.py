import os
from datetime import datetime
import re
import json
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import  CarModel
import requests
from .classes.cloudrequests import CloudRequest
from .restapis import add_review 
from dotenv import load_dotenv
load_dotenv()
#REVIEW_URL = os.environ.get("REVIEW_URL")
REVIEW_URL = "https://b2c76643.us-south.apigw.appdomain.cloud/getreviewbydealerid/api/review"

class SignupForm(forms.Form):
    error_message = {
        "username_duplication": "The username already exists!",
        "short_password": "The pasword should contain at least 9 character!",
        "wrong_password_format_missing_number": "The password should contain at least one number!",
        "wrong_password_format_missing_letter": "The password should contain at least one nonnumeric character!",
    }

    username = forms.CharField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        ),
    )
    first_name = forms.CharField(
        label="First name",
        max_length=60,
        widget=forms.TextInput(
            attrs={"placeholder": "First name", "class": "form-control"}
        ),
    )
    last_name = forms.CharField(
        label="Last name",
        max_length=60,
        widget=forms.TextInput(
            attrs={"placeholder": "Last name", "class": "form-control"}
        ),
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}))

    def clean_username(self):
        username = self.cleaned_data["username"]
        res = User.objects.filter(username=username)
        if res.count():
            raise ValidationError(self.error_message["username_duplication"])
        return username

    def clean_password(self):
        password = self.cleaned_data["password"]
        re_patt_number = r"\d+"
        re_patt_letter = r"[a-zA-Z]+"

        if len(password) < 9:
            # logger.error('short password')
            raise ValidationError(self.error_message["short_password"])
        if not re.findall(re_patt_number, password):
            raise ValidationError(
                self.error_message["wrong_password_format_missing_number"]
            )
        if not re.findall(re_patt_letter, password):
            raise ValidationError(
                self.error_message["wrong_password_format_missing_letter"]
            )
        # logger.error('Good password')
        return password

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            password=self.cleaned_data["password"],
        )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Your password", "class": "form-control"}),
    )
def get_CarModel_list_by_dealer_id(dealer_id):
    car_set = CarModel.objects.filter(dealer_id=dealer_id)
    car_detail_list =[("default" , "Model-Make-Year")]
    if car_set.exists() is False:
        print("Does not exist")
        tp = ("N/A","N/A")
        car_detail_list.append(tp)
        return car_detail_list
    for car in car_set:
        print(car.carMake)
    for i in range(len(car_set)):
        tp = (i, "-".join([str(car_set[i].name), str(car_set[i].carMake), str(car_set[i].year)]))
        car_detail_list.append(tp)
    return car_detail_list 

class ReviewSubmission(forms.Form):

    def __init__(self, *args, dealer_id, **kwargs):
        self.dealer_id = dealer_id
        super().__init__(*args, **kwargs)
        self.fields["car_description"].choices = get_CarModel_list_by_dealer_id(self.dealer_id) 

    review =forms.CharField(
        label="Review",
        max_length= 600,
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "Your review", "class": "form-control"}
        ),
    )

    purchase = forms.BooleanField(
            required = False,
            label="Has been purchased the car from this dealership? (select purchased car information if checked)",
            widget=forms.CheckboxInput(
                attrs={"class": "form-check-input mx-2 "}
                ),
            )
    car_description = forms.ChoiceField(
            required = False,
            choices = [],
            label = "Select your car:",
            widget = forms.Select(
                attrs={"class": "form-select mx-3",
                    "disabled":"disabled"}
                )
            )

    purchase_date = forms.DateField(
            required = False,
            label = "Purchase date",
            widget = forms.DateInput(
                attrs = {"class":"date-own form-control",
                    "autocomplete":"off",
                    "disabled":"disabled"
                    }

                )
            )

    def save(self, session_object, cloud_request_instance):
        purchase_date = None
        model = None
        make = None
        year = None
        if self.cleaned_data["purchase"] == True:
            purchase_date = self.cleaned_data["purchase_date"]
            if ((self.cleaned_data["car_description"] == "default") or
                 (self.cleaned_data["car_description"] == "N/A") or   (not self.cleaned_data["car_description"])):
                model = None
                make = None
                year = None
            else:
                print("+++",self.cleaned_data["car_description"])
                choice_number = int(self.cleaned_data["car_description"])
                choiced_value = self.fields["car_description"].choices[choice_number]
                sp_ls = choiced_value[1].split("-")
                model = sp_ls[0]
                make = sp_ls[1]
                year = sp_ls[2]
        else:
            purchase_date = None
            model = None
            make = None
            year = None
        
        params = {
                "dealership" : int(self.dealer_id),
                "review" : self.cleaned_data["review"],
                "review_date" : datetime.utcnow().isoformat(),
                "purchase" : self.cleaned_data["purchase"],
                "purchase_date" : purchase_date,
                "car_make" : make, 
                "car_model" : model,
                "car_year" : year,
                }
        print(params["dealership"])
        print(params["car_make"])
        print(params["car_model"])
        print(params["car_year"])
        print(params["review"])
        print(params["review_date"])
        print(params["purchase"])
        print(params["purchase_date"])
        respond = add_review(REVIEW_URL, session_object, cloud_request_instance, params=params)
        return respond

