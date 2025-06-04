from config import API_KEYS
import openai
import google.generativeai as genai

def call_ai(model_name, prompt):
    if model_name == "Gemini":
        genai.configure(api_key=API_KEYS["Gemini"])
        model = genai.GenerativeModel("gemini-2.0-flash")
        return model.generate_content(prompt).text

    elif model_name == "OpenAI":
        openai.api_key = API_KEYS["OpenAI"]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    elif model_name == "DeepSeek":
        return f"[DeepSeek placeholder] Prompt: {prompt}"

    else:
        return "❌ Unsupported model."
