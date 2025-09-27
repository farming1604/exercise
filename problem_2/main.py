from dotenv import load_dotenv
import os
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import dspy

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def set_up_dspy_config(**kwargs):
    lm = dspy.LM(
        model="openrouter/gpt-oss-20b:free",
        api_key=OPENROUTER_API_KEY,
        **kwargs,
    )
    dspy.configure(
        lm=lm,
    )
    dspy.configure_cache(
        enable_disk_cache=False,
        enable_memory_cache=False,
    )

class TranslationStyle(str, Enum):
    FORMAL_ACADEMIC = "Formal / Academic"
    INFORMAL_CONVERSATIONAL = "Informal / Conversational"
    TECHNICAL_SPECIALIZED = "Technical / Specialized"
    LITERARY_CREATIVE = "Literary / Creative"
    BUSINESS_PROFESSIONAL = "Business / Professional"
    MARKETING_PERSUASIVE = "Marketing / Persuasive"
    NEUTRAL_LITERAL = "Neutral / Literal"
    HUMOROUS_CASUAL = "Humorous / Casual"

class Translator(dspy.Signature):
    """You are an expert professional translator with deep knowledge of multiple languages, linguistics, and cultural contexts. Your task is not only to translate words but to convey meaning, nuance, and tone as accurately as possible.
When processing the text provided:
1. Language Identification: Accurately detect the original language of the text, even if it contains mixed languages, slang, or technical jargon.
2. Accurate Translation: Translate the text into target_language with precision, keeping the meaning intact. Avoid literal translation if it changes the sense; prefer natural and fluent rendering in the target_language.
3. Preserve Original Structure: Maintain the original formatting, line breaks, punctuation, and paragraph structure. Do not alter names, proper nouns, or technical terms unless there is an established standard translation.
4. Maintain Style and Tone: Recognize and retain the style, tone, and register of the original text, including formal, informal, academic, literary, or technical style as specified by {style}.
5. Cultural Sensitivity: Be aware of cultural references, idioms, and context. Adapt them appropriately to ensure the translation is understandable and culturally relevant in the target language.
    """
    text: str = dspy.InputField(
        desc="Text to be translated",
    )
    target_language: str = dspy.InputField(
        desc="Target language for translation",
        default="vi",
    )
    translation_style: TranslationStyle = dspy.InputField(
        desc="Style of translation",
        default=TranslationStyle.INFORMAL_CONVERSATIONAL,
    )

    source_languages: list[str] = dspy.OutputField(
        desc="Detected source languages",
    )
    translated_text: str = dspy.OutputField(
        desc="Translated text",
    )

def solve_problem_3_1(input_data: dict):
    text = input_data.get("text", "")
    dest_language = input_data.get("dest_language", "vi")

    response = dspy.Predict(Translator)(
        text=text,
        target_language=dest_language,
        translation_style=TranslationStyle.FORMAL_ACADEMIC,
    )

    return response, input_data

def solve_problem_3_2(input_data: dict):
    texts = input_data.get("text", [])
    dest_language = input_data.get("dest_language", "vi")

    results: list[(dspy.Prediction, dict)] = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_text = {
            executor.submit(
                solve_problem_3_1,
                {
                    "text": text,
                    "dest_language": dest_language,
                }
            ): text for text in texts
        }

        for future in as_completed(future_to_text):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error processing text: {future_to_text[future]}. Error: {e}")

    results.sort(key=lambda x: texts.index(x[1]["text"]))
    results_only = [
        result[0] for result in results
    ]
    return results_only, input_data

if __name__ == "__main__":
    set_up_dspy_config(
        temperature=0.0,
    )

    output_problem_3_1, _ = solve_problem_3_1({
        "text": "Hello",
        "dest_language": "vi"
    })

    print("Output Problem 3.1:")
    print(output_problem_3_1.translated_text)

    output_problem_3_2, _ = solve_problem_3_2({
        "text": ["Hello", "I am Peter"],
        "dest_language": "vi"
    })

    print("Output Problem 3.2:")
    for result in output_problem_3_2:
        print(result.translated_text)