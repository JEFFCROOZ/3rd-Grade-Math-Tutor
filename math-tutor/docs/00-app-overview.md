# 00 — App Overview & Design Notes

Internal reference document. Explains what this version of the app is for and why it is shaped the way it is.

## Why This Exists

The original app solved a real family problem: a child needed math practice that matched school methods, and a parent needed help understanding the method well enough to coach at home.

This version keeps that core idea, but changes the timing and scope. Instead of being a pure Grade 3 practice app, it is now a **summer bridge**:

1. lock in third grade foundations that still feel shaky
2. introduce fourth grade ideas early enough that the school-year jump feels smaller

That makes the app useful for tutoring over the summer, not just test prep during the school year.

## Who This Is For

- **Primary user**: a rising fourth grader who should be able to practice mostly independently
- **Secondary user**: a parent who can do the math, but wants to understand the method, the vocabulary, and the instructional logic behind it

## Core Product Shape

### Child mode

- Pick a topic from one of two lanes: `Grade 3 Review` or `Grade 4 Preview`
- Get one problem at a time
- Ask for hints without seeing the answer
- Earn stars for correct answers
- End with a short session summary

### Parent mode

- See progress by topic
- Set a focus topic
- Learn the method in adult language
- Review wrong answers one by one

## Key Design Decisions

### Keep Streamlit

The app already has a good-enough child and parent experience in Streamlit. Rewriting to a different framework would slow down the educational improvements that matter most right now.

### Keep the app shell, swap the content layer

Most of the original architecture was reusable:

- page flow
- state handling
- star system
- parent dashboard
- wrong-answer review
- persistence layer

The real scope change lives in:

- standards and topic definitions
- fallback content
- prompt wording
- docs and setup instructions

### Switch from Anthropic to OpenAI

The live AI layer now uses the **OpenAI Responses API**. This keeps billing under one provider and follows current OpenAI guidance for new projects. The default model is `gpt-5-mini`, which is fast and cost-efficient for structured text generation.

### Preserve dual persistence paths

This repo now keeps both existing storage approaches:

- file-based progress for local use
- optional Postgres when `DATABASE_URL` is available

That avoids breaking the current lightweight setup while keeping a cleaner upgrade path for persistent hosted usage.

### Make the Grade 4 content a preview, not a pressure test

The fourth grade lane should feel like a head start, not a sudden jump in difficulty. That means:

- clearer wording
- moderate problem complexity
- lots of conceptual framing
- continued use of visuals where helpful

## What the Model Does

- generates varied practice problems
- provides one pre-generated hint with each problem
- writes child-safe method explanations
- writes adult-facing parent explanations
- explains wrong answers on demand
- returns structured visual payloads for Python to render

## What the Model Does Not Do

- control navigation
- decide app state
- directly render HTML for visuals
- persist data

The model is a content engine, not the app itself.

## Educational Framing

The bridge follows the broad structure of New York elementary math expectations:

- Grade 3 review emphasizes multiplication/division, place value to 1,000, early fractions, area/perimeter, and shape attributes.
- Grade 4 preview emphasizes multiplicative comparison, multi-step problems, larger place value, multi-digit operations, fraction equivalence and operations, measurement conversions, angles, and geometry classification.

The app is not trying to replace curriculum. It is trying to make home tutoring more aligned, more consistent, and less frustrating.
