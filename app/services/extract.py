from io import BytesIO

def extract_text(filename: str, data: bytes) -> str:
    name = (filename or "").lower()

    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(BytesIO(data))
            pages_text = []

            for p in reader.pages[:10]: # MVP: limita 10 paginas
                pages_text.append(p.extract_text() or "")
            return "\n".join(pages_text).strip()
        except Exception:
            # Se falhar, devolve vazio e o resumo vira "nao consegui extrair"
            return ""
        
    # fallback para txt
    if name.endswith(".txt"):
        try:
            return data.decode("utf-8", errors="ignore").strip()
        except Exception:
            return ""
        
    # outros tipos: por enquanto não extrai
    return ""