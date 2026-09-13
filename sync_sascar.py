import os
import time
from datetime import datetime
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SASCAR_USER = os.getenv("SASCAR_USER")
SASCAR_PASS = os.getenv("SASCAR_PASS")

def sincronizar_telemetria_sascar():
    # Insira aqui a chamada real à API/SOAP da SASCAR para obter os dados brutos
    dados_sascar = [] 

    veiculos_unicos = {}

    for item in dados_sascar:
        id_veiculo = str(item.get("id_veiculo", "")).strip()
        if not id_veiculo:
            continue

        velocidade_real = float(item.get("velocidade", 0))
        if velocidade_real < 1:
            velocidade_real = 0.0

        payload_tratado = {
            "id_veiculo": id_veiculo,
            "data_posicao": item.get("data_posicao", datetime.now().isoformat()),
            "velocidade": velocidade_real,
            "latitude": item.get("latitude"),
            "longitude": item.get("longitude"),
            "ignicao": bool(item.get("ignicao", False)),
            "cidade": item.get("cidade", ""),
            "uf": item.get("uf", ""),
            "rua": item.get("rua", "")
        }

        veiculos_unicos[id_veiculo] = payload_tratado

    headers_supabase = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    for id_veic, dados in veiculos_unicos.items():
        requests.post(
            f"{SUPABASE_URL}/rest/v1/posicoes_sascar",
            headers=headers_supabase,
            json=dados
        )

if __name__ == "__main__":
    sincronizar_telemetria_sascar()
