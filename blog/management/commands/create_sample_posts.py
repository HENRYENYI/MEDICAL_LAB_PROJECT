from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import BlogPost, BlogCategory

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample blog posts'

    def handle(self, *args, **options):
        # Get or create a user for the blog posts
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
        )
        
        # Create categories
        health_category, _ = BlogCategory.objects.get_or_create(
            name='Health Tips',
            defaults={'description': 'General health and wellness tips'}
        )
        
        medical_category, _ = BlogCategory.objects.get_or_create(
            name='Medical News',
            defaults={'description': 'Latest medical news and breakthroughs'}
        )
        
        # Sample blog posts data
        posts_data = [
            {
                'title': 'The Importance of Regular Health Checkups',
                'excerpt': 'Regular health checkups are crucial for early detection and prevention of diseases. Learn why you should prioritize your health screenings.',
                'content': '''Regular health checkups are one of the most important steps you can take to maintain your health and well-being. These routine visits to your healthcare provider can help detect potential health issues before they become serious problems.

**Why Regular Checkups Matter:**

1. **Early Detection**: Many health conditions, including diabetes, high blood pressure, and certain cancers, can develop without obvious symptoms. Regular screenings can catch these conditions early when they're most treatable.

2. **Prevention**: Your healthcare provider can recommend preventive measures based on your risk factors, family history, and lifestyle.

3. **Monitoring**: If you have existing health conditions, regular checkups help monitor your progress and adjust treatments as needed.

**What to Expect:**

During a routine checkup, your healthcare provider will typically:
- Review your medical history
- Perform a physical examination
- Order appropriate screening tests
- Discuss lifestyle factors
- Update vaccinations if needed

**How Often Should You Get Checked?**

The frequency of checkups depends on your age, health status, and risk factors. Generally:
- Adults 18-39: Every 2-3 years
- Adults 40-65: Every 1-2 years
- Adults 65+: Annually

Remember, investing in regular health checkups today can save you from more serious health issues and higher medical costs in the future.''',
                'category': health_category,
                'is_featured': True,
                'status': 'published'
            },
            {
                'title': 'Understanding Blood Test Results: A Complete Guide',
                'excerpt': 'Blood tests provide valuable insights into your health. Learn how to interpret common blood test results and what they mean for your wellbeing.',
                'content': '''Blood tests are among the most common diagnostic tools used in medicine. They can reveal a wealth of information about your health, from detecting infections to monitoring chronic conditions.

**Common Blood Tests and What They Measure:**

**Complete Blood Count (CBC):**
- Red blood cells: Carry oxygen throughout your body
- White blood cells: Fight infections
- Platelets: Help with blood clotting
- Hemoglobin: Protein that carries oxygen

**Basic Metabolic Panel (BMP):**
- Glucose: Blood sugar levels
- Electrolytes: Sodium, potassium, chloride
- Kidney function markers: Creatinine, BUN

**Lipid Panel:**
- Total cholesterol
- LDL (bad) cholesterol
- HDL (good) cholesterol
- Triglycerides

**Understanding Your Results:**

Each test has a normal range, but these can vary slightly between laboratories. Your healthcare provider will interpret your results in the context of your overall health, symptoms, and medical history.

**When Results Are Abnormal:**

Don't panic if some results fall outside the normal range. Many factors can affect blood test results, including:
- Recent meals
- Medications
- Physical activity
- Stress levels
- Time of day

**Next Steps:**

Always discuss your results with your healthcare provider. They can explain what the numbers mean for your specific situation and recommend any necessary follow-up tests or treatments.

Regular blood testing is an important part of preventive healthcare and can help you stay on top of your health.''',
                'category': medical_category,
                'is_featured': True,
                'status': 'published'
            },
            {
                'title': '10 Essential Health Habits for a Longer Life',
                'excerpt': 'Simple daily habits can significantly impact your longevity and quality of life. Discover the top 10 health habits backed by science.',
                'content': '''Living a long, healthy life isn't just about genetics—your daily habits play a crucial role. Here are 10 evidence-based habits that can help you live longer and feel better.

**1. Stay Physically Active**
Aim for at least 150 minutes of moderate exercise per week. This can include walking, swimming, cycling, or any activity you enjoy.

**2. Eat a Balanced Diet**
Focus on whole foods: fruits, vegetables, lean proteins, whole grains, and healthy fats. Limit processed foods and added sugars.

**3. Get Quality Sleep**
Aim for 7-9 hours of sleep per night. Good sleep is essential for physical recovery and mental health.

**4. Manage Stress**
Chronic stress can harm your health. Practice stress-reduction techniques like meditation, deep breathing, or yoga.

**5. Stay Hydrated**
Drink plenty of water throughout the day. Proper hydration supports all bodily functions.

**6. Don't Smoke**
If you smoke, quitting is the single best thing you can do for your health. Seek support if needed.

**7. Limit Alcohol**
If you drink, do so in moderation. This means up to one drink per day for women and two for men.

**8. Maintain Social Connections**
Strong relationships and social support are linked to better health and longevity.

**9. Regular Health Screenings**
Stay up to date with recommended health screenings and vaccinations.

**10. Practice Good Hygiene**
Simple habits like handwashing can prevent many illnesses.

**Start Small:**

You don't need to change everything at once. Pick one or two habits to focus on first, then gradually add others. Small, consistent changes can lead to significant health improvements over time.

Remember, it's never too late to start taking better care of your health!''',
                'category': health_category,
                'is_featured': True,
                'status': 'published'
            }
        ]
        
        # Create the blog posts
        for post_data in posts_data:
            post, created = BlogPost.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'author': user,
                    'excerpt': post_data['excerpt'],
                    'content': post_data['content'],
                    'category': post_data['category'],
                    'is_featured': post_data['is_featured'],
                    'status': post_data['status']
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created blog post: {post.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Blog post already exists: {post.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Sample blog posts creation completed!')
        )