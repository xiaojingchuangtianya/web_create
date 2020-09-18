from django.shortcuts import render

# Create your views here.
def first_demo(request):
    return render(request,"first_demo.html")

def second_demo(request):
    return render(request,"second_demo.html")
