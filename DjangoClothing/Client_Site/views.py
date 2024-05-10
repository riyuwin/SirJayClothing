from django.shortcuts import render

def LaunchAddCustomer(request):
    return render(request, 'home.html')


def LaunchIndex(request):
    return render(request, 'index.html')