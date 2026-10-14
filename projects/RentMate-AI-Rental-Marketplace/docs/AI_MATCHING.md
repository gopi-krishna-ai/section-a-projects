# RentMate AI Matching Engine

This document explains how RentMate uses Natural Language Processing (NLP) to connect renters with the items they need, even if they don't know the exact name of the item.

## 1. The Core Idea

Traditional search engines rely on keyword matching. If you search for "chair", you only see items with "chair" in the title or description.

RentMate uses **Semantic Search**. This means the AI understands the *meaning* and *context* of your request.
For example, if you write: *"I am organizing an outdoor movie night"*, the AI understands that you likely need a Projector, a Projector Screen, and a Speaker.

## 2. How It Works (Step-by-Step)

### A. Sentence Embeddings
We use a lightweight NLP model called `sentence-transformers` (`all-MiniLM-L6-v2`).
This model reads a piece of text and converts it into a high-dimensional mathematical vector (a list of 384 numbers).
- **Item Vectors:** When an owner lists a "Table Fan", we combine its name, category, and description, and generate an embedding vector. This is stored in memory.
- **Query Vector:** When you type *"I need cooling"*, we generate an embedding vector for that specific sentence in real-time.

### B. Cosine Similarity
To figure out which items match your query, we use a mathematical formula called **Cosine Similarity**.
Cosine Similarity measures the angle between two vectors.
- If the vectors point in the exact same direction (angle = 0°), the similarity is 1.0 (100%).
- If they point in completely different directions (angle = 90°), the similarity is 0.0 (0%).

**The Formula:**
`similarity(A,B) = (A · B) / (||A|| * ||B||)`

*In simple terms: It calculates how much the "meaning" of your sentence overlaps with the "meaning" of the item's description.*

### C. Filtering & Ranking
Once we calculate the similarity score between your request and every active item in the database:
1. We filter out items that have a very low score (e.g., < 25%).
2. We rank the remaining items from highest to lowest score.
3. The UI explains *why* an item was matched (e.g., "Description is highly semantically similar").

## 3. Why Run Locally?
By using `sentence-transformers`, RentMate runs its AI matching engine entirely locally without relying on expensive cloud APIs (like OpenAI). This makes the platform free to operate, fast, and highly private.
