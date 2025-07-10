import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.llm_preprocessor import generate_insights

def test_preprocessor():
    context = """
    [NVIDIA docs]: NVIDIA has released a new GPU with 30% more power efficiency.
    [NVIDIA news]: Customer reviews highlight better AI inference speeds.
    """
    insights = generate_insights(context)
    for idx, insight in enumerate(insights, 1):
        print(f"Insight {idx}: {insight}")

if __name__ == "__main__":
    test_preprocessor()
