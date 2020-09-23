from django.urls import path
from .views import *

urlpatterns=[
    path("",home,name="home"),
    path("dashboard",FacultyNoteListView.as_view(),name="dashboard"),
    path("createquestion",CreateQuestion.as_view(),name="createquestion"),
    path("questions",AllQuestions,name="questions"),
    path("questions/student",StudentAllQuestions.as_view(),name="studentquestions"),
    path("questions/student/answer",studentQuestionanswer.as_view(),name="studentanswer"),
    path("questions/student/answered",StudentAllAnswered.as_view(),name="studentanswered"),
    path("questions/student/answer/<slug:question_slug>",ShowStudentAnswers,name="showanswer"),
    path("questions/<slug:questionans>",getQA),
    path("faculty/note/create",NoteCreateView.as_view(),name="notecreate"),
    path("faculty/note/createassignment",assignmentquestions.as_view(),name="createassignment"),
    path("student/assignments",assignmentsview.as_view(),name="allassignments"),
    path("student/assignments/submitassignment",SubmitAssignmentView.as_view(),name="submitassignment"),
    path("faculty/assignments",ShowSubmitAssignments,name="facultyassignments"),
    path("<slug:dept_name>",get_dept_subjects,name="subjects"),
    path("subject/<slug:group_name>/<slug:subject_name>",groupcource,name="groupsubjects"),
    path("<slug:dep_name>/<slug:sub_name>/<slug:ch_name>/<slug:tp_name>",topic_detail,name="topicdetails"),
    path("faculty/notes/<slug:note_id>/update/",noteupdate,name="facultynoteupdate"),
    path("notes/<int:pk>/delete/",PostDeleteView.as_view(),name="notes-delete"),
    path("questions/<int:pk>/delete",QuestionDeleteView.as_view(),name="deletequestion")
    
    
]