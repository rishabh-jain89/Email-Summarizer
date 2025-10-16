from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiCrewAI(ChatGoogleGenerativeAI):

    def supports_stop_words(self) -> bool:
        return False

    def token_counter(self, text: str) -> int:
        return len(text.split())

    @property
    def model_name(self):
        return self.model

    def call(self, prompt, stop=None, **kwargs):
        response = self.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)
