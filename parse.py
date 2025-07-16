import os

USE_OLLAMA = os.getenv("USE_OLLAMA", "false").lower() == "true"

if USE_OLLAMA:
    from langchain_ollama import OllamaLLM
    from langchain_core.prompts import ChatPromptTemplate

    model = OllamaLLM(model="llama2")
    prompt = ChatPromptTemplate.from_template(
        "Extract info from: {dom_content}\nQuery: {parse_description}"
    )

    def parse_with_ollama(dom_chunks, parse_description):
        chain = prompt | model
        parsed = [chain.invoke({"dom_content": c, "parse_description": parse_description}) for c in dom_chunks]
        return "\n".join(parsed)

else:
    print("⚠️ Using fallback keyword-based parser (Ollama disabled)")

    def parse_with_ollama(dom_chunks, parse_description):
        keyword = parse_description.strip().lower()
        lines = []
        for chunk in dom_chunks:
            lines.extend([line for line in chunk.splitlines() if keyword in line.lower()])
        return "\n".join(lines)
