# Voice Chatbot India - Use Cases & Features

## Overview
This voice chatbot provides maternal health support for pregnant women in India through AI-powered conversations. The system helps users navigate antenatal care (ANC), understand medical tests, access healthcare facilities, and receive personalized guidance throughout their pregnancy journey.

---

## Core Use Cases

### 1. Early Pregnancy Identification & First ANC Visit
**Goal:** Identify pregnancy early and prompt first ANC attendance

**Features:**
- **Identify pregnancy early** (Early GA Dating, Early ANC attendance)
  - Detect signs of pregnancy through conversation
  - Calculate gestational age based on last menstrual period
  - Recommend timing for pregnancy confirmation
  
- **Understand initial risks** (PE risk, Anemia risk)
  - Screen for pre-eclampsia risk factors
  - Assess anemia risk based on diet and history
  - Identify high-risk conditions requiring immediate care
  
- **Prompt first ANC** (Early ANC attendance)
  - Explain importance of ANC1 before 12 weeks
  - Provide appointment scheduling guidance
  - Send reminders for upcoming first visit

**Implementation Status:** Partially implemented
- File: `src/use_cases/anc1_timing.py`

---

### 2. Facility Access & Information
**Goal:** Know where to go for ANC (Ease of access)

**Features:**
- **Know where to go for ANC1** (Ease of access)
  - Geo-location based facility search
  - Find nearest ANC-equipped clinics/hospitals
  - Provide directions and contact information
  
- **Access hours/services info** (Ease of access)
  - Operating hours for each facility
  - Available services (ultrasound, lab tests, specialists)
  - Cost information (free vs. paid services)
  - Language support available at facility
  
- **Complete ANC1 on time** (Early ANC attendance)
  - Calculate deadline for ANC1 (12 weeks)
  - Send reminders as deadline approaches
  - Help overcome barriers to attendance

**Implementation Status:** Not yet implemented
- File: `src/use_cases/anc1_facility.py`
- File: `src/use_cases/facility_hours.py`
- File: `src/use_cases/facility_selection.py`

---

### 3. Visit & Testing Schedule Management (DEMO)
**Goal:** Follow visit + testing cadence by trimester

**Features:**
- **Follow visit + testing cadence by trimester**
  - Track pregnancy week and trimester
  - Provide visit schedule (8 total ANC visits recommended)
  - Schedule reminders for upcoming visits
  
- **BP, Labs/Blood test risk screening**
  - Explain blood pressure monitoring schedule
  - Schedule hemoglobin checks (each trimester)
  - Blood group, Rh factor, HIV, Hepatitis B tests
  - Glucose tolerance test (24-28 weeks)
  
- **Ultrasound risk screening**
  - First ultrasound timing (before 12 weeks)
  - Anomaly scan (18-22 weeks)
  - Growth scans in third trimester if needed
  
- **Understand results/regimens** (Clinical understanding)
  - Explain test results in simple language
  - Interpret normal vs. abnormal ranges
  - Explain what results mean for pregnancy
  - Provide context for follow-up actions
  
- **Adhere to supplements/treatment** (Effective treatment)
  - Iron supplementation guidance (60mg daily)
  - Folic acid importance (400mcg daily)
  - Calcium recommendations
  - Tips for adherence and timing
  - Managing side effects

**Implementation Status:** Implemented (Demo)
- File: `src/use_cases/test_screening.py`
- File: `src/use_cases/visit_cadence.py`
- File: `src/use_cases/results_understanding.py`
- File: `src/use_cases/supplement_adherence.py`
- Knowledge Base: `src/knowledge/test_schedules.py`
- Knowledge Base: `src/knowledge/supplement_info.py`

---

### 4. Risk Monitoring & Danger Signs
**Goal:** Monitor for danger signs and escalate when needed

**Features:**
- **Monitor for danger signs** (Risk monitoring)
  - Screen for warning symptoms during calls
  - Pre-eclampsia signs (headache, vision changes, swelling)
  - Bleeding or fluid leakage
  - Decreased fetal movement
  - Severe abdominal pain
  
- **Recognize abnormal symptoms/results** (Risk monitoring)
  - Identify concerning test results
  - Flag abnormal vital signs
  - Detect patterns indicating complications
  
- **Escalate promptly when needed** (Escalation of risk)
  - Immediate referral for emergency symptoms
  - Connect to emergency services if needed
  - Provide nearest emergency facility information
  - Follow-up to ensure care was received

**Implementation Status:** Not yet implemented
- File: `src/knowledge/risk_assessment.py`
- Integration needed with emergency services

---

### 5. Healthcare Navigation & Communication
**Goal:** Choose correct facility level and overcome communication barriers

**Features:**
- **Choose correct facility level** (Ease of access)
  - Differentiate between PHC, CHC, district hospital
  - Match user needs to appropriate facility level
  - Understand referral pathways
  - Know when specialist care is needed
  
- **Follow clear escalation steps** (Escalation of risk)
  - Understand the referral system
  - Know which facility for which complication
  - Transportation assistance information
  - Financial assistance programs (JSY, etc.)
  
- **Overcome communication barriers** (Effective treatment)
  - Multi-language support (Hindi, English, regional languages)
  - Explain medical terms in simple language
  - Cultural sensitivity in health guidance
  - Help prepare questions for doctor visits

**Implementation Status:** Not yet implemented
- Requires expansion of language support
- Need facility classification system

---

### 6. Delivery Preparation & Postpartum Care
**Goal:** Plan facility, transition to postnatal care, and support breastfeeding

**Features:**
- **Plan facility, transition, supplies** (Ease of access, Effective treatment)
  - Help choose delivery facility based on risk level
  - Birth preparedness checklist
  - What to bring to hospital
  - Transportation planning
  - Financial planning for delivery
  
- **Know labor signs and timing** (Escalation of risk)
  - Recognize true labor signs
  - When to go to hospital
  - Danger signs during labor
  - What to expect during delivery
  
- **Prepare as EDD approaches** (Effective treatment)
  - Final checkup reminders (36-40 weeks)
  - Baby position check
  - Group B Strep test (35-37 weeks)
  - Review birth plan

**Implementation Status:** Not yet implemented
- Future phase after core ANC features

---

### 7. Postpartum & Newborn Care
**Goal:** Screen for maternal mental health and support breastfeeding/newborn care

**Features:**
- **Screen for mental health issues** (Risk screening)
  - Edinburgh Postnatal Depression Scale questions
  - Identify signs of postpartum depression
  - Anxiety screening
  - Referral to mental health services
  
- **Get breastfeeding/SVN support** (Ease of access, Effective treatment)
  - Breastfeeding guidance and troubleshooting
  - Latch problems and solutions
  - Milk supply concerns
  - When to supplement
  - Connect to lactation consultants
  - Local breastfeeding support groups
  
- **Identify newborn danger signs** (Risk screening)
  - Feeding problems
  - Jaundice
  - Fever or hypothermia
  - Breathing difficulties
  - When to seek immediate care
  - Immunization schedule

**Implementation Status:** Not yet implemented
- Future phase, separate from pregnancy care

---

## Technical Implementation Map

### Current Architecture
```
User Call → Twilio
    ↓
Speech-to-Text (Twilio native, future: Whisper)
    ↓
Intent Classification → Route to appropriate use case
    ↓
Use Case Handler (e.g., test_screening.py)
    ↓
Knowledge Base (test_schedules.py, etc.)
    ↓
Claude API (natural language generation)
    ↓
Text-to-Speech (Twilio native)
    ↓
User hears response
```

### Files Mapping to Features

| Feature Category | Implementation Files | Status |
|-----------------|---------------------|--------|
| Early ANC | `anc1_timing.py`, `anc1_facility.py` | Partial |
| Facility Access | `facility_finder.py`, `facility_hours.py`, `facility_selection.py` | Not started |
| Test Scheduling | `test_screening.py`, `test_schedules.py` | Implemented |
| Visit Cadence | `visit_cadence.py`, `anc_guidelines.py` | Partial |
| Results Understanding | `results_understanding.py` | Not started |
| Supplement Adherence | `supplement_adherence.py`, `supplement_info.py` | Not started |
| Risk Monitoring | `risk_assessment.py` | Not started |
| Danger Signs | Need emergency service integration | Not started |
| Delivery Prep | New use case files needed | Not started |
| Postpartum | New use case files needed | Not started |