from fastapi import APIRouter
from app.schemas.schemas import BulletRewriteRequest, BulletRewriteResponse, InterviewPrepRequest, InterviewPrepResponse

router = APIRouter()

@router.post("/rewrite-bullet", response_model=BulletRewriteResponse, summary="Rewrite resume bullet using STAR/XYZ formula")
def rewrite_bullet(payload: BulletRewriteRequest):
    """Enhance a weak resume bullet point with metric-driven variants."""
    return BulletRewriteResponse(
        original_bullet=payload.bullet_text,
        enhanced_variants=[
            {
                "formula": "Google XYZ (Accomplished [X] as measured by [Y], by doing [Z])",
                "text": f"Engineered scalable backend service addressing {payload.bullet_text}, resulting in a 35% reduction in API latency and 99.9% uptime.",
                "rationale": "Directly links action to a measurable business outcome and reliability metric."
            },
            {
                "formula": "STAR Method (Situation, Task, Action, Result)",
                "text": f"Spearheaded technical optimization for {payload.target_role} workflows related to '{payload.bullet_text}', boosting operational throughput by 40%.",
                "rationale": "Demonstrates technical leadership and quantifiable operational enhancement."
            }
        ]
    )

@router.post("/interview-prep", response_model=InterviewPrepResponse, summary="Generate tailored interview questions")
def interview_prep(payload: InterviewPrepRequest):
    """Generate interview questions targeting missing skills and job requirements."""
    return InterviewPrepResponse(
        role_title=payload.role_title,
        questions=[
            {
                "category": "Technical",
                "question": f"How have you applied your core skills in {', '.join(payload.skills[:3]) if payload.skills else 'modern software engineering'} in production systems?",
                "context": "Assesses depth of production hands-on experience.",
                "suggested_talking_points": ["Architecture decisions", "Trade-offs considered", "Production monitoring"]
            },
            {
                "category": "Gap Exploration",
                "question": f"Given the role requires familiarity with {', '.join(payload.missing_skills[:2]) if payload.missing_skills else 'advanced tooling'}, how would you approach ramping up quickly?",
                "context": "Evaluates learning agility and adaptability to the target stack.",
                "suggested_talking_points": ["Proof of concept delivery", "Documentation reading", "Community best practices"]
            }
        ]
    )
