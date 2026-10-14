import React from 'react';

export default function AIModePage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">How Our AI Works</h1>
      
      <div className="prose prose-lg">
        <p className="lead text-xl text-gray-600 mb-8">
          RentMate uses Natural Language Processing (NLP) to understand the <em>intent</em> behind your search, not just the keywords.
        </p>

        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 mb-8">
          <h2 className="text-2xl font-bold mb-4">The Pipeline</h2>
          <ol className="list-decimal pl-5 space-y-4">
            <li><strong>User Requirement:</strong> You type "I need cooling for a small event."</li>
            <li><strong>Natural Language Processing:</strong> The AI reads the sentence and extracts context (cooling, small event).</li>
            <li><strong>Semantic Embedding:</strong> We use <code className="bg-gray-100 px-2 py-1 rounded">sentence-transformers</code> to convert your sentence into a high-dimensional math vector.</li>
            <li><strong>Item Embedding:</strong> All items in our database (e.g., Table Fan, Air Cooler, Projector) are already converted into vectors.</li>
            <li><strong>Cosine Similarity:</strong> The system calculates the distance between your vector and the item vectors.</li>
            <li><strong>Filtering:</strong> We remove items that are booked for your dates or outside your location.</li>
            <li><strong>Final Ranking:</strong> Items with the highest similarity score are recommended.</li>
          </ol>
        </div>

        <div className="bg-emerald-50 p-8 rounded-2xl border border-emerald-100">
          <h3 className="text-xl font-bold text-emerald-900 mb-2">Math Made Simple</h3>
          <p className="text-emerald-800 mb-4">
            Cosine Similarity measures the angle between two lines (vectors). If they point in the exact same direction, the similarity is 100%. If they are perpendicular, the similarity is 0%.
          </p>
          <code className="block bg-emerald-900 text-emerald-100 p-4 rounded-lg font-mono text-sm">
            similarity(A,B) = (A · B) / (||A|| * ||B||)
          </code>
        </div>
      </div>
    </div>
  );
}
