"""
Structured Concept Lessons for AI Aptitude Mastery Coach.
Follows the 15-step pedagogical sequence:
1. Concept Definition
2. Why Needed
3. Simple Language
4. Real-World Example
5. Underlying Intuition
6. Important Terms
7. Formulas & Why They Work
8. Simple Worked Example
9. Placement-Level Example
10. Common Traps & Misconceptions
11. Guided Questions
12. Key Takeaways
"""

LESSONS = {
    "percentages": {
        "title": "Percentages (Foundations to Placement Mastery)",
        "category": "Quantitative Aptitude",
        "concept_summary": "A percentage is a dimensionless ratio expressing a fraction of 100 ('per cent' = per hundred). It allows direct comparisons between quantities of different scales.",
        "why_needed": "Whether evaluating salary hikes, company growth rates, profit margins, or discount campaigns, percentages normalize different numbers to a standard baseline of 100 for effortless comparison.",
        "simple_explanation": "Think of a percentage as cutting any total quantity into exactly 100 equal slices. If you take 25 of those slices, you have 25% of the total. 100% means the entire object, 50% is half, and 200% is twice the original.",
        "real_world_example": "If Company A's revenue grew from $10M to $12M (a $2M increase) and Startup B grew from $100k to $300k (a $200k increase), Startup B actually had the superior growth percentage (200% vs 20%). Percentages reveal the true rate of change.",
        "intuition": "Always locate the BASE (the 'of' value). In 'What percent of X is Y?', X is the foundation (the denominator 100%). Whenever the base changes (like consecutive price changes), you cannot simply add the percentages together!",
        "important_terms": [
            {"term": "Base Value", "definition": "The reference amount corresponding to 100% (the denominator)."},
            {"term": "Percentage Increase", "definition": "(Change / Original Base) × 100% when final > original."},
            {"term": "Percentage Decrease", "definition": "(Change / Original Base) × 100% when final < original."},
            {"term": "Successive Percentage Change", "definition": "Changes applied consecutively where the second change acts on the already updated value."}
        ],
        "formulas": [
            {
                "name": "Basic Percentage",
                "formula": "Percentage = (Part / Whole) × 100%",
                "why_works": "Divides the part by the whole to find the fractional unit, then scales it to a 100-point scale.",
                "when_to_use": "When finding what fraction one number is of another."
            },
            {
                "name": "Percentage Change",
                "formula": "% Change = ((Final - Initial) / Initial) × 100%",
                "why_works": "Measures the net delta relative to the starting benchmark.",
                "when_to_use": "For price revisions, salary increments, population growth."
            },
            {
                "name": "Successive Changes (a% and b%)",
                "formula": "Net % Change = a + b + (a × b / 100)",
                "why_works": "Combines initial change 'a' with second change 'b' plus the compounding effect of 'b' acting on 'a'.",
                "when_to_use": "Consecutive discounts or price markups followed by discounts."
            }
        ],
        "step_by_step_example": {
            "question": "If 20% of a number is 80, what is the number?",
            "steps": [
                "Step 1: Translate the English statement into a mathematical equation. Let the unknown number be 'x'.",
                "Step 2: '20% of x' translates to (20 / 100) × x = 0.2x.",
                "Step 3: Equate to given value: 0.2x = 80.",
                "Step 4: Solve for x: x = 80 / 0.2 = 400."
            ],
            "solution": "The number is 400. Verification: 10% of 400 is 40, so 20% is 40 × 2 = 80."
        },
        "placement_example": {
            "question": "A product price is increased by 25%. By what percentage must the new price be decreased so that it returns to the original price?",
            "approach": "Do not answer 25%! When the price rises, the new base becomes larger. A smaller percentage of a larger base equals the original absolute increase.",
            "solution": "Let original price = 100. Increased price = 125. Required reduction = 25. Percentage reduction from new price = (25 / 125) × 100% = 1/5 × 100% = 20%.",
            "trap": "Believing that an x% increase followed by an x% decrease restores the initial value. It always results in a net decrease!"
        },
        "common_traps": [
            "Confusing the base: Always check whether the change is measured against the original value or the updated value.",
            "Directly adding consecutive percentage discounts (e.g. 50% + 50% discount is NOT free; it is 75% off!).",
            "Forgetting to divide by 100 when calculating decimals."
        ],
        "key_takeaways": [
            "Percentage means parts per hundred.",
            "Base value is always the denominator.",
            "To reverse an increase of a/b, you must decrease by a/(a+b)."
        ]
    },
    "profit_and_loss": {
        "title": "Profit and Loss (Commercial Arithmetic)",
        "category": "Quantitative Aptitude",
        "concept_summary": "Profit and Loss calculations measure commercial financial gain or deficit resulting from purchasing (Cost Price) and selling (Selling Price) goods.",
        "why_needed": "Core to all financial modeling, business transactions, valuation problems, and frequent placement aptitude sections.",
        "simple_explanation": "If you sell something for more than you bought it for, the difference is your Profit. If you sell it for less, the shortfall is your Loss. Both are traditionally evaluated with respect to what you originally paid (Cost Price).",
        "real_world_example": "A vendor buys 10 laptops for $500 each ($5,000 total CP) and sells them at $600 each ($6,000 total SP). Profit is $1,000, representing a 20% return on investment.",
        "intuition": "Unless explicitly stated otherwise by the problem, Cost Price (CP) is ALWAYS the 100% baseline. Profit % = (Profit / CP) × 100%.",
        "important_terms": [
            {"term": "Cost Price (CP)", "definition": "Total expenditure incurred to acquire or manufacture the item, including shipping/repairs."},
            {"term": "Selling Price (SP)", "definition": "The revenue received upon selling the item."},
            {"term": "Marked Price (MP / List Price)", "definition": "The printed sticker price before applying any discount."},
            {"term": "Discount", "definition": "Reduction offered strictly on the Marked Price: Discount = MP - SP."}
        ],
        "formulas": [
            {
                "name": "Profit & Loss",
                "formula": "Profit = SP - CP (if SP > CP); Loss = CP - SP (if CP > SP)",
                "why_works": "Direct difference between cash inflow and outflow.",
                "when_to_use": "To determine net monetary gain or loss."
            },
            {
                "name": "Profit/Loss Percentage",
                "formula": "Profit % = (Profit / CP) × 100; Loss % = (Loss / CP) × 100",
                "why_works": "Normalizes earnings relative to capital invested.",
                "when_to_use": "Evaluating transaction return rates."
            },
            {
                "name": "Selling Price from CP and Profit%",
                "formula": "SP = CP × (1 + Profit% / 100)",
                "why_works": "Scales the original investment by the profit factor.",
                "when_to_use": "Finding target selling price given expected margins."
            }
        ],
        "step_by_step_example": {
            "question": "A book is bought for $100 and sold for $120. Find the profit percentage.",
            "steps": [
                "Step 1: Identify given values: CP = $100, SP = $120.",
                "Step 2: Calculate absolute profit: Profit = SP - CP = $120 - $100 = $20.",
                "Step 3: Apply formula: Profit % = (Profit / CP) × 100 = (20 / 100) × 100 = 20%."
            ],
            "solution": "The profit percentage is 20%."
        },
        "placement_example": {
            "question": "A dishonest dealer professes to sell his goods at cost price, but uses a weight of 900 grams for a 1 kg weight. Find his gain percentage.",
            "approach": "He charges the customer for 1000g of goods (SP is equivalent to cost of 1000g), but actually dispenses only 900g (his real CP is 900g).",
            "solution": "Error = 100g. True Value = 1000g, Weight used = 900g. Gain % = (Error / (True Value - Error)) × 100% = (100 / 900) × 100% = 11.11%.",
            "trap": "Dividing the 100g error by 1000g instead of the actual goods delivered (900g)."
        },
        "common_traps": [
            "Calculating profit percentage over Selling Price instead of Cost Price.",
            "Neglecting overhead expenses (transportation, maintenance) which must be added to CP.",
            "Applying discount to Cost Price instead of Marked Price."
        ],
        "key_takeaways": [
            "Profit is SP - CP; Loss is CP - SP.",
            "CP is the standard base for profit/loss %.",
            "Discount is always calculated on Marked Price (MP)."
        ]
    },
    "time_and_work": {
        "title": "Time and Work (Unitary & LCM Methods)",
        "category": "Quantitative Aptitude",
        "concept_summary": "Time and Work problems examine the inverse relationship between the time taken to complete a task and the rate/efficiency of the workers.",
        "why_needed": "Appears in every placement exam (TCS, Infosys, Cognizant) and mirrors real-world task scheduling and resource allocation.",
        "simple_explanation": "If you can finish a painting in 4 days, then each day you complete 1/4 of the painting. If a friend completes it in 4 days too, working together you do 1/4 + 1/4 = 2/4 = 1/2 per day, finishing the job in 2 days.",
        "real_world_example": "Two server pipelines process data: Worker Server A takes 6 hours to index a database, and Server B takes 3 hours. Running both concurrently indexes the database in 2 hours.",
        "intuition": "Work is constant. Efficiency is inversely proportional to time: Time × Efficiency = Total Work. Using the LCM method (setting total work as LCM of days) turns tricky fraction math into clean integer addition!",
        "important_terms": [
            {"term": "Efficiency", "definition": "Amount of work done per unit of time (e.g. units/day)."},
            {"term": "Total Work", "definition": "The entire job, often modeled as 1 or as the LCM of individual times."},
            {"term": "Negative Work", "definition": "Work that destroys or empties progress (e.g. leaking pipes)."}
        ],
        "formulas": [
            {
                "name": "One Day's Work",
                "formula": "If A finishes in n days, 1 day's work = 1 / n",
                "why_works": "Unitary rate of progress per unit time.",
                "when_to_use": "Combining multiple workers' daily output."
            },
            {
                "name": "Combined Time for A and B",
                "formula": "Time = (A × B) / (A + B)",
                "why_works": "Derived from 1/T = 1/A + 1/B = (A+B)/(A×B), then inverted.",
                "when_to_use": "Two workers working simultaneously from start to end."
            },
            {
                "name": "LCM Method",
                "formula": "Total Units = LCM(t1, t2, ...); Efficiency = Total Units / Time",
                "why_works": "Transforms fractional addition into easy integer arithmetic.",
                "when_to_use": "3+ workers, alternating days, or workers leaving mid-way."
            }
        ],
        "step_by_step_example": {
            "question": "A can do a piece of work in 10 days and B in 15 days. How long will they take working together?",
            "steps": [
                "Step 1: Let Total Work = LCM(10, 15) = 30 units.",
                "Step 2: Find A's efficiency = 30 / 10 = 3 units/day.",
                "Step 3: Find B's efficiency = 30 / 15 = 2 units/day.",
                "Step 4: Combined efficiency = 3 + 2 = 5 units/day.",
                "Step 5: Total days required = Total Work / Combined Efficiency = 30 / 5 = 6 days."
            ],
            "solution": "Working together, A and B take 6 days."
        },
        "placement_example": {
            "question": "A can finish in 12 days, B in 18 days. They begin together, but A leaves 2 days before completion. In how many days was the work completed?",
            "approach": "Instead of subtracting A, pretend A stayed for those last 2 days. Add 2 days of A's work to total work, then divide by (A + B).",
            "solution": "LCM(12, 18) = 36 units. Rate A = 3 u/day, Rate B = 2 u/day. If A worked the last 2 days, extra work = 3 × 2 = 6 units. Total = 36 + 6 = 42 units. Both working at 5 u/day: 42 / 5 = 8.4 days.",
            "trap": "Confusing 'leaving 2 days after start' with 'leaving 2 days before end'."
        },
        "common_traps": [
            "Directly adding days (e.g. 10 days + 15 days = 25 days) instead of adding rates.",
            "Forgetting to invert the combined 1-day rate to find total days."
        ],
        "key_takeaways": [
            "Time = Total Work / Total Efficiency.",
            "LCM method avoids ugly fraction arithmetic.",
            "Rates add up; time periods never do."
        ]
    },
    "series": {
        "title": "Series & Pattern Recognition",
        "category": "Logical Reasoning",
        "concept_summary": "A sequence of numbers, symbols, or letters structured according to a deterministic mathematical or positional algorithm.",
        "why_needed": "Tests analytical observation, algorithmic thinking, and rapid pattern detection indispensable in programming and debugging.",
        "simple_explanation": "A series is like a puzzle where each step follows a secret rule. Your goal is to inspect the gaps, multiplications, or alternating positions to discover that hidden rule.",
        "real_world_example": "Predicting load spikes on cloud infrastructure by observing hourly traffic patterns: 100, 150, 225, 337.5... (multiplicative 1.5x scaling).",
        "intuition": "Step 1: Compute first differences. If constant, it's arithmetic. Step 2: Compute ratios. If constant, it's geometric. Step 3: Compute second differences. If constant, it's quadratic (n²). Step 4: Check squares, cubes, primes, or alternating interleaved series.",
        "important_terms": [
            {"term": "Arithmetic Progression (AP)", "definition": "Successive terms differ by a constant difference d: a, a+d, a+2d..."},
            {"term": "Geometric Progression (GP)", "definition": "Successive terms differ by a constant ratio r: a, ar, ar²..."},
            {"term": "Fibonacci Pattern", "definition": "Each term is the sum of preceding terms: 0, 1, 1, 2, 3, 5, 8..."},
            {"term": "Interleaved / Dual Series", "definition": "Two distinct series woven together at odd and even positions."}
        ],
        "formulas": [
            {
                "name": "N-th Term of AP",
                "formula": "T_n = a + (n - 1)d",
                "why_works": "Adds (n-1) increments of common difference to initial term.",
                "when_to_use": "Finding future terms in additive sequences."
            },
            {
                "name": "N-th Term of GP",
                "formula": "T_n = a × r^(n - 1)",
                "why_works": "Multiplies initial term by the growth factor (n-1) times.",
                "when_to_use": "Exponential or multiplicative sequences."
            }
        ],
        "step_by_step_example": {
            "question": "Find the missing number in the series: 2, 5, 11, ?, 47",
            "steps": [
                "Step 1: Check differences: 5 - 2 = 3; 11 - 5 = 6. Differences are doubling (3, 6, ...).",
                "Step 2: Alternatively check algebraic recurrence: 2 × 2 + 1 = 5; 5 × 2 + 1 = 11.",
                "Step 3: Test recurrence on next term: 11 × 2 + 1 = 23.",
                "Step 4: Verify with subsequent term: 23 × 2 + 1 = 47. Perfectly matches!"
            ],
            "solution": "The missing number is 23."
        },
        "placement_example": {
            "question": "Find the next term: 2, 12, 36, 80, 150, ?",
            "approach": "Look for cube and square combinations: n³ + n².",
            "solution": "1³ + 1² = 2; 2³ + 2² = 12; 3³ + 3² = 36; 4³ + 4² = 80; 5³ + 5² = 150. For n=6: 6³ + 6² = 216 + 36 = 252.",
            "trap": "Stopping at first differences without checking polynomial n² or n³ relationships."
        },
        "common_traps": [
            "Assuming every sequence is arithmetic before checking squares or cubes.",
            "Failing to spot alternating sequences with two alternating patterns."
        ],
        "key_takeaways": [
            "Always calculate first differences first.",
            "Check for n² ± k or n³ ± k when differences grow fast.",
            "Look for interleaved patterns if numbers go up and down."
        ]
    },
    "programming_fundamentals": {
        "title": "Programming Fundamentals (Code Trace & State)",
        "category": "Technical Aptitude",
        "concept_summary": "Core semantics of variables, operator precedence, evaluation order, memory models, loops, and type casting in C, C++, Java, and Python.",
        "why_needed": "Essential for technical screening rounds in software engineering placements (TCS Digital, Infosys SP, Cognizant GenC Next).",
        "simple_explanation": "Computers execute instructions deterministically. Tracing code requires acting like the CPU: maintaining an exact variable state table and executing operations according to language rules.",
        "real_world_example": "Debugging an off-by-one loop index that leads to an array buffer overflow or index error in production.",
        "intuition": "Post-increment (x++) uses the old value first, then increments. Pre-increment (++x) increments first, then provides the new value. In Python, integers and strings are immutable, while lists and dicts are passed by reference.",
        "important_terms": [
            {"term": "Post-increment (x++)", "definition": "Evaluates to current value of x in expression, then adds 1 to x."},
            {"term": "Pre-increment (++x)", "definition": "Increments x by 1 first, then evaluates to the new value."},
            {"term": "Short-circuit evaluation", "definition": "In boolean 'A and B', if A is false, B is never evaluated."},
            {"term": "Bitwise Shift (>> / <<)", "definition": "x >> k computes floor(x / 2^k); x << k computes x * 2^k."}
        ],
        "formulas": [
            {
                "name": "Right Shift Division",
                "formula": "x >> k = floor(x / 2^k)",
                "why_works": "Binary positional representation shifts bits to lower place values.",
                "when_to_use": "Fast integer division by powers of 2."
            },
            {
                "name": "Bitwise Parity Check",
                "formula": "x & 1 == 0 (Even) / 1 (Odd)",
                "why_works": "The least significant bit in binary dictates odd vs even.",
                "when_to_use": "Checking odd/even in O(1) without modulo."
            }
        ],
        "step_by_step_example": {
            "question": "What is the output of this C code: int x = 5; printf('%d', x++); ?",
            "steps": [
                "Step 1: Inspect expression: `x++` is post-increment.",
                "Step 2: Post-increment yields current value to caller before mutating.",
                "Step 3: Value passed to `printf` is 5.",
                "Step 4: After the statement finishes, x becomes 6 in memory."
            ],
            "solution": "The output is 5."
        },
        "placement_example": {
            "question": "In Python, what is printed: a = [1, 2]; b = a; b.append(3); print(len(a)) ?",
            "approach": "Remember that assignment in Python binds a reference, it does not clone the object.",
            "solution": "Both `a` and `b` reference the same underlying list in memory. Mutating `b` modifies `a`. Thus len(a) is 3.",
            "trap": "Believing `b = a` created a shallow or deep copy of the list."
        },
        "common_traps": [
            "Confusing pre-increment (++x) and post-increment (x++).",
            "Integer division truncating towards zero in C/Java vs floor in Python.",
            "Object reference aliasing in Python and Java."
        ],
        "key_takeaways": [
            "Always trace variable values step-by-step.",
            "Remember language-specific evaluation order and type conversion rules.",
            "Bitwise operators work on binary bits directly."
        ]
    }
}
