# ==============================
# IMPORT LIBRARIES
# ==============================

import spacy

# ==============================
# LOAD NLP MODEL
# ==============================

nlp = spacy.load("en_core_web_sm")

# ==============================
# SKILLS DATABASE
# ==============================

SKILLS_DB = [
    "python",
    "sql",
    "machine learning",
    "data analysis",
    "excel",
    "power bi",
    "tableau",
    "deep learning",
    "statistics",
    "communication",
    "leadership",
    "pandas",
    "numpy"
]

# ==============================
# PREPROCESS TEXT
# ==============================

def preprocess(text):

    return text.lower().strip()

# ==============================
# EXTRACT SKILLS
# ==============================

def extract_skills(text):

    found_skills = [
        skill for skill in SKILLS_DB
        if skill in text
    ]

    return found_skills

# ==============================
# CONTENT QUALITY
# ==============================

def content_quality(text):

    doc = nlp(text)

    words = [
        token for token in doc
        if not token.is_stop
    ]

    word_count = len(words)

    weak_words = [
        "hardworking",
        "motivated",
        "looking for job"
    ]

    weak_count = sum(
        1 for w in weak_words
        if w in text
    )

    return word_count, weak_count

# ==============================
# MAIN ANALYSIS FUNCTION
# ==============================

def analyze_profile(text):

    clean_text = preprocess(text)

    skills = extract_skills(clean_text)

    word_count, weak_words = content_quality(
        clean_text
    )

    # ==============================
    # SCORE CALCULATION
    # ==============================

    skill_score = len(skills) * 8

    length_score = min(word_count, 40)

    weak_penalty = weak_words * 3

    total_score = (
        skill_score +
        length_score -
        weak_penalty
    )

    total_score = max(
        0,
        min(total_score, 100)
    )

    # ==============================
    # SUGGESTIONS
    # ==============================

    suggestions = []

    if len(skills) < 4:
        suggestions.append(
            "Add more relevant technical skills."
        )

    if word_count < 30:
        suggestions.append(
            "Expand your profile summary."
        )

    if weak_words > 0:
        suggestions.append(
            "Avoid vague terms like 'hardworking'."
        )

    # ==============================
    # RETURN RESULTS
    # ==============================

    return {

        "score": total_score,

        "skills_found": skills,

        "word_count": word_count,

        "grammar_errors": 0,

        "weak_phrases": weak_words,

        "suggestions": suggestions
    }