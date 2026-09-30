# Optical Character Recognition (OCR) Pipeline

Project of my AI Internship at DecodeLabs.

## What I Built

A document text-extraction pipeline that takes an image, cleans it up with adaptive thresholding, and pulls out the readable text using Tesseract OCR — with preview windows so you can see exactly what the OCR engine is working from.

## Tech Stack

- Python
- OpenCV (image preprocessing and preview windows)
- pytesseract (Tesseract OCR wrapper)

## How It Works

1. **Load:** The input image is read from disk and converted to grayscale
2. **Threshold:** Gaussian adaptive thresholding is applied instead of a single global threshold, since real-world document scans often have uneven lighting and shadows across the page. A local window size of 11 pixels handles these gradients well, with a small bias constant (`C=2`) to keep low-contrast character edges separated from background noise
3. **Extract:** The cleaned binary image is passed to Tesseract, which returns the recognized text
4. **Preview:** Both the original and preprocessed images are displayed in resizable OpenCV windows so you can visually compare them

## Project Structure

```text
DecodeLabs_OCR/
├── optical_character_recognition.py   # Main script
├── sample_image.jpg                   # Sample document image
└── README.md                          # Project documentation
```

## Getting Started

### Prerequisites

This project needs the Tesseract OCR engine installed separately from the Python packages, since pytesseract is just a wrapper around it.

1. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) for Windows
2. Update the `tesseract_cmd` path in the script if your install location differs from the default
3. Install the Python dependencies:

```bash
pip install opencv-python pytesseract
```

### Running It

Place your document image in the project folder as `sample_image.jpg`, then run:

```bash
python optical_character_recognition.py
```

The extracted text prints to the console, and two windows pop up showing the original and preprocessed images. Press any key to close them.

## What I Learned

Adaptive thresholding makes a real difference over a simple global threshold once you're dealing with scanned or photographed documents rather than clean digital images — uneven lighting on a physical page would otherwise wipe out whole sections of text. I also learned that raw Tesseract works well for clean, single-column documents, but a more complex layout (multi-column pages, tables) would need something like PaddleOCR or EasyOCR that handles page segmentation properly.

## Author

Wireko Fosu Eric — AI Intern, DecodeLabs
