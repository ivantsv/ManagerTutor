from langchain_core.prompts import PromptTemplate

EVALUATION_PROMPT = """
You are an expert tutor evaluating a manager's feedback skills. Analyze the conversation between a manager (student) and an employee (AI role).
Answer in Russian.

**Expected framework:** {{ expected_framework }} (e.g., SBI, Radical Candor, BOFF)

Analyze the conversation history and evaluate the manager's performance based on these metrics:

1. **Specificity (0-10)** — concrete examples instead of vague statements?
2. **Structure (0-10)** — followed the framework correctly?
3. **Empathy (0-10)** — respectful and considerate tone?
4. **Actionability (0-10)** — clear next steps?
5. **Timing (0-10)** — appropriate feedback timing?

**Output format (JSON):**
{% raw %}
{
  "total_score": 0-100,
  "metrics": {
    "specificity": {"score": 0-10, "comment": "короткий комментарий на русском"},
    "structure": {"score": 0-10, "comment": "короткий комментарий на русском"},
    "empathy": {"score": 0-10, "comment": "короткий комментарий на русском"},
    "actionability": {"score": 0-10, "comment": "короткий комментарий на русском"},
    "timing": {"score": 0-10, "comment": "короткий комментарий на русском"}
  },
  "strengths": ["сильная сторона 1", "сильная сторона 2"],
  "areas_for_improvement": ["что улучшить 1", "что улучшить 2"],
  "example_feedback": "Пример того, как можно было бы сформулировать лучше"
}
{% endraw %}

Be critical but constructive. Focus on actionable improvements. Always mention strengths.
"""

evaluation_prompt_template = PromptTemplate(
    input_variables=["expected_framework"],
    template=EVALUATION_PROMPT,
    template_format="jinja2",
)