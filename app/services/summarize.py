def summarize_text(text: str) -> str: 
    text = (text or "").strip()
    if not text:
        return "Não consegui extrair texto do arquivo (talvez seja imagem ou PDF escaneado)"
    
    # MVP: "resumo" simples (primeiras linhas)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    snippet = "\n".join(lines[:12])

    return (
        "Resumo (MVP):\n"
        f"{snippet}\n\n"
        "Se quiser, eu ligo isso num LLM pra gerar um resumo mais inteligente."
    )