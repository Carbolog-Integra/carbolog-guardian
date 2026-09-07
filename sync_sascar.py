import os
from datetime import datetime
from zoneinfo import ZoneInfo
import zeep
from zeep.transports import Transport
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SASCAR_USER = os.getenv("SASCAR_USER")
SASCAR_PASS = os.getenv("SASCAR_PASS")

def buscar_e_sincronizar_sascar():
    print(f"[{datetime.now()}] Conectando ao WSDL da SASCAR via Zeep...")
    url_wsdl = "https://sasintegra.sascar.com.br/SasIntegra/SasIntegraWSService?wsdl"
    
    try:
        session = requests.Session()
        transport = Transport(session=session)
        client = zeep.Client(wsdl=url_wsdl, transport=transport)
        
        print("Buscando pacote de posições da frota...")
        
        resposta = client.service.obterPacotePosicoes(
            usuario=SASCAR_USER, 
            senha=SASCAR_PASS, 
            quantidade=1000
        )
        
        if not resposta:
            print("Nenhum dado retornado pela SASCAR.")
            return

        print(f"Total de registros obtidos: {len(resposta)}. Sincronizando com o Supabase...")

        headers_sup = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"
        }
        url_sup = f"{SUPABASE_URL}/rest/v1/posicoes_sascar"

        fuso_brasilia = ZoneInfo("America/Sao_Paulo")

        for item in resposta:
            data_original = getattr(item, 'data', None)
            
            if isinstance(data_original, datetime):
                # Força a interpretação como UTC caso venha ingênua e converte para Brasília
                if data_original.tzinfo is None:
                    data_original = data_original.replace(tzinfo=ZoneInfo("UTC"))
                data_brasilia = data_original.astimezone(fuso_brasilia).isoformat()
            else:
                data_brasilia = datetime.now(fuso_brasilia).isoformat()

            # Tenta capturar a placa real por diferentes atributos possíveis no objeto SASCAR
            placa_veiculo = (
                getattr(item, 'placa', None) or 
                getattr(item, 'placaVeiculo', None) or 
                str(getattr(item, 'idVeiculo', 'N/D'))
            )

            payload_supabase = {
                "id_veiculo": placa_veiculo,
                "latitude": float(getattr(item, 'latitude', 0.0)),
                "longitude": float(getattr(item, 'longitude', 0.0)),
                "velocidade": int(getattr(item, 'velocidade', 0)),
                "ignicao": int(1 if getattr(item, 'ignicao', False) else 0),
                "odometro": int(getattr(item, 'odometro', 0)),
                "data_posicao": data_brasilia
            }

            res = requests.post(url_sup, json=payload_supabase, headers=headers_sup)
            if res.status_code not in [200, 201]:
                print(f"Erro ao salvar veículo {payload_supabase['id_veiculo']}: {res.text}")

        print(f"[{datetime.now()}] Sincronização concluída com sucesso!")

    except Exception as e:
        print(f"Erro na execução da sincronização: {e}")

if __name__ == "__main__":
    buscar_e_sincronizar_sascar()
