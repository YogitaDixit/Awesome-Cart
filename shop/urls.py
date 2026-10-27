from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path(
    "my-orders/",
    views.my_orders,
    name="MyOrders"
),
    path(
    "order-success/<int:order_id>/",
    views.order_success,
    name="OrderSuccess"
),path(
    "my-orders/",
    views.my_orders,
    name="MyOrders"
),

path(
    "order-details/<int:order_id>/",
    views.order_details,
    name="OrderDetails"
),
    path("add-address/", views.add_address, name="AddAddress"),
    path("addresses/", views.addresses, name="addresses"),
    path("edit-address/<int:id>/", views.edit_address, name="EditAddress"),
    path("delete-address/<int:id>/", views.delete_address, name="DeleteAddress"),
    path("set-default-address/<int:id>/", views.set_default_address, name="SetDefaultAddress"),

    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("cart-count/", views.cart_count, name="cart_count"),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path("cart/", views.cart, name="cart"),
    
    path(
    'increase-cart/<int:item_id>/',
    views.increase_cart,
    name='increase_cart'
),

path(
    'decrease-cart/<int:item_id>/',
    views.decrease_cart,
    name='decrease_cart'
),

path(
    'remove-cart/<int:item_id>/',
    views.remove_cart,
    name='remove_cart'
),
]



