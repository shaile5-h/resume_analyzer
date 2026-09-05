import axios from 'axios';
import {
  HealthResponse,
  Resume,
  Analysis,
  BulletRewriteResponse,
  InterviewPrepResponse
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

export const resumeApi = {
  // Health check
  checkHealth: async (): Promise<HealthResponse> => {
    const response = await apiClient.get<HealthResponse>('/health');
    return response.data;
  },

  // Resumes
  listResumes: async (): Promise<Resume[]> => {
    const response = await apiClient.get<Resume[]>('/api/v1/resumes/');
    return response.data;
  },

  getResume: async (id: number): Promise<Resume> => {
    const response = await apiClient.get<Resume>(`/api/v1/resumes/${id}`);
    return response.data;
  },

  // Analyses
  listAnalyses: async (): Promise<Analysis[]> => {
    const response = await apiClient.get<Analysis[]>('/api/v1/analyses/history');
    return response.data;
  },

  getAnalysis: async (id: number): Promise<Analysis> => {
    const response = await apiClient.get<Analysis>(`/api/v1/analyses/${id}`);
    return response.data;
  },

  // Career Copilot
  rewriteBullet: async (bulletText: string, targetRole: string = 'Software Engineer'): Promise<BulletRewriteResponse> => {
    const response = await apiClient.post<BulletRewriteResponse>('/api/v1/copilot/rewrite-bullet', {
      bullet_text: bulletText,
      target_role: targetRole,
    });
    return response.data;
  },

  getInterviewPrep: async (
    roleTitle: string,
    skills: string[],
    missingSkills: string[]
  ): Promise<InterviewPrepResponse> => {
    const response = await apiClient.post<InterviewPrepResponse>('/api/v1/copilot/interview-prep', {
      role_title: roleTitle,
      skills: skills,
      missing_skills: missingSkills,
    });
    return response.data;
  },
};
