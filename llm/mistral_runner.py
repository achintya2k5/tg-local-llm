from llama_cpp import Llama
def llm_gen(chunks, query):
    llm=Llama(
    model_path="models\\mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=8
    )
    context="\n\n".join(chunks)
    prompt = f"[INST] Using the following context, answer the question.\n\nContext:\n{context}\n\nQuestion: {query} [/INST]"
    response = llm(prompt, max_tokens=300, stream=False)

    # stream=False should return a completion dict. This keeps runtime safe.
    if isinstance(response, dict):
        print(response["choices"][0]["text"].strip())
        return

    generated_text = ""
    for part in response:
        generated_text += part.get("choices", [{}])[0].get("text", "")
    print(generated_text.strip())