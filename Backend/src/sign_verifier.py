import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

class L1DistanceLayer(layers.Layer):
    
    def __init__(self, **kwargs):
        super(L1DistanceLayer, self).__init__(**kwargs)
    
    def call(self, inputs):
        emb_a, emb_b = inputs
        diff = tf.abs(emb_a - emb_b)
        distance = tf.reduce_sum(diff, axis=1, keepdims=True)
        return distance
    
    def get_config(self):
        return super(L1DistanceLayer, self).get_config()

class SignatureVerifier:
    def __init__(self, model_path=None, model=None):
        if model is not None:
            self.model = model
        elif model_path is not None:
            self.model = self.load_model_safe(model_path)
        else:
            raise ValueError("Either model_path or model must be provided")
    
    @staticmethod
    def load_model_safe(model_path):
        try:
            custom_objects = {'L1DistanceLayer': L1DistanceLayer}
            
            model = tf.keras.models.load_model(
                model_path,
                custom_objects=custom_objects,
                compile=False
            )
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def preprocess_signature(self, img_path, target_size=(220, 155)):
        try:
            img = cv2.imread(img_path)
            if img is None:
                raise FileNotFoundError(f"Image not found: {img_path}")
            
            img = cv2.resize(img, target_size)
            img = img.astype("float32") / 255.0
            return img
        except Exception as e:
            print(f"Error preprocessing image {img_path}: {e}")
            raise
    
    def verify_signatures(self, sig1_path, sig2_path, threshold=0.5):
        try:
            sig1 = self.preprocess_signature(sig1_path)
            sig2 = self.preprocess_signature(sig2_path)
            
            sig1 = np.expand_dims(sig1, axis=0)
            sig2 = np.expand_dims(sig2, axis=0)
            
            distance = self.model.predict([sig1, sig2], verbose=0)[0][0]
            
            prediction = distance < threshold

            confidence = abs(distance - threshold) / threshold
            confidence = min(1.0, confidence)
            
            return {
                'distance': round(float(distance), 2),
                'prediction': bool(prediction),
                'confidence': round(float(confidence), 2),
                'threshold': threshold
            }
            
        except Exception as e:
            print(f"Error during verification: {e}")
            return None
    
    def batch_verify(self, signature_pairs, threshold=0.5):
        results = []
        for sig1_path, sig2_path in signature_pairs:
            result = self.verify_signatures(sig1_path, sig2_path, threshold)
            if result:
                result['pair'] = (sig1_path, sig2_path)
                results.append(result)
        return results