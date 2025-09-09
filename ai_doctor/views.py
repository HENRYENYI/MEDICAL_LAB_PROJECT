from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import uuid
from .models import AIConsultation
from tests.models import LabTest
from consultation.models import ConsultationSpecialty

def ai_doctor_home(request):
    return render(request, 'ai_doctor/ai_doctor.html')

@csrf_exempt
@require_POST
def ask_ai_doctor(request):
    try:
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        
        if not question:
            return JsonResponse({'error': 'Question is required'}, status=400)
        
        # Generate AI response based on keywords
        ai_response, suggested_tests, suggested_consultations = generate_ai_response(question)
        
        # Save consultation
        session_id = request.session.get('ai_session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session['ai_session_id'] = session_id
        
        consultation = AIConsultation.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_id=session_id if not request.user.is_authenticated else None,
            question=question,
            ai_response=ai_response
        )
        
        # Add suggested tests and consultations
        if suggested_tests:
            consultation.suggested_tests.set(suggested_tests)
        if suggested_consultations:
            consultation.suggested_consultations.set(suggested_consultations)
        
        # Prepare response data
        response_data = {
            'response': ai_response,
            'suggested_tests': [
                {
                    'id': test.id,
                    'name': test.name,
                    'price': float(test.price),
                    'description': test.short_description or 'Professional lab test'
                } for test in suggested_tests
            ],
            'suggested_consultations': [
                {
                    'id': consultation_spec.id,
                    'name': consultation_spec.name,
                    'price': float(consultation_spec.price),
                    'description': consultation_spec.description
                } for consultation_spec in suggested_consultations
            ]
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generate_ai_response(question):
    """Generate AI response based on keywords and suggest relevant tests/consultations"""
    question_lower = question.lower()
    
    # Medical keywords mapping
    medical_keywords = {
        'diabetes': {
            'response': 'Based on your concern about diabetes, I recommend monitoring your blood sugar levels. Diabetes can be managed effectively with proper testing and lifestyle changes.',
            'tests': ['glucose', 'hba1c', 'diabetes'],
            'consultations': ['general physician']
        },
        'blood pressure': {
            'response': 'High blood pressure is a serious condition that requires regular monitoring. I suggest getting your cardiovascular health checked.',
            'tests': ['lipid', 'cardiac', 'cholesterol'],
            'consultations': ['general physician']
        },
        'pregnancy': {
            'response': 'Congratulations on your pregnancy journey! Regular prenatal testing is important for both mother and baby health.',
            'tests': ['pregnancy', 'prenatal', 'hcg'],
            'consultations': ['gynecology']
        },
        'std': {
            'response': 'STD testing is important for sexual health. We offer confidential and anonymous testing options.',
            'tests': ['std', 'hiv', 'syphilis', 'chlamydia'],
            'consultations': ['general physician']
        },
        'thyroid': {
            'response': 'Thyroid disorders can affect your metabolism and energy levels. Testing can help determine if your thyroid is functioning properly.',
            'tests': ['thyroid', 'tsh', 't3', 't4'],
            'consultations': ['general physician']
        },
        'liver': {
            'response': 'Liver function is crucial for your overall health. Regular liver function tests can help detect issues early.',
            'tests': ['liver', 'alt', 'ast', 'bilirubin'],
            'consultations': ['general physician']
        },
        'kidney': {
            'response': 'Kidney health is vital for filtering waste from your body. Regular kidney function tests are recommended.',
            'tests': ['kidney', 'creatinine', 'urea'],
            'consultations': ['general physician']
        },
        'cancer': {
            'response': 'Early detection is key in cancer prevention. Regular screening tests can help identify potential issues early.',
            'tests': ['psa', 'cea', 'cancer', 'tumor'],
            'consultations': ['general physician']
        },
        'heart': {
            'response': 'Heart health is crucial for your overall wellbeing. Cardiac tests can help assess your cardiovascular risk.',
            'tests': ['cardiac', 'troponin', 'cholesterol', 'lipid'],
            'consultations': ['general physician']
        },
        'infection': {
            'response': 'Infections can be serious if left untreated. Laboratory tests can help identify the cause and guide treatment.',
            'tests': ['blood culture', 'wbc', 'esr', 'crp'],
            'consultations': ['microbiology', 'general physician']
        }
    }
    
    # Default response
    ai_response = "Thank you for your question. Based on your symptoms, I recommend consulting with a healthcare professional for proper evaluation. Regular health screening is always beneficial for maintaining good health."
    suggested_tests = []
    suggested_consultations = []
    
    # Check for keywords and generate appropriate response
    for keyword, info in medical_keywords.items():
        if keyword in question_lower:
            ai_response = info['response']
            
            # Find matching tests
            for test_keyword in info['tests']:
                tests = LabTest.objects.filter(
                    name__icontains=test_keyword, 
                    is_available=True
                )[:3]  # Limit to 3 tests
                suggested_tests.extend(tests)
            
            # Find matching consultations
            for consultation_keyword in info['consultations']:
                consultations = ConsultationSpecialty.objects.filter(
                    name__icontains=consultation_keyword,
                    is_available=True
                )[:2]  # Limit to 2 consultations
                suggested_consultations.extend(consultations)
            
            break
    
    # Remove duplicates
    suggested_tests = list(set(suggested_tests))
    suggested_consultations = list(set(suggested_consultations))
    
    return ai_response, suggested_tests, suggested_consultations