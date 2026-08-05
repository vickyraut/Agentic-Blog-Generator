# Language Categories and Language Options

CATEGORY_GLOBAL = "🌍 Global Languages"
CATEGORY_INDIAN = "🇮🇳 Indian Languages"

LANGUAGE_CATEGORIES = [CATEGORY_GLOBAL, CATEGORY_INDIAN]

GLOBAL_LANGUAGES = [
    "English",
    "Spanish",
    "French",
    "German",
    "Portuguese",
    "Chinese (Simplified)",
    "Japanese",
    "Korean",
    "Arabic",
    "Russian"
]

INDIAN_LANGUAGES = [
    "English",
    "Hindi",
    "Marathi",
    "Gujarati",
    "Bengali",
    "Punjabi",
    "Tamil",
    "Telugu",
    "Kannada",
    "Malayalam"
]

def get_languages_for_category(category: str) -> list[str]:
    """Return language list based on selected category."""
    if category == CATEGORY_INDIAN:
        return INDIAN_LANGUAGES
    return GLOBAL_LANGUAGES
