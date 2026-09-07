import os
import requests
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SASCAR_USER = os.getenv("SASCAR_USER")
SASCAR_PASS = os.getenv("SASCAR_PASS")

def buscar_telemetria_sascar():
    print(f"[{datetime.now()}] Conectando à API SASCAR...")
    
    # 1. Autenticação e requisição na API da SASCAR
    # Ajuste o endpoint conforme a documentação oficial da SASCAR utilizada pela sua frota
    url_sascar = "https://api.sascar.com.br/telemetria/v1/posicoes" # Exemplo de endpoint oficial
    headers = {"Content-Type": "application/json"}
    payload = {
        "usuario": SASCAR_USER,
        "senha": SASCAR_PASS
    }
    
    try:
        # Se sua API usa Basic Auth ou Bearer Token, ajuste o cabeçalho conforme necessário:
        response = requests.post(url_sascar, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            dados = response.json()
            print(f"Sucesso: {len(dados)} posições obtidas da SASCAR.")
            return dados
        else:
            print(f"Erro na API SASCAR (Status {response.status_code}): {response.text}")
            return []
    except Exception as e:
        print(f"Falha de conexão com a SASCAR: {e}")
        return []

def atualizar_banco_supabase(veiculos):
    if not veiculos:
        print("Nenhum dado para sincronizar no Supabase.")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    url = f"{SUPABASE_URL}/rest/v1/posicoes_sascar"

    for v in veiculos:
        # Garanta que as chaves do dicionário correspondem às colunas da sua tabela no Supabase
        payload_supabase = {
            "id_veiculo": str(v.get("id_veiculo")),
            "latitude": float(v.get("latitude", 0)),
            "longitude": float(v.get("longitude", 0)),
            "velocidade": int(v.get("velocidade", 0)),
            "ignicao": int(v.get("ignicao", 0)),
            "odometro": int(v.get("odometro", 0)),
            "data_posicao": v.get("data_posicao", datetime.now().isoformat())
        }

        response = requests.post(url, json=payload_supabase, headers=headers)
        if response.status_code in [200, 201]:
            print(f"Veículo {payload_supabase['id_veiculo']} atualizado no Supabase.")
        else:
            print(f"Erro ao salvar veículo {payload_supabase['id_veiculo']}: {response.text}")

if __name__ == "__main__":
    frota_dados = buscar_telemetria_sascar()
    atualizar_banco_supabase(frota_dados)
