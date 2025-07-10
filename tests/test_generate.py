import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.llm_preprocessor import generate_insights

def test_generate():
    context = """
    [vGPU]: NVIDIA virtual GPU software improves productivity and security.
    [CUDA]: CUDA Toolkit provides dev tools for GPU-accelerated apps.
    [DGX]: DGX platform is optimized for enterprise AI.
    """
    insights = generate_insights(context)
    print("Generated Insights:")
    for i in insights:
        print("-", i)

if __name__ == "__main__":
    test_generate()
