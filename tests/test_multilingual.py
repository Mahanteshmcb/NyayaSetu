import os
from backend.services import multilingual

def test_openrouter_env_variables_are_supported(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    monkeypatch.setenv("OPENROUTER_MODEL", "provider/model-test")
    monkeypatch.setenv("OPENAI_API_KEY", "")
    key, base, model = multilingual._provider_config()
    assert key == "test-key"
    assert base == "https://openrouter.ai/api/v1"
    assert model == "provider/model-test"

def test_kannada_prompt_requires_kannada_script(monkeypatch):
    captured = {}
    def fake(messages, temperature=0.2):
        captured["messages"] = messages
        return "ಕನ್ನಡ ಉತ್ತರ"
    monkeypatch.setattr(multilingual, "ask_model", fake)
    result = multilingual.analyze_document_text("sample legal text", "test.pdf", "kn")
    assert result["model_used"] is True
    assert "ಕನ್ನಡ" in captured["messages"][0]["content"]
    assert "Do not answer in English" in captured["messages"][0]["content"]

def test_model_unavailable_does_not_return_english_analysis(monkeypatch):
    monkeypatch.setattr(multilingual, "ask_model", lambda *a, **k: None)
    result = multilingual.analyze_document_text("sample legal text", "test.pdf", "kn")
    assert result["model_used"] is False
    assert result["analysis"] == ""
    assert "provider" in result["provider_error"].lower()
