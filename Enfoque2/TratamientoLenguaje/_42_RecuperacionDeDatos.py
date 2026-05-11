# _42_RecuperacionDeDatos.py
# Recuperacion de Datos (Information Retrieval)
# Dado un conjunto de documentos y una consulta, recuperar los documentos
# mas relevantes. Modelo clasico: TF-IDF + similitud coseno.
#
# TF  (Term Frequency):    frecuencia del termino en el documento
# IDF (Inverse Doc Freq):  penaliza terminos muy comunes
# TF-IDF = TF * IDF  ->  alta en terminos frecuentes en doc pero raros en corpus

import math
from collections import defaultdict

print("=" * 55)
print("  RECUPERACION DE DATOS — TF-IDF + COSENO")
print("=" * 55)

# ---- Corpus de documentos ----
documentos = {
    "doc1": "el gato come pescado fresco todos los dias",
    "doc2": "el perro juega en el parque con el nino",
    "doc3": "el gato y el perro son mascotas populares",
    "doc4": "el pescado es un alimento rico en proteinas",
    "doc5": "los ninos juegan con mascotas en el parque",
}

def tokenizar(texto):
    return texto.lower().split()

# ---- Calcular TF ----
def tf(termino, doc_tokens):
    return doc_tokens.count(termino) / len(doc_tokens)

# ---- Calcular IDF ----
def idf(termino, corpus):
    N = len(corpus)
    df = sum(1 for doc in corpus.values() if termino in tokenizar(doc))
    return math.log((N + 1) / (df + 1)) + 1   # suavizado

# ---- Calcular TF-IDF para todos los documentos ----
vocab = set()
for texto in documentos.values():
    vocab.update(tokenizar(texto))

idf_vals = {t: idf(t, documentos) for t in vocab}

def vector_tfidf(doc_texto):
    tokens = tokenizar(doc_texto)
    return {t: tf(t, tokens) * idf_vals[t] for t in vocab}

vectores = {doc_id: vector_tfidf(texto) for doc_id, texto in documentos.items()}

# ---- Similitud Coseno ----
def coseno(v1, v2):
    dot   = sum(v1[t]*v2[t] for t in vocab)
    norm1 = math.sqrt(sum(v**2 for v in v1.values()))
    norm2 = math.sqrt(sum(v**2 for v in v2.values()))
    return dot / (norm1 * norm2 + 1e-10)

# ---- Busqueda ----
def buscar(consulta_str, top_k=3):
    vec_consulta = vector_tfidf(consulta_str)
    scores = {doc_id: coseno(vec_consulta, vectores[doc_id])
              for doc_id in documentos}
    return sorted(scores.items(), key=lambda x: -x[1])[:top_k]

consultas = [
    "gato pescado",
    "nino parque mascotas",
    "proteinas alimento",
]

print("\nCorpus:")
for doc_id, texto in documentos.items():
    print(f"  {doc_id}: '{texto}'")

for consulta in consultas:
    print(f"\nConsulta: '{consulta}'")
    resultados = buscar(consulta)
    for doc_id, score in resultados:
        print(f"  {doc_id} (sim={score:.4f}): '{documentos[doc_id]}'")
