from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableConfig
from langchain_core.output_parsers import StrOutputParser
from .prompts.mentor_prompt import mentor_prompt_template

class MentorAgent:
    def __init__(self, mistralai_api_key: str):
        self._llm = ChatMistralAI(
            model="mistral-small-latest",
            temperature=0.3,
            mistral_api_key=mistralai_api_key,
        )

        self._session_id = "default"

        self._chat_history = InMemoryChatMessageHistory()

        self._system_prompt = mentor_prompt_template.format()

        self._messages = [
            ("system", self._system_prompt),
            MessagesPlaceholder("history"),
            ("user", "{user_message}")
        ]
        self._prompt = ChatPromptTemplate(self._messages)

        self._chain = self._prompt | self._llm
        self._chain_with_history = RunnableWithMessageHistory(
            self._chain,
            lambda session_id: self._chat_history,
            input_messages_key="user_message",
            history_messages_key="history"
        )

        self._final_chain = self._chain_with_history | StrOutputParser()

    def answer(self, user_message: str) -> str:
        """Функция ведения диалога с пользователем"""
        str_ai_response = self._final_chain.invoke(
            {"user_message": user_message},
            config=RunnableConfig(configurable={"session_id": self._session_id})
        )
        return str_ai_response

    def clear_memory(self):
        """Очистить память агента"""
        self._chat_history.clear()