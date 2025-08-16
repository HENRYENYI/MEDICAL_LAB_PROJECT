# tests/models.py
from django.db import models

class TestCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g., General Health, Sexual Health")
    image = models.ImageField(upload_to='category_images/', blank=True, null=True, help_text="Optional image for the category")

    class Meta:
        verbose_name_plural = "Test Categories"

    def __str__(self):
        return self.name

class LabTest(models.Model):
    # Core Info
    name = models.CharField(max_length=200, help_text="e.g., Complete Blood Count (CBC) Test")
    category = models.ForeignKey(TestCategory, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Display Info
    short_description = models.TextField(blank=True, help_text="A brief, one-sentence description for the test list page.")
    long_description = models.TextField(blank=True, help_text="A detailed 'About the test' description for the detail page.")
    
    # Test Specifics
    sample_type = models.CharField(max_length=100, blank=True, help_text="e.g., Blood, Urine, Saliva")
    preparation = models.TextField(blank=True, help_text="e.g., No special preparation is required. or Fasting for 8 hours is required.")
    test_type = models.CharField(max_length=100, blank=True, help_text="e.g., In Person, At-Home Kit")
    turnaround_time = models.CharField(max_length=50, blank=True, help_text="e.g., 24-48 hours")

    # Status & Flags
    is_available = models.BooleanField(default=True)
    is_best_seller = models.BooleanField(default=False, help_text="Check this to display a 'Best Seller' tag.")
    is_anonymous = models.BooleanField(default=True, help_text="Can this test be booked without an account?")

    def __str__(self):
        return self.name

class TestPackage(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g., Executive Wellness Package")
    description = models.TextField()
    tests = models.ManyToManyField(LabTest)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="The total price for the package")
    
    # Status & Flags
    is_available = models.BooleanField(default=True)
    is_best_seller = models.BooleanField(default=False, help_text="Check this to display a 'Best Seller' tag for the package.")

    def __str__(self):
        return self.name