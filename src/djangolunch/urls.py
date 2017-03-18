"""djangolunch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
import debug_toolbar

from users.views import UserAccountViewSet
from orders.views import OrderGroupViewSet, OrderViewSet
from restaurants.views import (
    RestaurantViewSet,
    MenuItemListViewSet,
    MenuItemBesidesListViewSet,
    MenuItemUpdateByRestaurantView,
)
from polls.views import (
    QuestionViewSet,
    ChoiceListViewSet,
    ChoiceBesidesListViewSet,
)
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='LunchBar API')

root_router = DefaultRouter()

# /account/:username
root_router.register(r'account', UserAccountViewSet)

# api root
root_router.register(r'orders', OrderViewSet)
root_router.register(r'groups', OrderGroupViewSet)
root_router.register(r'restaurants', RestaurantViewSet)
root_router.register(r'menuitems', MenuItemBesidesListViewSet)
root_router.register(r'questions', QuestionViewSet)
root_router.register(r'choices', ChoiceBesidesListViewSet)

# /restaurants/:restaurant_id/menuitems
restaurants_router = routers.NestedSimpleRouter(root_router, r'restaurants', lookup='restaurant')
restaurants_router.register(r'menuitems', MenuItemListViewSet)

# /questions/:question_id/choices
questions_router = routers.NestedSimpleRouter(root_router, r'questions', lookup='question')
questions_router.register(r'choices', ChoiceListViewSet)

# minor feature for convenience
urlpatterns = [
    url(r'^menuitems/price/$', MenuItemUpdateByRestaurantView.as_view()),
]

# implicitly route by ModelViewset
urlpatterns += [
    url(r'^', include(root_router.urls)),
    url(r'^', include(restaurants_router.urls)),
    url(r'^', include(questions_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^api/$', schema_view)
    # url(r'^admin/', admin.site.urls),
]
