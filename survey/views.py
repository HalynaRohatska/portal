from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Survey, Question, Choice, Answer

class SurveyListView(LoginRequiredMixin, ListView):
    model = Survey
    template_name = 'survey_list.html'
    context_object_name = 'surveys'
    queryset = Survey.objects.filter(is_active=True)

class SurveyTakeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk)
        questions = survey.questions.all() # type: ignore
        
        session_key = f'survey_{pk}_progress'
        current_q_index = request.session.get(session_key, 0)
        
        if current_q_index >= questions.count():
            request.session[session_key] = 0
            return redirect('survey:results', pk=pk)
            
        question = questions[current_q_index]
        return render(request, 'take_survey.html', {'survey': survey, 'question': question})

    def post(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk)
        questions = survey.questions.all() # type: ignore
        
        session_key = f'survey_{pk}_progress'
        current_q_index = request.session.get(session_key, 0)
        
        if current_q_index < questions.count():
            question = questions[current_q_index]
            choice_id = request.POST.get('choice')
            
            if choice_id:
                choice = get_object_or_404(Choice, pk=choice_id)
                Answer.objects.update_or_create(
                    user=request.user,
                    question=question,
                    survey=survey,
                    defaults={'choice': choice}
                )
                request.session[session_key] = current_q_index + 1
                
        return redirect('survey:take', pk=pk)

class SurveyResultView(LoginRequiredMixin, View):
    def get(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk)
        return render(request, 'results.html', {'survey': survey})