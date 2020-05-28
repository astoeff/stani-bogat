from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/questions/', views.QuestionDetailView.as_view(), name='q_detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    
    # path('', views.home, name='home'),
    # path('<int:category_price/', views.QuestionsView.as_view(), name='questions')
]
