from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/questions/', views.QuestionDetailView.as_view(), name='q_detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('random/<int:category_id>', views.choose_random, name='random'),
    path('<int:question_id>/<int:choice_id>/results/', views.result, name='results'),
    path('game/', views.game, name='game'),
    path('game/vote/<int:question_id>/', views.game_vote, name='game_vote'),
    path('game/take-money', views.take_money, name='take_money')


    # path('', views.home, name='home'),
    # path('<int:category_price/', views.QuestionsView.as_view(), name='questions')
]
