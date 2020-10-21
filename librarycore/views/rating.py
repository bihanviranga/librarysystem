from django.views import View
from django.shortcuts import redirect, render
from librarycore import models
from .helpers import *

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
    def get(self, request, pk):
        ratingObj = models.BookRating.objects.get(pk=pk)
        bookId = ratingObj.book.id
        if (ratingObj.user == request.user or isUserAdmin(request.user)):
            models.BookRating.objects.filter(pk=pk).delete()
        return redirect('book-detail', bookId)

class RatingUpdate(View):
    def post(self, request, pk):
        rating = models.BookRating.objects.get(pk=pk)
        if rating.user == request.user:
            if 'comment' in request.POST:
                rating.comment = request.POST['comment']
            if 'rating' in request.POST:
                rating.ratings = request.POST['rating']
            rating.save()
        return redirect('book-detail', rating.book.id)

    def get(self, request, pk):
        rating = models.BookRating.objects.get(pk=pk)
        context = {'rating': rating}
        return render(request, 'librarycore/rating_update.html', context)

