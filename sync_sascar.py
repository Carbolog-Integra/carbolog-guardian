import os
import requests
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SASCAR_USER = os.getenv("SASCAR_USER")
SASCAR_PASS = os.getenv("SASCAR_PASS")

def buscar_telemetria_sascar():
    print(f"[{datetime.now()}] Buscando posições na SASCAR...")
    # Insira aqui a requisição real para a API da SASCAR usando SASCAR_USER e SASCAR_PASS
    # Exemplo estruturado que retorna uma lista de dicionários com os veículos:
    posicoes_atualizadas = [
        # Exemplo: {"id_veiculo": "FRS2A84", "latitude": -23.9618, "longitude": -46.3919, "velocidade": 65, "ignicao": 1, "ododmetro": 501404, "data_posicao": datetime.now().isoformat()}
    ]
    return posicoes_atualizadas

def atualizar_banco_supabase(veiculos):
    if not veiculos:
        print("Nenhuma posição nova retornada pela SASCAR nesta execução.")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    url = f"{SUPABASE_URL}/rest/v1/posicoes_sascar"

    for v in veiculos:
        response = requests.post(url, json=v, headers=headers)
        if response.status_code in [200, 201]:
            print(f"Veículo {v.get('id_veiculo')} atualizado no Supabase.")
        else:
            print(f"Erro ao atualizar {v.get('id_veiculo')}: {response.text}")

if __name__ == "__main__":
    dados_frota = buscar_telemetria_sascar()
    atualizar_banco_supabase(dados_frota)
