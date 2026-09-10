#!/usr/bin/env python3
"""
Test OpenModelProvider configuration, auto-detection, and fallback handling
"""
import asyncio
from app.ai.open_model_provider import OpenModelProvider
from app.ai.service import AIService
from app.config import settings

def test_provider_detection():
    print("Testing OpenModelProvider auto-detection...")

    # Test Groq configuration
    groq_prov = OpenModelProvider(provider_type="groq", api_key="gsk_test123")
    assert groq_prov.base_url == "https://api.groq.com/openai/v1"
    assert "llama" in groq_prov.model
    print("✓ Groq configuration verified")

    # Test OpenRouter configuration
    router_prov = OpenModelProvider(provider_type="openrouter", api_key="sk-or-test123")
    assert router_prov.base_url == "https://openrouter.ai/api/v1"
    assert "llama" in router_prov.model or "instruct" in router_prov.model
    print("✓ OpenRouter configuration verified")

    # Test Together AI configuration
    together_prov = OpenModelProvider(provider_type="together", api_key="tog_test123")
    assert together_prov.base_url == "https://api.together.xyz/v1"
    assert "llama" in together_prov.model.lower()
    print("✓ Together AI configuration verified")

    # Test Ollama / Local custom endpoint
    ollama_prov = OpenModelProvider(provider_type="ollama", base_url="http://localhost:11434/v1", model="llama3.2")
    assert ollama_prov.base_url == "http://localhost:11434/v1"
    assert ollama_prov.model == "llama3.2"
    print("✓ Local Ollama configuration verified")

def test_json_extraction():
    print("\nTesting open model JSON extraction parsing...")
    prov = OpenModelProvider(provider_type="none")

    # 1. Direct JSON
    sample_json = '{"title": "Open Models in AI", "summary": "How open weights change AI.", "category": "tech"}'
    res = prov._extract_json(sample_json)
    assert res.get("title") == "Open Models in AI"
    print("✓ Direct JSON parse verified")

    # 2. Markdown fenced code block
    markdown_sample = """Here is the extracted analysis:
```json
{
  "title": "Llama 3.3 Capabilities",
  "summary": "High efficiency 70B open model.",
  "category": "ai"
}
```
Hope this helps!"""
    res = prov._extract_json(markdown_sample)
    assert res.get("title") == "Llama 3.3 Capabilities"
    print("✓ Markdown code fence extraction verified")

    # 3. Unfenced JSON
    unfenced_sample = """Analysis result:
    {"title": "DeepSeek Insights", "summary": "MoE architecture reasoning."}
    Done."""
    res = prov._extract_json(unfenced_sample)
    assert res.get("title") == "DeepSeek Insights"
    print("✓ Unfenced JSON extraction verified")

def test_ai_service_integration():
    print("\nTesting AIService integration...")
    service = AIService()
    assert service.llm_provider is not None
    print(f"✓ AIService initialized with provider: {service.llm_provider.__class__.__name__}")

if __name__ == "__main__":
    test_provider_detection()
    test_json_extraction()
    test_ai_service_integration()
    print("\n✅ All Open Model tests passed!")
