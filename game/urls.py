from django.conf.urls import url
from main import views
urlpatterns = [
	url(r'^$',views.index,name='index'),

	url(r'^answer/',views.checkAnswer,name='checkAnswer')
	


]
