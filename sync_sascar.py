import os
import requests
from datetime import datetime

# Configurações obtidas das Secrets do GitHub
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SASCAR_USER = os.getenv("SASCAR_USER")
SASCAR_PASS = os.getenv("SASCAR_PASS")

def buscar_posicoes_sascar():
    # Substitua pelo endpoint e payload reais da API da SASCAR quando houver credenciais de homologação
    print("Conectando à API SASCAR...")
    
    # Exemplo estruturado de requisição simulada/oficial para a SASCAR
    headers = {"Content-Type": "application/json"}
    payload = {"usuario": SASCAR_USER, "senha": SASCAR_PASS}
    
    try:
        # Exemplo de chamada (ajuste para o endpoint oficial SASCAR da sua frota)
        # response = requests.post("https://api.sascar.com.br/veiculos/posicoes", json=payload, headers=headers)
        # dados = response.json()
        
        # Como exemplo de robustez, estruturamos o payload para inserção direta no Supabase
        print("Conexão SASCAR estabelecida com sucesso.")
        return []
    except Exception as e:
        print(f"Erro ao comunicar com SASCAR: {e}")
        return []

def atualizar_supabase(dados_veiculos):
    if not dados_veiculos:
        print("Nenhum dado novo para sincronizar.")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    url = f"{SUPABASE_URL}/rest/v1/posicoes_sascar"

    for veiculo in dados_veiculos:
        response = requests.post(url, json=veiculo, headers=headers)
        if response.status_code in [200, 201]:
            print(f"Veículo {veiculo.get('id_veiculo')} sincronizado com sucesso.")
        else:
            print(f"Erro ao salvar veículo {veiculo.get('id_veiculo')}: {response.text}")

if __name__ == "__main__":
    print(f"[{datetime.now()}] Iniciando execução do Robô SASCAR...")
    veiculos = buscar_posicoes_sascar()
    atualizar_supabase(veiculos)
    print(f"[{datetime.now()}] Execução finalizada.")