from django.urls import path
from . import views

app_name = "review"

urlpatterns = [
    path("create/<int:order_id>/", views.review_create, name="create"),
    path("share/<int:review_id>/", views.review_share, name="share"),          # 生成链接
    path("share/<str:token>/", views.review_share_page, name="share_page"),   # 打开链接
    path("report/<int:review_id>/", views.review_report, name="report"),
    path("edit/<int:review_id>/", views.review_edit, name="edit"),
    path("delete/<int:review_id>/", views.review_delete, name="delete"),
    path("score/<int:review_id>/", views.review_score, name="score"),
    path("list/", views.review_list, name="list"),
    path("search/", views.review_search, name="search"),
]