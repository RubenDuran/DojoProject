from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.main),
    url(r'^main$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^add_wish/(?P<id>\d+)$', views.add_wish),
    url(r'^add$', views.add),
    url(r'^wish_items/create$', views.create),
    url(r'^wish_items/(?P<id>\d+)$', views.item),
]
