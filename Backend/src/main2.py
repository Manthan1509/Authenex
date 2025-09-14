import cv2
import numpy as np
import os
from PIL import Image, ImageChops, ImageEnhance
import io

def create_sample_certificate():
    """Generates a sample certificate with a pasted element to simulate editing."""
    base_image = Image.new('RGB', (800, 600), 'white')
    base_image.save("base_temp.jpg", "JPEG", quality=95)
    base_image = Image.open("base_temp.jpg")

    pasted_element = Image.new('RGB', (250, 100), (253, 253, 253)) 
    pasted_element.save("paste_temp.jpg", "JPEG", quality=75)
    pasted_element = Image.open("paste_temp.jpg")

    base_image.paste(pasted_element, (275, 400))
    final_certificate = "certificate_to_analyze.jpg"
    base_image.save(final_certificate, "JPEG", quality=90)

    os.remove("base_temp.jpg")
    os.remove("paste_temp.jpg")

    print(f"Generated a sample edited certificate: '{final_certificate}'")
    return final_certificate

def analyze_for_edits(image_path, resave_quality=90, enhancement_factor=15.0):
    """
    Analyzes a single image for digital alterations using Error Level Analysis (ELA)
    and provides an automated verdict.

    Args:
        image_path (str): The path to the image file to analyze.
        resave_quality (int): The JPEG quality level to use for the ELA comparison.
        enhancement_factor (float): How much to brighten the ELA result to make it visible.
    """
    try:
        original_image = Image.open(image_path).convert('RGB')
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return

    buffer = io.BytesIO()
    original_image.save(buffer, 'JPEG', quality=resave_quality)
    buffer.seek(0)
    resaved_image = Image.open(buffer)

    ela_image = ImageChops.difference(original_image, resaved_image)

    enhancer = ImageEnhance.Brightness(ela_image)
    enhanced_ela_image = enhancer.enhance(enhancement_factor)

    ela_np = np.array(ela_image)
    average_ela = ela_np.mean()

    threshold = 7.5
    
    print("\n--- ELA Analysis Results ---")
    print(f"Average Error Level: {average_ela:.2f}")
    print(f"Detection Threshold: {threshold}")

    if average_ela > threshold:
        verdict = "POTENTIALLY EDITED OR FORGED"
        print(f"VERDICT: {verdict}")
        print("Reason: The average error level is high, suggesting that some areas of the image have a different compression history than the rest.")
    else:
        verdict = "LIKELY ORIGINAL"
        print(f"VERDICT: {verdict}")
        print("Reason: The average error level is low, indicating the image has a uniform compression history.")


    original_cv = np.array(original_image)
    original_cv = cv2.cvtColor(original_cv, cv2.COLOR_RGB2BGR)
    enhanced_ela_cv = np.array(enhanced_ela_image)
    enhanced_ela_cv = cv2.cvtColor(enhanced_ela_cv, cv2.COLOR_RGB2BGR)

    cv2.imshow("Original Certificate", original_cv)
    cv2.imshow(f"ELA Result (Verdict: {verdict})", enhanced_ela_cv)

    print("\nPress any key to close the windows.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    """Main function to run the document analysis process."""
    certificate_path = "image copy.png"

    if not os.path.exists(certificate_path):
        print("Sample certificate not found. Creating one now...")
        create_sample_certificate()
        print("-" * 30)

    analyze_for_edits(certificate_path)

if __name__ == "__main__":
    main()

