# tests/views.py
from django.shortcuts import render, get_object_or_404
from .models import LabTest, TestPackage, TestCategory

def test_list_view(request):
    """
    Displays all available tests and packages.
    """
    individual_tests = LabTest.objects.filter(is_available=True).order_by('name')
    packages = TestPackage.objects.filter(is_available=True).order_by('name')
    
    context = {
        'individual_tests': individual_tests,
        'packages': packages,
        'page_title': 'All Available Tests',
    }
    
    return render(request, 'tests/test_list.html', context)


def test_detail_view(request, pk):
    """
    Displays the details for a single test.
    """
    test = get_object_or_404(LabTest, pk=pk, is_available=True)
    
    context = {
        'test': test,
    }
    
    return render(request, 'tests/test_detail.html', context)


# --- NEW VIEW FOR ANONYMOUS TESTS ---
def anonymous_test_list_view(request):
    """
    Displays only tests and packages that can be booked anonymously.
    """
    # Filter for tests that are available AND flagged as anonymous
    anonymous_tests = LabTest.objects.filter(
        is_available=True, 
        is_anonymous=True
    ).order_by('name')

    # For now, we'll assume all packages can be booked anonymously.
    # If you add an 'is_anonymous' flag to TestPackage, you can filter it here too.
    packages = TestPackage.objects.filter(is_available=True).order_by('name')
    
    context = {
        'individual_tests': anonymous_tests,
        'packages': packages,
        'page_title': 'Anonymous Tests & Packages', # A more specific title for this page
    }
    
    # We cleverly reuse the same template as the main test list page.
    return render(request, 'tests/test_list.html', context)

def category_list_view(request):
    """
    Displays all test categories.
    """
    categories = TestCategory.objects.all().order_by('name')
    context = {
        'categories': categories,
    }
    return render(request, 'tests/category_list.html', context)

def category_detail_view(request, pk):
    """
    Displays tests in a specific category.
    """
    category = get_object_or_404(TestCategory, pk=pk)
    tests = LabTest.objects.filter(category=category, is_available=True).order_by('name')
    
    context = {
        'category': category,
        'individual_tests': tests,
        'packages': [],  # Empty for now, can add package filtering later
        'page_title': f'{category.name} Tests',
    }
    return render(request, 'tests/test_list.html', context)