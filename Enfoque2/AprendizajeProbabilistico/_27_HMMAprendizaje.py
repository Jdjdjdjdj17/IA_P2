# _27_HMMAprendizaje.py
# Aprendizaje en Modelos Ocultos de Markov (Baum-Welch)
# El algoritmo Baum-Welch es una aplicacion del EM para HMMs:
#   E-step: calcular probabilidades forward-backward
#   M-step: re-estimar A (transicion) y B (emision) y pi
#
# Aprende los parametros del HMM a partir de secuencias de observaciones.

import random
import math

print("=" * 55)
print("  HMM — APRENDIZAJE (BAUM-WELCH)")
print("=" * 55)

# ---- HMM con 2 estados ocultos y 3 observaciones ----
N = 2   # estados ocultos
M = 3   # observaciones posibles
obs_vals = [0, 1, 2]

# Parametros iniciales (aleatorios pero normalizados)
random.seed(1)
def rand_norm(n):
    v = [random.random() for _ in range(n)]
    t = sum(v); return [x/t for x in v]

pi = rand_norm(N)
A  = [rand_norm(N) for _ in range(N)]
B  = [rand_norm(M) for _ in range(N)]

# ---- Generar datos de entrenamiento con HMM "real" ----
A_real = [[0.7,0.3],[0.4,0.6]]
B_real = [[0.5,0.4,0.1],[0.1,0.3,0.6]]
pi_real= [0.6, 0.4]

def generar_secuencia(T=15):
    s = random.choices(range(N), weights=pi_real)[0]
    obs = []
    for _ in range(T):
        obs.append(random.choices(obs_vals, weights=B_real[s])[0])
        s = random.choices(range(N), weights=A_real[s])[0]
    return obs

secuencias = [generar_secuencia() for _ in range(10)]

def forward(obs, pi, A, B):
    T = len(obs); alpha = [[0]*N for _ in range(T)]
    for i in range(N): alpha[0][i] = pi[i]*B[i][obs[0]]
    for t in range(1,T):
        for j in range(N):
            alpha[t][j] = sum(alpha[t-1][i]*A[i][j] for i in range(N))*B[j][obs[t]]
    return alpha

def backward(obs, A, B):
    T = len(obs); beta = [[0]*N for _ in range(T)]
    for i in range(N): beta[T-1][i] = 1
    for t in range(T-2,-1,-1):
        for i in range(N):
            beta[t][i] = sum(A[i][j]*B[j][obs[t+1]]*beta[t+1][j] for j in range(N))
    return beta

print(f"\nEntrenando con {len(secuencias)} secuencias, {20} iteraciones de Baum-Welch\n")
print(f"{'Iter':<6} {'Log-verosim.'}")
print("-" * 22)

for it in range(20):
    # Acumuladores
    pi_new = [0.0]*N
    A_num  = [[0.0]*N for _ in range(N)]
    A_den  = [0.0]*N
    B_num  = [[0.0]*M for _ in range(N)]
    B_den  = [0.0]*N
    log_v  = 0.0

    for obs in secuencias:
        T     = len(obs)
        alpha = forward(obs, pi, A, B)
        beta  = backward(obs, A, B)
        p_obs = sum(alpha[T-1])
        if p_obs < 1e-300: continue
        log_v += math.log(p_obs + 1e-300)

        # gamma[t][i] = P(Xt=i | obs)
        gamma = [[alpha[t][i]*beta[t][i]/p_obs for i in range(N)] for t in range(T)]
        # xi[t][i][j] = P(Xt=i, Xt+1=j | obs)
        for i in range(N): pi_new[i] += gamma[0][i]
        for t in range(T-1):
            for i in range(N):
                for j in range(N):
                    xi = alpha[t][i]*A[i][j]*B[j][obs[t+1]]*beta[t+1][j]/p_obs
                    A_num[i][j] += xi
                    A_den[i]    += xi
        for t in range(T):
            for i in range(N):
                B_num[i][obs[t]] += gamma[t][i]
                B_den[i]         += gamma[t][i]

    # Actualizar parametros
    t_pi = sum(pi_new); pi = [x/t_pi for x in pi_new]
    for i in range(N):
        A[i] = [A_num[i][j]/(A_den[i]+1e-10) for j in range(N)]
        B[i] = [B_num[i][m]/(B_den[i]+1e-10) for m in range(M)]

    if it < 5 or it % 5 == 4:
        print(f"{it+1:<6} {log_v:.4f}")

print(f"\nParametros aprendidos vs reales:")
print(f"  pi aprendido: {[round(x,3) for x in pi]}  real: {pi_real}")
print(f"  A[0] aprendido: {[round(x,3) for x in A[0]]}  real: {A_real[0]}")
print(f"  B[0] aprendido: {[round(x,3) for x in B[0]]}  real: {B_real[0]}")
