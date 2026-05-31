import json
import requests


OLLAMA_URL = "http://200.27.101.243:11434/api/chat"

OLLAMA_MODEL = "gemma4:e2b"


def evaluate_with_llm(
    prompt: str,
    student_name: str
) -> dict:

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,

            "messages": [
                {
                    "role": "system",
                    "content": """
Eres un evaluador automático de código.

Tu única tarea es responder JSON válido.

NO expliques.
NO converses.
NO des ejemplos.
NO escribas markdown.

La respuesta DEBE ser JSON válido.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            "stream": False,

            "format": "json",

            "options": {
                "temperature": 0
            }
        }
    )

    if response.status_code != 200:

        raise Exception(
            f"""
Error Ollama.

Status:
{response.status_code}

Respuesta:
{response.text}
"""
        )

    raw_response = response.json()

    content = raw_response["message"]["content"]

    print("\n========== RAW RESPONSE ==========")
    print(content)
    print("==================================\n")

    try:

        parsed_json = json.loads(content)

        return parsed_json

    except Exception as e:

        raise Exception(
            f"""
            Error parseando JSON.

            Error:
            {str(e)}

            Contenido:
            {content}
            """)