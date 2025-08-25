# import requests
# from llama_index.core import SimpleDirectoryReader
# from llama_index.core.node_parser import SentenceSplitter
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np
# def get_procurement_summary() -> str: 
#     # Load PDFs from the folder
#     documents = SimpleDirectoryReader("./contracts").load_data()

#     # Split into chunks
#     splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
#     nodes = splitter.get_nodes_from_documents(documents)

#     # Sentence Embeddings
#     model = SentenceTransformer('all-MiniLM-L6-v2')
#     texts = [node.text for node in nodes]
#     embeddings = model.encode(texts, show_progress_bar=True)

#     # FAISS Index
#     dimension = embeddings[0].shape[0]
#     index = faiss.IndexFlatL2(dimension)
#     index.add(np.array(embeddings))
#     text_id_map = {i: text for i, text in enumerate(texts)}

# # === Prompt Generator ===
# def generate_summary_prompt(context, question):
#     prompt = f"""
# You are a supply chain legal assistant. Based on the following context from procurement contracts, answer the question briefly and clearly.

# 📄 Context:
# {context}

# ❓ Question:
# {question}

# 🎯 Answer:"""
#     return prompt

# # === LLM Call via TinyLLaMA ===
# def get_llm_response(prompt):
#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={"model": "tinyllama", "prompt": prompt, "stream": False}
#     )
#     return response.json().get("response", "").strip()

# # === Semantic Search ===
# def semantic_search(query, model, index, text_id_map, top_k=3):
#     if not query or query.strip() == "":
#         print("❌ Empty query provided!")
#         return ""

#     query_embedding = model.encode([query])
#     D, I = index.search(np.array(query_embedding), top_k)
#     matched_texts = [text_id_map[i] for i in I[0]]

#     context = "\n\n".join(matched_texts)
#     print(f"\n🔎 Top {top_k} matching chunks for: '{query}'\n")
#     for i, text in enumerate(matched_texts):
#         print(f"📄 Chunk {i+1}:\n{text}\n" + "-"*80)

#     return context

# # === Single Query for Testing ===
# def single_query(question):
#     print(f"📝 Processing question: {question}")
#     try:
#         context = semantic_search(question, model, index, text_id_map)
#         if context:
#             prompt = generate_summary_prompt(context, question)
#             response = get_llm_response(prompt)
#             print(f"\n🤖 Answer:\n{response}")
#         else:
#             print("❌ No relevant context found!")
#     except Exception as e:
#         print(f"❌ Error: {e}")

# # === Interactive Query System ===
# def run_query_system():
#     while True:
#         print("\n" + "="*60)
#         print("📋 Contract Query System")
#         print("="*60)

#         query = input("📝 Enter your question (or 'quit' to exit): ").strip()

#         if query.lower() in ['quit', 'exit', 'q']:
#             print("👋 Goodbye!")
#             break

#         if not query:
#             print("❌ Please enter a valid question!")
#             continue

#         try:
#             context = semantic_search(query, model, index, text_id_map)
#             if not context:
#                 print("❌ No relevant context found!")
#                 continue

#             prompt = generate_summary_prompt(context, query)
#             response = get_llm_response(prompt)

#             # print("\n🤖 Answer:")
#             # print("-" * 40)
#             # print(response)
#             # print("-" * 40)

#         except Exception as e:
#             print(f"❌ Error processing query: {e}")

# # === Optional: Summarize All Contracts for Dashboard Agent ===
# def summarize_procurement_contracts():
#     context = "\n\n".join(text_id_map.values())[:3000]  # Truncate for token safety
#     question = "Summarize the key terms, risks, and decision points in these procurement contracts."
#     prompt = generate_summary_prompt(context, question)
#     return get_llm_response(prompt)

# # === Main ===
# if __name__ == "__main__":
#     print("🧪 Running a sample query...")
#     test_question = "Under what conditions can the agreement be terminated?"
#     single_query(test_question)

    # Uncomment to run interactive query loop
    # run_query_system()

    # Optional: get overall summary for dashboard agent
    # summary = summarize_procurement_contracts()
    # print("\n📊 Procurement Summary:\n", summary) 

# load_contracts.py

import requests
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def get_procurement_summary() -> str:
    # Step 1: Load and chunk documents
    documents = SimpleDirectoryReader("./contracts").load_data()
    splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    nodes = splitter.get_nodes_from_documents(documents)
    texts = [node.text for node in nodes]

    # Step 2: Generate embeddings and FAISS index
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts)
    dimension = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    text_id_map = {i: text for i, text in enumerate(texts)}

    # Step 3: Generate LLM Summary
    context = "\n\n".join(text_id_map.values())[:3000]  # truncate context
    prompt = f"""
You are a supply chain legal assistant. Based on the following context from procurement contracts, summarize key terms, risks, and decision points.

📄 Context:
{context}

🎯 Summary:"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "tinyllama", "prompt": prompt, "stream": False}
    )
    return response.json().get("response", "").strip()

# Optional: Keep this for manual test runs
if __name__ == "__main__":
    summary = get_procurement_summary()
    print("\n📋 Procurement Summary:\n", summary)

