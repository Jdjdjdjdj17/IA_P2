# _39_ModeloProbabilisticoLenguaje.py
# Modelo Probabilistico del Lenguaje (N-gramas)
# Asigna probabilidades a secuencias de palabras usando un corpus de texto.
# Modelo de N-gramas: P(palabra_n | palabra_1,...,palabra_{n-1})
#   - Unigrama: P(w)
#   - Bigrama:  P(w_n | w_{n-1})
#   - Trigrama: P(w_n | w_{n-2}, w_{n-1})
# Usa la hipotesis de Markov: solo depende de las N-1 palabras anteriores.

from collections import defaultdict
import math

print("=" * 55)
print("  MODELO PROBABILISTICO DEL LENGUAJE (N-GRAMAS)")
print("=" * 55)

# ---- Corpus de ejemplo ----
corpus = [
    "el gato come pescado",
    "el perro come carne",
    "el gato duerme mucho",
    "el perro corre rapido",
    "el gato corre rapido",
    "la gata come pescado",
    "la gata duerme mucho",
]

def tokenizar(corpus):
    tokens = []
    for oracion in corpus:
        tokens += ["<s>"] + oracion.split() + ["</s>"]
    return tokens

tokens = tokenizar(corpus)
vocab  = set(tokens)

# ---- Contar unigramas y bigramas ----
uni = defaultdict(int)
bi  = defaultdict(int)
for t in tokens:
    uni[t] += 1
for i in range(len(tokens)-1):
    bi[(tokens[i], tokens[i+1])] += 1

N_tokens = len(tokens)
V = len(vocab)

# ---- Probabilidades con suavizado de Laplace ----
def p_unigrama(w):
    return (uni[w] + 1) / (N_tokens + V)

def p_bigrama(w2, w1):
    return (bi[(w1, w2)] + 1) / (uni[w1] + V)

print(f"\nCorpus: {len(corpus)} oraciones, {N_tokens} tokens, {V} palabras en vocabulario")

print("\nProbabilidades de unigramas (top 8):")
top_uni = sorted(uni.items(), key=lambda x: -x[1])[:8]
for w, c in top_uni:
    print(f"  P({w:12}) = {p_unigrama(w):.4f}  (conteo={c})")

print("\nProbabilidades de bigramas (P(w2 | w1)):")
bigramas_consulta = [("gato","el"), ("perro","el"), ("come","gato"), ("duerme","gato")]
for w2, w1 in bigramas_consulta:
    print(f"  P({w2:10} | {w1:10}) = {p_bigrama(w2,w1):.4f}")

# ---- Generar texto con el modelo de bigrama ----
import random
def generar_oracion(max_len=8):
    w = "<s>"
    oracion = []
    for _ in range(max_len):
        candidatos = [v for v in vocab if v not in ["<s>"]]
        probs = [p_bigrama(v, w) for v in candidatos]
        w = random.choices(candidatos, weights=probs)[0]
        if w == "</s>": break
        oracion.append(w)
    return " ".join(oracion)

print("\nOraciones generadas con el modelo de bigrama:")
random.seed(3)
for _ in range(4):
    print(f"  '{generar_oracion()}'")

# ---- Perplejidad ----
def perplejidad(oracion_str, p_bigrama_fn):
    tokens_o = ["<s>"] + oracion_str.split() + ["</s>"]
    log_prob  = sum(math.log(p_bigrama_fn(tokens_o[i+1], tokens_o[i]) + 1e-10)
                    for i in range(len(tokens_o)-1))
    return math.exp(-log_prob / (len(tokens_o)-1))

print("\nPerplejidad (menor = mejor modelo):")
for oracion in ["el gato come pescado", "el robot vuela alto"]:
    pp = perplejidad(oracion, p_bigrama)
    print(f"  '{oracion}': {pp:.2f}")
