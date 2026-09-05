export interface HealthResponse {
  status: string;
  app_name: string;
  environment: string;
  timestamp: string;
}

export interface Resume {
  id: number;
  filename: string;
  file_type: string;
  page_count: number;
  file_hash: string;
  raw_text: string;
  uploaded_at: string;
}

export interface RecommendationItem {
  category: 'Impact' | 'Formatting' | 'Skills' | 'Structure' | string;
  priority: 'High' | 'Medium' | 'Low' | string;
  issue: string;
  suggestion: string;
}

export interface Analysis {
  id: number;
  resume_id: number;
  job_description_id?: number | null;
  overall_ats_score: number;
  skills_score: number;
  experience_score: number;
  formatting_score: number;
  candidate_name?: string | null;
  candidate_email?: string | null;
  candidate_phone?: string | null;
  summary?: string | null;
  matched_skills: string[];
  missing_skills: string[];
  strengths: string[];
  weaknesses: string[];
  recommendations: RecommendationItem[];
  created_at: string;
}

export interface BulletRewriteVariant {
  formula: string;
  text: string;
  rationale: string;
}

export interface BulletRewriteResponse {
  original_bullet: string;
  enhanced_variants: BulletRewriteVariant[];
}

export interface InterviewQuestion {
  category: string;
  question: string;
  context: string;
  suggested_talking_points: string[];
}

export interface InterviewPrepResponse {
  role_title: string;
  questions: InterviewQuestion[];
}
