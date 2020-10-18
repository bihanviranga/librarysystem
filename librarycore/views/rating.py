from django.views import View
from django.shortcuts import redirect
from librarycore import models

class RatingCreate(View):
    def post(self, request, bookId):
        book = models.Book.objects.get(pk=bookId)
        models.BookRating.objects.create(
            book=book,
            user=request.user,
            ratings=request.POST['rating'],
            comment=request.POST['comment']
        )
        return redirect('book-detail', book.id)

class RatingDelete(View):
    def post(self, request):
        pass

class RatingUpdate(View):
    def post(self, request):
        pass

