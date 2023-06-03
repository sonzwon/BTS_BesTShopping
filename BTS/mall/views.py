from django.shortcuts import render
from django.contrib.auth import login, logout
from .models import MyUser
from .forms import UserCreationForm


# # Create your views here.

def index(request):
    user = MyUser.objects.filter(username="admin").first()
    email = user.email if user else "Anonymous user"
    print(email)
    if request.user.is_authenticated is False:
        email = "Anonymous user"
    return render(request, "index.html", {"hello_msg": f"hello {email}"})



def register(request):
        form = UserCreationForm(request.POST)
        msg = "올바르지 않은 데이터 입니다."
        if form.is_valid():
            form.save()
        return render(request, "register.html", {"form":form, "msg":msg})