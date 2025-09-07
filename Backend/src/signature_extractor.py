import os
import cv2
from ultralytics import YOLO


def crop_signatures(image_path, model_path, output_folder=r".\Authenex\cropped_signatures"):
    os.makedirs(output_folder, exist_ok=True)
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not read the image at: {image_path}")

    model = YOLO(model_path)
    results = model(image)
    cropped_paths = []

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy()

        for idx, (bbox, cls_id) in enumerate(zip(boxes, class_ids)):
            if int(cls_id) == 0:  # signature class
                x1, y1, x2, y2 = map(int, bbox)
                cropped = image[y1:y2, x1:x2]
                cropped_name = f"{os.path.splitext(os.path.basename(image_path))[0]}_signature_{idx}.png"
                cropped_path = os.path.join(output_folder, cropped_name)
                cv2.imwrite(cropped_path, cropped)
                cropped_paths.append(cropped_path)

    return cropped_paths if cropped_paths else ["null"]
