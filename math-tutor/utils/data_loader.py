"""
Pure data layer — no Streamlit imports.
All topics, static content, fallback problems, and config live here.
"""

# Change this before sharing the app. Will be overridden by st.secrets["PARENT_PIN"] if set.
PARENT_PIN = "1234"

APP_NAME = "Grade 3 to 4 Math Bridge"
APP_SHORT_NAME = "Math Bridge"
APP_TAGLINE = (
    "Review third grade foundations, preview fourth grade methods, "
    "and build confidence over the summer."
)

LANES = {
    "grade3_review": {
        "label": "Grade 3 Review",
        "emoji": "🔁",
        "description": "Revisit the biggest third grade ideas before the new school year starts.",
    },
    "grade4_preview": {
        "label": "Grade 4 Preview",
        "emoji": "🚀",
        "description": "Get a gentle head start on the math that shows up in fourth grade.",
    },
}

# ── Topic Registry ────────────────────────────────────────────────────────────

TOPICS = {
    "3OA": {
        "label": "Multiplication & Division Review",
        "emoji": "✖️",
        "subtopics": ["Arrays", "Equal Groups", "Word Problems", "Unknown Factor"],
        "standard": "3.OA",
        "lane": "grade3_review",
        "description": "Review equal groups, arrays, multiplication facts, and division thinking.",
    },
    "3NBT": {
        "label": "Place Value to 1,000 Review",
        "emoji": "🔢",
        "subtopics": ["Rounding", "Add & Subtract within 1,000", "Multiply by Multiples of 10"],
        "standard": "3.NBT",
        "lane": "grade3_review",
        "description": "Strengthen rounding, place value, and operations up to 1,000.",
    },
    "3NF": {
        "label": "Fractions Review",
        "emoji": "🍕",
        "subtopics": ["Parts of a Whole", "Number Line Fractions", "Comparing Fractions"],
        "standard": "3.NF",
        "lane": "grade3_review",
        "description": "Review fractions as numbers and compare simple fractions with confidence.",
    },
    "3MD": {
        "label": "Measurement & Data Review",
        "emoji": "📏",
        "subtopics": ["Telling Time", "Area & Perimeter", "Bar Graphs"],
        "standard": "3.MD",
        "lane": "grade3_review",
        "description": "Practice time, area, perimeter, and reading simple data displays.",
    },
    "3G": {
        "label": "Shapes Review",
        "emoji": "🔷",
        "subtopics": ["Shape Attributes", "Equal Parts"],
        "standard": "3.G",
        "lane": "grade3_review",
        "description": "Review shape attributes and partitioning shapes into equal parts.",
    },
    "4OA": {
        "label": "Operations & Problem Solving",
        "emoji": "🧩",
        "subtopics": ["Multiplicative Comparison", "Multi-Step Word Problems", "Factors & Multiples", "Patterns"],
        "standard": "4.OA",
        "lane": "grade4_preview",
        "description": "Preview comparison problems, multi-step thinking, and number patterns.",
    },
    "4NBT": {
        "label": "Place Value & Big Numbers",
        "emoji": "🏗️",
        "subtopics": ["Place Value to 1,000,000", "Rounding", "Multi-Digit Addition & Subtraction", "Multiplication & Division Strategies"],
        "standard": "4.NBT",
        "lane": "grade4_preview",
        "description": "Preview larger numbers and the first big jump into multi-digit arithmetic.",
    },
    "4NF": {
        "label": "Fractions & Decimals",
        "emoji": "🥧",
        "subtopics": ["Equivalent Fractions", "Compare Fractions", "Add & Subtract Like Denominators", "Whole Number × Fraction", "Tenths & Hundredths"],
        "standard": "4.NF",
        "lane": "grade4_preview",
        "description": "Preview the fraction work that becomes central in fourth grade.",
    },
    "4MD": {
        "label": "Measurement, Data & Angles",
        "emoji": "📐",
        "subtopics": ["Measurement Conversions", "Area & Perimeter", "Line Plots", "Angles"],
        "standard": "4.MD",
        "lane": "grade4_preview",
        "description": "Preview conversions, line plots, and the new angle concepts in Grade 4.",
    },
    "4G": {
        "label": "Geometry Preview",
        "emoji": "📘",
        "subtopics": ["Lines & Rays", "Triangles", "Quadrilaterals", "Symmetry"],
        "standard": "4.G",
        "lane": "grade4_preview",
        "description": "Preview lines, angle-based shape classification, and symmetry.",
    },
}

ENCOURAGEMENT_MESSAGES = [
    "Amazing work today! You're building a strong bridge into fourth grade! 🌟",
    "Great job! Every problem you try makes your brain stronger! 🧠",
    "You worked really hard today. That's what matters most! 💪",
    "Wow, look at those stars! Keep it up! ⭐",
    "You should be really proud of yourself today! 🎉",
    "Math gets easier every time you practice. You proved that today! 🚀",
    "Super effort! You're getting more ready for fourth grade every day! 🍎",
    "You stuck with it even when it was tricky. That's a superpower! 💫",
    "Nice work, math bridge builder! See you next time! 🌈",
    "Every problem you tried made you better. Keep going! 🏆",
]

# ── Fallback Problems (used when the live API is unavailable) ────────────────

FALLBACK_PROBLEMS = {
    "3OA": [
        {
            "problem_text": "There are 3 rows of apples. Each row has 4 apples. How many apples are there in all?",
            "answer": "12",
            "distractors": ["7", "10", "15"],
            "visual_type": "array",
            "visual_data": {"rows": 3, "cols": 4, "emoji": "🍎"},
            "hint_1": "How many rows do you see? How many apples are in each row?",
            "explanation_child": "Think of each row as one equal group. Multiply the number of rows by the apples in each row to find the total.",
            "explanation_parent": "This is a classic array problem (3.OA.1). Arrays model multiplication as equal groups arranged in rows and columns. Common Core uses arrays to build conceptual understanding before fact memorization.",
        },
        {
            "problem_text": "What is 6 × 7?",
            "answer": "42",
            "distractors": ["36", "48", "13"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "Do you know 6 × 6? What happens if you add one more group of 6?",
            "explanation_child": "Start with a multiplication fact you already know, then build from it one group at a time.",
            "explanation_parent": "This targets multiplication fluency (3.OA.7). The hint nudges the child to use a known fact plus one more group, which is a Common Core fact-building strategy.",
        },
        {
            "problem_text": "There are 24 crayons shared equally among 4 students. How many crayons does each student get?",
            "answer": "6",
            "distractors": ["4", "8", "20"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "Think: 4 times what number equals 24?",
            "explanation_child": "Try thinking about division as making equal groups. Ask yourself what number goes with 4 to make 24.",
            "explanation_parent": "This is division as equal sharing (3.OA.2). Common Core links division to multiplication so students see 4 × ? = 24 before relying on a formal algorithm.",
        },
    ],
    "3NBT": [
        {
            "problem_text": "Round 347 to the nearest hundred.",
            "answer": "300",
            "distractors": ["350", "400", "340"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "Look at the tens digit. Is 347 closer to 300 or 400?",
            "explanation_child": "Use the digit to the right of the hundreds place to decide which hundred the number is closer to.",
            "explanation_parent": "This targets rounding to the nearest hundred (3.NBT.1). Students are meant to reason about which benchmark number is closer, not just apply a memorized rule.",
        },
        {
            "problem_text": "What is 456 + 237?",
            "answer": "693",
            "distractors": ["683", "703", "623"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "Try adding the ones first, then the tens, then the hundreds.",
            "explanation_child": "Add one place at a time so you can keep track of what each digit is worth.",
            "explanation_parent": "This reviews addition within 1,000 (3.NBT.2). Common Core emphasizes place-value meaning so students understand why regrouping works.",
        },
    ],
    "3NF": [
        {
            "problem_text": "A pizza is cut into 4 equal slices. Sarah ate 1 slice. What fraction of the pizza did she eat?",
            "answer": "1/4",
            "distractors": ["1/3", "2/4", "4/1"],
            "visual_type": "fraction",
            "visual_data": {"numerator": 1, "denominator": 4, "shape": "circle"},
            "hint_1": "How many equal pieces is the whole pizza cut into? How many pieces were eaten?",
            "explanation_child": "The bottom number tells how many equal parts the whole has. The top number tells how many parts we are counting.",
            "explanation_parent": "This is unit-fraction work (3.NF.1). Students learn that the denominator names the size of the parts and the numerator counts them.",
        },
        {
            "problem_text": "Which fraction is greater: 1/2 or 1/4?",
            "answer": "1/2",
            "distractors": ["1/4", "They are equal", "Cannot tell"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "If you cut one sandwich into 2 pieces and another into 4 pieces, which single piece is bigger?",
            "explanation_child": "When the top numbers match, think about the size of one piece. Fewer equal pieces means bigger pieces.",
            "explanation_parent": "This is comparing unit fractions (3.NF.3d). Common Core wants students to reason visually and conceptually before relying on symbolic tricks.",
        },
    ],
    "3MD": [
        {
            "problem_text": "A rectangle has a length of 5 units and a width of 3 units. What is its area?",
            "answer": "15 square units",
            "distractors": ["8 square units", "16 square units", "30 square units"],
            "visual_type": "array",
            "visual_data": {"rows": 3, "cols": 5, "emoji": "🟦"},
            "hint_1": "How many rows of square tiles would fit? How many tiles are in each row?",
            "explanation_child": "Area tells how many square units fit inside the rectangle. Multiply the rows by the squares in each row.",
            "explanation_parent": "This is area through tiling and arrays (3.MD.7). The same structure as multiplication appears again so children connect geometry back to equal groups.",
        },
        {
            "problem_text": "The clock shows 2:45. What time will it be in 30 minutes?",
            "answer": "3:15",
            "distractors": ["2:75", "3:45", "3:00"],
            "visual_type": "clock",
            "visual_data": {"hour": 2, "minute": 45},
            "hint_1": "How many minutes does it take to get from 2:45 to 3:00? Then how many minutes are still left to add?",
            "explanation_child": "Try jumping to the next hour first, then add the minutes that are left over.",
            "explanation_parent": "This is elapsed-time thinking (3.MD.1). Common Core often teaches children to count up in jumps instead of treating time as simple subtraction.",
        },
    ],
    "3G": [
        {
            "problem_text": "A square is divided into 4 equal parts. What fraction does each part represent?",
            "answer": "1/4",
            "distractors": ["1/2", "2/4", "4/4"],
            "visual_type": "fraction",
            "visual_data": {"numerator": 1, "denominator": 4, "shape": "rectangle"},
            "hint_1": "If the whole is split into 4 equal pieces, what fraction names one of those pieces?",
            "explanation_child": "One equal part means the top number is 1. The total number of equal parts becomes the bottom number.",
            "explanation_parent": "This connects geometry to fractions (3.G.2). Students learn that fractions describe equal-area partitions, not just numbers written with a slash.",
        },
    ],
    "4OA": [
        {
            "problem_text": "Lena has 4 times as many stickers as Max. Max has 6 stickers. How many stickers does Lena have?",
            "answer": "24",
            "distractors": ["10", "18", "30"],
            "visual_type": "array",
            "visual_data": {"rows": 4, "cols": 6, "emoji": "⭐"},
            "hint_1": "If Max has 6, what does 4 times as many mean?",
            "explanation_child": "The words 'times as many' mean equal groups. Make 4 groups of 6 to find Lena's total.",
            "explanation_parent": "This previews multiplicative comparison (4.OA.1). Fourth grade shifts from simple equal groups to comparing one quantity as a multiple of another.",
        },
        {
            "problem_text": "A class collected 18 cans on Monday and 27 cans on Tuesday. They packed the cans equally into 5 boxes. How many cans were left over?",
            "answer": "0",
            "distractors": ["5", "8", "9"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "First find the total number of cans. Then think about splitting that total into 5 equal groups.",
            "explanation_child": "This is a multi-step problem. Solve one part at a time and keep track of what the question is asking at the end.",
            "explanation_parent": "This previews multi-step word problems and interpreting the full situation (4.OA.3). Fourth grade expects students to chain operations and check whether a remainder makes sense in context.",
        },
        {
            "problem_text": "Which number is a factor of 36?",
            "answer": "9",
            "distractors": ["7", "11", "13"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "A factor divides a number into equal groups with nothing left over. Does 36 split evenly by each choice?",
            "explanation_child": "Try each choice and see whether it makes equal groups with no leftovers.",
            "explanation_parent": "This previews factors and multiples (4.OA.4). Students begin thinking about divisibility and the structure of whole numbers, which later supports fraction equivalence and division.",
        },
    ],
    "4NBT": [
        {
            "problem_text": "Which number has a 7 in the ten-thousands place?",
            "answer": "374,218",
            "distractors": ["437,218", "347,218", "324,718"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "Start at the ones place on the right and count place values to the left.",
            "explanation_child": "Read the number by place value one digit at a time so you can find the ten-thousands place correctly.",
            "explanation_parent": "This previews the Grade 4 extension of place value to 1,000,000 (4.NBT.1-2). The key shift is that children must read, compare, and reason about much larger numbers.",
        },
        {
            "problem_text": "What is 3,482 + 1,759?",
            "answer": "5,241",
            "distractors": ["5,131", "4,241", "5,341"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "Add by place value and check whether any place needs regrouping.",
            "explanation_child": "Work from the ones place up and keep track of regrouping carefully.",
            "explanation_parent": "This previews fluent multi-digit addition (4.NBT.4). In fourth grade, the standard algorithm is expected, but it is still grounded in place-value reasoning.",
        },
        {
            "problem_text": "What is 24 × 6?",
            "answer": "144",
            "distractors": ["124", "164", "84"],
            "visual_type": "array",
            "visual_data": {"rows": 6, "cols": 24, "emoji": "🟧"},
            "hint_1": "Can you break 24 into 20 and 4, then multiply each part by 6?",
            "explanation_child": "Break the bigger number into friendlier parts, then combine the products.",
            "explanation_parent": "This previews multi-digit multiplication strategies (4.NBT.5). Area-model and partial-product thinking are common bridges into the standard algorithm.",
        },
    ],
    "4NF": [
        {
            "problem_text": "Which fraction is equivalent to 2/3?",
            "answer": "4/6",
            "distractors": ["3/6", "2/6", "5/6"],
            "visual_type": "fraction",
            "visual_data": {"numerator": 4, "denominator": 6, "shape": "rectangle"},
            "hint_1": "Equivalent fractions name the same amount. How could both the top and bottom numbers change in the same way?",
            "explanation_child": "Think about making more equal parts without changing the size of the whole amount.",
            "explanation_parent": "This previews fraction equivalence (4.NF.1). Students are expected to explain why two fractions are equal using visual models, not just memorize cross-multiplication tricks.",
        },
        {
            "problem_text": "What is 3/8 + 2/8?",
            "answer": "5/8",
            "distractors": ["5/16", "1/8", "4/8"],
            "visual_type": "fraction",
            "visual_data": {"numerator": 5, "denominator": 8, "shape": "rectangle"},
            "hint_1": "When the denominators match, what stays the same and what changes?",
            "explanation_child": "If the pieces are the same size, keep the bottom number and combine the number of pieces.",
            "explanation_parent": "This previews addition with like denominators (4.NF.3). The conceptual target is that only the count of equal parts changes, not the size of the parts.",
        },
        {
            "problem_text": "What is 3 × 1/4?",
            "answer": "3/4",
            "distractors": ["1/12", "4/3", "1/4"],
            "visual_type": "fraction",
            "visual_data": {"numerator": 3, "denominator": 4, "shape": "rectangle"},
            "hint_1": "If you have 3 groups of one fourth, how many fourths do you have altogether?",
            "explanation_child": "Think of this as repeated addition: one fourth plus one fourth plus one fourth.",
            "explanation_parent": "This previews multiplying a whole number by a fraction (4.NF.4). The bridge idea is repeated addition of unit fractions and fractional parts.",
        },
    ],
    "4MD": [
        {
            "problem_text": "A rope is 3 feet long. How many inches long is the rope?",
            "answer": "36 inches",
            "distractors": ["12 inches", "24 inches", "48 inches"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "How many inches are in 1 foot? What happens if you have 3 of those groups?",
            "explanation_child": "Use the size of one foot to build the size of three feet.",
            "explanation_parent": "This previews measurement conversion (4.MD.1). Fourth graders connect multiplication to unit conversion by thinking about how many smaller units fit inside a larger one.",
        },
        {
            "problem_text": "A rectangle has an area of 24 square units and a length of 6 units. What is its width?",
            "answer": "4",
            "distractors": ["3", "6", "18"],
            "visual_type": "array",
            "visual_data": {"rows": 4, "cols": 6, "emoji": "🟦"},
            "hint_1": "Area means rows times columns. What number multiplied by 6 gives 24?",
            "explanation_child": "Use what you know about multiplication facts to find the missing side.",
            "explanation_parent": "This previews using the area formula to find an unknown side (4.MD.3). It blends multiplication, division, and geometric meaning.",
        },
        {
            "problem_text": "An angle measures 35 degrees. Another angle next to it measures 25 degrees. What is the total angle measure?",
            "answer": "60 degrees",
            "distractors": ["10 degrees", "50 degrees", "70 degrees"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "If two smaller angles join to make one bigger angle, what do you do with their measures?",
            "explanation_child": "Angle measure can be added when smaller angles fit together without overlapping.",
            "explanation_parent": "This previews additive angle measure (4.MD.7). Fourth grade introduces angle as a measurable quantity, not just a shape to recognize.",
        },
    ],
    "4G": [
        {
            "problem_text": "Which shape has exactly one line of symmetry?",
            "answer": "an isosceles triangle",
            "distractors": ["a scalene triangle", "a trapezoid with no equal sides", "an irregular quadrilateral"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "A line of symmetry lets a shape fold into matching halves. Which choice could do that exactly once?",
            "explanation_child": "Picture folding each shape in half and see whether both sides would match.",
            "explanation_parent": "This previews symmetry (4.G.3). The emphasis is on seeing geometric structure, not just memorizing vocabulary.",
        },
        {
            "problem_text": "What kind of triangle has one right angle?",
            "answer": "right triangle",
            "distractors": ["acute triangle", "obtuse triangle", "equilateral triangle"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "A right angle is a square-corner angle. Which triangle name matches that idea?",
            "explanation_child": "Triangle names can come from the kind of angles they have.",
            "explanation_parent": "This previews classifying triangles by angle size (4.G.2a). Fourth grade geometry leans more on precise attributes and classification language.",
        },
    ],
}


# ── Helper Functions ──────────────────────────────────────────────────────────

def get_topics() -> dict:
    return TOPICS


def get_topic_list():
    return [(k, v["label"]) for k, v in TOPICS.items()]


def get_topics_by_lane(lane_key: str) -> dict:
    return {k: v for k, v in TOPICS.items() if v.get("lane") == lane_key}


def get_subtopics(topic_key: str):
    return TOPICS.get(topic_key, {}).get("subtopics", [])


def get_fallback_problem(topic_key: str) -> dict:
    import random

    fallback_key = topic_key if topic_key in FALLBACK_PROBLEMS else "3OA"
    problems = FALLBACK_PROBLEMS.get(fallback_key, FALLBACK_PROBLEMS["3OA"])
    return random.choice(problems)


def get_encouragement(accuracy_pct: float) -> str:
    import random

    if accuracy_pct >= 0.8:
        pool = ENCOURAGEMENT_MESSAGES[:5]
    elif accuracy_pct >= 0.5:
        pool = ENCOURAGEMENT_MESSAGES[5:8]
    else:
        pool = ENCOURAGEMENT_MESSAGES[8:]
    return random.choice(pool)
