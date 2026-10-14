import React, { useEffect, useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';
import { BarChart3, TrendingUp, AlertTriangle, CheckCircle2, Award, Sparkles } from 'lucide-react';
import { api } from '../api/client';
import { DashboardData, Topic } from '../types';

const COLORS = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'];

export const Analytics: React.FC = () => {
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.getDashboard(), api.getTopics()]).then(([dRes, tRes]) => {
      setDashboard(dRes);
      setTopics(tRes);
      setLoading(false);
    });
  }, []);

  if (loading || !dashboard) {
    return (
      <div className="p-8 flex flex-col items-center justify-center min-h-[50vh] text-slate-500 gap-3">
        <div className="w-8 h-8 border-3 border-blue-600 border-t-transparent rounded-full animate-spin" />
        <p className="text-sm font-medium">Computing performance analytics...</p>
      </div>
    );
  }

  // Prepare topic chart data (topics with attempts)
  const activeTopics = topics.filter((t) => t.total_questions > 0).slice(0, 8);
  const topicChartData = activeTopics.map((t) => ({
    name: t.name.length > 12 ? t.name.slice(0, 10) + '..' : t.name,
    mastery: t.mastery_score,
    accuracy: t.unassisted_accuracy
  }));

  // Mistake distribution data
  const errorChartData = dashboard.top_repeated_mistakes.map((m) => ({
    name: m.error_category.length > 15 ? m.error_category.slice(0, 13) + '..' : m.error_category,
    count: m.count
  }));

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      <div>
        <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900">Progress & Learning Analytics</h1>
        <p className="text-xs sm:text-sm text-slate-500">
          Transparent metrics derived from your real practice attempts and error diagnoses.
        </p>
      </div>

      {/* Summary KPI row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-1">
          <div className="text-xs font-bold text-slate-500 uppercase">Bank Coverage</div>
          <div className="text-2xl font-bold text-slate-900">
            {dashboard.total_attempted_unique} <span className="text-xs text-slate-400 font-normal">/ 1,800</span>
          </div>
          <div className="text-[11px] text-blue-600 font-medium">Distinct items attempted</div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-1">
          <div className="text-xs font-bold text-slate-500 uppercase">Independent Accuracy</div>
          <div className="text-2xl font-bold text-emerald-600">{dashboard.unassisted_accuracy}%</div>
          <div className="text-[11px] text-slate-500 font-medium">Without using hints</div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-1">
          <div className="text-xs font-bold text-slate-500 uppercase">Assisted Accuracy</div>
          <div className="text-2xl font-bold text-blue-600">{dashboard.overall_accuracy}%</div>
          <div className="text-[11px] text-slate-500 font-medium">Including hint assistance</div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-1">
          <div className="text-xs font-bold text-slate-500 uppercase">Revision Load</div>
          <div className="text-2xl font-bold text-amber-600">{dashboard.due_revisions_count}</div>
          <div className="text-[11px] text-amber-700 font-medium">Due in spaced schedule</div>
        </div>
      </div>

      {/* Actionable Coach Recommendation */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 space-y-2">
        <div className="flex items-center gap-2 text-blue-900 font-bold text-xs uppercase tracking-wider">
          <Sparkles className="w-4 h-4 text-blue-600" />
          <span>Diagnostic Recommendation from Learning Coach</span>
        </div>
        <p className="text-xs sm:text-sm text-blue-950 font-medium leading-relaxed">
          {dashboard.unassisted_accuracy < 50 && dashboard.total_attempted_unique > 0
            ? "Your unassisted accuracy is below placement threshold (70%). Focus on Guided Practice mode with progressive hints before attempting timed tests."
            : dashboard.topics_needing_improvement.length > 0
            ? `Your calculation setup is sound, but ${dashboard.topics_needing_improvement[0].topic_name} requires targeted practice. Work through the corrective exercises in your Mistake Notebook.`
            : "Strong performance across foundational categories! Transition to Timed Practice and Placement Mock Tests to lock in exam-speed accuracy."}
        </p>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Topic Mastery Bar Chart */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-4">
          <h3 className="text-sm font-bold text-slate-900">Topic Mastery & Accuracy Breakdown</h3>
          <div className="h-64 sm:h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topicChartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <XAxis dataKey="name" tick={{ fontSize: 11 }} angle={-25} textAnchor="end" />
                <YAxis tick={{ fontSize: 11 }} domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="mastery" fill="#2563eb" name="Mastery %" radius={[4, 4, 0, 0]} />
                <Bar dataKey="accuracy" fill="#10b981" name="Accuracy %" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Error Taxonomy Distribution */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-4">
          <h3 className="text-sm font-bold text-slate-900">Mistake Taxonomy Breakdown</h3>
          {errorChartData.length === 0 ? (
            <div className="h-64 flex items-center justify-center text-xs text-slate-400">
              No error data yet. Practice more questions to generate mistake taxonomy graphs.
            </div>
          ) : (
            <div className="h-64 sm:h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={errorChartData}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    dataKey="count"
                    label={({ name, percent }: { name?: string; percent?: number }) => `${name} (${((percent || 0) * 100).toFixed(0)}%)`}
                  >
                    {errorChartData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
