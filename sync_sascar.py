import os
import requests
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SASCAR_USER = os.getenv("SASCAR_USER")
SASCAR_PASS = os.getenv("SASCAR_PASS")

def sincronizar_dados():
    print(f"[{datetime.now()}] Conectando ao integrador SASCAR...")
    
    # Exemplo de payload padronizado para ingestão na tabela posicoes_sascar do Supabase
    # Insira aqui os dados retornados pela API ou sua rotina de integração de frotas
    payload_exemplo = []

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Erro: Credenciais do Supabase não configuradas nas Secrets.")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    url = f"{SUPABASE_URL}/rest/v1/posicoes_sascar"

    # Se houver dados novos capturados, enviamos para o Supabase
    for item in payload_exemplo:
        response = requests.post(url, json=item, headers=headers)
        if response.status_code in [200, 201]:
            print(f"Registro do veículo {item.get('id_veiculo')} atualizado com sucesso.")
        else:
            print(f"Falha ao salvar: {response.text}")

if __name__ == "__main__":
    sincronizar_dados()
