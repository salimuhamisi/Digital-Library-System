from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book,Reaches,CustomUser,Borrowing,supplier,Notification, Order, Invoice, Video
from .forms import BorrowForm
from django.template.loader import render_to_string
import os
from django.http import HttpResponse
from twilio.rest import Client
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404




# Create your views here.
def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        new_entry = Reaches(
            name=name,
            email=email,
            message=message,
        )
        new_entry.save()
        messages.success(request, 'Entry posted Successfully!')
        return redirect('contact')
    return render(request, 'contact.html')

def signup(request):

    error_message = None
    if request.method == 'POST':
        regNo = request.POST['regNo']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        
       

        # Check if the username already exists
        if CustomUser.objects.filter(username=username).exists():
            error_message = 'Username is already taken'
        else:
            # Create a new user object with the submitted data
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                regNo=regNo,
                email=email,
            )

            messages.success(request, 'Account created successfully')

            # Redirect to home page or any other page
            return redirect('signin')
    return render(request, 'signup.html', {'error_message': error_message})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if request.user.username in ['hamisi', 'admin1', 'admin2', 'admin3']:
                return redirect('administration')
            else:
                return redirect("students")
        
        else:
            messages.error(request, "invalid credentials")
            return redirect('signin')
    return render(request, 'signin.html')

def administration(request):

    # Default to retrieving all entries
    entries = Book.objects.all()
    user = request.user

    # Check if a category is clicked
    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            # Filter books based on the selected category
            entries = Book.objects.filter(book_category=category)



    if request.method == 'POST' and 'submit' in request.POST:
        book_category = request.POST.get('book_category')
        book_name = request.POST.get('book_name')
        description = request.POST.get('description')
        number_of_books = request.POST.get('number_of_books')
        book_type = request.POST.get('book_type')
        document = request.FILES.get('document')
        
        # Do something with the form data, such as saving it to the database
        new_entry = Book(
            book_category=book_category,
            book_name=book_name,
            description=description,
            number_of_books=number_of_books,
            book_type=book_type,
            document=document,
        )
        new_entry.save()
        messages.success(request, 'Entry posted Successfully!')
        return redirect('administration')

    if request.method == 'POST' and 'add_video' in request.POST:
        video_name = request.POST.get('video_name')
        video_category = request.POST.get('video_category')
        video_url = request.POST.get('video_url')

        # Do something with the form data, such as saving it to the database
        new_entry = Video(
            video_name=video_name,
            category=video_category,
            video=video_url,
        )
        new_entry.save()
        messages.success(request, 'Entry posted Successfully!')
        return redirect('administration')
    return render(request, 'administration.html', {'entries': entries, 'user': user})


def students(request):
    # Retrieve all entries
    entries = Book.objects.all()

    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            # Filter books based on the selected category
            entries = Book.objects.filter(book_category=category)

    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            book_id = form.cleaned_data['book_id']
            borrowing_date = form.cleaned_data['borrowing_date']
            returning_date = form.cleaned_data['returning_date']
            student = request.user  # Assuming the student is the logged-in user

            # Check if the book is already borrowed by the current user
            if Borrowing.objects.filter(student=student, book_id=book_id, is_borrowed=True).exists():
                messages.warning(request, 'You have already borrowed this book.')
            else:
                # Create a new Borrowing object and set is_borrowed to True
                borrowing = Borrowing.objects.create(
                    student=student,
                    book_id=book_id,
                    borrowing_date=borrowing_date,
                    returning_date=returning_date,
                    is_borrowed=True
                )

                # Create a notification for the user
                book = Book.objects.get(pk=book_id)
                ticket_link = "#"  # Replace "#" with your actual link generation logic
                notification_message = render_to_string('nmessage.html', {
                    'username': student.username,
                    'borrowing_date': borrowing_date,
                    'returning_date': returning_date,
                    'book_name': book.book_name,
                    'ticket_link': ticket_link
                })
                Notification.objects.create(user=student, message=notification_message)

                # Redirect back to the students page to avoid form resubmission
                return redirect('students')

    else:  # If it's a GET request, render the template with the form
        form = BorrowForm()

    # Get the list of borrowed book IDs for the current user
    user = request.user
    borrowed_books = Borrowing.objects.filter(student=user, is_borrowed=True).values_list('book_id', flat=True)

    # Pass the entries, user, and form to the template
    return render(request, 'students.html', {'entries': entries, 'user': user, 'form': form, 'borrowed_books': borrowed_books})



def snotifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'snotifications.html', {'notifications': notifications})


def aborrowed(request):

    #entries = Borrowing.objects.all()
    entries = Borrowing.objects.filter(student__username__startswith='student')
    user = request.user

    if request.method == 'POST' and 'return_book' in request.POST:
        borrowing_id = request.POST.get('borrowing_id')
        try:
            borrowing = Borrowing.objects.get(id=borrowing_id)
            # Mark the book as returned
            borrowing.is_borrowed = False
            borrowing.save()
            messages.success(request, 'Book returned successfully!')
        except Borrowing.DoesNotExist:
            messages.error(request, 'Borrowing entry does not exist.')
        
        # Redirect back to the administration page
        return redirect('aborrowed')
    
    return render(request,'aborrowed.html', {'user': user, 'entries': entries})


def suppliers(request):

    if request.method == 'POST' and 'add_supplier' in request.POST:
        
        compName = request.POST.get('company_name')
        bookTitle = request.POST.get('book_tittle')
        number_of_books = request.POST.get('number_of_books')
        delivery_date = request.POST.get('delivery_date')
        contacts = request.POST.get('contact')


        # Do something with the form data, such as saving it to the database
        new_entry = supplier(
            company_name=compName,
            book_tittle=bookTitle,
            number_of_books=number_of_books,
            delivery_date=delivery_date,
            contact=contacts,
        )
        new_entry.save()
        messages.success(request, 'Supplier Added Successfully!')
        return redirect('suppliers')

    if request.method == 'POST':
        # Get form data
        company_name = request.POST.get('company_name')
        book_title = request.POST.get('book_tittle')
        num_books = request.POST.get('quantity')
        contact = request.POST.get('contact')

        #save the details first
        myorder = Order(
            company_name=company_name,
            book_tittle=book_title,
            num_books=num_books,

        )
        myorder.save()

        # Create a notification for the user
        notification_message = render_to_string('amessage.html', { 
            'company_name': myorder.company_name,
            'book_tittle': myorder.book_tittle,
            'num_books': myorder.num_books,
        })
        user = request.user
        Invoice.objects.create(user=user, message=notification_message)


        #############################################################################################
        # PART OF CODE TO SEND MESSAGE WAS REMOVED!!
        
        # Find your Account SID and Auth Token at twilio.com/console
        # Find your Account SID and Auth Token at twilio.com/console
        
        
        # Redirect or provide any response as needed
        return HttpResponse("Order placed successfully. SMS sent to supplier.")
    else:
        # Retrieve all entries by default
        entries = supplier.objects.all()
        return render(request, "suppliers.html", {'entries': entries})
def staffs(request):
    # Filter entries for staff users
    entries = Borrowing.objects.filter(student__username__startswith='staff')
    user = request.user

    if request.method == 'POST' and 'return_book' in request.POST:
        borrowing_id = request.POST.get('borrowing_id')
        try:
            borrowing = Borrowing.objects.get(id=borrowing_id)
            # Mark the book as returned
            borrowing.is_borrowed = False
            borrowing.save()
            messages.success(request, 'Book returned successfully!')
        except Borrowing.DoesNotExist:
            messages.error(request, 'Borrowing entry does not exist.')
        
        # Redirect back to the administration page
        return redirect('staffs')
    return render(request,'staffs.html', {'user': user, 'entries': entries})

def sborrowed(request):
    user = request.user
    entries = Borrowing.objects.filter(student=user)
    return render(request,'sborrowed.html', {'user': user, 'entries': entries})

def signout(request):
    logout(request)
    return redirect('index')

def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('administration')

def reaches(request):
    entries = Reaches.objects.all().order_by('-created_at')
    user = request.user
    return render(request,'reaches.html', {'entries': entries, 'user': user})

def orders(request):
    entries = Order.objects.all().order_by('-created_at')
    user = request.user
    return render(request,'orders.html', {'entries': entries, 'user': user})

def invoices(request):
    user = request.user
    notifications = Invoice.objects.all().order_by('-created_at')
    return render(request,'invoices.html', {'user': user, 'notifications': notifications})

def videos(request):
    category = request.GET.get('category')
    if category:
        # Filter videos based on the selected category
        videos = Video.objects.filter(category=category)
    else:
        # If no category is specified, retrieve all videos
        videos = Video.objects.all()

    num_videos_per_row = 3  # Define the number of videos per row
    num_videos = len(videos)
    num_rows = (num_videos + num_videos_per_row - 1) // num_videos_per_row  # Calculate number of rows needed
    videos_grouped = [videos[i*num_videos_per_row:(i+1)*num_videos_per_row] for i in range(num_rows)]  # Group videos into rows

    return render(request, 'videos.html', {'videos_grouped': videos_grouped})







