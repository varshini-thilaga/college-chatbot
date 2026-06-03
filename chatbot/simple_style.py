try:
    from .retrieval import InMemoryStore
    SEMANTIC_SEARCH_AVAILABLE = True
except Exception:
    SEMANTIC_SEARCH_AVAILABLE = False

from .utils import clean_text

_store_cache = None

KEYWORD_MAP = [
    (['placement', 'job', 'company', 'package', 'salary', 'career'], 'placement'),
    (['hostel fee', 'hostel cost'], 'hostel_fee'),
    (['fee', 'fees', 'cost', 'price', 'tuition'], 'fee'),
    (['course', 'courses', 'program', 'degree', 'branch', 'ug courses'], 'course'),
    (['admission', 'admissions', 'apply', 'eligibility', 'counselling', 'counseling', 'dote', 'lateral entry', 'entrance'], 'admission'),
    (['hostel', 'accommodation', 'room', 'mess'], 'hostel'),
    (['transport', 'bus', 'route', 'commute'], 'transport'),
    (['scholarship', 'waiver', 'discount', 'financial'], 'scholarship'),
    (['hod', 'head of department', 'department head'], 'hod'),
    (['facility', 'facilities'], 'facility'),
    (['lab', 'labs', 'laboratory', 'research'], 'lab'),
    (['contact', 'phone', 'address', 'location'], 'contact'),
    (['email'], 'email'),
]

ANSWERS = {
    'placement': """SECE Placement Record:

• 120+ global companies visited in 2024/2025
• Top package: Rs.40 lakhs per annum
• Alumni working at Accenture, BorgWarner, AB InBev and more
• Students pursuing MS abroad (USA, Canada, Germany, UK)

Contact Placements:
• Dr. J. Arun: +91 97870 97171
• placements@sece.ac.in""",

    'hostel_fee': """Hostel Fee Details (per year):

Boys Hostel:
• Four Sharing: Rs.1,00,000
• Triple Sharing: Rs.1,15,000
• Double Sharing: Rs.1,35,000

Girls Hostel:
• Four Sharing: Rs.1,00,000
• Triple Sharing: Rs.1,15,000
• Double Sharing: Rs.1,35,000

All rooms: Wi-Fi enabled with attached bathrooms.""",

    'fee': """SECE Fee Structure:

Academic Fees:
• UG Programs (4 years): Rs.8 lakhs total
• PG Programs (2 years): Rs.2,00,000 total
• Lateral Entry (3 years): Rs.6 lakhs

Scholarships Available:
• Merit-based: up to 100% tuition fee waiver
• First Graduate Scholarship: Rs.25,000 discount
• CGPA 9+: Additional scholarship eligible
• SC/ST: Special consideration""",

    'course': """SECE Academic Programs:

UG Programs (B.E./B.Tech - 4 years):
• Computer Science and Engineering (CSE)
• Artificial Intelligence and Data Science (AI&DS)
• Information Technology (IT)
• Electronics and Communication Engineering (ECE)
• Electrical and Electronics Engineering (EEE)
• Mechanical Engineering (ME)
• Civil Engineering (CE)
• Computer Science and Business Systems (CSBS)
• Robotics and Automation
• Cyber Security

PG Programs (M.E./M.Tech - 2 years):
• M.E. Computer Science and Engineering
• M.E. Applied Electronics
• M.E. VLSI Design

PhD programs available across all disciplines.
Affiliated to Anna University, Chennai. Autonomous since 2019.""",

    'admission': """SECE Admission Details:

Eligibility (UG):
• 10+2 with Physics, Chemistry, Mathematics
• Minimum 45% aggregate (40% for SC/ST)

Eligibility (Lateral Entry):
• Diploma in relevant Engineering
• Minimum 45% in Diploma

Admission Process:
• Register at TNEA portal
• Single Window Counselling by DoTE, Chennai
• Select SECE and preferred branch
• Document verification and fee payment

Documents Required:
• 10th & 12th mark sheets
• Transfer Certificate (TC)
• Community Certificate (if applicable)
• Passport size photographs

Contact: 04259-200300 | sece@sece.ac.in""",

    'hostel': """SECE Hostel Facilities:

Accommodation:
• Boys: Double, Triple, Four sharing rooms
• Girls: Single, 3-4 sharing, 5-6 sharing rooms

Facilities:
• Wi-Fi enabled rooms with attached bathrooms
• 24x7 security and CCTV surveillance
• Laundry, gym, beauty salon
• RO drinking water

Mess Menu:
• South Indian, North Indian, Chinese cuisine
• Non-veg twice weekly
• Evening snacks and fresh fruits""",

    'transport': """SECE Transport:

• Bus service for day scholars across Coimbatore
• Public bus stop outside campus

Distance:
• 34.5 km from Coimbatore Airport
• 29 km from Gandhipuram Bus Stand
• 27 km from Coimbatore Railway Station

Transport Officer: Dr. Y. Sureshbabu
• +91 98428 95216 | sureshbabu.y@sece.ac.in""",

    'scholarship': """SECE Scholarships:

Merit-Based (12th marks out of 200):
• 190-200: 100% tuition fee waiver
• 188-189.75: 75% tuition fee waiver
• 185-187.75: 50% tuition fee waiver

Other Scholarships:
• First Graduate: Rs.25,000 discount
• SC/ST: Full fee waiver (govt norms)
• CGPA 9+: Additional scholarship
• Educational loans through partner banks""",

    'hod': """SECE Department HODs:

• CSE: Dr. R. Subha
• ECE: Dr. N. Shanmugasundaram
• EEE: Dr. W. Rajan Babu
• Mechanical: Dr. R. Suresh Kumar
• AI&DS: M. Mohammed Mustafa
• CSBS: C. Arunkumar
• Mathematics: Dr. R. Maheswari

Contact: 04259-200300 | sece@sece.ac.in""",

    'facility': """SECE Facilities:

Academic:
• Modern labs and research centers
• Digital library (8:30 AM - 7:00 PM)
• Smart classrooms, Wi-Fi campus

Sports:
• Basketball, volleyball, cricket, football
• Tennis court, 400m track, gymnasium

Research Centers:
• Centre for Research and Development (CRD)
• AI & Robotics Centre of Excellence
• IoT & Embedded Systems Labs
• VLSI Design Labs

Other:
• Boys and girls hostels
• Transportation, medical, banking/ATM""",

    'lab': """SECE Research Labs:

• Centre for Research and Development (CRD)
• AI & Robotics Centre of Excellence
• AI Innovation Lab (MoU with ITSS Global)
• Centre for AI & Machine Learning (CAIML)
• IoT & Embedded Systems Labs
• VLSI Design and Software Development Labs
• Innovation & Entrepreneurship Cell""",

    'contact': """SECE Contact Details:

• General Office: 04259-200300
• Email: sece@sece.ac.in
• Director: Shri R. Rajaram - +91 73736 17171
• Dean Academics: Dr. R.K. Suresh - +91 94421 10920
• Placements: Dr. J. Arun - +91 97870 97171
• Transport: Dr. Y. Sureshbabu - +91 98428 95216

Location:
• 34.5 km from Coimbatore Airport
• 29 km from Gandhipuram Bus Stand
• 27 km from Coimbatore Railway Station""",

    'email': "sece@sece.ac.in",
}

GREETINGS = ["hi", "hello", "hey", "vanakam", "vanakkam", "namaskaram", "namaste", "hola", "bonjour", "good morning", "good afternoon"]


def _get_intent(query_lower: str):
    for keywords, intent in KEYWORD_MAP:
        if any(k in query_lower for k in keywords):
            return intent
    return None


def simple_answer(query: str, raw_text: str, session_ctx: dict):
    global _store_cache

    query_lower = query.lower().strip()

    # Greetings — instant, no model needed
    if any(greet in query_lower for greet in GREETINGS):
        return "Hello! How can I assist you today? You can ask about admissions, courses, fees, placements, hostel, transport, or any other college-related topic."

    # Keyword match — instant, no model needed
    intent = _get_intent(query_lower)
    if intent:
        # Special case: fee + hostel
        if intent == 'fee' and 'hostel' in query_lower:
            return ANSWERS['hostel_fee']
        return ANSWERS[intent]

    # Fallback: semantic search (only if available and no keyword matched)
    if SEMANTIC_SEARCH_AVAILABLE:
        if _store_cache is None:
            _store_cache = InMemoryStore(raw_text)
        hits = _store_cache.search(query, top_k=3)
        if hits:
            context = " ".join([clean_text(h) for h in hits])
            if len(context) > 500:
                context = context[:500] + "..."
            return context

    return "I can help with courses, fees, admissions, placements, hostel, transport, scholarships and more. Please ask a specific question about SECE."