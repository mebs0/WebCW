from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Hobby, CustomUser, Friendship, FriendRequest
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash

from django.db.models import Count, Q, ExpressionWrapper, F, DurationField, IntegerField
from django.db.models.functions import Now
from datetime import timedelta, datetime, date
import json


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'api/registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(main_spa)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'api/registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request, 'api/registration/logout.html')


@login_required
def user_api(request):
    """API endpoint for user-related operations."""
    current_user = request.user

    if request.method == 'POST':
        POST = json.loads(request.body)
        hobby = Hobby.objects.get(id=POST['hobby_id'])
        current_user.hobbies.add(hobby)
        current_user.save()
        return JsonResponse({'message': 'Hobby added successfully'})

    if request.method == 'PUT':
        PUT = json.loads(request.body)

        # Update user details
        current_user.name = PUT.get('name', current_user.name)
        current_user.username = PUT.get('username', current_user.username)
        current_user.email = PUT.get('email', current_user.email)
        current_user.date_of_birth = PUT.get('date_of_birth', current_user.date_of_birth)

        # Handle password change
        if 'old_password' in PUT and 'new_password' in PUT:
            if not check_password(PUT['old_password'], current_user.password):
                return JsonResponse({'error': 'Current password is incorrect.'}, status=400)
            current_user.set_password(PUT['new_password'])
            update_session_auth_hash(request, current_user)

        current_user.save()
        return JsonResponse({'message': 'User updated successfully'})

    if request.method == 'DELETE':
        DELETE = json.loads(request.body)
        hobby = Hobby.objects.get(id=DELETE['hobby_id'])
        if not current_user.hobbies.filter(id=hobby.id).exists():
            return JsonResponse({'error': 'Hobby not associated with user'}, status=400)
        current_user.hobbies.remove(hobby)
        current_user.save()
        return JsonResponse({'message': 'Hobby removed successfully'})

    return JsonResponse(current_user.as_dict())


@login_required
def hobby_api(request):
    """API endpoint for hobby-related operations."""

    if request.method == 'POST':
        POST = json.loads(request.body)
        hobby_name = POST.get('name', '').strip()

        if not hobby_name:
            return JsonResponse({'error': 'Hobby name cannot be empty'}, status=400)

        hobby, created = Hobby.objects.get_or_create(name=hobby_name)
        return JsonResponse({
            'message': 'Hobby added successfully' if created else 'Hobby already exists',
            'hobby': hobby.as_dict()
        })

    return JsonResponse({
        'hobbies': [
            hobby.as_dict() for hobby in Hobby.objects.all()
        ]
    })


@login_required
def similar_users(request):
    # Get the hobbies of the current user and compare it with all other users
    current_user = request.user
    user_hobbies = current_user.hobbies.values_list('id', flat=True)

    # Retrieve age parameters from the request
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')

    # Annotate users with their age
    users_with_age = CustomUser.objects.all()

    # Filter users based on the minimum age if provided
    if min_age is not None:
        min_age = int(min_age)
        min_age_date = date.today() - timedelta(days=min_age * 365) # Converting minimum age in years to a date object so it can be compared
        users_with_age = users_with_age.filter(date_of_birth__lte=min_age_date)

    # Filter users based on the maximum age if provided
    if max_age is not None:
        max_age = int(max_age)
        max_age_date = date.today() - timedelta(days=max_age * 365)
        users_with_age = users_with_age.filter(date_of_birth__gte=max_age_date)

    # Count how many hobbies every user shares with the current user
    similar_users = (
        users_with_age.exclude(id=current_user.id)
        .annotate(shared_hobbies=Count('hobbies', filter=Q(hobbies__id__in=user_hobbies)))
        .filter(shared_hobbies__gte=0)
        .order_by('-shared_hobbies')
    )

    print(f"Similar users: {similar_users}")
    # The annotate line gets the users who have the same hobbies as the current user and then this is counted and stored in the shared_hobbies variable
    # The second filter is used to only retrieve users with shared hobbies (greater than 0)
    # The hyphen - indicates descending order

    # Pagination to display 10 users 
    page = int(request.GET.get('page', 1))
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = similar_users[start:end]

    # Create a dictionary containing each username and the number of shared hobbies
    users_data = [
        {
            'id': user.id,
            'username': user.username,
            'shared_hobbies': user.shared_hobbies,
            'age': (date.today() - user.date_of_birth).days // 365 if user.date_of_birth else None,
        }
        for user in paginated_users
    ]

    return JsonResponse({
        'users': users_data,
        'total': similar_users.count(),
        'page': page,
        'per_page': per_page,
    })

##Views for friend requests
def incoming_fr_api(request): 
    user = request.user
    if request.method == 'GET': ##gets all incoming friend requests for the current user
        incoming_requests = FriendRequest.objects.filter(receiver=user)
        return JsonResponse({
            'incoming_requests':[
                friendRequest.as_dict()
                for friendRequest in incoming_requests
            ]
        })
    return JsonResponse({'error': 'Invalid HTTP method for friend request operations'}, status=405)
       
def outgoing_fr_api(request): 
    user = request.user
    if request.method == 'GET': ##gets all outgoing friend requests for the current user
        incoming_requests = FriendRequest.objects.filter(sender=user)
        return JsonResponse({
            'outgoing_requests':[
                friendRequest.as_dict()
                for friendRequest in incoming_requests
            ]
        })
    return JsonResponse({'error': 'Invalid HTTP method for friend request operations'}, status=405)

def get_friends(request):
    user = request.user
    if request.method == 'GET': ##gets all outgoing friend requests for the current user
        friends = Friendship.objects.filter(user1=user)
        return JsonResponse({
            'friends':[
                friend.as_dict()
                for friend in friends
            ]
        })
    return JsonResponse({'error': 'Invalid HTTP method for friend request operations'}, status=405)

def remove_friend(request):
    if request.method == "DELETE":
        DELETE = json.loads(request.body)
        friendship = Friendship.objects.get(id=DELETE["id"])
        user1 = request.user
        user2 = friendship.user2
        reverseFriendship = Friendship.objects.get(user1=user2, user2=user1)
        friendship.delete()
        reverseFriendship.delete()
        return JsonResponse ({})
    
def delete_friend_request(request):
    if request.method == "DELETE":
        DELETE = json.loads(request.body)
        friend_request = FriendRequest.objects.get(id=DELETE["id"])
        friend_request.delete()
        return JsonResponse ({})
    
def accept_friend_request(request):
    if request.method == "POST":
        POST = json.loads(request.body)
        friend_request = FriendRequest.objects.get(id=POST["id"])
        sender = friend_request.sender
        receiver = friend_request.receiver
        friendship, created = Friendship.objects.get_or_create(user1=sender, user2=receiver)
        reversefriendship, created2 = Friendship.objects.get_or_create(user1=receiver, user2=sender)
        friend_request.delete()
        if created and created2:
            return JsonResponse ({'friendship':reversefriendship.as_dict()})
        else:
            return JsonResponse ({'error': 'Friendship already exists'})


def send_fr_api(request):
    """ This is for the send friend request button in the similar hobbies page """
    user = request.user
    if request.method == 'POST': ##creates a new outgoing friend request
        POST = json.loads(request.body)
        receiver = CustomUser.objects.get(id = POST["id"])
        if FriendRequest.objects.filter(sender=user, receiver=receiver).exists():
            return JsonResponse({'error': 'Friend request already sent.'}, status=400)

        # Check if they are already friends
        if receiver in user.friends.all():
            return JsonResponse({'error': 'You are already friends.'}, status=400)

        # Create a new friend request
        newRequest = FriendRequest.objects.create(sender=user, receiver=receiver)
        return JsonResponse(newRequest.as_dict())

