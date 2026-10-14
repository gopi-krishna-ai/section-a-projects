import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import {
  BookOpen, Sparkles, AlertCircle, ArrowRight, CheckCircle2,
  Lock, BookCheck, HelpCircle, Layers, Lightbulb, Zap
} from 'lucide-react';
import { api } from '../api/client';
import { Topic, ConceptLesson } from '../types';

export const Learn: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopicId, setSelectedTopicId] = useState<string>('percentages');
  const [lesson, setLesson] = useState<ConceptLesson | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [loading, setLoading] = useState(true);
  const [lessonLoading, setLessonLoading] = useState(false);

  useEffect(() => {
    loadTopics();
  }, []);

  const loadTopics = async () => {
    try {
      setLoading(true);
      const res = await api.getTopics();
      setTopics(res);

      const topicFromUrl = searchParams.get('topic');
      if (topicFromUrl && res.some((t) => t.id === topicFromUrl)) {
        setSelectedTopicId(topicFromUrl);
        loadLesson(topicFromUrl);
      } else if (res.length > 0) {
        setSelectedTopicId(res[0].id);
        loadLesson(res[0].id);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadLesson = async (topicId: string) => {
    setLessonLoading(true);
    try {
      const res = await api.getTopicLesson(topicId);
      setLesson(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLessonLoading(false);
    }
  };

  const handleSelectTopic = (topicId: string) => {
    setSelectedTopicId(topicId);
    setSearchParams({ topic: topicId });
    loadLesson(topicId);
  };

  const categories = ['All', ...new Set(topics.map((t) => t.category))];
  const filteredTopics = selectedCategory === 'All'
    ? topics
    : topics.filter((t) => t.category === selectedCategory);

  const selectedTopic = topics.find((t) => t.id === selectedTopicId);

  if (loading) {
    return (
      <div className="p-8 flex flex-col items-center justify-center min-h-[50vh] text-slate-500 gap-3">
        <div className="w-8 h-8 border-3 border-blue-600 border-t-transparent rounded-full animate-spin" />
        <p className="text-sm font-medium">Loading syllabus and concept lessons...</p>
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Category Filter Pills */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3.5 py-1.5 rounded-full whitespace-nowrap font-medium transition-colors cursor-pointer ${
              selectedCategory === cat
                ? 'bg-blue-600 text-white font-bold shadow-xs'
                : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Main 2-Column Syllabus & Lesson Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Topic Syllabus List (4 Cols) */}
        <div className="lg:col-span-4 bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden flex flex-col max-h-[82vh]">
          <div className="px-4 py-3 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-700 uppercase tracking-wider">
              <Layers className="w-4 h-4 text-blue-600" />
              <span>Syllabus Topics ({filteredTopics.length})</span>
            </div>
          </div>

          <div className="divide-y divide-slate-100 overflow-y-auto flex-1">
            {filteredTopics.map((t) => {
              const isSelected = t.id === selectedTopicId;
              return (
                <div
                  key={t.id}
                  onClick={() => handleSelectTopic(t.id)}
                  className={`p-3.5 transition-colors cursor-pointer flex flex-col gap-1 ${
                    isSelected
                      ? 'bg-blue-50/80 border-l-4 border-blue-600'
                      : 'hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-900">{t.name}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded-full font-semibold bg-slate-100 text-slate-600">
                      {t.total_questions} Qs
                    </span>
                  </div>
                  <div className="text-[11px] text-slate-500 line-clamp-1">{t.category}</div>
                  <div className="flex items-center justify-between mt-1 text-[10px]">
                    <span className={`font-semibold capitalize ${
                      t.status === 'proficient' ? 'text-emerald-600' :
                      t.status === 'learning' ? 'text-blue-600' :
                      t.status === 'needs_practice' ? 'text-amber-600' : 'text-slate-400'
                    }`}>
                      {t.status.replace('_', ' ')}
                    </span>
                    <span className="font-bold text-slate-600">{t.mastery_score}% mastery</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Structured Lesson Content (8 Cols) */}
        <div className="lg:col-span-8 bg-white rounded-xl border border-slate-200 shadow-xs p-6 space-y-6">
          {lessonLoading ? (
            <div className="py-20 flex flex-col items-center justify-center text-slate-400 gap-2">
              <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
              <p className="text-xs">Loading structured lesson...</p>
            </div>
          ) : lesson ? (
            <div className="space-y-6">
              {/* Header & Quick Action */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-200">
                <div>
                  <span className="text-xs font-bold text-blue-600 uppercase tracking-wider">
                    {lesson.category}
                  </span>
                  <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900">
                    {lesson.title}
                  </h2>
                </div>
                <button
                  onClick={() => navigate(`/workspace?topic=${lesson.topic_id}`)}
                  className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs sm:text-sm flex items-center justify-center gap-1.5 shadow-sm transition-all cursor-pointer shrink-0"
                >
                  <Zap className="w-4 h-4 text-amber-300" />
                  <span>Practice Questions ({selectedTopic?.total_questions || 100})</span>
                </button>
              </div>

              {/* 1. Concept Definition & Why Needed */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                  <div className="text-xs font-bold text-slate-800 mb-1 flex items-center gap-1.5">
                    <BookCheck className="w-4 h-4 text-blue-600" />
                    <span>What is the Concept?</span>
                  </div>
                  <p className="text-xs sm:text-sm text-slate-700 leading-relaxed font-medium">
                    {lesson.concept_summary}
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                  <div className="text-xs font-bold text-slate-800 mb-1 flex items-center gap-1.5">
                    <Lightbulb className="w-4 h-4 text-amber-500" />
                    <span>Why Do We Need It?</span>
                  </div>
                  <p className="text-xs sm:text-sm text-slate-700 leading-relaxed font-medium">
                    {lesson.why_needed}
                  </p>
                </div>
              </div>

              {/* 2. Simple Explanation & Real World Example */}
              <div className="p-4 rounded-xl bg-blue-50/60 border border-blue-100 space-y-2">
                <div className="text-xs font-bold text-blue-900 flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-blue-600" />
                  <span>Plain English Explanation</span>
                </div>
                <p className="text-xs sm:text-sm text-blue-950 leading-relaxed font-medium">
                  {lesson.simple_explanation}
                </p>
                {lesson.real_world_example && (
                  <div className="pt-2 text-xs text-blue-900 border-t border-blue-200/60 font-medium">
                    <span className="font-bold">Real-World Case:</span> {lesson.real_world_example}
                  </div>
                )}
              </div>

              {/* 3. Underlying Intuition */}
              <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200/80">
                <div className="text-xs font-bold text-amber-900 mb-1 flex items-center gap-1.5">
                  <AlertCircle className="w-4 h-4 text-amber-600" />
                  <span>Underlying Problem-Solving Intuition</span>
                </div>
                <p className="text-xs sm:text-sm text-amber-950 leading-relaxed font-medium">
                  {lesson.intuition}
                </p>
              </div>

              {/* 4. Formulas with 'Why Works' & 'When to Use' */}
              {lesson.formulas && lesson.formulas.length > 0 && (
                <div className="space-y-3">
                  <h3 className="text-sm font-bold text-slate-900">Governing Formulas & Principles</h3>
                  <div className="space-y-3">
                    {lesson.formulas.map((f, i) => (
                      <div key={i} className="p-3.5 rounded-xl border border-slate-200 bg-slate-50/70">
                        <div className="text-xs font-bold text-slate-800">{f.name}</div>
                        <div className="my-1.5 font-mono text-sm font-bold text-blue-700 bg-white px-3 py-1.5 rounded-lg border border-slate-200 inline-block">
                          {f.formula}
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2 text-xs">
                          <div className="text-slate-600">
                            <span className="font-semibold text-slate-800">Why it works:</span> {f.why_works}
                          </div>
                          <div className="text-slate-600">
                            <span className="font-semibold text-slate-800">When to use:</span> {f.when_to_use}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 5. Step-by-Step Worked Example */}
              {lesson.step_by_step_example && lesson.step_by_step_example.question && (
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
                  <div className="text-xs font-bold text-slate-800">Guided Step-by-Step Demonstration</div>
                  <div className="text-xs sm:text-sm font-semibold text-slate-900">
                    Q: {lesson.step_by_step_example.question}
                  </div>
                  <div className="space-y-1.5 pl-3 border-l-2 border-blue-500">
                    {lesson.step_by_step_example.steps?.map((st, i) => (
                      <div key={i} className="text-xs text-slate-700 font-medium">
                        {st}
                      </div>
                    ))}
                  </div>
                  <div className="p-2.5 rounded-lg bg-emerald-50 border border-emerald-200 text-xs text-emerald-900 font-bold">
                    Result: {lesson.step_by_step_example.solution}
                  </div>
                </div>
              )}

              {/* 6. Placement-Level Trap & Solution */}
              {lesson.placement_example && lesson.placement_example.question && (
                <div className="p-4 rounded-xl bg-indigo-50/60 border border-indigo-200 space-y-2">
                  <div className="text-xs font-bold text-indigo-900 flex items-center justify-between">
                    <span>Placement-Level Example</span>
                    <span className="px-2 py-0.5 rounded-full bg-indigo-200 text-indigo-900 text-[10px] font-bold">
                      Exam Trap
                    </span>
                  </div>
                  <div className="text-xs sm:text-sm font-semibold text-indigo-950">
                    {lesson.placement_example.question}
                  </div>
                  <div className="text-xs text-indigo-900 leading-relaxed font-medium">
                    <span className="font-bold">Correct Approach:</span> {lesson.placement_example.approach}
                  </div>
                  <div className="text-xs text-indigo-900 font-medium">
                    <span className="font-bold">Solution:</span> {lesson.placement_example.solution}
                  </div>
                  {lesson.placement_example.trap && (
                    <div className="p-2 rounded-lg bg-rose-50 border border-rose-200 text-xs text-rose-900 font-medium">
                      <span className="font-bold">Common Pitfall:</span> {lesson.placement_example.trap}
                    </div>
                  )}
                </div>
              )}

              {/* 7. Common Traps & Key Takeaways */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {lesson.common_traps && lesson.common_traps.length > 0 && (
                  <div className="p-4 rounded-xl bg-rose-50/60 border border-rose-200 space-y-2">
                    <div className="text-xs font-bold text-rose-900">Common Traps & Misconceptions</div>
                    <ul className="list-disc pl-4 space-y-1 text-xs text-rose-950 font-medium">
                      {lesson.common_traps.map((trap, idx) => (
                        <li key={idx}>{trap}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {lesson.key_takeaways && lesson.key_takeaways.length > 0 && (
                  <div className="p-4 rounded-xl bg-emerald-50/60 border border-emerald-200 space-y-2">
                    <div className="text-xs font-bold text-emerald-900">Key Takeaways for Placement</div>
                    <ul className="list-disc pl-4 space-y-1 text-xs text-emerald-950 font-medium">
                      {lesson.key_takeaways.map((takeaway, idx) => (
                        <li key={idx}>{takeaway}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Bottom CTA to practice */}
              <div className="pt-4 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-3 bg-blue-50/50 p-4 rounded-xl border">
                <div>
                  <h4 className="text-sm font-bold text-slate-900">Ready to test your understanding?</h4>
                  <p className="text-xs text-slate-600">Solve 100 verified placement questions on {selectedTopic?.name || 'this topic'} with the step-by-step AI coach.</p>
                </div>
                <button
                  onClick={() => navigate(`/workspace?topic=${lesson.topic_id}`)}
                  className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs sm:text-sm flex items-center justify-center gap-2 shadow-md shadow-blue-500/20 transition-all cursor-pointer shrink-0"
                >
                  <Zap className="w-4 h-4 text-amber-300" />
                  <span>Start Practicing ({selectedTopic?.total_questions || 100} Qs)</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          ) : (
            <div className="py-12 text-center text-slate-400 text-sm">
              Select a topic from the syllabus to view its concept lesson.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
