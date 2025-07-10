import ollama
import time

def generate_insights(context):
    start_time = time.time()
    prompt = f"""
    Given the following context, generate three actionable insights about the company or product:
    {context}
    """
    try:
        response = ollama.generate(
            model='mistral:latest',  # Updated to Mistral
            prompt=prompt[:2000],  # Limit input size
            options={'num_ctx': 2048, 'temperature': 0.7}
        )
        latency = (time.time() - start_time) * 1000
        print(f"Inference latency: {latency:.2f} ms")
        return response['response'].split('\n')[:3]
    except Exception as e:
        print(f"LLM error: {e}")
        return []