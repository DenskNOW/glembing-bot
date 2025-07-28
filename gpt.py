import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_post():
    prompt = (
        "Напиши короткий мотивационный пост в Telegram на тему: "
        "'Путь к $100,000 через стратегии Glembing'. "
        "Стиль: воодушевляющий, современный, немного провокационный. "
        "Макс. 100 слов."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    return response["choices"][0]["message"]["content"].strip()