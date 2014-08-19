from django.conf.urls import patterns
from .views import page1, MyView, MyView2

# special urls for flatpage test cases
urlpatterns = patterns('',
    (r'^page1/$', page1),
    (r'^page2/$', MyView.as_view()),
    (r'^(?P<pk>\d+)/$', MyView2.as_view()),
)

