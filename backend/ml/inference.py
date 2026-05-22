import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "ml", "models")

try:
    sentiment_pipeline = joblib.load(os.path.join(MODEL_DIR, "sentiment_pipeline.pkl"))
    category_pipeline = joblib.load(os.path.join(MODEL_DIR, "category_pipeline.pkl"))
    print("✅ ML Models loaded successfully from:", MODEL_DIR)
except Exception as e:
    print(f"⚠️ Model loading failed: {e}")
    sentiment_pipeline = None
    category_pipeline = None


def predict_review(text):
    if sentiment_pipeline is None or category_pipeline is None:
        return {"sentiment": "Neutral", "category": "General"}

    try:
        sentiment_pred = sentiment_pipeline.predict([text])[0]
        category_pred = category_pipeline.predict([text])[0]
        
        # Parse sentiment label safely (extracting from HF dict if present)
        if isinstance(sentiment_pred, dict):
            sentiment_lbl = sentiment_pred.get("label", "NEUTRAL")
        elif isinstance(sentiment_pred, list) and len(sentiment_pred) > 0 and isinstance(sentiment_pred[0], dict):
            sentiment_lbl = sentiment_pred[0].get("label", "NEUTRAL")
        else:
            sentiment_lbl = str(sentiment_pred)
            
        sentiment_val = sentiment_lbl.upper().replace("LABEL_", "").title()
        category_val = str(category_pred).replace("_", " ").title()
        
        return {
            "sentiment": sentiment_val,
            "category": category_val
        }
    except:
        return {"sentiment": "Neutral", "category": "General"}


def retrain_model(extra_texts, extra_labels):
    global category_pipeline
    if category_pipeline is None:
        return False
    
    try:
        vectorizer = category_pipeline.named_steps['vectorizer']
        classifier = category_pipeline.named_steps['classifier']
        
        # Representative seed reviews to maintain stability across standard categories
        seeds = [
            ("I cannot login to my account. The password reset is not working.", "account_access"),
            ("Access denied, cannot log in.", "account_access"),
            ("My account is locked.", "account_access"),
            ("I was charged twice for this purchase.", "billing"),
            ("There is a billing error on my invoice.", "billing"),
            ("Why did you charge my card?", "billing"),
            ("The app keeps crashing when I open the dashboard.", "bug_report"),
            ("There is a bug in the submission form.", "bug_report"),
            ("The screen goes blank.", "bug_report"),
            ("I want a refund for my order.", "refund_request"),
            ("Please return my money, I am not satisfied.", "refund_request"),
            ("Refund my transaction.", "refund_request"),
            ("My order has not arrived yet.", "shipping_delivery"),
            ("Where is my delivery? It is late.", "shipping_delivery"),
            ("Tracking information is not updating.", "shipping_delivery")
        ]
        
        VALID_CATEGORIES = {'account_access', 'billing', 'bug_report', 'refund_request', 'shipping_delivery'}
        
        X_texts = []
        y_labels = []
        
        # Add stable anchor seed data
        for text, label in seeds:
            X_texts.append(text)
            y_labels.append(label)
            
        # Add feedback data
        for text, label in zip(extra_texts, extra_labels):
            if label in VALID_CATEGORIES:
                X_texts.append(text)
                y_labels.append(label)
                
        # Transform and fit model on combined dataset
        X_features = vectorizer.transform(X_texts)
        classifier.fit(X_features, y_labels)
        
        # Save back to disk
        joblib.dump(category_pipeline, os.path.join(MODEL_DIR, "category_pipeline.pkl"))
        print("✅ Category model successfully retrained!")
        return True
    except Exception as e:
        print(f"❌ Error during model retraining: {e}")
        return False