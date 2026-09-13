import requests
from datetime import datetime

# Configurações de API e Supabase (Conforme os repositórios carbolog-integra)
SUPABASE_URL = "https://oyrqywoctnyottwvqrji.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95cnF5d29jdG55b3R0d3ZxcmppIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgyMjMyOTQsImV4cCI6MjEwMzc5OTI5NH0.VdqJLc_u1VXFrnOe59Bw7wLWV-GZLnx6_fjzBV_TU8w"

def sincronizar_telemetria_sascar():
    # 1. Consulta a API oficial do SASCAR (Substitua pela URL e headers reais da API SASCAR)
    # headers_sascar = { "Authorization": "Bearer TOKEN_SASCAR" }
    # resposta = requests.get("https://api.sascar.com.br/v1/veiculos/posicoes", headers=headers_sascar)
    # dados_sascar = resposta.json()
    
    # Exemplo simulado da estrutura retornada pelo SASCAR em tempo real:
    dados_sascar = [
        # Insira aqui o mapeamento dos dados vindos diretamente da API SASCAR
    ]

    veiculos_unicos = {}

    # 2. Garante estritamente o filtro do ÚLTIMO pacote real por veículo
    for item in dados_sascar:
        id_veiculo = str(item.get("id_veiculo")).strip()
        if not id_veiculo:
            continue

        # Força velocidade 0 se o veículo estiver parado ou sem deslocamento real
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

        # Sobrescreve para manter apenas o pacote mais recente varrido na API
        veiculos_unicos[id_veiculo] = payload_tratado

    # 3. Envia os dados limpos e consolidados para o Supabase
    headers_supabase = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    for id_veic, dados in veiculos_unicos.items():
        # Faz o upsert no Supabase utilizando a chave única do veículo
        requests.post(
            f"{SUPABASE_URL}/rest/v1/posicoes_sascar",
            headers=headers_supabase,
            json=dados
        )

if __name__ == "__main__":
    sincronizar_telemetria_sascar()
