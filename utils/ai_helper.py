from config import API_KEYS
import google.generativeai as genai
import openai

def call_ai(model, prompt):
    if model.lower() == "gemini":
        genai.configure(api_key=API_KEYS["Gemini"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text

    elif model.lower() == "openai":
        openai.api_key = API_KEYS["OpenAI"]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    elif model.lower() == "deepseek":
        return "DeepSeek integration pending."

    return "Unsupported model."
