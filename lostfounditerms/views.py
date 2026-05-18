
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json
from .models import LostItem, FoundItem, User

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data["username"]
        email = data.get("email")
        password = data["password"]

        if not email:
            return JsonResponse({"error": "Email is required to create an account!"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "User already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return JsonResponse({
            "message": "User registered successfully",
            "user_id": user.id
        })

    return JsonResponse({"error": "Only POST allowed"}, status=405)

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data["username"]
        password = data["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            return JsonResponse({
                "message": "Login successful",
                "user_id": user.id,
                "is_staff": user.is_staff
            })
        else:
            return JsonResponse({
                "error": "Invalid credentials"
            }, status=401)

    return JsonResponse({"error": "Only POST allowed"}, status=405)
@csrf_exempt
def password_reset_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = request.get_host()
            # This link opens your reset-password.html file
            reset_link = f"http://{domain}/resetpwd.html?uid={uid}&token={token}"
            print(f"\nRESET LINK: {reset_link}\n")
            return JsonResponse({"message": "Reset link sent to terminal!"})
        return JsonResponse({"error": "Email not found"}, status=404)

@csrf_exempt
def simple_password_reset(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            new_password = data.get("new_password")

            # Check if all fields were actually sent
            if not username or not email or not new_password:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            user = User.objects.filter(username=username, email=email).first()

            if user:
                user.set_password(new_password)
                user.save()
                return JsonResponse({"message": "Password updated successfully!"})
            else:
                return JsonResponse({"error": "Username and email do not match."}, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
            
    return JsonResponse({"error": "Method not allowed"}, status=405)

def get_all_items(request):
    items = LostItem.objects.all()
    data = []
    for item in items:
        # Check if image exists to avoid errors
        img_url = request.build_absolute_uri(item.image.url) if item.image else None
        
        data.append({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "location": item.location,
            "category": item.category,
            "contact": item.contact,
            "status": item.status,
            "image": img_url # This sends the full http://127.0.0.1:8000/media/... link
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def add_item(request):
    if request.method == "POST":
        # 1. First, get the file from request.FILES
        image_file = request.FILES.get("image")

        # 2. Create the item using the actual file object
        item = LostItem.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            location=request.POST.get("location"),
            category=request.POST.get("category"),
            contact=request.POST.get("contact"),
            status=request.POST.get("status"),
            image=image_file  # Pass the file object here, NOT the URL
        )

        # 3. Now that 'item' exists, you can build the URL if you want to return it
        image_url = request.build_absolute_uri(item.image.url) if item.image else None

        return JsonResponse({
            "message": "Item added successfully",
            "image_url": image_url  # Optional: return the URL to the frontend
        })

    return JsonResponse({"error": "Only POST allowed"}, status=405)

@csrf_exempt
def update_item(request, item_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            item = LostItem.objects.get(id=item_id)
            item.name = data.get("name", item.name)
            item.description = data.get("description", item.description)
            item.location = data.get("location", item.location)
            item.category = data.get("category", item.category)
            item.contact = data.get("contact", item.contact)
            item.status = data.get("status", item.status) # <--- Update status too
            item.save()
            return JsonResponse({"message": "Item updated successfully"})
        except LostItem.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)
    return JsonResponse({"error": "Only PUT allowed"}, status=405)

# 1. GET ALL ITEMS (For the Dashboard Table)
 # Only admins can call this API
def get_all_items(request):
    items = LostItem.objects.all().order_by('-date_reported')
    data = []
    for item in items:
        img_url = request.build_absolute_uri(item.image.url) if item.image else None
        
        data.append({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "location": item.location,
            "category": item.category,
            "contact": item.contact,
            "status": item.status,
            "image": img_url,
            "date": item.date_reported.strftime("%Y-%m-%d %H:%M")
        })
    return JsonResponse(data, safe=False)

# 2. DELETE ITEM (Action for the Frontend)
@csrf_exempt
#@user_passes_test(lambda u: u.is_staff)
def delete_lost_item(request, item_id):
    if request.method == "DELETE":
        try:
            item = LostItem.objects.get(id=item_id)
            item.delete()
            return JsonResponse({"message": "Item deleted successfully"}, status=200)
        except LostItem.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)

from django.contrib.auth.models import User

# List all users
#@user_passes_test(lambda u: u.is_staff)
def get_all_users(request):
    users = User.objects.all().values('id', 'username', 'email', 'is_staff', 'date_joined')
    return JsonResponse(list(users), safe=False)

# Delete a user
@csrf_exempt
#@user_passes_test(lambda u: u.is_staff)
def delete_user(request, user_id):
    if request.method == "DELETE":
        if request.user.id == user_id:
            return JsonResponse({"error": "You cannot delete yourself!"}, status=400)
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({"message": "User removed"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        
        import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_item_status(request, item_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_status = data.get('status') # This will be 'lost' or 'found'
            
            item = LostItem.objects.get(id=item_id)
            item.status = new_status
            item.save()
            
            return JsonResponse({"message": "Status updated!"}, status=200)
        except LostItem.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
#@user_passes_test(lambda u: u.is_staff)
def update_user_role(request, user_id):
    if request.method == "POST":
        try:
            # Prevent changing your own role (so you don't lock yourself out!)
            if request.user.id == user_id:
                return JsonResponse({"error": "You cannot change your own role."}, status=400)

            data = json.loads(request.body)
            new_role = data.get('role') # 'admin' or 'user'
            
            user = User.objects.get(id=user_id)
            user.is_staff = True if new_role == 'admin' else False
            user.save()
            
            return JsonResponse({"message": "User role updated!"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)