"""
All OpenAI API interactions.
Every function is wrapped in try/except — API failures must never crash the child's session.
"""

import json
import os
from typing import Generator

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

MODEL = "gpt-5-mini"

_PROBLEM_SYSTEM = """You are a math problem generator for a New York City summer bridge app helping a rising 4th grader.

CRITICAL: Respond with ONLY valid JSON — no markdown fences, no explanation, no other text.

Required schema (all keys mandatory):
{
  "problem_text": "string — clear, specific math question at an elementary reading level",
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
  "explanation_parent": "string — 3-4 sentences: name the method or standard idea, explain a likely mistake, and how a parent can help"
}

Rules:
- distractors must contain EXACTLY 3 items
- answer must NOT appear in distractors
- hint_1 must NEVER contain the answer or a number equal to the answer
- choose a visual when it helps elementary understanding:
  - array for multiplication, area, multiplicative comparison
  - fraction for fraction problems
  - number_line for fraction or decimal placement
  - bar_graph for data questions
  - clock for elapsed time or time-telling
  - none otherwise
- the problem must match the requested standard and subtopic
- the problem must be solvable by a typical rising 4th grader in under 2 minutes
- keep contexts child-friendly and realistic without being babyish"""

_HINT_SYSTEM = """You are a kind, patient math tutor helping an elementary student. Your ONLY job is to give hints that help the child think — you must NEVER reveal the answer, give the answer value, or say any number that equals the answer.

Rules:
- 1-2 sentences maximum
- Use simple, warm, encouraging language
- Ask a Socratic question that guides thinking
- Never say "the answer is" or complete the calculation for the child
- Never include the numerical value of the correct answer"""

_PARENT_CONCEPT_SYSTEM = """You are explaining elementary math methods to a parent who is mathematically literate but may not have learned using current school methods.

Be direct, clear, and adult. No condescension. Explain the pedagogical why, not just the steps. Use a concrete example with small numbers. Keep it practical."""

_PARENT_WRONG_SYSTEM = """You are explaining a math problem to a parent who wants to understand why their child may have made a specific error. Be concise, accurate, and practical."""


def _validate_problem(problem: dict) -> bool:
    required = {
        "problem_text",
        "answer",
        "distractors",
        "visual_type",
        "visual_data",
        "hint_1",
        "explanation_child",
        "explanation_parent",
    }
    if not required.issubset(problem.keys()):
        return False
    if not isinstance(problem["distractors"], list) or len(problem["distractors"]) != 3:
        return False
    if problem["answer"] in problem["distractors"]:
        return False
    return True


def _read_runtime_value(name: str, default: str = "") -> str:
    value = os.environ.get(name)
    if value:
        return value
    try:
        import streamlit as st
        secret_value = st.secrets.get(name, default)
        if secret_value:
            return secret_value
    except Exception:
        pass
    return default


def _get_client_and_model():
    api_key = _read_runtime_value("OPENAI_API_KEY", "")
    model = _read_runtime_value("OPENAI_MODEL", MODEL)
    if OpenAI is None or not api_key:
        return None, model
    try:
        return OpenAI(api_key=api_key), model
    except Exception:
        return None, model


def _create_text_response(instructions: str, user_prompt: str, max_output_tokens: int = 900) -> str:
    client, model = _get_client_and_model()
    if client is None:
        raise RuntimeError("OpenAI API unavailable")

    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=[{"role": "user", "content": user_prompt}],
        max_output_tokens=max_output_tokens,
        store=False,
    )
    return response.output_text.strip()


def generate_problem(topic_key: str, subtopic: str = None, difficulty: str = "medium") -> dict:
    """
    Returns a problem dict. Falls back to data_loader fallback on any error.
    difficulty: "easy" | "medium" | "hard"
    """
    from utils.data_loader import TOPICS, LANES, get_fallback_problem

    runtime_client, _runtime_model = _get_client_and_model()
    if runtime_client is None:
        return get_fallback_problem(topic_key)

    topic_info = TOPICS.get(topic_key, {})
    standard = topic_info.get("standard", topic_key)
    topic_label = topic_info.get("label", topic_key)
    lane_key = topic_info.get("lane", "grade3_review")
    lane_label = LANES.get(lane_key, {}).get("label", lane_key)
    sub = subtopic or (topic_info.get("subtopics", [""])[0])

    user_prompt = (
        f"Generate one summer bridge math problem.\n"
        f"Lane: {lane_label}\n"
        f"Standard: {standard}\n"
        f"Topic area: {topic_label}\n"
        f"Subtopic: {sub}\n"
        f"Difficulty: {difficulty}\n\n"
        f"If the lane is Grade 3 Review, reinforce third grade foundations.\n"
        f"If the lane is Grade 4 Preview, preview fourth grade thinking in a gentle way.\n"
        f"The problem must be multiple-choice-friendly with one unambiguous correct answer."
    )

    try:
        raw = _create_text_response(_PROBLEM_SYSTEM, user_prompt, max_output_tokens=900)
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
    runtime_client, _runtime_model = _get_client_and_model()
    if runtime_client is None:
        return problem_dict.get(
            "hint_1",
            "Think about what the problem is asking you to find. What do you already know?",
        )

    problem_text = problem_dict.get("problem_text", "")
    answer = problem_dict.get("answer", "")

    if attempt_count == 0:
        directness = "Give a gentle opening question to help the child get started."
    else:
        directness = (
            f"The child has asked for {attempt_count + 1} hints. Be a bit more direct, "
            f"but still do not reveal the answer."
        )

    user_prompt = (
        f"Problem: {problem_text}\n"
        f"Correct answer (DO NOT reveal): {answer}\n\n"
        f"{directness}"
    )

    try:
        return _create_text_response(_HINT_SYSTEM, user_prompt, max_output_tokens=140)
    except Exception:
        return problem_dict.get("hint_1", "Think carefully — what do you already know that might help?")


def explain_concept_for_parent(topic_key: str, subtopic: str = None) -> Generator[str, None, None]:
    """
    Generator for st.write_stream(). Yields a single completed response.
    """
    from utils.data_loader import TOPICS, LANES

    runtime_client, _runtime_model = _get_client_and_model()
    if runtime_client is None:
        yield "⚠️ API unavailable. Please check your OPENAI_API_KEY and try again."
        return

    topic_info = TOPICS.get(topic_key, {})
    topic_label = topic_info.get("label", topic_key)
    standard = topic_info.get("standard", topic_key)
    lane_label = LANES.get(topic_info.get("lane", ""), {}).get("label", "Summer Bridge")
    sub = subtopic or ""

    topic_str = f"{topic_label} ({standard})"
    if sub:
        topic_str += f" — specifically '{sub}'"

    user_prompt = (
        f"Explain how **{topic_str}** fits into the {lane_label} lane of a Grade 3 to 4 Math Bridge app.\n\n"
        f"Structure your response in exactly two sections with these exact headers:\n\n"
        f"## What This Method Is (and Why They Teach It This Way)\n"
        f"[Explain clearly for a mathematically literate adult who may not have seen this approach. Include a small worked example.]\n\n"
        f"## How to Practice This at Home\n"
        f"[Give 3-4 specific, hands-on activities. No worksheets. Use activities a parent and rising fourth grader can do together over the summer.]"
    )

    try:
        yield _create_text_response(_PARENT_CONCEPT_SYSTEM, user_prompt, max_output_tokens=1000)
    except Exception as exc:
        yield f"\n\n⚠️ Something went wrong: {exc}. Please try again."


def explain_wrong_answer_for_parent(problem_dict: dict, wrong_answer: str) -> str:
    """
    Returns a parent-level explanation of a specific wrong answer.
    Used in the Parent Review page.
    """
    runtime_client, _runtime_model = _get_client_and_model()
    if runtime_client is None:
        return problem_dict.get(
            "explanation_parent",
            "API unavailable. The saved parent explanation is shown instead.",
        )

    problem_text = problem_dict.get("problem_text", "")
    correct = problem_dict.get("answer", "")

    user_prompt = (
        f"Problem: {problem_text}\n"
        f"Correct answer: {correct}\n"
        f"Child's wrong answer: {wrong_answer}\n\n"
        f"In 3-4 sentences explain: "
        f"(1) which math idea or method this tests, "
        f"(2) why '{wrong_answer}' is a common mistake, and "
        f"(3) one concrete way to help a child understand the better approach."
    )

    try:
        return _create_text_response(_PARENT_WRONG_SYSTEM, user_prompt, max_output_tokens=300)
    except Exception:
        return problem_dict.get("explanation_parent", "Could not generate explanation. Please check your API key.")
