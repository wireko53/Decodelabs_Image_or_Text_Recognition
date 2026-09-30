from pathlib import Path
import cv2
import pytesseract

# Explicitly declare Tesseract binary location for Windows environment
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- Pipeline Configuration ---
SCRIPT_DIR = Path(__file__).parent
IMAGE_PATH = str(SCRIPT_DIR / "sample_image.jpg")

# Adaptive threshold parameters: Gaussian window size of 11 pixels handles local illumination gradients well,
# while C=2 acts as a slight bias subtractor to separate low-contrast character edges from background noise.
ADAPTIVE_BLOCK_SIZE = 11
ADAPTIVE_C = 2

# GUI Display Configuration
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 800


def preprocess_document_image(raw_image_path: str):
    """Converts input image to grayscale and applies local adaptive thresholding."""
    raw_image = cv2.imread(raw_image_path)
    if raw_image is None:
        raise FileNotFoundError(f"Could not load image file from {raw_image_path}")

    grayscale_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)

    # Using Gaussian adaptive thresholding over global Otsu thresholding because real-world document 
    # scans often suffer from non-uniform light sources and shadow gradients across the page.
    binary_threshold_image = cv2.adaptiveThreshold(
        grayscale_image,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=ADAPTIVE_BLOCK_SIZE,
        C=ADAPTIVE_C
    )

    return raw_image, binary_threshold_image


def extract_text_from_binary_image(binary_image) -> str:
    """Executes Tesseract OCR engine on preprocessed binary frame."""
    # Trade-off: Running raw Tesseract on binary thresholds works fast for clean, axis-aligned documents, 
    # but lacks page segmentation handling (PSM). For complex multi-column layouts, PaddleOCR or EasyOCR 
    # would be better suited for production.
    return pytesseract.image_to_string(binary_image)


def run_pipeline():
    original_frame, clean_binary_frame = preprocess_document_image(IMAGE_PATH)
    parsed_text = extract_text_from_binary_image(clean_binary_frame)

    print("--- Extracted Text Output ---")
    print(parsed_text if parsed_text.strip() else "[No text detected in document]")

    # Configure resizable OpenCV preview windows
    cv2.namedWindow("Original Input", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Preprocessed Binary", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Original Input", DISPLAY_WIDTH, DISPLAY_HEIGHT)
    cv2.resizeWindow("Preprocessed Binary", DISPLAY_WIDTH, DISPLAY_HEIGHT)

    # Display preview frames
    cv2.imshow("Original Input", original_frame)
    cv2.imshow("Preprocessed Binary", clean_binary_frame)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_pipeline()