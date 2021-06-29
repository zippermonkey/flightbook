from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('buy/<int:cid>/<int:fid>/', views.buy, name="buy"),
    path('orders/<int:cid>', views.orders, name='orders'),
    path('cancel/<int:cid>/<int:oid>', views.cancel, name='cancel'),
    path('pay/<int:cid>/<int:oid>', views.pay, name='pay'),
    path('collectticket/<int:cid>/<int:oid>', views.collectticket, name='collectticket'),
    path('tickets/<int:cid>', views.tickets, name='tickets'),
    path('error', views.error, name='error'),
    path('manage', views.manage, name='manage'),
    path('manage/flight',views.manageflight,name='manageflight'),
    path('manage/deleteflight/<int:fid>',views.deleteflight,name='deleteflight'),
    path('manage/modifyflight/<int:fid>', views.modifyflight, name='modifyflight'),
    path('manage/checkorders',views.checkorders,name = 'checkorders')

]
