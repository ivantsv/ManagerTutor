from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableConfig
from langchain_core.output_parsers import StrOutputParser

class RoleAgent:
    def __init__(self):
        self._llm = ChatOllama(
            model="mistral:7b",
            temperature=0.8
        )

        self._session_id = "default"

        self._chat_history = InMemoryChatMessageHistory()

        self._messages = [
            ("system", "{system}"),
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

    def answer(self, user_message: str, system: str) -> str:
        str_ai_response = self._final_chain.invoke(
            {"user_message": user_message, "system": system},
            config=RunnableConfig(configurable={"session_id": self._session_id}))
        return str_ai_response