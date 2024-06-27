from django.urls import path,include
from .views import *

urlpatterns = [
    path('', index, name='homepage'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add_transaction/', add_transaction, name='add_transaction'),
    path('add_income/', add_income, name='add_income'),
    path('chart/', chart_view, name='chart'),
    path('chart/data/', chart_data, name='chart_data'),
   path('delete/<int:item_id>/<str:item_type>/',delete_item, name='delete_item'),
]
