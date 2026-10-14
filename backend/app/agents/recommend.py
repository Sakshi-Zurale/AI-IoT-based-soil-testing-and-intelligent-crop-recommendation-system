def explain(crop, soil_analysis, preferred, rag_docs):
    statuses = {
        k: v["status"]
        for k, v in soil_analysis["parameters"].items()
    }

    positives = [
        k for k, v in statuses.items()
        if v == "Normal"
    ]

    base = (
        f"{crop} was returned by the Random Forest model "
        "using the available soil and environmental inputs."
    )

    soil_note = (
        " Parameters within the configured reference range: "
        f"{', '.join(positives) if positives else 'none'}."
    )

    pref_note = (
        " This matches the farmer's preferred crop."
        if preferred and preferred.lower() == crop.lower()
        else (
            " The farmer's preferred crop is evaluated separately."
            if preferred else ""
        )
    )

    rag_note = (
        f" Agricultural context retrieved from the local "
        f"knowledge base included: {rag_docs[0]['title']}."
        if rag_docs else ""
    )

    return base + soil_note + pref_note + rag_note


def compatibility(preferred, crop, soil_analysis):
    statuses = [
        v["status"]
        for v in soil_analysis["parameters"].values()
    ]

    soil = (
        "Compatible with available soil indicators"
        if statuses.count("Normal") >= 3
        else "Requires closer soil review"
    )

    pref = (
        "Matches preference"
        if preferred and preferred.lower() == crop.lower()
        else (
            "Different from preference"
            if preferred else "No preference supplied"
        )
    )

    suitability = "Model-supported candidate"

    return suitability, soil, pref