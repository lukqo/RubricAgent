import json


def build_evaluation_prompt(
    student_name: str,
    rubric: dict,
    code: str
) -> str:

    language = rubric.get(
        "language",
        "text"
    )

    restrictions = rubric.get(
        "restrictions",
        "No hay restricciones."
    )

    exercises = rubric.get(
        "exercises",
        []
    )

    if isinstance(exercises, list) and exercises:

        formatted_exercises = "\n\n".join(

            f"Ejercicio {item.get('id', '')}:\n"
            f"{item.get('description', '').strip()}"

            for item in exercises
        )

    else:

        formatted_exercises = (
            "No hay ejercicios específicos."
        )

    rubric_json = json.dumps(

        rubric["criteria"],

        ensure_ascii=False,

        indent=2
    )

    prompt = f"""
Evalúa el código {language} del alumno {student_name}.

EJERCICIO QUE DEBÍA RESOLVER:
{formatted_exercises}

RESTRICCIONES (elementos PROHIBIDOS en el código):
{restrictions}

NIVELES DE EVALUACIÓN:
- Destacado: implementado completo y sin errores
- Bueno: implementado con errores menores o algo faltante
- Aceptable: implementado parcialmente o con errores importantes
- Insuficiente: no implementado o no funciona

REGLAS OBLIGATORIAS:
1. Lista de listas en vez de listas separadas → Modelado baja UN nivel (Destacado→Bueno, Bueno→Aceptable)
2. Validación con números en vez de texto → Resolución baja UN nivel
3. if en vez de elif en el menú → Control de flujo baja UN nivel
4. try/except, funciones, clases o módulos → ese criterio baja UN nivel
5. Si el programa funciona y completa el objetivo → Resolución mínimo Aceptable, nunca Insuficiente
6. Cada error afecta SOLO su criterio correspondiente, no otros criterios
IMPORTANTE: La lista de listas afecta SOLO el criterio "Modelado de datos".
NO debe bajar la nota de Operadores, Strings, Control de flujo ni FOR por ese motivo.
Cada error tiene UN solo criterio donde se penaliza.

RÚBRICA:
{rubric_json}

CÓDIGO:
```{language}
{code}
```

Responde SOLO con este JSON, sin texto adicional:

{{
  "student_name": "{student_name}",
  "criteria_results": [
    {{
      "criterion_id": 1,
      "criterion_name": "Uso de operadores",
      "level": "Bueno",
      "score": 10,
      "feedback": "explicación concreta de qué hizo bien y qué le faltó"
    }}
  ],
  "general_feedback": "resumen de qué ejercicio resolvió, qué funcionó y qué falló"
}}
"""

    return prompt