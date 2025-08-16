from django.shortcuts import render

# Create your views here.
# core/views.py
from django.shortcuts import render
from tests.models import TestCategory, LabTest, TestPackage # Import models from the 'tests' app

def home(request):
    # Fetch data from the database
    categories = TestCategory.objects.filter(labtest__is_available=True).distinct()
    all_tests = LabTest.objects.filter(is_available=True)
    packages = TestPackage.objects.filter(is_available=True)

    # Create a context dictionary to pass the data to the template
    context = {
        'categories': categories,
        'all_tests': all_tests,
        'packages': packages,
    }
    
    # Render the HTML template with the data
    return render(request, 'core/home.html', context)

def about_view(request):
    # This view simply renders the about page template.
    return render(request, 'core/about.html')