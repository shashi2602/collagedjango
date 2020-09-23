from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,ListView,UpdateView,DeleteView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.admin import User
from .models import Notes,Faculty,Dept,Subjects,Student,Questions,Answers,Assignment,SubmitAssignment
from .forms import Notesform
from .filters import Showassignmentsfilter
from django.contrib.messages.views import SuccessMessageMixin

def home(request):
    context={
        "depts":Dept.objects.all()
    }
    return render(request,"home.html",context)


class NoteCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model=Notes
    template_name="base/faculty_notes_form.html"
    fields= ["Subject","year","sem","dept","chapter_name","topic_name","video_clip_url","PDF_url","notes"]
    success_url='/dashboard'
    success_message="Note Created success"
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super(NoteCreateView,self).form_valid(form)


def groupcource(request,group_name,subject_name):
    dept=get_object_or_404(Dept,shortname=group_name)
    subjects=get_object_or_404(Subjects,short_name=subject_name)
    sub=Notes.objects.filter(dept=dept,Subject=subjects)
    context={
        "subs":sub,
        "dept":group_name,
        "subject":subject_name
    }
    return render(request,"base/subject_details.html",context)

def get_dept_subjects(request,dept_name):
    subs=Subjects.objects.filter(dept__shortname=dept_name)
    context={
        "subjects":subs,
        "dept":dept_name
    }
    return render(request,"base/subjects.html",context)

def topic_detail(request,dep_name,sub_name,ch_name,tp_name):
    depts=get_object_or_404(Dept,shortname=dep_name)
    subjects=get_object_or_404(Subjects,short_name=sub_name)
    topic=Notes.objects.filter(slug_c=ch_name,slug_t=tp_name,Subject=subjects,dept=depts)
    context={
        "details":topic,
        "dept":dep_name,
        "sub":sub_name,
        "ch":ch_name,
        "tp":tp_name
    }
    return render(request,"base/dept_subjects_chapter_details.html",context)


class FacultyNoteListView(TemplateView):
    # model = Notes
    template_name = 'home_login.html' 
     # <app>/<model>_<viewtype>.html
    # context_object_name = 'notes'
    def get_context_data(self,**kwargs):
        context=super(FacultyNoteListView,self).get_context_data(**kwargs)
        user = get_object_or_404(User,username=self.request.user)
        context['notes']=Notes.objects.filter(author=user).order_by('-date')[0:10]
        context['depts']=Dept.objects.all()
        context['students']=Student.objects.all()
        context['subjects']=Subjects.objects.all()
        context['allnotes']=Notes.objects.all().order_by("-date")[0:10]
        return context
    # def get_queryset(self):
    #     user = get_object_or_404(User,username=self.request.user)
    #     return Notes.objects.filter(author=user)


@login_required(login_url="/")
def noteupdate(request,note_id):
    note=get_object_or_404(Notes,id=note_id)
    form=Notesform(instance=note)

    if request.method=='POST':
        form=Notesform(request.POST,request.FILES,instance=note)
        if form.is_valid():
            form.save()
        return redirect("/")

    context={
        "form":form
    }
    return render(request,"base/faculty_note_update.html",context)


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    model=Notes
    success_url='/dashboard'
    success_message="Deleted successfully"
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        else :
            return False


class CreateQuestion(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model=Questions
    template_name="base/faculty_question.html"
    fields=['question','year','subject','dept']
    success_url="/dashboard"
    success_message="created successfully"

    def form_valid(self,form):
        form.instance.question_by=self.request.user
        return super(CreateQuestion,self).form_valid(form)


class QuestionDeleteView(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model=Questions
    success_url='/questions'
    success_message="Deleted successfully"

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        else :
            return False

def AllQuestions(request):
    context={
        'qus':Questions.objects.all()
    }
    return render(request,'base/faculty_allquestions.html',context)

@login_required(redirect_field_name="/")
def getQA(request,questionans):
    qns=get_object_or_404(Questions,slug_q=questionans)
    answers=Answers.objects.filter(question=qns)
    context={
        "ans":answers,
        "qns":qns,
    }
    return render(request,"base/faculty_qns.html",context)


class StudentAllQuestions(LoginRequiredMixin,TemplateView):
    template_name="base/student_allquestions.html"
    def get_context_data(self,**kwargs):
        context=super(StudentAllQuestions,self).get_context_data(**kwargs)
        user = get_object_or_404(User,username=self.request.user)
        context['ans']=Answers.objects.filter(answer_by=user)
        context['questions']=Questions.objects.all()
        return context


class studentQuestionanswer(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model=Answers
    template_name="base/student_write_answer.html"
    fields=['question','answer']
    success_url="/dashboard"
    success_message="Aswered succesfully"

    def form_valid(self,form):
        form.instance.answer_by=self.request.user
        return super(studentQuestionanswer,self).form_valid(form)

class StudentAllAnswered(LoginRequiredMixin,TemplateView):
    template_name="base/student_answered.html"
    def get_context_data(self,**kwargs):
        context=super(StudentAllAnswered,self).get_context_data(**kwargs)
        user = get_object_or_404(User,username=self.request.user)
        context['ans']=Answers.objects.filter(answer_by=user)
        context['questions']=Questions.objects.all()
        return context

def ShowStudentAnswers(request,question_slug):
    context={
        "answers":Answers.objects.filter(question__slug_q=question_slug)
    }
    return render(request,"base/student_question_answers.html",context)


class assignmentquestions(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model=Assignment
    template_name="base/createassignment.html"
    fields=['title','questions','year','dept','subject']
    success_url="/dashboard"
    success_message="Created success"

    def form_valid(self,form):
        form.instance.by=self.request.user
        return super(assignmentquestions,self).form_valid(form)

class assignmentsview(LoginRequiredMixin,TemplateView):
    template_name="base/student_assignment_questions.html"
    def get_context_data(self,**kwargs):
        context=super(assignmentsview,self).get_context_data(**kwargs)
        user = get_object_or_404(User,username=self.request.user)
        context['ans']=SubmitAssignment.objects.filter(submit_by=user)
        context['assignquestions']=Assignment.objects.all()
        return context

class SubmitAssignmentView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model=SubmitAssignment
    template_name="base/studentsubmitassignment.html"
    fields=['assignment','Link']
    success_url="/dashboard"
    success_message="submitted "

    def form_valid(self,form):
        form.instance.submit_by=self.request.user
        return super(SubmitAssignmentView,self).form_valid(form)

@login_required()
def ShowSubmitAssignments(request):
    data=SubmitAssignment.objects.all()
    myfilters=Showassignmentsfilter(request.GET, queryset=data)
    data=myfilters.qs
    context={
        'assignments':data,
        "filter":myfilters
    }
    return render(request,'base/faculty_Assignments.html',context=context)
    # template_name="base/faculty_Assignments.html"
    # def get_context_data(self,**kwargs):
    #     context=super(ShowSubmitAssignments,self).get_context_data(**kwargs)
    #     user = get_object_or_404(User,username=self.request.user)
    #     context['assignments']=ShowSubmitAssignments
    #     context['myfilter']=showassignmentsfilter(request.GET, queryset='assignments')
    #     return context
