from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .prompts.evaluation_prompt import evaluation_prompt_template
import json
import re


class EvaluationAgent:
    def __init__(self, mistralai_api_key: str, expected_framework: str):
        self._llm = ChatMistralAI(
            model="mistral-small-latest",
            temperature=0.3,
            mistral_api_key=mistralai_api_key,
        )

        self._expected_framework = expected_framework

        system_prompt = SystemMessagePromptTemplate(prompt=evaluation_prompt_template)

        user_prompt = HumanMessagePromptTemplate.from_template("Проанализируй этот разговор:\n{chat_history}")

        self._prompt = ChatPromptTemplate.from_messages([system_prompt, user_prompt])

        self._chain = self._prompt | self._llm | StrOutputParser()

    def _extract_json(self, text: str) -> dict:
        """Извлекает JSON из ответа модели"""
        try:
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)

            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))

            raise ValueError("No JSON found in response")

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}")

    def analyze(self, chat_history: list) -> dict:
        """
        Анализирует историю чата и возвращает словарь с оценкой

        Args:
            chat_history: список словарей [{'role': 'user', 'content': '...'}, ...]

        Returns:
            dict с полями: total_score, metrics, strengths, areas_for_improvement, example_feedback
        """
        history_text = "\n".join([
            f"{'Менеджер' if msg['role'] == 'user' else 'Сотрудник'}: {msg['content']}"
            for msg in chat_history
        ])

        response = self._chain.invoke({
            "expected_framework": self._expected_framework,
            "chat_history": history_text
        })

        try:
            evaluation = self._extract_json(response)
            return evaluation
        except ValueError as e:
            print(f"Error parsing evaluation: {e}")
            print(f"Raw response: {response}")
            return {
                "total_score": 70,
                "metrics": {
                    "specificity": {"score": 7, "comment": "Ошибка парсинга"},
                    "structure": {"score": 7, "comment": "Ошибка парсинга"},
                    "empathy": {"score": 7, "comment": "Ошибка парсинга"},
                    "actionability": {"score": 7, "comment": "Ошибка парсинга"},
                    "timing": {"score": 7, "comment": "Ошибка парсинга"}
                },
                "strengths": ["Не удалось распарсить ответ"],
                "areas_for_improvement": ["Попробуйте снова"],
                "example_feedback": "Ошибка парсинга"
            }