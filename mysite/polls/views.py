from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question, Category, Episode
from django.db.models import Q
import random
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.paginator import Paginator


def index(request):
    return render(request, 'polls/index.html')


class ListCategories(generic.ListView):
    # template_name = 'polls/index.html'
    # context_object_name = 'latest_question_list'

    # def get_queryset(self):
    #     """
    #     Return the last five published questions (not including those set to be
    #     published in the future).
    #     """
    #     return Question.objects.filter(
    #         pub_date__lte=timezone.now()
    #     ).order_by('-pub_date')[:5]

    template_name = 'polls/list_categories.html'
    context_object_name = 'categories_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Category.objects.all().order_by('price')


class ListEpisodes(generic.ListView):
    model = Episode
    template_name = 'polls/list_episodes.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'episodes'  # Default: object_list
    paginate_by = 3
    queryset = Episode.objects.all()  # Default: Model.objects.all()


def list_episodes(request):
    episodes = Episode.objects.all().order_by('number')
    return render(request, 'polls/list_episodes.html', {'episodes_list': episodes})
# class ListEpisodes(generic.ListView):
#     # template_name = 'polls/index.html'
#     # context_object_name = 'latest_question_list'

#     # def get_queryset(self):
#     #     """
#     #     Return the last five published questions (not including those set to be
#     #     published in the future).
#     #     """
#     #     return Question.objects.filter(
#     #         pub_date__lte=timezone.now()
#     #     ).order_by('-pub_date')[:5]

#     template_name = 'polls/list_episodes.html'
#     context_object_name = 'episodes_list'

#     def get_queryset(self):
#         """
#         Return the last five published questions (not including those set to be
#         published in the future).
#         """
#         return Episode.objects.all().order_by('number')


# class QuestionsView(generic.ListView):
#     model = Category
#     template_name = 'polls/questions.html'
#     # context_object_name = 'latest_question_list'

#     # def get_queryset(self):
#     #     """
#     #     Return the last five published questions (not including those set to be
#     #     published in the future).
#     #     """
#     #     return Category.objects.all()


class DetailView(generic.DetailView):
    model = Category
    template_name = 'polls/detail.html'

    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet.
    #     """
    #     items = Question.objects.all()
    #     random_item = random.choice(items)
    #     return random_item
    #     # return render(request, 'polls/detail.html', {
    #     #     'question': question,
    #     #     'error_message': "You didn't select a choice.",
    #     # })


class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = 'polls/q_detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/q_detail.html', {
            'question': question,
            'error_message': "Моля, изберете отговор!",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # return HttpResponseRedirect(reverse('polls:results', args=(question.id, selected_choice.id)))
        return render(request, 'polls/results.html', {'question': question, 'choice': selected_choice})


def choose_random_question_in_category(category_id):
    category = Category.objects.all().filter(pk=category_id)[0]
    question = random.choice(category.question_set.all())
    return question


def choose_random(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    try:
        if 'question' in request.POST.keys():
            selected_choice = random.choice(category.question_set.all().filter(~Q(id=request.POST['question'])))
        else:
            selected_choice = random.choice(category.question_set.all())
    except (KeyError, Category.DoesNotExist):
        return render(request, 'polls/index.html', {})
        # pass
    else:
        return HttpResponseRedirect(reverse('polls:q_detail', args=(selected_choice.id,)))


def result(request, question_id, choice_id):
    question = get_object_or_404(Question, pk=question_id)
    choice = get_object_or_404(Choice, pk=choice_id)
    return render(request, 'polls/results', {'question': question, 'choice': choice})


def get_all_categories_sorted_by_price():
    return Category.objects.all().order_by('price')


# def game(request):
#     price = int(request.POST['category_price'])
#     category = Category.objects.all().filter(price=price)[0]
#     return HttpResponseRedirect(reverse('polls:random', args=(category.id,)))

def game(request):
    # money_if_game_lost = '1000'
    position = int(request.POST['category_position'])
    if position == 15:
        return render(request, 'polls/congratulations.html', {})
    category = get_all_categories_sorted_by_price()[position]
    question = choose_random_question_in_category(category.id)
    return render(request, 'polls/process_question.html', {'question': question, 'price': category,
                'position': position + 1})


def game_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    position = request.POST['position']
    print(position)
    # return 0
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/process_question.html', {
            'question': question,
            'price': question.category.price,
            'position': position,
            'error_message': "Моля, изберете отговор!",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # return HttpResponseRedirect(reverse('polls:results', args=(question.id, selected_choice.id)))
        return render(request, 'polls/game_results.html', {'question': question, 'choice': selected_choice, 'position': position})

def take_money(request):
    categories = get_all_categories_sorted_by_price()
    category = Category.objects.all().filter(price=request.POST['price'])[0]
    index = (*categories,).index(category)
    if index == 0:
        price_won = 0
    else:
        price_won = categories[index - 1]
    return render(request, 'polls/take_money.html', {'price': price_won})

# def home(request):
#     # question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     # except (KeyError, Choice.DoesNotExist):
#     #     # Redisplay the question voting form.
#     #     return render(request, 'polls/detail.html', {
#     #         'question': question,
#     #         'error_message': "You didn't select a choice.",
#     #     })
#     # else:
#     #     selected_choice.votes += 1
#     #     selected_choice.save()
#     #     # Always return an HttpResponseRedirect after successfully dealing
#     #     # with POST data. This prevents data from being posted twice if a
#     #     # user hits the Back button.
#     return HttpResponseRedirect(reverse('polls:index'))
