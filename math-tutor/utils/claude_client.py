"""
All Anthropic API interactions.
Every function is wrapped in try/except — API failures must never crash the child's session.
"""

import json
import os
from typing import Generator

try:
    import anthropic
    _client = anthropic.Anthropic()
    # Quick check that the key is actually set
    if not os.environ.get("ANTHROPIC_API_KEY") and not os.environ.get("ANTHROPIC_API_KEY", "").startswith("sk-"):
        pass  # client will raise on first call, handled in each function
    API_AVAILABLE = True
except Exception:
    API_AVAILABLE = False
    _client = None

MODEL = "claude-sonnet-4-6"

_PROBLEM_SYSTEM = """You are a math problem generator for NYC 3rd grade standardized test preparation (NYS Math Assessment, Common Core Grade 3).

CRITICAL: Respond with ONLY valid JSON — no markdown fences, no explanation, no other text.

Required schema (all keys mandatory):
{
  "problem_text": "string — question at 2nd-3rd grade reading level, clear and specific",
  "answer": "string — the single correct answer",
  "distractors": ["string", "string", "string"],
  "visual_type": "array" or "fraction" or "number_line" or "bar_graph" or "clock" or "none",
  "visual_data": {
    // For array: {"rows": integer, "cols": integer, "emoji": "single emoji"}
    // For fraction: {"numerator": integer, "denominator": integer, "shape": "circle" or "rectangle"}
    // For number_line: {"start": integer, "end": integer, "mark": number, "label": "string"}
    // For bar_graph: {"title": "string", "y_label": "string", "bars": [{"label": "string", "value": integer}, ...]}
    //   CRITICAL: every bar "value" must be the EXACT integer from the problem — never 0, never a placeholder
    // For clock: {"hour": integer (1-12), "minute": integer (0-59)}
    // For none: {}
  },
  "hint_1": "string — Socratic question that guides thinking WITHOUT revealing the answer or any number that is the answer",
  "explanation_child": "string — 1-2 warm sentences explaining the METHOD or approach to solve this problem. CRITICAL: do NOT state the final answer, do NOT complete the calculation, do NOT reveal what the correct answer is. Explain how to think about it, not the result.",
  "explanation_parent": "string — 3-4 sentences: names the Common Core method, explains why the child might have gotten it wrong, how to help"
}

Rules:
- distractors must contain EXACTLY 3 items
- answer must NOT appear in distractors
- hint_1 must NEVER contain the answer or a number equal to the answer
- visual_type should be "array" for multiplication/area problems, "fraction" for fraction problems, "bar_graph" for data/graph problems (3.MD), "clock" for time-telling problems (3.MD), "none" otherwise
- CRITICAL for bar_graph: the "value" in every bar must be the exact number stated in problem_text — the visual and the text must match perfectly
- problem_text must be solvable by a typical 3rd grader in under 2 minutes"""

_HINT_SYSTEM = """You are a kind, patient math tutor helping an 8-year-old. Your ONLY job is to give hints that help her think — you must NEVER reveal the answer, give the answer value, or say any number that equals the answer.

Rules:
- 1-2 sentences maximum
- Use simple, warm, encouraging language
- Ask a Socratic question that guides her thinking
- Never say "the answer is" or complete the calculation for her
- Never include the numerical value of the correct answer"""

_PARENT_CONCEPT_SYSTEM = """You are explaining Common Core elementary math methods to a parent who is mathematically literate but was taught using traditional methods.

Be direct, clear, and adult. No condescension. Explain the pedagogical "why" — what understanding is this method building that the traditional approach didn't? Use a concrete example with small numbers. Keep it practical."""

_PARENT_WRONG_SYSTEM = """You are explaining a math problem to a parent who wants to understand why their child may have made a specific error. Be concise and practical."""


def _validate_problem(p: dict) -> bool:
    required = {"problem_text", "answer", "distractors", "visual_type", "visual_data", "hint_1", "explanation_child", "explanation_parent"}
    if not required.issubset(p.keys()):
        return False
    if not isinstance(p["distractors"], list) or len(p["distractors"]) != 3:
        return False
    if p["answer"] in p["distractors"]:
        return False
    return True


def generate_problem(topic_key: str, subtopic: str = None, difficulty: str = "medium") -> dict:
    """
    Returns a problem dict. Falls back to data_loader fallback on any error.
    difficulty: "easy" | "medium" | "hard"
    """
    from utils.data_loader import TOPICS, get_fallback_problem

    if not API_AVAILABLE or _client is None:
        return get_fallback_problem(topic_key)

    topic_info = TOPICS.get(topic_key, {})
    standard = topic_info.get("standard", topic_key)
    topic_label = topic_info.get("label", topic_key)
    sub = subtopic or (topic_info.get("subtopics", [""])[0])

    user_prompt = (
        f"Generate one {standard} problem about '{sub}' for a 3rd grader preparing for the NYS Math Assessment.\n"
        f"Topic area: {topic_label}\n"
        f"Subtopic: {sub}\n"
        f"Difficulty: {difficulty}\n\n"
        f"The problem must be multiple-choice-appropriate with one unambiguous correct answer."
    )

    try:
        response = _client.messages.create(
            model=MODEL,
            max_tokens=800,
            system=_PROBLEM_SYSTEM,
            messages=[{"role": "user", "content": user_prompt}],
            timeout=15.0,
        )
        raw = response.content[0].text.strip()
        # Strip markdown fences if Claude added them anyway
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        problem = json.loads(raw)
        if _validate_problem(problem):
            return problem
    except Exception:
        pass

    return get_fallback_problem(topic_key)


def get_hint(problem_dict: dict, attempt_count: int = 0) -> str:
    """
    Returns a Socratic hint. More direct on 2nd+ attempt.
    Never reveals the answer.
    """
    if not API_AVAILABLE or _client is None:
        return problem_dict.get("hint_1", "Think about what the problem is asking you to find. What information do you already know?")

    problem_text = problem_dict.get("problem_text", "")
    answer = problem_dict.get("answer", "")

    if attempt_count == 0:
        directness = "Give her a gentle opening question to get her started thinking."
    else:
        directness = f"She has asked for {attempt_count + 1} hints. Be a bit more direct — guide her closer to the method, but still no answer."

    user_prompt = (
        f"Problem: {problem_text}\n"
        f"Correct answer (DO NOT reveal): {answer}\n\n"
        f"{directness}"
    )

    try:
        response = _client.messages.create(
            model=MODEL,
            max_tokens=120,
            system=_HINT_SYSTEM,
            messages=[{"role": "user", "content": user_prompt}],
            timeout=15.0,
        )
        return response.content[0].text.strip()
    except Exception:
        return problem_dict.get("hint_1", "Think carefully — what do you already know that might help?")


def explain_concept_for_parent(topic_key: str, subtopic: str = None) -> Generator[str, None, None]:
    """
    Generator for st.write_stream(). Streams the explanation.
    Yields empty string on error so the UI doesn't crash.
    """
    from utils.data_loader import TOPICS

    if not API_AVAILABLE or _client is None:
        yield "⚠️ API unavailable. Please check your ANTHROPIC_API_KEY and try again."
        return

    topic_info = TOPICS.get(topic_key, {})
    topic_label = topic_info.get("label", topic_key)
    standard = topic_info.get("standard", topic_key)
    sub = subtopic or ""

    topic_str = f"{topic_label} ({standard})" + (f" — specifically '{sub}'" if sub else "")

    user_prompt = (
        f"Explain how **{topic_str}** is taught in Common Core 3rd grade.\n\n"
        f"Structure your response in exactly two sections with these exact headers:\n\n"
        f"## What This Method Is (and Why They Teach It This Way)\n"
        f"[Explain clearly for a mathematically literate adult who just never saw this approach. Include a small worked example.]\n\n"
        f"## How to Practice This at Home\n"
        f"[3-4 specific, hands-on activities — no worksheets. Things a parent and 8-year-old can actually do together.]"
    )

    try:
        with _client.messages.stream(
            model=MODEL,
            max_tokens=900,
            system=_PARENT_CONCEPT_SYSTEM,
            messages=[{"role": "user", "content": user_prompt}],
        ) as stream:
            for text in stream.text_stream:
                yield text
    except Exception as e:
        yield f"\n\n⚠️ Something went wrong: {e}. Please try again."


def explain_wrong_answer_for_parent(problem_dict: dict, wrong_answer: str) -> str:
    """
    Returns a parent-level explanation of a specific wrong answer.
    Used in the Parent Review page.
    """
    if not API_AVAILABLE or _client is None:
        return problem_dict.get("explanation_parent", "API unavailable. The explanation_parent field from the original problem is shown above.")

    problem_text = problem_dict.get("problem_text", "")
    correct = problem_dict.get("answer", "")

    user_prompt = (
        f"Problem: {problem_text}\n"
        f"Correct answer: {correct}\n"
        f"Child's wrong answer: {wrong_answer}\n\n"
        f"In 3-4 sentences explain: (1) which Common Core method or concept this tests, "
        f"(2) why '{wrong_answer}' is a common mistake, "
        f"(3) one concrete way to help a child understand the correct approach."
    )

    try:
        response = _client.messages.create(
            model=MODEL,
            max_tokens=300,
            system=_PARENT_WRONG_SYSTEM,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text.strip()
    except Exception:
        return problem_dict.get("explanation_parent", "Could not generate explanation. Please check your API key.")
