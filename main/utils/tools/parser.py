import io
import requests
from PIL import Image
import pytesseract
import fitz
import filetype
import base64

def parse_url_to_text(url: str) -> str:
    """
    Downloads a file from the provided URL, detects its type, and extracts readable text.

    This function works entirely in memory (no local file storage) to reduce
    security risks. It supports:
      - Images (JPEG, PNG, etc.) via OCR using Tesseract.
      - PDFs via direct text extraction with PyMuPDF (fitz).

    Unsupported or unknown file types will return a descriptive placeholder message.

    Args:
        url (str): A direct URL to the file (image or PDF). The file must be
                   publicly accessible or the request must include any
                   required authentication in the URL.

    Returns:
        str: The extracted text content. If the file type is unsupported or
             unrecognized, returns a descriptive error message string.

    Raises:
        requests.exceptions.RequestException:
            If the HTTP request fails (e.g., network error, invalid URL).
        ValueError:
            If the file cannot be processed due to corruption or unreadable format.
        pytesseract.TesseractError:
            If OCR processing fails for image files.
        fitz.FileDataError:
            If PDF parsing fails or the file is invalid.

    File Type Handling:
        - image/*  → Processed via Pillow + Tesseract OCR.
        - application/pdf → Processed via PyMuPDF (fitz) page-by-page text extraction.
        - other types → Returns "[Unsupported file type: <mime>]".
        - unrecognized type → Returns "[Unknown file type]".

    Example:
        >>> parse_url_to_text("https://example.com/document.pdf")
        'This is the extracted text from the PDF file...'

        >>> parse_url_to_text("https://example.com/image.png")
        'Text read from the image via OCR...'

        >>> parse_url_to_text("https://example.com/file.zip")
        '[Unsupported file type: application/zip]'
    """

    response = requests.get(url)
    response.raise_for_status()
    file_bytes = io.BytesIO(response.content)

    kind = filetype.guess(file_bytes.getvalue())
    text = ""

    if kind is None:
        return "[Unknown file type]"

    mime = kind.mime

    if mime.startswith("image/"):
        # Image OCR
        image = Image.open(file_bytes)
        text = pytesseract.image_to_string(image)

    elif mime == "application/pdf":
        # PDF text extraction
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        for page in pdf:
            text += page.get_text()

    else:
        text = f"[Unsupported file type: {mime}]"

    return text.strip()

def imageparse(base64string: str) -> str:
    """
    Converts a Base64-encoded image string into text using OCR (Tesseract).

    This function decodes the Base64 string into image bytes, reconstructs
    the image in memory with Pillow, and then extracts any readable text
    using Tesseract OCR.

    Args:
        base64string (str): The Base64-encoded representation of an image
                            (e.g., PNG or JPEG).

    Returns:
        str: The extracted text content from the image. If no readable text
             is found, an empty string is returned.

    Raises:
        ValueError:
            If the Base64 string is invalid or cannot be decoded into an image.
        pytesseract.TesseractError:
            If OCR processing fails for the provided image.

    Example:
        >>> encoded = image_to_base64("example.png")
        >>> imageparse(encoded)
        'Extracted text from the image...'
    """
    image_data = base64.b64decode(base64string)
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    return text.strip()

def image_to_base64(image: Image.Image) -> str:
    """
    Converts a PIL Image object into a Base64-encoded string.

    This function works entirely in memory without writing to disk.

    Args:
        image (PIL.Image.Image): A Pillow image object.

    Returns:
        str: Base64-encoded string representation of the image.

    Example:
        >>> img = Image.open("example.png")
        >>> encoded = image_to_base64(img)
        >>> print(encoded[:50])  # prints first 50 characters
    """
    buffered = io.BytesIO()
    image.save(buffered, format=image.format or "PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")