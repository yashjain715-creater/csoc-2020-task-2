from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from datetime import date
from decimal import Decimal

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    
    book = get_object_or_404(Book,id=bid)
    num = BookCopy.objects.filter(book__title=book.title,status=True).count()

    if(request.user.is_authenticated):
        user = User.objects.get(username = request.user.username)
        ratingofuser = rating.objects.filter(book = book,user = user).count()
        if(ratingofuser>0):
            rate = rating.objects.get(book = book,user = user).rate
        else:
            rate = 0.0
    else:
        rate = 0.0    
    if num==0:
        context = {
            'book': book, # set this to an instance of the required book
            'num_available': 'Sorry Book not available', # set this to the number of copies of the book available, or 0 if the book isn't available
            'rate': rate,
        }
    else:
        context = {
            'book': book,
            'num_available': num,
            'rate': rate,
        }
    # START YOUR CODE HERE
    
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'

    title = request.GET.get("title")
    author = request.GET.get("author")
    genre = request.GET.get("genre")
    if(title and author and genre):
        books = Book.objects.filter(title=title,author=author,genre=genre)
    elif(title and author):
        books = Book.objects.filter(title=title,author=author)
    elif(title and genre):
        books = Book.objects.filter(title=title,genre=genre)
    elif(author and genre):
        books = Book.objects.filter(author=author,genre=genre)
    elif(title):
        books = Book.objects.filter(title=title)
    elif(author):
        books = Book.objects.filter(author=author)
    elif(genre):
        books = Book.objects.filter(genre=genre)
    else:
        books = Book.objects.all()

    context = {
        'books': books, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }

    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    user = User.objects.get(username = request.user.username)
    books = BookCopy.objects.filter(borrower = user)
    context = {
        'books': books,
    }

    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    book_id = request.POST.get("bid") # get the book id from post data
    book = Book.objects.get(id=book_id)
    bookcopy = BookCopy.objects.filter(book__title=book.title,status=True).first()
    Numberofbooks = BookCopy.objects.filter(book__title=book.title,status=True).count()
    
    if(Numberofbooks != 0):
        user = User.objects.get(username = request.user.username)
        bookcopy.borrower = user
        bookcopy.status = False
        bookcopy.borrow_date = date.today()
        bookcopy.save()
        response_data = {
        'message': 'success',
    }
    else:
        response_data = {
        'message': 'failure',
    }
    

    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    book_id = request.POST.get('bid')
    print(book_id)
    book = BookCopy.objects.get(id=book_id)
    user = User.objects.get(username = request.user.username)
    if(book!=0):
        book.borrower = None
        book.status = True
        book.borrow_date = None
        book.save()
        response_data = {
        'message': 'success',
        }
    else:
        response_data = {
        'message': 'failure',
    }

    return JsonResponse(response_data)


@csrf_exempt
@login_required
def ratingsystem(request):
    if request.method == 'POST':
        rate = request.POST.get('rate')
        bid = request.POST.get('bid')
        book = Book.objects.get(id = bid)
        user = User.objects.get(username = request.user.username)
        rateuser = rating()
        rateuser.user = user
        rateuser.rate = rate
        rateuser.book = book
        availableRateUser = rating.objects.filter(book=book,user=user)
        availableRateUser.delete()
        rateuser.save()

        bookRate = rating.objects.filter(book = book)
        sum = 0
        for i in bookRate:
            sum = sum + i.rate
        totalrate = sum/bookRate.count()
        x = Decimal(totalrate)
        rate = round(x,2)
        book.rating = rate
        book.save()
        response_data = {
           'message': 'success',
        }
        return JsonResponse(response_data)
