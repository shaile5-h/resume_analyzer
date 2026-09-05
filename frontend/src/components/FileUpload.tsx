import React, { useState, useRef } from 'react';
import { resumeApi } from '../services/api';
import { ResumeUploadResponse } from '../types';
import {
  UploadCloud,
  FileText,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Clock,
  Sparkles,
  Zap,
  Mail,
  Phone,
  Linkedin,
  Github
} from 'lucide-react';

interface FileUploadProps {
  onUploadSuccess?: (data: ResumeUploadResponse) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [uploadResult, setUploadResult] = useState<ResumeUploadResponse | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragging(true);
    } else if (e.type === 'dragleave') {
      setIsDragging(false);
    }
  };

  const processFile = async (file: File) => {
    setErrorMsg(null);

    // Validate extension
    const ext = file.name.split('.').pop()?.toLowerCase();
    if (ext !== 'pdf' && ext !== 'docx') {
      setErrorMsg('Please upload a valid PDF (.pdf) or Word document (.docx).');
      return;
    }

    // Validate size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      setErrorMsg('File size exceeds the 10MB limit. Please upload a smaller file.');
      return;
    }

    setIsUploading(true);
    try {
      const data = await resumeApi.uploadResume(file);
      setUploadResult(data);
      if (onUploadSuccess) {
        onUploadSuccess(data);
      }
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Failed to upload and parse resume. Ensure backend is running.';
      setErrorMsg(msg);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  return (
    <div className="space-y-6">
      {/* Drag & Drop Card */}
      <div
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center transition-all cursor-pointer ${
          isDragging
            ? 'border-indigo-600 bg-indigo-50/60 scale-[1.01]'
            : 'border-slate-300 hover:border-indigo-400 bg-white hover:bg-slate-50/50 shadow-sm'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx"
          onChange={handleFileInputChange}
          className="hidden"
        />

        <div className="max-w-md mx-auto flex flex-col items-center">
          <div className="w-16 h-16 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-4 shadow-sm shadow-indigo-100">
            {isUploading ? (
              <Zap className="w-8 h-8 animate-pulse text-indigo-600" />
            ) : (
              <UploadCloud className="w-8 h-8" />
            )}
          </div>

          <h3 className="text-lg font-bold text-slate-900 mb-1">
            {isUploading ? 'Ingesting & Auditing Resume...' : 'Upload your resume (PDF or DOCX)'}
          </h3>
          <p className="text-xs sm:text-sm text-slate-500 mb-4">
            Drag and drop your file here, or click to browse. Max size 10MB.
          </p>

          <div className="flex items-center space-x-3 text-xs text-slate-400">
            <span className="flex items-center">
              <FileText className="w-3.5 h-3.5 mr-1 text-slate-500" />
              PDF & DOCX
            </span>
            <span>&bull;</span>
            <span>PyMuPDF Text Engine</span>
            <span>&bull;</span>
            <span>Deterministic ATS Audit</span>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm flex items-center space-x-2">
          <XCircle className="w-5 h-5 shrink-0 text-rose-600" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Upload & ATS Audit Results Card */}
      {uploadResult && (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-6">
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 gap-2">
            <div>
              <div className="flex items-center space-x-2">
                <FileText className="w-5 h-5 text-indigo-600" />
                <h3 className="text-base font-bold text-slate-900">{uploadResult.filename}</h3>
                {uploadResult.is_cached && (
                  <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center">
                    <Zap className="w-3 h-3 mr-1" /> SHA-256 Cached
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-500 mt-0.5">
                Format: <strong className="uppercase">{uploadResult.file_type}</strong> &bull; {uploadResult.page_count} {uploadResult.page_count === 1 ? 'page' : 'pages'} &bull; {uploadResult.word_count} words
              </p>
            </div>

            {/* Score Ring / Badge */}
            <div className="flex items-center space-x-3 self-start sm:self-auto">
              <div className="text-right">
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">
                  ATS Parsability Score
                </span>
                <span className={`text-2xl font-extrabold ${
                  uploadResult.audit.formatting_score >= 80 ? 'text-emerald-600' : uploadResult.audit.formatting_score >= 60 ? 'text-amber-600' : 'text-rose-600'
                }`}>
                  {uploadResult.audit.formatting_score}<span className="text-sm font-normal text-slate-400">/100</span>
                </span>
              </div>
            </div>
          </div>

          {/* Contact Details & Metric Badges */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            <div className={`p-3 rounded-xl border text-xs flex items-center space-x-2.5 ${
              uploadResult.audit.contact_info.email ? 'bg-emerald-50/50 border-emerald-200 text-emerald-900' : 'bg-rose-50/50 border-rose-200 text-rose-900'
            }`}>
              <Mail className="w-4 h-4 shrink-0" />
              <div className="truncate">
                <div className="font-semibold">Email</div>
                <div className="truncate font-mono">{uploadResult.audit.contact_info.email || 'Missing'}</div>
              </div>
            </div>

            <div className={`p-3 rounded-xl border text-xs flex items-center space-x-2.5 ${
              uploadResult.audit.contact_info.phone ? 'bg-emerald-50/50 border-emerald-200 text-emerald-900' : 'bg-rose-50/50 border-rose-200 text-rose-900'
            }`}>
              <Phone className="w-4 h-4 shrink-0" />
              <div className="truncate">
                <div className="font-semibold">Phone</div>
                <div className="truncate font-mono">{uploadResult.audit.contact_info.phone || 'Missing'}</div>
              </div>
            </div>

            <div className={`p-3 rounded-xl border text-xs flex items-center space-x-2.5 ${
              uploadResult.audit.contact_info.linkedin ? 'bg-emerald-50/50 border-emerald-200 text-emerald-900' : 'bg-slate-50 border-slate-200 text-slate-600'
            }`}>
              <Linkedin className="w-4 h-4 shrink-0" />
              <div className="truncate">
                <div className="font-semibold">LinkedIn</div>
                <div className="truncate">{uploadResult.audit.contact_info.linkedin ? 'Detected' : 'Not detected'}</div>
              </div>
            </div>

            <div className={`p-3 rounded-xl border text-xs flex items-center space-x-2.5 ${
              uploadResult.audit.contact_info.github ? 'bg-emerald-50/50 border-emerald-200 text-emerald-900' : 'bg-slate-50 border-slate-200 text-slate-600'
            }`}>
              <Github className="w-4 h-4 shrink-0" />
              <div className="truncate">
                <div className="font-semibold">GitHub</div>
                <div className="truncate">{uploadResult.audit.contact_info.github ? 'Detected' : 'Not detected'}</div>
              </div>
            </div>
          </div>

          {/* Section Headers Detected */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2.5">
              Standard ATS Section Headers
            </h4>
            <div className="flex flex-wrap gap-2">
              {uploadResult.audit.sections.detected.map((sec) => (
                <span
                  key={sec}
                  className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200"
                >
                  <CheckCircle2 className="w-3.5 h-3.5 mr-1.5 text-emerald-600" />
                  {sec}
                </span>
              ))}
              {uploadResult.audit.sections.missing.map((sec) => (
                <span
                  key={sec}
                  className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium bg-amber-50 text-amber-700 border border-amber-200"
                >
                  <AlertTriangle className="w-3.5 h-3.5 mr-1.5 text-amber-600" />
                  Missing: {sec}
                </span>
              ))}
            </div>
          </div>

          {/* Action Verbs & Quantified Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
              <span className="text-xs font-bold text-slate-700 block mb-2">
                Strong Action Verbs ({uploadResult.audit.action_verbs.length} detected)
              </span>
              <div className="flex flex-wrap gap-1.5 max-h-24 overflow-y-auto">
                {uploadResult.audit.action_verbs.slice(0, 15).map((verb) => (
                  <span key={verb} className="px-2 py-0.5 rounded bg-white text-slate-700 text-[11px] font-mono border border-slate-200">
                    {verb}
                  </span>
                ))}
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
              <span className="text-xs font-bold text-slate-700 block mb-2">
                Quantified Metrics ({uploadResult.audit.quantifiable_metrics.length} detected)
              </span>
              <div className="flex flex-wrap gap-1.5 max-h-24 overflow-y-auto">
                {uploadResult.audit.quantifiable_metrics.map((metric, i) => (
                  <span key={i} className="px-2 py-0.5 rounded bg-white text-indigo-700 text-[11px] font-mono border border-indigo-200">
                    {metric}
                  </span>
                ))}
                {uploadResult.audit.quantifiable_metrics.length === 0 && (
                  <span className="text-xs text-slate-400 italic">No quantifiable metrics detected</span>
                )}
              </div>
            </div>
          </div>

          {/* ATS Formatting Recommendations */}
          {uploadResult.audit.recommendations.length > 0 && (
            <div className="space-y-2 pt-2">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                Actionable ATS Formatting Improvements
              </h4>
              <div className="space-y-2">
                {uploadResult.audit.recommendations.map((rec, i) => (
                  <div key={i} className="p-3 rounded-xl border border-slate-200 bg-slate-50/50 flex items-start space-x-3 text-xs">
                    <span className={`px-2 py-0.5 rounded font-semibold text-[10px] shrink-0 uppercase tracking-wide ${
                      rec.priority === 'High' ? 'bg-rose-100 text-rose-700 border border-rose-200' : 'bg-amber-100 text-amber-700 border border-amber-200'
                    }`}>
                      {rec.priority}
                    </span>
                    <div className="space-y-0.5">
                      <div className="font-semibold text-slate-800">{rec.issue}</div>
                      <div className="text-slate-600">{rec.suggestion}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
