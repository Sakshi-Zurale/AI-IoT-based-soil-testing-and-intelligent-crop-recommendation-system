
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

REPORT_DIR = Path(__file__).resolve().parents[2] / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

MARATHI_FONT_PATH = Path(r"C:\Windows\Fonts\Nirmala.ttc")
MARATHI_FONT = "KrushiAINirmala"

CROP_TRANSLATIONS = {
    "rice": "भात",
    "maize": "मका",
    "chickpea": "हरभरा",
    "kidneybeans": "राजमा",
    "pigeonpeas": "तूर",
    "mothbeans": "मटकी",
    "mungbean": "मूग",
    "blackgram": "उडीद",
    "lentil": "मसूर",
    "pomegranate": "डाळिंब",
    "banana": "केळी",
    "mango": "आंबा",
    "grapes": "द्राक्षे",
    "watermelon": "कलिंगड",
    "muskmelon": "खरबूज",
    "apple": "सफरचंद",
    "orange": "संत्रे",
    "papaya": "पपई",
    "coconut": "नारळ",
    "cotton": "कापूस",
    "jute": "ताग",
    "coffee": "कॉफी",
    "wheat": "गहू",
    "sugarcane": "ऊस",
    "soybean": "सोयाबीन",
    "onion": "कांदा",
    "tomato": "टोमॅटो",
    "potato": "बटाटा",
    "groundnut": "भुईमूग",
    "sunflower": "सूर्यफूल",
    "millet": "बाजरी",
    "sorghum": "ज्वारी",
}

LABELS_MR = {
    "Farmer Information": "शेतकऱ्याची माहिती",
    "Soil Measurements": "मातीचे मोजमाप",
    "AI Crop Recommendations": "AI आधारित पीक शिफारसी",
    "Parameter": "घटक",
    "Value": "मूल्य",
    "Status": "स्थिती",
    "Crop": "पीक",
    "Model Score": "मॉडेल गुण",
    "Suitability": "योग्यता",
    "Name": "नाव",
    "Mobile": "मोबाईल क्रमांक",
    "Village": "गाव",
    "Taluka": "तालुका",
    "District": "जिल्हा",
    "State": "राज्य",
    "Farm/Plot": "शेताचे नाव",
    "Preferred Crop": "पसंतीचे पीक",
    "Nitrogen": "नायट्रोजन",
    "Phosphorus": "स्फुरद",
    "Potassium": "पालाश",
    "Soil Moisture": "मातीतील ओलावा",
    "Air Temperature": "हवेचे तापमान",
    "Humidity": "आर्द्रता",
    "Test ID": "चाचणी क्रमांक",
    "Data Source": "माहितीचा स्रोत",
    "Source": "स्रोत",
    "Explanation": "स्पष्टीकरण",
    "Important Notice": "महत्त्वाची सूचना",
}

STATUS_MR = {
    "normal": "सामान्य",
    "low": "कमी",
    "high": "जास्त",
    "adequate": "पुरेसे",
    "deficient": "कमतरता",
    "optimal": "योग्य",
    "moderate": "मध्यम",
    "unknown": "माहिती उपलब्ध नाही",
    "not available": "माहिती उपलब्ध नाही",
    "model-supported candidate": "मॉडेलने सुचवलेले पीक",
}


# ============================================================
# HELPERS
# ============================================================

def safe_text(value):
    """Escape dynamic text before placing it inside a PDF paragraph."""
    if value is None or str(value).strip() == "":
        return "Not supplied"
    return escape(str(value))


def display_value(value):
    if value is None or str(value).strip() == "":
        return "Not available"
    return str(value)


def register_marathi_font():
    if MARATHI_FONT in pdfmetrics.getRegisteredFontNames():
        return MARATHI_FONT

    if not MARATHI_FONT_PATH.exists():
        raise FileNotFoundError(
            f"Marathi font not found: {MARATHI_FONT_PATH}"
        )

    font = TTFont(
        MARATHI_FONT,
        str(MARATHI_FONT_PATH),
        subfontIndex=0,
        shapable=True,
    )
    pdfmetrics.registerFont(font)
    pdfmetrics.registerFontFamily(
        MARATHI_FONT,
        normal=MARATHI_FONT,
        bold=MARATHI_FONT,
        italic=MARATHI_FONT,
        boldItalic=MARATHI_FONT,
    )
    return MARATHI_FONT


def make_styles(bilingual=False):
    styles = getSampleStyleSheet()

    if bilingual:
        register_marathi_font()
        font = MARATHI_FONT
    else:
        font = "Helvetica"

    styles.add(ParagraphStyle(
        name="KrushiTitle",
        parent=styles["Title"],
        fontName=font,
        fontSize=16,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name="KrushiHeading",
        parent=styles["Heading2"],
        fontName=font,
        fontSize=11,
        leading=16,
        spaceBefore=8,
        spaceAfter=5,
    ))

    styles.add(ParagraphStyle(
        name="KrushiBody",
        parent=styles["BodyText"],
        fontName=font,
        fontSize=9,
        leading=13,
    ))

    styles.add(ParagraphStyle(
        name="KrushiSmall",
        parent=styles["BodyText"],
        fontName=font,
        fontSize=8,
        leading=11,
    ))

    return styles


def paragraph(text, style):
    return Paragraph(text, style)


def bilingual_cell(english, marathi, style):
    return Paragraph(
        f"{safe_text(english)}<br/>"
        f"<font name='{MARATHI_FONT}'>"
        f"{safe_text(marathi)}</font>",
        style,
    )


def translated_status(value):
    text = display_value(value)
    return STATUS_MR.get(text.lower().strip(), text)


def crop_name(crop):
    english = display_value(crop)
    marathi = CROP_TRANSLATIONS.get(
        english.lower().strip(), english
    )
    return english, marathi


def is_simulated(test):
    source = str(
        getattr(test, "input_source", "") or ""
    ).lower()
    return "simulat" in source or "developer" in source


def get_parameters(analysis):
    return analysis.get("parameters", {})


SOIL_FIELDS = [
    ("nitrogen", "Nitrogen", "नायट्रोजन"),
    ("phosphorus", "Phosphorus", "स्फुरद"),
    ("potassium", "Potassium", "पालाश"),
    ("soil_moisture", "Soil Moisture", "मातीतील ओलावा"),
    ("air_temperature", "Air Temperature", "हवेचे तापमान"),
    ("humidity", "Humidity", "आर्द्रता"),
]


def english_explanation(rec):
    crop = display_value(rec.crop)
    score = (
        "not available"
        if rec.ml_probability is None
        else f"{rec.ml_probability * 100:.1f}%"
    )

    return (
        f"The model ranked {safe_text(crop)} using the recorded soil "
        f"and environmental inputs. Its model score is {score}. "
        "This score is not the probability of a successful harvest "
        "and does not guarantee yield or profit."
    )


def marathi_explanation(rec):
    crop_en, crop_mr = crop_name(rec.crop)
    score = (
        "उपलब्ध नाही"
        if rec.ml_probability is None
        else f"{rec.ml_probability * 100:.1f}%"
    )

    return (
        f"{safe_text(crop_mr)} ({safe_text(crop_en)}) या पिकाला "
        "नोंदवलेल्या मातीच्या आणि पर्यावरणीय माहितीच्या आधारे "
        f"मॉडेलने क्रम दिला आहे. मॉडेल गुण: {score}. "
        "हे गुण पीक यशस्वी होण्याची शक्यता दर्शवत नाहीत. "
        "त्यावरून उत्पादन किंवा नफा निश्चित होत नाही."
    )


def make_document(path, margins=14 * mm):
    return SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=margins,
        leftMargin=margins,
        topMargin=margins,
        bottomMargin=margins,
    )


def make_table(rows, widths, bilingual=False, repeat_rows=0):
    table = Table(
        rows,
        colWidths=widths,
        repeatRows=repeat_rows,
    )
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def farmer_rows_english(farmer, styles):
    fields = [
        ("Name", farmer.name),
        ("Mobile", farmer.mobile),
        ("Village", farmer.village),
        ("Taluka", farmer.taluka),
        ("District", farmer.district),
        ("State", farmer.state),
        ("Farm/Plot", farmer.farm_name),
        ("Preferred Crop", farmer.preferred_crop),
    ]

    return [
        [
            Paragraph(safe_text(label), styles["KrushiSmall"]),
            Paragraph(safe_text(value), styles["KrushiBody"]),
        ]
        for label, value in fields
    ]


def farmer_rows_bilingual(farmer, styles):
    fields = [
        ("Name", "नाव", farmer.name),
        ("Mobile", "मोबाईल क्रमांक", farmer.mobile),
        ("Village", "गाव", farmer.village),
        ("Taluka", "तालुका", farmer.taluka),
        ("District", "जिल्हा", farmer.district),
        ("State", "राज्य", farmer.state),
        ("Farm/Plot", "शेताचे नाव", farmer.farm_name),
        ("Preferred Crop", "पसंतीचे पीक", farmer.preferred_crop),
    ]

    return [
        [
            bilingual_cell(en, mr, styles["KrushiSmall"]),
            Paragraph(safe_text(value), styles["KrushiBody"]),
        ]
        for en, mr, value in fields
    ]


# ============================================================
# ENGLISH REPORT
# ============================================================

def build_report(farmer, test, analysis, recommendations):
    path = REPORT_DIR / f"{test.test_id}.pdf"

    styles = make_styles()
    body = styles["KrushiBody"]
    small = styles["KrushiSmall"]
    heading = styles["KrushiHeading"]
    story = []

    story.append(Paragraph(
        "KrushiAI — Soil Testing &amp; Crop Recommendation Report",
        styles["KrushiTitle"],
    ))
    story.append(Paragraph(
        "Soil analysis and AI-assisted crop recommendations",
        body,
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        f"<b>Test ID:</b> {safe_text(test.test_id)}",
        body,
    ))
    story.append(Paragraph(
        f"<b>Data source:</b> {safe_text(test.input_source)}",
        body,
    ))

    if is_simulated(test):
        story.append(Paragraph(
            "<b>SIMULATED DATA:</b> These readings were generated by a "
            "developer simulator and are not live sensor measurements.",
            small,
        ))

    story.append(Paragraph("Farmer Information", heading))
    story.append(make_table(
        farmer_rows_english(farmer, styles),
        [45 * mm, 125 * mm],
    ))

    story.append(Paragraph("Soil Measurements", heading))
    story.append(Paragraph(
        "Values are shown as recorded by the system. Confirm units, "
        "sensor calibration, and laboratory results before using them "
        "for fertilizer or soil-treatment decisions.",
        small,
    ))

    params = get_parameters(analysis)
    rows = [[
        Paragraph("Parameter", small),
        Paragraph("Recorded value", small),
        Paragraph("System status", small),
    ]]

    for key, label, _ in SOIL_FIELDS:
        item = params.get(key, {})
        rows.append([
            Paragraph(safe_text(label), small),
            Paragraph(safe_text(item.get("value")), body),
            Paragraph(safe_text(item.get("status")), small),
        ])

    story.append(make_table(
        rows,
        [60 * mm, 45 * mm, 65 * mm],
        repeat_rows=1,
    ))

    # Weather section removed.

    story.append(Paragraph("AI Crop Recommendations", heading))
    story.append(Paragraph(
        "The model score is a relative model output, not the probability "
        "of a successful harvest. It does not guarantee yield or profit. "
        "Use local agronomic guidance before selecting a crop.",
        small,
    ))

    rows = [[
        Paragraph("Crop", small),
        Paragraph("Model score", small),
        Paragraph("System suitability label", small),
    ]]

    for rec in recommendations:
        score = (
            "Not available"
            if rec.ml_probability is None
            else f"{rec.ml_probability * 100:.1f}%"
        )
        rows.append([
            Paragraph(safe_text(rec.crop), body),
            Paragraph(score, body),
            Paragraph(safe_text(rec.suitability), small),
        ])

    story.append(make_table(
        rows,
        [48 * mm, 42 * mm, 80 * mm],
        repeat_rows=1,
    ))

    for rec in recommendations:
        story.append(Spacer(1, 5))
        story.append(Paragraph(
            f"<b>{safe_text(rec.crop)}</b>",
            body,
        ))
        story.append(Paragraph(
            english_explanation(rec),
            small,
        ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Important Notice", heading))
    story.append(Paragraph(
        "This report is a decision-support aid, not a substitute for "
        "laboratory soil testing or advice from a qualified local "
        "agricultural expert. Soil nutrient values and their interpretation "
        "depend on the measurement method and calibration. Consider crop "
        "season, irrigation, local climate, pests, input costs, and market "
        "conditions before making a farming decision.",
        small,
    ))

    make_document(path, margins=16 * mm).build(story)
    return path


# ============================================================
# BILINGUAL ENGLISH + MARATHI REPORT
# ============================================================

def build_bilingual_report(
    farmer,
    test,
    analysis,
    recommendations,
):
    path = REPORT_DIR / f"{test.test_id}_bilingual.pdf"

    register_marathi_font()

    styles = make_styles(bilingual=True)
    body = styles["KrushiBody"]
    small = styles["KrushiSmall"]
    heading = styles["KrushiHeading"]
    title = styles["KrushiTitle"]
    story = []

    story.append(Paragraph(
        "KrushiAI — Soil Testing &amp; Crop Recommendation Report<br/>"
        "<font name='KrushiAINirmala'>"
        "मृदा परीक्षण आणि पीक शिफारस अहवाल</font>",
        title,
    ))
    story.append(Paragraph(
        "Soil analysis and AI-assisted crop recommendations<br/>"
        "<font name='KrushiAINirmala'>"
        "मातीचे विश्लेषण आणि कृत्रिम बुद्धिमत्तेवर आधारित पीक शिफारसी"
        "</font>",
        body,
    ))
    story.append(Spacer(1, 7))

    story.append(bilingual_cell(
        f"Test ID: {test.test_id}",
        f"चाचणी क्रमांक: {test.test_id}",
        body,
    ))
    story.append(bilingual_cell(
        f"Data Source: {test.input_source}",
        f"माहितीचा स्रोत: {test.input_source}",
        body,
    ))

    if is_simulated(test):
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            "<b>SIMULATED DATA</b><br/>"
            "<font name='KrushiAINirmala'>"
            "<b>प्रात्यक्षिकासाठी तयार केलेली माहिती</b></font><br/>"
            "These readings were generated by a developer simulator, "
            "not by a live sensor.<br/>"
            "<font name='KrushiAINirmala'>"
            "ही माहिती डेव्हलपर सिम्युलेटरमधून तयार केली आहे; "
            "ती प्रत्यक्ष सेन्सरमधून घेतलेली नाही.</font>",
            small,
        ))

    story.append(Paragraph(
        "Farmer Information / शेतकऱ्याची माहिती",
        heading,
    ))
    story.append(make_table(
        farmer_rows_bilingual(farmer, styles),
        [65 * mm, 105 * mm],
    ))

    story.append(Paragraph(
        "Soil Measurements / मातीचे मोजमाप",
        heading,
    ))
    story.append(Paragraph(
        "Values are shown as recorded. Confirm measurement units and "
        "sensor calibration before making soil-treatment decisions.<br/>"
        "<font name='KrushiAINirmala'>"
        "मूल्ये प्रणालीमध्ये नोंदवल्याप्रमाणे दाखवली आहेत. "
        "मातीवर उपचार करण्यापूर्वी मोजमापाची एकके आणि सेन्सरचे "
        "कॅलिब्रेशन तपासा.</font>",
        small,
    ))

    params = get_parameters(analysis)
    rows = [[
        bilingual_cell("Parameter", "घटक", small),
        bilingual_cell("Recorded value", "नोंदवलेले मूल्य", small),
        bilingual_cell("System status", "प्रणालीतील स्थिती", small),
    ]]

    for key, english, marathi in SOIL_FIELDS:
        item = params.get(key, {})
        status = display_value(item.get("status"))

        rows.append([
            bilingual_cell(english, marathi, small),
            Paragraph(safe_text(item.get("value")), body),
            bilingual_cell(status, translated_status(status), small),
        ])

    story.append(make_table(
        rows,
        [62 * mm, 43 * mm, 65 * mm],
        repeat_rows=1,
    ))

    # Weather section removed.

    story.append(Paragraph(
        "AI Crop Recommendations / AI आधारित पीक शिफारसी",
        heading,
    ))
    story.append(Paragraph(
        "The model score is not the probability of a successful harvest "
        "and does not guarantee yield or profit.<br/>"
        "<font name='KrushiAINirmala'>"
        "मॉडेलचे गुण म्हणजे पीक यशस्वी होण्याची शक्यता नव्हे. "
        "त्यावरून उत्पादन किंवा नफा निश्चित होत नाही.</font>",
        small,
    ))

    rows = [[
        bilingual_cell("Crop", "पीक", small),
        bilingual_cell("Model score", "मॉडेल गुण", small),
        bilingual_cell("Suitability label", "योग्यतेचे वर्णन", small),
    ]]

    for rec in recommendations:
        english, marathi = crop_name(rec.crop)
        score = (
            "Not available"
            if rec.ml_probability is None
            else f"{rec.ml_probability * 100:.1f}%"
        )
        suitability = display_value(rec.suitability)
        suitability_mr = STATUS_MR.get(
            suitability.lower().strip(),
            suitability,
        )

        rows.append([
            bilingual_cell(english, marathi, small),
            Paragraph(score, body),
            bilingual_cell(suitability, suitability_mr, small),
        ])

    story.append(make_table(
        rows,
        [48 * mm, 47 * mm, 75 * mm],
        repeat_rows=1,
    ))

    for rec in recommendations:
        english, marathi = crop_name(rec.crop)

        story.append(Spacer(1, 6))
        story.append(Paragraph(
            f"<b>{safe_text(english)} / "
            f"<font name='KrushiAINirmala'>"
            f"{safe_text(marathi)}</font></b>",
            body,
        ))
        story.append(Paragraph(
            f"Explanation: {english_explanation(rec)}<br/>"
            f"<font name='KrushiAINirmala'>"
            f"स्पष्टीकरण: {marathi_explanation(rec)}</font>",
            small,
        ))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Important Notice / महत्त्वाची सूचना",
        heading,
    ))
    story.append(Paragraph(
        "This report is a decision-support aid, not a substitute for "
        "laboratory soil testing or advice from a qualified local "
        "agricultural expert. Confirm nutrient measurements, units, "
        "crop season, irrigation, and local conditions before acting "
        "on these recommendations.<br/>"
        "<font name='KrushiAINirmala'>"
        "हा अहवाल निर्णय घेण्यासाठी मदत करणारे साधन आहे. "
        "तो मातीच्या प्रयोगशाळेतील तपासणीचा किंवा स्थानिक कृषी "
        "तज्ज्ञांच्या सल्ल्याचा पर्याय नाही. या शिफारसींनुसार "
        "निर्णय घेण्यापूर्वी मातीतील पोषक घटकांची मोजमापे, एकके, "
        "पीक हंगाम, सिंचन आणि स्थानिक परिस्थिती तपासा.</font>",
        small,
    ))

    make_document(path).build(story)
    return path
