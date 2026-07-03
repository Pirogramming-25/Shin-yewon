from django.urls import path
from . import views

app_name = "ideas"

urlpatterns = [
    path("", views.idea_list, name="idea_list"),
    path("ideas/create/", views.idea_create, name="idea_create"),
    path("ideas/<int:idea_id>/", views.idea_detail, name="idea_detail"),
    path("ideas/<int:idea_id>/update/", views.idea_update, name="idea_update"),
    path("ideas/<int:idea_id>/delete/", views.idea_delete, name="idea_delete"),
    path("ideas/<int:idea_id>/interest/<str:direction>/", views.idea_interest, name="idea_interest"),
    path("ideas/<int:idea_id>/star/", views.idea_star_toggle, name="idea_star_toggle"),

    path("devtools/", views.devtool_list, name="devtool_list"),
    path("devtools/create/", views.devtool_create, name="devtool_create"),
    path("devtools/<int:devtool_id>/", views.devtool_detail, name="devtool_detail"),
    path("devtools/<int:devtool_id>/update/", views.devtool_update, name="devtool_update"),
    path("devtools/<int:devtool_id>/delete/", views.devtool_delete, name="devtool_delete"),
]