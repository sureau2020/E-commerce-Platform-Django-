from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("BID", views.BID, name="BID"),
    path("categories", views.categories_view, name="categories"),
    path("watchinglist", views.watchinglist_view, name="watchinglist"),
    path("createitme", views.createitme, name="createitme"),
    path("<int:auction_id>",views.auction_view, name="auction"),
    path("comment",views.comment, name="comment"),
    path("auction_close/<int:auction_id>",views.auction_close, name="auction_close"),
    path("watchlist_remove/<int:auction_id>",views.watchlist_remove, name="watchlist_remove"),
    path("watchlist_add/<int:auction_id>",views.watchlist_add, name="watchlist_add"),
    path("<str:category_name>",views.category, name="category"),



]
