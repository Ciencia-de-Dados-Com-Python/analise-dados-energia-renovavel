import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

print("Iniciando a análise de dados de energia...")

# --- 1. Geração de Dados Simulados ---
# Vamos simular a capacidade instalada (em GW - Gigawatts) ao longo dos anos
# e o Custo Nivelado de Energia (LCOE - em $/MWh)

anos = np.arange(2010, 2031, 1) # Anos de 2010 a 2030

# Capacidade Instalada (GW)
# Simulação: Fósseis crescem lentamente e depois estabilizam/declinam, renováveis crescem exponencialmente
capacidade_fosseis = 200 + 5 * (anos - 2010) - 0.5 * (anos - 2010)**2
capacidade_fosseis[capacidade_fosseis < 150] = 150 # Limite mínimo para não ir negativo
capacidade_fosseis = [max(150, val) for val in capacidade_fosseis] # Garantir um mínimo

capacidade_renovaveis = 50 + 2 * (anos - 2010)**2.2 # Crescimento mais acentuado

# LCOE ($/MWh)
# Simulação: Fósseis relativamente estáveis com flutuações, renováveis em declínio acentuado
lcoe_fosseis = 80 + 10 * np.sin((anos - 2010) / 3) + np.random.normal(0, 3, len(anos))
lcoe_renovaveis = 150 - 6 * (anos - 2010) + np.random.normal(0, 5, len(anos))
lcoe_renovaveis[lcoe_renovaveis < 30] = 30 # Limite mínimo para LCOE renovável

# Criando um DataFrame pandas
df_energia = pd.DataFrame({
    'Ano': anos,
    'Capacidade_Fosseis_GW': capacidade_fosseis,
    'Capacidade_Renovaveis_GW': capacidade_renovaveis,
    'LCOE_Fosseis_USD_MWh': lcoe_fosseis,
    'LCOE_Renovaveis_USD_MWh': lcoe_renovaveis
})

print("\nDados simulados gerados:")
print(df_energia.head())
print(df_energia.tail())

# --- 2. Visualização dos Dados ---

# Estilo dos gráficos
sns.set_style("whitegrid")
plt.figure(figsize=(14, 10))

# Gráfico 1: Capacidade Instalada ao longo do tempo
plt.subplot(2, 1, 1) # 2 linhas, 1 coluna, primeiro gráfico
plt.plot(df_energia['Ano'], df_energia['Capacidade_Fosseis_GW'], label='Capacidade Fósseis (GW)', marker='o', linestyle='--', color='red')
plt.plot(df_energia['Ano'], df_energia['Capacidade_Renovaveis_GW'], label='Capacidade Renováveis (GW)', marker='o', linestyle='-', color='green')
plt.title('Evolução da Capacidade de Geração de Energia (2010-2030)', fontsize=16)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Capacidade Instalada (GW)', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, linestyle=':', alpha=0.7)
plt.xticks(anos[::2]) # Mostra anos alternados para melhor legibilidade
plt.tight_layout()

# Gráfico 2: Custo Nivelado de Energia (LCOE) ao longo do tempo
plt.subplot(2, 1, 2) # 2 linhas, 1 coluna, segundo gráfico
plt.plot(df_energia['Ano'], df_energia['LCOE_Fosseis_USD_MWh'], label='LCOE Fósseis ($/MWh)', marker='s', linestyle='--', color='darkorange')
plt.plot(df_energia['Ano'], df_energia['LCOE_Renovaveis_USD_MWh'], label='LCOE Renováveis ($/MWh)', marker='s', linestyle='-', color='darkgreen')
plt.title('Evolução do Custo Nivelado de Energia (LCOE) (2010-2030)', fontsize=16)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('LCOE ($/MWh)', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, linestyle=':', alpha=0.7)
plt.xticks(anos[::2]) # Mostra anos alternados
plt.tight_layout()

plt.show()

# --- 3. Análise e Insights Básicos ---
print("\n--- Análise de Insights ---")

# Encontrar o ano em que a capacidade renovável ultrapassa a fóssil (se ocorrer)
cruzamento_capacidade = df_energia[df_energia['Capacidade_Renovaveis_GW'] > df_energia['Capacidade_Fosseis_GW']]
if not cruzamento_capacidade.empty:
    ano_cruzamento_cap = cruzamento_capacidade['Ano'].iloc[0]
    print(f"A capacidade de energia renovável ultrapassa a fóssil por volta de: {ano_cruzamento_cap}")
else:
    print("A capacidade de energia renovável não ultrapassa a fóssil neste período simulado.")

# Encontrar o ano em que o LCOE renovável fica mais baixo que o fóssil (se ocorrer)
cruzamento_lcoe = df_energia[df_energia['LCOE_Renovaveis_USD_MWh'] < df_energia['LCOE_Fosseis_USD_MWh']]
if not cruzamento_lcoe.empty:
    ano_cruzamento_lcoe = cruzamento_lcoe['Ano'].iloc[0]
    print(f"O LCOE de energia renovável se torna mais baixo que o fóssil por volta de: {ano_cruzamento_lcoe}")
else:
    print("O LCOE de energia renovável não se torna mais baixo que o fóssil neste período simulado.")

# Variação percentual do LCOE renovável no período
lcoe_renovaveis_inicial = df_energia['LCOE_Renovaveis_USD_MWh'].iloc[0]
lcoe_renovaveis_final = df_energia['LCOE_Renovaveis_USD_MWh'].iloc[-1]
variacao_lcoe_renovaveis = ((lcoe_renovaveis_final - lcoe_renovaveis_inicial) / lcoe_renovaveis_inicial) * 100
print(f"Variação do LCOE de renováveis (2010-2030): {variacao_lcoe_renovaveis:.2f}%")

print("\nAnálise concluída. Verifique os gráficos para uma melhor compreensão!")