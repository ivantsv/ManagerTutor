from langchain_core.prompts import PromptTemplate

EVALUATION_PROMPT = """You are an expert tutor evaluating a manager's feedback skills. Analyze the conversation between a manager (student) and an employee (AI role).
Answer in Russian.

**Expected framework:** {expected_framework} (e.g., SBI, Radical Candor, BOFF)

**Conversation history:**
{chat_history}

Evaluate the manager's performance based on these metrics:

1. **Specificity (0-10)**: Did they use concrete examples instead of vague statements?
2. **Structure (0-10)**: Did they follow the framework correctly? (e.g., Situation-Behavior-Impact for SBI)
3. **Empathy (0-10)**: Was the tone respectful and considerate?
4. **Actionability (0-10)**: Did they provide clear next steps or suggestions?
5. **Timing and Relevance (0-10)**: Was the feedback appropriate for the situation?

**Output format (JSON):**
```json
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
```

Be critical but constructive. Focus on actionable improvements."""

evaluation_prompt = PromptTemplate(
    input_variables=["expected_framework", "chat_history"],
    template=EVALUATION_PROMPT
)