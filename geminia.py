import google.generativeai as genai
import PyPDF2

from const import GOOGLE_API_KEY


class GeminiIa:
    def __init__(self) -> None:
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(
            "gemini-pro",
            generation_config={"candidate_count": 1, "temperature": 0.5},
        )

    def _get_pdf_text(self, filename):
        with open(f"files/{filename}", "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            return text

    def execute(self, filename):
        try:
            pdf_text = self._get_pdf_text(filename)
            prompt = f"Gere 10 perguntas e depois uma lista com suas respostas deste texto: \n\n{pdf_text}"
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return "Seu arquivo é muito grande. Podemos tentar com um outro?"
