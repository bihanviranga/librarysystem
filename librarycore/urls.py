from django.urls import path, include
from django.contrib.auth import views as auth_views
from librarycore import views

urlpatterns = [
    path('', views.index, name='index'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('profile/<str:username>/', views.UserDetail.as_view(), name='profile'),
    path('users/', views.UserList.as_view(), name='users'),

    path('books/', views.Books.as_view(), name='books'),
    path('books/new/', views.BookCreate.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('books/create-update/', views.BookCreateAndUpdate.as_view(), name='book-create-update'),

    path('bookinstances/new/', views.BookInstanceCreate.as_view(), name='instance-create'),
    path('bookinstances/<str:pk>/', views.BookInstanceDetail.as_view(), name='instance-detail'),
    path('bookinstances/<str:pk>/delete/', views.BookInstanceDelete.as_view(), name='instance-delete'),
    path('bookinstances/<str:pk>/update/', views.BookInstanceUpdate.as_view(), name='instance-update'),
    path('bookinstances/borrow', views.BookInstanceBorrow.as_view(), name='instance-borrow'),
    path('bookinstances/return', views.BookInstanceReturn.as_view(), name='instance-return'),

    path('authors/', views.AuthorList.as_view(), name='authors'),
    path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='author-detail'),
    path('authors/new/', views.AuthorCreate.as_view(), name='author-create'),
    path('authors/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),

    path('ratings/new/', views.RatingCreate.as_view(), name='rating-create'),
    path('ratings/<int:pk>/delete/', views.RatingDelete.as_view(), name='rating-delete'),
    path('ratings/<int:pk>/update/', views.RatingUpdate.as_view(), name='rating-update'),
]
