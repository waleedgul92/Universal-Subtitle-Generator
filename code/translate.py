from transcribe import save_translated_text
from model import load_gemini_model
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def translate_text(llm, text, target_language="english", source_language="japanese", audio_filename=None):
    """
    Translates the given text to the target language using the loaded Gemini model.
    """
    
    if not llm:
        logger.error("Translation model is not available.")
        return "Translation model is not available.", None

    if not text:
        logger.error("No text provided for translation.")
        return "No text provided for translation.", None

    try:
        logger.info(f"Translating text to {target_language} from {source_language}... ")
        logger.info(f"Text to translate: {text[:100]}...")  # Log the first 100 characters for brevity
        response = llm.invoke(
            f"Translate the following text to {target_language}: {text}.The original language is {source_language}. DO NOT CHANGE THE FORMAT OF THE TEXT, ONLY TRANSLATE IT. \
            KEEP THE TIMESTAMP AS IT IS . PLUS IGNORE THE TIMESTAMP DURING \
            TRANSLATION. TAKE WHOLE TEXT AS INPUT AND TRANSLATE IT TO {target_language}.\
            MAP THE TIMESTAMP TO THE TRANSLATED TEXT. \
            DO NOT ADD ANYTHING EXTRA. "
        )
        logger.info("Translation completed successfully.")
        if not response or not hasattr(response, 'content'):
            logger.error("Invalid response from the translation model.")
            return "Translation failed due to an invalid response.", None
        
        # Save the translated text with descriptive filename
        output_path = save_translated_text(
            response.content, 
            audio_filename=audio_filename, 
            source_language=source_language, 
            target_language=target_language
        )
        
        return response.content, output_path
        
    except Exception as e:
        logger.error(f"Error during translation: {e}")
        return "Translation failed due to an error.", None
    

    
# text=""
# input_file = "./files/transcription.vtt"
# target_language = "english"
# source_language = "japanese"
# with open(input_file, "r", encoding="utf-8") as f:
#     text = f.read()
# llm = load_gemini_model()
# translated_text = translate_text(llm,text, target_language,source_language)
# save_translated_text(translated_text)