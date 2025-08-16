from django.shortcuts import render



def consultation_home(request):
    return render(request, 'consultation/consultation_home.html')