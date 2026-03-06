"""
Pure data layer — no Streamlit imports.
All topics, static content, fallback problems, and config live here.
"""

# Change this before sharing the app. Will be overridden by st.secrets["PARENT_PIN"] if set.
PARENT_PIN = "1234"

# ── Topic Registry ────────────────────────────────────────────────────────────

TOPICS = {
    "3OA": {
        "label": "Multiplication & Division",
        "emoji": "✖️",
        "subtopics": ["Arrays", "Word Problems", "Properties of Multiplication", "Unknown Factor"],
        "standard": "3.OA",
        "description": "Multiply and divide using arrays, equal groups, and word problems.",
    },
    "3NBT": {
        "label": "Numbers to 1,000",
        "emoji": "🔢",
        "subtopics": ["Rounding", "Add & Subtract within 1,000", "Multiply by Multiples of 10"],
        "standard": "3.NBT",
        "description": "Work with place value, rounding, and operations up to 1,000.",
    },
    "3NF": {
        "label": "Fractions",
        "emoji": "🍕",
        "subtopics": ["Parts of a Whole", "Fractions on a Number Line", "Comparing Fractions"],
        "standard": "3.NF",
        "description": "Understand fractions as equal parts, place them on a number line, and compare.",
    },
    "3MD": {
        "label": "Measurement & Data",
        "emoji": "📏",
        "subtopics": ["Telling Time", "Area & Perimeter", "Bar & Picture Graphs"],
        "standard": "3.MD",
        "description": "Measure time, area, and perimeter. Read and create graphs.",
    },
    "3G": {
        "label": "Shapes",
        "emoji": "🔷",
        "subtopics": ["Shape Attributes", "Partitioning Shapes into Equal Areas"],
        "standard": "3.G",
        "description": "Identify shape properties and divide shapes into equal parts.",
    },
}

ENCOURAGEMENT_MESSAGES = [
    "Amazing work today! You're getting stronger at math every day! 🌟",
    "Great job! Every problem you try makes your brain smarter! 🧠",
    "You worked really hard today. That's what matters most! 💪",
    "Wow, look at those stars! Keep it up! ⭐",
    "You should be really proud of yourself today! 🎉",
    "Math gets easier every time you practice. You proved that today! 🚀",
    "Super effort! Your teacher would be so proud! 🍎",
    "You stuck with it even when it was tricky. That's a superpower! 💫",
    "Nice work, math star! See you next time! 🌈",
    "Every problem you tried made you better. Keep going! 🏆",
]

# ── Fallback Problems (used when Claude API is unavailable) ───────────────────

FALLBACK_PROBLEMS = {
    "3OA": [
        {
            "problem_text": "There are 3 rows of apples. Each row has 4 apples. How many apples are there in all?",
            "answer": "12",
            "distractors": ["7", "10", "15"],
            "visual_type": "array",
            "visual_data": {"rows": 3, "cols": 4, "emoji": "🍎"},
            "hint_1": "Can you count how many rows there are? Now count how many apples are in each row. What do you notice?",
            "explanation_child": "Think about how many rows there are and how many apples are in each row. Multiply the rows by the apples in each row to find the total.",
            "explanation_parent": "This is a classic array problem (3.OA.1). Arrays model multiplication as equal groups arranged in rows and columns. 3 × 4 = 12. Common Core uses arrays to build conceptual understanding before abstract fact memorization.",
        },
        {
            "problem_text": "What is 6 × 7?",
            "answer": "42",
            "distractors": ["36", "48", "13"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "Do you know 6 × 6? Try adding one more group of 6 to that.",
            "explanation_child": "Try starting with a fact you already know, like 6 × 6. Then think about what happens when you add one more group of 6.",
            "explanation_parent": "This targets fluency with multiplication facts (3.OA.7). The hint guides the student to use a known fact plus one more group — a Common Core strategy called 'building from a known fact'.",
        },
        {
            "problem_text": "There are 24 crayons shared equally among 4 students. How many crayons does each student get?",
            "answer": "6",
            "distractors": ["4", "8", "20"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "If 4 students share 24 crayons equally, think: 4 times what number equals 24?",
            "explanation_child": "Think about splitting 24 crayons into 4 equal groups. Ask yourself: 4 times what number gets you to 24?",
            "explanation_parent": "Division as equal sharing (3.OA.2). Common Core connects division to multiplication: 4 × ? = 24. This builds understanding before the standard algorithm.",
        },
    ],
    "3NBT": [
        {
            "problem_text": "Round 347 to the nearest hundred.",
            "answer": "300",
            "distractors": ["350", "400", "340"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "Look at the tens digit in 347. Is 47 closer to 0 or closer to 100?",
            "explanation_child": "Look at the tens digit to decide which hundred is closer. If the tens digit is less than 5, we round toward the lower hundred.",
            "explanation_parent": "Rounding to nearest hundred (3.NBT.1). Common Core uses the midpoint rule: digits 0-4 round down, 5-9 round up. Students look at the digit one place to the right of the rounding place.",
        },
        {
            "problem_text": "What is 456 + 237?",
            "answer": "693",
            "distractors": ["683", "693", "703"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "Try adding the ones first: 6 + 7 = ? Then the tens: 5 + 3 = ? Then the hundreds.",
            "explanation_child": "Try adding place by place — start with the ones, then the tens, then the hundreds. Remember to carry over if your ones add up to more than 9.",
            "explanation_parent": "Addition within 1,000 (3.NBT.2). Common Core builds place value understanding before the standard algorithm — students add by place value, understanding why carrying works.",
        },
    ],
    "3NF": [
        {
            "problem_text": "A pizza is cut into 4 equal slices. Sarah ate 1 slice. What fraction of the pizza did she eat?",
            "answer": "1/4",
            "distractors": ["1/3", "2/4", "4/1"],
            "visual_type": "fraction",
            "visual_data": {"numerator": 1, "denominator": 4, "shape": "circle"},
            "hint_1": "The bottom number tells us how many equal pieces the whole pizza is cut into. The top number tells us how many pieces were eaten.",
            "explanation_child": "The bottom number of a fraction tells you how many equal pieces the whole is cut into. The top number tells you how many pieces were taken.",
            "explanation_parent": "Unit fractions (3.NF.1). Common Core defines fractions as equal parts of a whole. The denominator names the size of each part; the numerator counts parts. Students learn meaning before computation.",
        },
        {
            "problem_text": "Which fraction is greater: 1/2 or 1/4?",
            "answer": "1/2",
            "distractors": ["1/4", "They are equal", "Cannot tell"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "Imagine cutting a sandwich into 2 pieces and another sandwich into 4 pieces. Which piece would be bigger?",
            "explanation_child": "When the top numbers are the same, think about the size of each piece. Fewer cuts means bigger pieces — so which denominator gives you the bigger slice?",
            "explanation_parent": "Comparing unit fractions (3.NF.3d). Common Core builds intuition: for unit fractions, a larger denominator means smaller pieces. Students use visual models before symbolic comparison.",
        },
    ],
    "3MD": [
        {
            "problem_text": "A rectangle has a length of 5 units and a width of 3 units. What is its area?",
            "answer": "15 square units",
            "distractors": ["8 square units", "16 square units", "30 square units"],
            "visual_type": "array",
            "visual_data": {"rows": 3, "cols": 5, "emoji": "🟦"},
            "hint_1": "Area means how many square tiles fit inside the rectangle. Can you count the rows and columns of tiles?",
            "explanation_child": "Count the rows of tiles and the tiles in each row. Multiplying those two numbers gives you the total number of square units inside.",
            "explanation_parent": "Area via array/tiling (3.MD.7). Common Core connects area to multiplication using the array model — the same visual used for 3.OA. This is intentional: students see multiplication and area as the same structure.",
        },
        {
            "problem_text": "The clock shows 2:45. What time will it be in 30 minutes?",
            "answer": "3:15",
            "distractors": ["2:75", "3:45", "3:00"],
            "visual_type": "none",
            "visual_data": {},
            "hint_1": "Start at 2:45. How many minutes until 3:00? Then how many minutes are left over?",
            "explanation_child": "Try jumping to the next hour first, then count how many minutes are still left to add after that.",
            "explanation_parent": "Elapsed time (3.MD.1). Common Core uses the 'jump strategy' — count up to the next hour, then add remaining minutes. This builds number sense rather than relying on rote subtraction.",
        },
    ],
    "3G": [
        {
            "problem_text": "A square is divided into 4 equal parts. What fraction does each part represent?",
            "answer": "1/4",
            "distractors": ["1/2", "2/4", "4/4"],
            "visual_type": "fraction",
            "visual_data": {"numerator": 1, "denominator": 4, "shape": "rectangle"},
            "hint_1": "The square is cut into 4 equal pieces. Each piece is one out of how many total pieces?",
            "explanation_child": "When a shape is cut into equal parts, the number of parts becomes the bottom number of the fraction. Each single part is one out of that many.",
            "explanation_parent": "Partitioning shapes (3.G.2). Common Core connects geometry to fractions — the same equal-parts concept from 3.NF. Students see that 1/4 represents both a number and a geometric relationship.",
        },
    ],
}


# ── Helper Functions ──────────────────────────────────────────────────────────

def get_topics() -> dict:
    return TOPICS


def get_topic_list():
    return [(k, v["label"]) for k, v in TOPICS.items()]


def get_subtopics(topic_key: str):
    return TOPICS.get(topic_key, {}).get("subtopics", [])


def get_fallback_problem(topic_key: str) -> dict:
    problems = FALLBACK_PROBLEMS.get(topic_key, FALLBACK_PROBLEMS["3OA"])
    import random
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
