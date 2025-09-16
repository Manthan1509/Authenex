# src/pixel_mismatch.py
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
import io
import os

def analyze_for_edits(image_path: str, resave_quality: int = 90, enhancement_factor: float = 15.0):
    """
    Analyze an image for digital alterations using Error Level Analysis (ELA).

    Args:
        image_path (str): Path to the image file (JPEG/PNG).
        resave_quality (int): JPEG quality for ELA resave step.
        enhancement_factor (float): Brightness factor to enhance differences.

    Returns:
        dict: Analysis results containing average error level, threshold, verdict, reason.
    """
    if not os.path.exists(image_path):
        return {"error": f"File not found: {image_path}"}

    try:
        original_image = Image.open(image_path).convert('RGB')
    except Exception as e:
        return {"error": f"Failed to open image: {str(e)}"}

    # Save into buffer at given quality → resaved version
    buffer = io.BytesIO()
    original_image.save(buffer, 'JPEG', quality=resave_quality)
    buffer.seek(0)
    resaved_image = Image.open(buffer)

    # Difference between original & resaved
    ela_image = ImageChops.difference(original_image, resaved_image)

    # Enhance difference for visibility
    enhancer = ImageEnhance.Brightness(ela_image)
    enhanced_ela_image = enhancer.enhance(enhancement_factor)

    # Numeric measure
    ela_np = np.array(ela_image)
    average_ela = float(ela_np.mean())

    threshold = 7.5  # Tunable
    if average_ela > threshold:
        verdict = "POTENTIALLY EDITED OR FORGED"
        reason = "High error level → different compression history in some areas."
    else:
        verdict = "LIKELY ORIGINAL"
        reason = "Low error level → uniform compression history."

    return {
        "average_error_level": round(average_ela, 2),
        "threshold": threshold,
        "verdict": verdict,
        "reason": reason
    }
