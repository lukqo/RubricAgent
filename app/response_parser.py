def normalize_response(response: dict) -> dict:

    normalized_results = []

    criteria_results = response.get(
        "criteria_results",
        []
    )

    # Filtrar criterios duplicados o inválidos por criterion_id
    seen_ids = set()
    clean_results = []
    for index, item in enumerate(criteria_results):
        raw_id = item.get("criterion_id", index + 1)
        # Convertir a int, si falla usar el índice
        try:
            cid = int(raw_id)
        except (ValueError, TypeError):
            cid = index + 1
        # Saltar duplicados
        if cid in seen_ids:
            continue
        seen_ids.add(cid)
        item["criterion_id"] = cid
        clean_results.append(item)

    total_score = 0
    for index, item in enumerate(clean_results):

        criterion_name = (
            item.get("criterion_name")
            or item.get("name")
            or item.get("criterion")
            or item.get("category")
            or f"Criterio {index + 1}"
        )

        level = (
            item.get("level")
            or item.get("performance")
            or "Básico"
        )

        feedback = (
            item.get("feedback")
            or item.get("comment")
            or item.get("observation")
            or "Sin observaciones."
        )

        normalized_item = {

            "criterion_id":
                item.get(
                    "criterion_id",
                    index + 1
                ),

            "criterion_name":
                criterion_name,

            "level":
                level,

            "score":
                int(float(str(item.get("score", 0)).replace("points", "0").strip()))
                if str(item.get("score", 0)).replace("points", "0").strip().replace(".", "").isdigit()
                else 0,

            "feedback":
                feedback
        }
        total_score += normalized_item["score"]

        normalized_results.append(
            normalized_item
        )

    feedback_lines = []

    for item in normalized_results:

        feedback = item.get(
            "feedback",
            ""
        ).strip()

        if feedback:

            feedback_lines.append(
                f"{feedback}"
            )

    llm_general_feedback = response.get(
        "general_feedback",
        ""
    ).strip()

    if llm_general_feedback:

        feedback_lines.append("")
        feedback_lines.append(
            "Conclusión general:"
        )

        feedback_lines.append(
            llm_general_feedback
        )

    final_general_feedback = " ".join(
        feedback_lines
    )

    normalized_response = {

        "student_name":
            response.get(
                "student_name",
                "Desconocido"
            ),

        "criteria_results":
            normalized_results,

        "total_score": str(total_score),

        "general_feedback":
            final_general_feedback
    }

    return normalized_response