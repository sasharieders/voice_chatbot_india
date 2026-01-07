"""
Testing schedules by trimester for ANC in India.
Based on WHO guidelines and Indian national protocols.
"""

# Complete test schedule organized by trimester
TEST_SCHEDULE = {
    "first_trimester": {
        "weeks": "0-13",
        "required_tests": [
            {
                "name": "Blood Pressure",
                "timing": "First visit (before 12 weeks)",
                "frequency": "Every visit",
                "why": "Detect high blood pressure and pre-eclampsia risk early",
                "normal_range": "120/80 or lower",
                "hindi_name": "रक्तचाप जांच"
            },
            {
                "name": "Blood Group & Rh Factor",
                "timing": "First visit",
                "frequency": "Once",
                "why": "Identify Rh incompatibility risk between mother and baby",
                "normal_range": "Any blood group, note if Rh negative",
                "hindi_name": "रक्त समूह परीक्षण"
            },
            {
                "name": "Hemoglobin (Anemia Test)",
                "timing": "First visit",
                "frequency": "Every trimester",
                "why": "Screen for anemia which is common in pregnancy",
                "normal_range": "11 g/dL or higher",
                "hindi_name": "हीमोग्लोबिन परीक्षण"
            },
            {
                "name": "Blood Sugar (Fasting)",
                "timing": "First visit",
                "frequency": "Once initially, then if at risk",
                "why": "Screen for diabetes",
                "normal_range": "Less than 92 mg/dL",
                "hindi_name": "रक्त शर्करा परीक्षण"
            },
            {
                "name": "Urine Test",
                "timing": "First visit",
                "frequency": "Every visit",
                "why": "Check for infections, protein (pre-eclampsia), and sugar (diabetes)",
                "normal_range": "No protein, sugar, or infection",
                "hindi_name": "मूत्र परीक्षण"
            },
            {
                "name": "HIV Test",
                "timing": "First visit",
                "frequency": "Once (with consent)",
                "why": "Early treatment prevents transmission to baby",
                "normal_range": "Negative",
                "hindi_name": "एचआईवी परीक्षण"
            },
            {
                "name": "Hepatitis B",
                "timing": "First visit",
                "frequency": "Once",
                "why": "Identify risk and prevent transmission",
                "normal_range": "Negative",
                "hindi_name": "हेपेटाइटिस बी परीक्षण"
            },
            {
                "name": "Syphilis (VDRL/RPR)",
                "timing": "First visit",
                "frequency": "Once",
                "why": "Early treatment prevents complications",
                "normal_range": "Negative",
                "hindi_name": "सिफलिस परीक्षण"
            }
        ]
    },
    
    "second_trimester": {
        "weeks": "14-26",
        "required_tests": [
            {
                "name": "Ultrasound (Anomaly Scan)",
                "timing": "18-22 weeks (ideally 20 weeks)",
                "frequency": "Once",
                "why": "Check baby's growth, development, and detect any abnormalities",
                "what_to_expect": "Check heart, brain, spine, limbs, and organs",
                "hindi_name": "अल्ट्रासाउंड जांच"
            },
            {
                "name": "Glucose Tolerance Test (GTT)",
                "timing": "24-28 weeks",
                "frequency": "Once",
                "why": "Screen for gestational diabetes",
                "normal_range": "Less than 140 mg/dL after 1 hour",
                "preparation": "Fasting required, drink glucose solution, test after 1-2 hours",
                "hindi_name": "ग्लूकोज सहनशीलता परीक्षण"
            },
            {
                "name": "Blood Pressure",
                "timing": "Every visit (every 4 weeks)",
                "frequency": "Every visit",
                "why": "Continue monitoring for pre-eclampsia",
                "normal_range": "120/80 or lower",
                "hindi_name": "रक्तचाप जांच"
            },
            {
                "name": "Hemoglobin",
                "timing": "Around 20-24 weeks",
                "frequency": "Once this trimester",
                "why": "Re-check for anemia as blood volume increases",
                "normal_range": "11 g/dL or higher",
                "hindi_name": "हीमोग्लोबिन परीक्षण"
            },
            {
                "name": "Urine Test",
                "timing": "Every visit",
                "frequency": "Every visit",
                "why": "Continue monitoring for infection and pre-eclampsia",
                "normal_range": "No protein, sugar, or infection",
                "hindi_name": "मूत्र परीक्षण"
            }
        ]
    },
    
    "third_trimester": {
        "weeks": "27-40",
        "required_tests": [
            {
                "name": "Blood Pressure",
                "timing": "Every visit (every 2 weeks after 28 weeks)",
                "frequency": "Every visit",
                "why": "Pre-eclampsia risk increases in third trimester",
                "normal_range": "120/80 or lower",
                "action_if_high": "More frequent monitoring, possible hospitalization",
                "hindi_name": "रक्तचाप जांच"
            },
            {
                "name": "Hemoglobin",
                "timing": "Around 28 weeks",
                "frequency": "Once",
                "why": "Final check before delivery to treat anemia if needed",
                "normal_range": "11 g/dL or higher",
                "hindi_name": "हीमोग्लोबिन परीक्षण"
            },
            {
                "name": "Baby Position Check",
                "timing": "32+ weeks",
                "frequency": "Every visit after 32 weeks",
                "why": "Determine if baby is head-down (ready for delivery)",
                "what_to_expect": "Doctor will feel abdomen to check position",
                "hindi_name": "शिशु की स्थिति जांच"
            },
            {
                "name": "Urine Test",
                "timing": "Every visit",
                "frequency": "Every visit",
                "why": "Continue monitoring for pre-eclampsia and infection",
                "normal_range": "No protein, sugar, or infection",
                "hindi_name": "मूत्र परीक्षण"
            },
            {
                "name": "Non-Stress Test (NST)",
                "timing": "After 34 weeks if high-risk",
                "frequency": "Weekly if high-risk",
                "why": "Monitor baby's heart rate and movement",
                "what_to_expect": "Baby's heartbeat monitored for 20-30 minutes",
                "hindi_name": "नॉन-स्ट्रेस टेस्ट"
            },
            {
                "name": "Group B Strep (GBS) Test",
                "timing": "35-37 weeks",
                "frequency": "Once",
                "why": "Prevent infection during delivery",
                "what_to_expect": "Vaginal and rectal swab",
                "hindi_name": "ग्रुप बी स्ट्रेप परीक्षण"
            }
        ]
    }
}


def get_trimester_from_week(week):
    """
    Determine which trimester based on pregnancy week.
    
    Args:
        week (int): Current pregnancy week (1-40)
    
    Returns:
        str: 'first_trimester', 'second_trimester', or 'third_trimester'
    """
    if week <= 13:
        return "first_trimester"
    elif week <= 26:
        return "second_trimester"
    else:
        return "third_trimester"


def get_tests_for_week(week):
    """
    Get all required tests for a specific pregnancy week.
    
    Args:
        week (int): Current pregnancy week (1-40)
    
    Returns:
        dict: Trimester info and list of required tests
    """
    trimester = get_trimester_from_week(week)
    trimester_data = TEST_SCHEDULE[trimester]
    
    return {
        "trimester": trimester,
        "weeks": trimester_data["weeks"],
        "tests": trimester_data["required_tests"],
        "pregnancy_week": week
    }


def get_all_tests_summary():
    """
    Get a summary of all tests across all trimesters.
    
    Returns:
        dict: All test schedules organized by trimester
    """
    return TEST_SCHEDULE


def get_upcoming_tests(current_week):
    """
    Get tests that should be done soon based on current week.
    
    Args:
        current_week (int): Current pregnancy week
    
    Returns:
        list: Tests due within the next 4 weeks
    """
    current_trimester = get_trimester_from_week(current_week)
    tests = TEST_SCHEDULE[current_trimester]["required_tests"]
    
    # Filter tests that are relevant for current week
    upcoming = []
    for test in tests:
        # This is a simplified version - you could parse timing more precisely
        if "Every visit" in test["frequency"]:
            upcoming.append(test)
        elif current_trimester == "first_trimester" and current_week <= 12:
            upcoming.append(test)
        elif current_trimester == "second_trimester" and "20" in test["timing"]:
            if 18 <= current_week <= 22:
                upcoming.append(test)
    
    return upcoming


# Example usage and testing
if __name__ == "__main__":
    # Test the functions
    print("Testing test_schedules.py\n")
    
    # Test 1: Get tests for week 10 (first trimester)
    print("Week 10 (First Trimester):")
    result = get_tests_for_week(10)
    print(f"Trimester: {result['trimester']}")
    print(f"Number of tests: {len(result['tests'])}")
    print(f"First test: {result['tests'][0]['name']}\n")
    
    # Test 2: Get tests for week 20 (second trimester)
    print("Week 20 (Second Trimester):")
    result = get_tests_for_week(20)
    print(f"Trimester: {result['trimester']}")
    print(f"Number of tests: {len(result['tests'])}")
    for test in result['tests']:
        print(f"  - {test['name']}: {test['timing']}")
    print()
    
    # Test 3: Get tests for week 35 (third trimester)
    print("Week 35 (Third Trimester):")
    result = get_tests_for_week(35)
    print(f"Trimester: {result['trimester']}")
    print(f"Number of tests: {len(result['tests'])}")
    print(f"Critical test: {result['tests'][-1]['name']}")