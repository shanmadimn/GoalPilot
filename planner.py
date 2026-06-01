import json
import re

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

import streamlit as st

groq_api_key = st.secrets["GROQ_API_KEY"]

def generate_plan(goal, duration, difficulty, model_name):

    
    llm = ChatGroq(
        model=model_name or "llama-3.3-70b-versatile",
        temperature=0.2,
        api_key=groq_api_key
    )
    
    template = """
    You are an AI execution planning assistant.

    Your job is to generate a structured plan in JSON format.

    Goal: {goal}
    Duration: {duration} months
    Difficulty Level: {difficulty}

    IMPORTANT:
    - 1 month = 4 weeks
    - Total weeks MUST be exactly {duration} * 4
    - Do NOT generate extra or fewer weeks

    Structure:
    {{
      "goal": "...",
      "duration_months": {duration},
      "difficulty": "...",
      "milestones": [
        {{
          "title": "...",
          "weeks": [
            {{
              "week": 1,
              "tasks": ["...", "..."]
            }}
          ]
        }}
      ]
    }}

    Difficulty Guidelines:
    Easy: 2–3 tasks
    Medium: 3–5 tasks
    Hard: 5–7 tasks

    Return ONLY valid JSON.
    """

    prompt = PromptTemplate(
        input_variables=["goal", "duration", "difficulty"],
        template=template,
    )

    chain = prompt | llm

    max_retries = 5

    for attempt in range(max_retries):
      response = chain.invoke({
        "goal": goal,
        "duration": duration,
        "difficulty": difficulty
      })

      response_text = response.content
      print("RAW LLM OUTPUT:\n", response_text)

      json_match = re.search(r'\{[\s\S]*\}', response_text)

      if not json_match:
        continue

      try:
        result = json.loads(json_match.group())

        expected_weeks = duration * 4

        # 🔹 Flatten all weeks
        all_weeks = []
        for m in result.get("milestones", []):
          for w in m.get("weeks", []):
            all_weeks.append(w)

        # 🔹 Trim extra weeks if LLM gives more
        all_weeks = all_weeks[:expected_weeks]

        # 🔹 If fewer weeks, retry
        if len(all_weeks) < expected_weeks:
          continue

        # 🔹 Reassign into a clean structure (single milestone OR keep yours if needed)
        result["milestones"] = [{
          "title": "Execution Plan",
          "weeks": all_weeks
        }]

        # 🔹 Fix week numbering
        week_counter = 1
        for w in all_weeks:
          w["week"] = week_counter
          week_counter += 1

        return result
            
      except Exception as e:
        print("JSON ERROR:", e)
        continue

    # ❌ After retries fail
    return {
        "error": f"Failed to generate correct plan after {max_retries} attempts. Try again."
    }
