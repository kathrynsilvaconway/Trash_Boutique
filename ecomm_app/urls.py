from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.render_login),
    path('register', views.render_register),
    path('process_reg', views.process_reg),
    path('process_login', views.process_login),
    path('logout', views.logout),
    path('3227751215', views.render_admin),
    path('create_item', views.create_item),
    path('create_cat', views.create_cat),
    path('show_empty_cart', views.show_empty_cart),
    path('display_orders', views.display_orders),
    path('single_product/<int:item_id>', views.single_product),
    path('display_cat/<int:cat_id>', views.display_cat),
    path('display_cart', views.display_cart),
    path('display_empty_cart', views.display_empty_cart),
    path('add_to_cart/<int:item_id>', views.add_to_cart),
    path('remove_from_cart/<int:item_id>', views.remove_from_cart),
    path('display_checkout', views.display_checkout),
    path('3227751215/delete_item/<int:item_id>', views.delete_item),
    path('process_order', views.process_order),
    path('render_order_success', views.render_order_success),
    path('delete_order/<int:order_id>', views.delete_order),
    path('add_review/<int:item_id>', views.add_review),
    path('delete_review/<int:review_id>', views.delete_review)
]
