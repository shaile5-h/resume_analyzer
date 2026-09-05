import re
from typing import Dict, Any, List

# Standard resume section regex patterns
SECTION_PATTERNS = {
    "Experience": r"(?i)\b(work\s+experience|professional\s+experience|employment\s+history|experience|work\s+history)\b",
    "Education": r"(?i)\b(education|academic\s+background|academics|qualifications|degrees?)\b",
    "Skills": r"(?i)\b(skills|technical\s+skills|core\s+competencies|technologies|proficiencies|tools)\b",
    "Summary": r"(?i)\b(professional\s+summary|executive\s+summary|summary|profile|about\s+me|career\s+objective|objective)\b",
    "Projects": r"(?i)\b(projects|technical\s+projects|key\s+projects|personal\s+projects|portfolio)\b",
    "Certifications": r"(?i)\b(certifications|certificates|licenses|credentials|awards|honors)\b"
}

# Strong action verbs favored by ATS systems
STRONG_ACTION_VERBS = {
    "accelerated", "accomplished", "achieved", "acquired", "adapted", "administered", "advised",
    "analyzed", "architected", "audited", "automated", "built", "centralized", "championed",
    "coached", "collaborated", "compiled", "composed", "conducted", "configured", "consolidated",
    "constructed", "coordinated", "created", "decreased", "delivered", "deployed", "designed",
    "developed", "devised", "diagnosed", "directed", "documented", "drove", "eliminated",
    "engineered", "enhanced", "established", "evaluated", "executed", "expanded", "expedited",
    "formulated", "founded", "generated", "guided", "headed", "identified", "implemented",
    "improved", "increased", "initiated", "innovated", "inspected", "installed", "instituted",
    "integrated", "introduced", "invented", "investigated", "launched", "lead", "led", "leveraged",
    "managed", "maximized", "mentored", "migrated", "minimized", "modernized", "negotiated",
    "operated", "optimized", "orchestrated", "organized", "overhauled", "oversaw", "partnered",
    "pioneered", "planned", "prepared", "produced", "programmed", "promoted", "proposed",
    "published", "re-engineered", "rearchitected", "rebuilt", "recommended", "reconciled",
    "redesigned", "reduced", "refactored", "refined", "remodeled", "reorganized", "replaced",
    "resolved", "restructured", "revamped", "reviewed", "revitalized", "saved", "scaled",
    "scheduled", "secured", "simplified", "solved", "spearheaded", "standardized", "streamlined",
    "strengthened", "structured", "succeeded", "supervised", "synthesized", "systematized",
    "targeted", "tested", "tracked", "trained", "transformed", "unified", "upgraded", "utilized",
    "validated", "visualized"
}

def extract_contact_info(text: str) -> Dict[str, Any]:
    """Extract and validate contact fields using standard regex patterns."""
    # Email pattern
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    emails = re.findall(email_pattern, text)
    email = emails[0] if emails else None

    # Phone pattern (supports US, international, with optional dashes/spaces/parentheses)
    phone_pattern = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    phones = re.findall(phone_pattern, text)
    phone = phones[0] if phones else None

    # LinkedIn profile pattern
    linkedin_pattern = r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/(?:in|profile)\/[a-zA-Z0-9_-]+"
    linkedin_matches = re.findall(linkedin_pattern, text, re.IGNORECASE)
    linkedin = linkedin_matches[0] if linkedin_matches else None

    # GitHub profile pattern
    github_pattern = r"(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]+"
    github_matches = re.findall(github_pattern, text, re.IGNORECASE)
    github = github_matches[0] if github_matches else None

    return {
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
    }

def detect_sections(text: str) -> Dict[str, List[str]]:
    """Detect which standard ATS sections are present vs missing."""
    detected = []
    missing = []

    for section_name, pattern in SECTION_PATTERNS.items():
        if re.search(pattern, text):
            detected.append(section_name)
        else:
            missing.append(section_name)

    return {"detected": detected, "missing": missing}

def count_quantifiable_metrics(text: str) -> List[str]:
    """Find metrics indicating quantified achievements (%, $, numbers, multipliers)."""
    metric_patterns = [
        r"\b\d+%\b",                                       # Percentages: 25%, 100%
        r"[\$€£]\s?\d+(?:,\d{3})*(?:\.\d+)?(?:\s?[kKmMbB])?", # Currency: $50k, $1.2M
        r"\b\d+(?:\.\d+)?\s?[kKmMbB]\b",                  # Quantities: 10k, 2M
        r"\b\d+\s*(?:x|times)\b",                         # Multipliers: 5x, 10 times
        r"\b\d+\+?\s+(?:users|clients|customers|requests|queries|downloads|endpoints|features)\b" # Quantified items
    ]
    matches = []
    for pat in metric_patterns:
        found = re.findall(pat, text, re.IGNORECASE)
        matches.extend(found)
    return list(set(matches))

def count_action_verbs(text: str) -> List[str]:
    """Identify instances of strong action verbs across the resume text."""
    words = set(re.findall(r"\b[a-zA-Z-]+\b", text.lower()))
    found_verbs = words.intersection(STRONG_ACTION_VERBS)
    return sorted(list(found_verbs))

def audit_resume_parsability(raw_text: str, page_count: int, file_type: str) -> Dict[str, Any]:
    """
    Runs deterministic ATS audit evaluating formatting, parsability, contact info,
    section integrity, and metric density without LLM dependencies.
    """
    contact_info = extract_contact_info(raw_text)
    sections = detect_sections(raw_text)
    metrics = count_quantifiable_metrics(raw_text)
    action_verbs = count_action_verbs(raw_text)

    words = raw_text.split()
    word_count = len(words)

    # -------------------------------------------------------------
    # 1. Contact Score (Max 25 pts)
    # -------------------------------------------------------------
    contact_score = 0.0
    if contact_info["email"]:
        contact_score += 10.0
    if contact_info["phone"]:
        contact_score += 8.0
    if contact_info["linkedin"]:
        contact_score += 4.0
    if contact_info["github"]:
        contact_score += 3.0

    # -------------------------------------------------------------
    # 2. Section Structure Score (Max 35 pts)
    # -------------------------------------------------------------
    section_score = 0.0
    detected_set = set(sections["detected"])
    if "Experience" in detected_set:
        section_score += 12.0
    if "Skills" in detected_set:
        section_score += 10.0
    if "Education" in detected_set:
        section_score += 8.0
    if "Summary" in detected_set:
        section_score += 3.0
    if "Projects" in detected_set or "Certifications" in detected_set:
        section_score += 2.0

    # -------------------------------------------------------------
    # 3. Length & Density Score (Max 20 pts)
    # -------------------------------------------------------------
    length_score = 0.0
    # Page count check (1-2 pages is ideal)
    if page_count in [1, 2]:
        length_score += 10.0
    elif page_count == 3:
        length_score += 5.0
    else:
        length_score += 2.0 # Penalty for >3 pages

    # Word count check (ideal density ~350-1000 words)
    if 350 <= word_count <= 1100:
        length_score += 10.0
    elif word_count < 350:
        length_score += max(2.0, (word_count / 350.0) * 10.0)
    else:
        length_score += 6.0 # Slightly verbose

    # -------------------------------------------------------------
    # 4. Action Verbs & Metrics Score (Max 20 pts)
    # -------------------------------------------------------------
    content_score = 0.0
    # Verbs (up to 10 pts)
    content_score += min(10.0, len(action_verbs) * 1.5)
    # Metrics (up to 10 pts)
    content_score += min(10.0, len(metrics) * 2.5)

    # Total Formatting Score (0 - 100)
    total_formatting_score = round(contact_score + section_score + length_score + content_score, 1)

    # -------------------------------------------------------------
    # Actionable Recommendations Generation
    # -------------------------------------------------------------
    recommendations = []

    # Contact recommendations
    if not contact_info["email"]:
        recommendations.append({
            "category": "Contact Information",
            "priority": "High",
            "issue": "Missing email address",
            "suggestion": "Include a professional email address prominently in the resume header."
        })
    if not contact_info["phone"]:
        recommendations.append({
            "category": "Contact Information",
            "priority": "High",
            "issue": "Missing phone number",
            "suggestion": "Add a reachable phone number with country code for recruiter phone screens."
        })
    if not contact_info["linkedin"]:
        recommendations.append({
            "category": "Contact Information",
            "priority": "Medium",
            "issue": "No LinkedIn profile detected",
            "suggestion": "Include a customized LinkedIn URL (e.g. linkedin.com/in/yourname)."
        })

    # Section recommendations
    if "Experience" not in detected_set:
        recommendations.append({
            "category": "Structure",
            "priority": "High",
            "issue": "Standard 'Experience' section missing or non-standard heading",
            "suggestion": "Label your work history with clear, standard ATS headers such as 'Professional Experience' or 'Work History'."
        })
    if "Skills" not in detected_set:
        recommendations.append({
            "category": "Structure",
            "priority": "High",
            "issue": "Skills section missing",
            "suggestion": "Create a dedicated 'Technical Skills' section listing languages, frameworks, and cloud tooling."
        })
    if "Education" not in detected_set:
        recommendations.append({
            "category": "Structure",
            "priority": "Medium",
            "issue": "Education section missing",
            "suggestion": "Add an 'Education' section specifying degrees, institutions, and graduation years."
        })

    # Length & metric recommendations
    if page_count > 2:
        recommendations.append({
            "category": "Formatting",
            "priority": "Medium",
            "issue": f"Resume length ({page_count} pages) is above standard limits",
            "suggestion": "Trim older roles or condensing bullet points to keep your resume to 1-2 pages."
        })
    if len(metrics) < 3:
        recommendations.append({
            "category": "Impact",
            "priority": "High",
            "issue": f"Low quantifiable metric density ({len(metrics)} detected)",
            "suggestion": "Quantify your achievements using numbers, percentages, or dollar values (e.g., 'Improved performance by 30%')."
        })
    if len(action_verbs) < 5:
        recommendations.append({
            "category": "Impact",
            "priority": "Medium",
            "issue": "Limited strong action verbs detected",
            "suggestion": "Start bullet points with high-impact verbs like 'Architected', 'Spearheaded', 'Engineered', or 'Automated'."
        })

    return {
        "formatting_score": total_formatting_score,
        "breakdown": {
            "contact_score": round(contact_score, 1),
            "section_score": round(section_score, 1),
            "length_score": round(length_score, 1),
            "content_score": round(content_score, 1)
        },
        "contact_info": contact_info,
        "sections": sections,
        "word_count": word_count,
        "page_count": page_count,
        "file_type": file_type,
        "quantifiable_metrics": metrics[:10],
        "action_verbs": action_verbs,
        "recommendations": recommendations
    }
