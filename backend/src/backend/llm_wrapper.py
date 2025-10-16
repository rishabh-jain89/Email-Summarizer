from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiCrewAI(ChatGoogleGenerativeAI):

    def supports_stop_words(self) -> bool:
        return False

    def call(self, prompt, stop=None, **kwargs):
        response = self.invoke(prompt)
        return getattr(response, "content", str(response))
