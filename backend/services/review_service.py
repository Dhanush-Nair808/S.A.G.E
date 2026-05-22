from ml.inference import predict_review
from rag.retriever import retrieve_context
from services.llm_service import generate_response

def process_review(review_text):
    try:
        # Get category & sentiment
        result = predict_review(review_text)

        # Get relevant policy context
        context = retrieve_context(review_text)

        # Generate proper response using LLM
        ai_reply = generate_response(
            review=review_text,
            context=context,
            category=result["category"],
            sentiment=result["sentiment"]
        )

        return {
            "category": result["category"],
            "sentiment": result["sentiment"],
            "reply": ai_reply
        }
    except Exception as e:
        print(f"Error in process_review: {e}")
        return {
            "category": "General",
            "sentiment": "neutral",
            "reply": "Thank you for your review. Our team will look into your concern and get back to you shortly."
        }