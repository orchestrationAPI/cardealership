from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date 

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
def current_year():
    return date.today().year

def validate_max_year(value):
    return MaxValueValidator(current_year())(value)
    
def validate_min_year(value):
    return MinValueValidator(1900)(value)
    
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=500)
    description =  models.CharField(null=False, max_length=500)
    
    def __str__(self) -> str:
        return self.name 

class CarModel(models.Model):
    CAR_TYPE =[
            ('SV','SUV'),
            ('TR', 'Truck'),
            ('SD', 'Sedan'),
            ('VN', 'Van'),
            ('CP', 'Coupe'),
            ('WA', 'Wagon'),
            ('CVT', 'Convertible'),
            ('SPC', 'Sport Car'),
            ('CO', 'Crossover'),
            ('LUX', 'Luxury Car'),
            ('HE', 'Hibrid/Electric'),
            ('Mu', 'Muscle')
            ]
    carMake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=500)
    car_type = models.CharField(null=False, max_length=300, choices=CAR_TYPE)
    year = models.PositiveIntegerField(default=current_year(), validators=[validate_min_year,validate_max_year]) 

    def __str__(self) -> str:
        return self.name + ' - '  + self.carMake.name

class CarDealer:
    def __init__(self, id, city, state, st, address, adr_zip, lat, long, short_name, full_name):
        self.id = id
        self.city = city
        self.state = state
        self.st = st
        self.address = address
        self.adr_zip = adr_zip
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.full_name = full_name

    def __str__(self) -> str:
        return 'Name: ' + self.full_name 


class DealerReview:
    def __init__(self, dealership, name, purchase, review_date, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.review_date = review_date
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
    def __str__(self) -> str:
        return 'dealership:' + self.dealership
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
