from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Event, Booking 
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone



def event_list(request):
    query = request.GET.get('q')
    filter_type = request.GET.get('filter')


    events = Event.objects.all()


    if query:
        events = Event.objects.filter(title__icontains=query) | Event.objects.filter(location__icontains=query)
    if filter_type == "upcoming":
        events = events.filter(date__gte=timezone.now())

    return render(request, 'events/event_list.html', {
        'events': events,
        'query': query,
        'filter_type': filter_type,
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})




@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # 🔴 NEW: check if already booked
    existing_booking = Booking.objects.filter(
        user=request.user,
        event=event
    ).first()

    if request.method == 'POST':
        print("➡️  Form submitted")

        if existing_booking:
            messages.warning(request, "You have already booked this event.")
            return redirect('my_bookings')

        try:
            seats = int(request.POST.get('seats', 0))
        except ValueError:
            messages.error(request, "Please enter a valid number of seats.")
            return render(request, 'events/book_event.html', {'event': event})

        if seats <= 0:
            messages.error(request, "Number of seats must be at least 1.")
            return render(request, 'events/book_event.html', {'event': event})

        # ✅ create booking (only once now)
        Booking.objects.create(
            user=request.user,
            event=event,
            seats_booked=seats
        )

        messages.success(request, "Booking successful! ✅")
        return redirect('event_list')

    return render(request, 'events/book_event.html', {'event': event})

@login_required
def my_bookings(request):
    bookings=Booking.objects.filter(user=request.user)
    return render(request,'events/my_bookings.html',{'bookings': bookings})

def register_view(request):
    if request.method == 'POST':
        form.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            message.success(request,"Account Created Successfully ! Please ")
            return redirect('login')    
    else:
        form = RegisterForm()
    return render(request,'events/register.html',{'form' : form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}! 🎉")
                return redirect('event_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'events/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 🔹 Automatically logs in the new user
            messages.success(request, "Account created and logged in successfully!")
            return redirect('event_list')
    else:
        form = RegisterForm()
    return render(request, 'events/register.html', {'form': form})

def logout_view(request):
    logout(request)
    message.info(request,"You have been logged out.")
    return redirect('login')   

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "❌ Booking cancelled successfully!")
    return redirect('my_bookings')
