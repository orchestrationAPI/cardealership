from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
path('about/', views.about, name='about'),

    # path for contact us view
path('contact/', views.contact, name='contact'),

path('login/', views.login_req, name='login'),
path('logout/', views.logout_req, name='logout'),
path('registrate/', views.registrate_req, name='registrate'),
path('add_review/<int:dealer_id>/<str:dealer_name>/', views.add_review_view, name='add_review'),  
path('dealer_details/<int:dealer_id>/<str:dealer_name>/', views.get_dealer_details, name='dealer_details'),  
# path for registration

    # path for login

    # path for logout

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view

    # path for add a review view

]
#+ static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
print(settings.STATIC_ROOT)
