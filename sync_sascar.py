import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import zeep
from zeep.transports import Transport
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SASCAR_USER = os.getenv("SASCAR_USER")
SASCAR_PASS = os.getenv("SASCAR_PASS")

def obter_endereco_por_coordenadas(lat, lon):
    if not lat or not lon:
        return {"cidade": "Desconhecido", "uf": "SP", "rua": "Coordenada inválida"}
    
    try:
        time.sleep(1)
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
        headers = {'User-Agent': 'CarbologGuardianFleetSystem/2.0'}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            address = data.get('address', {})
            
            cidade = (
                address.get('city') or 
                address.get('town') or 
                address.get('municipality') or 
                address.get('city_district') or 
                'Região Metropolitana'
            )
            uf = address.get('state_code') or address.get('state') or 'SP'
            if len(uf) > 2:
                uf = 'SP'
                
            rua = (
                address.get('road') or 
                address.get('pedestrian') or 
                address.get('suburb') or 
                address.get('highway') or 
                'Via Pública'
            )
            return {"cidade": cidade, "uf": uf.upper(), "rua": rua}
    except Exception as e:
        print(f"Aviso geocoding: {e}")
    
    return {"cidade": "Interior SP", "uf": "SP", "rua": "Rodovia Monitorada"}

def buscar_e_sincronizar_sascar():
    print(f"[{datetime.now()}] Conectando ao WSDL da SASCAR via Zeep...")
    url_wsdl = "https://sasintegra.sascar.com.br/SasIntegra/SasIntegraWSService?wsdl"
    
    try:
        session = requests.Session()
        transport = Transport(session=session)
        client = zeep.Client(wsdl=url_wsdl, transport=transport)
        
        print("Buscando pacote de posições atualizadas da frota...")
        
        resposta = client.service.obterPacotePosicoes(
            usuario=SASCAR_USER, 
            senha=SASCAR_PASS, 
            quantidade=1000
        )
        
        if not resposta:
            print("Nenhum dado retornado pela SASCAR.")
            return

        print(f"Total de registros obtidos: {len(resposta)}. Processando geolocalização e Supabase...")

        headers_sup = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"
        }
        url_sup = f"{SUPABASE_URL}/rest/v1/posicoes_sascar"

        fuso_brasilia = ZoneInfo("America/Sao_Paulo")

        for item in resposta:
            lat = float(getattr(item, 'latitude', 0.0))
            lon = float(getattr(item, 'longitude', 0.0))
            
            endereco = obter_endereco_por_coordenadas(lat, lon)

            data_original = getattr(item, 'data', None)
            if isinstance(data_original, datetime):
                if data_original.tzinfo is None:
                    data_original = data_original.replace(tzinfo=ZoneInfo("UTC"))
                data_brasilia = data_original.astimezone(fuso_brasilia).isoformat()
            else:
                data_brasilia = datetime.now(fuso_brasilia).isoformat()

            placa_veiculo = (
                getattr(item, 'placa', None) or 
                getattr(item, 'placaVeiculo', None) or 
                str(getattr(item, 'idVeiculo', 'N/D'))
            )

            velocidade_bruta = float(getattr(item, 'velocidade', 0))
            velocidade_tratada = int(round(velocidade_bruta)) if velocidade_bruta >= 1 else 0

            payload_supabase = {
                "id_veiculo": placa_veiculo,
                "latitude": lat,
                "longitude": lon,
                "velocidade": velocidade_tratada,
                "ignicao": int(1 if getattr(item, 'ignicao', False) else 0),
                "odometro": int(getattr(item, 'odometro', 0)),
                "data_posicao": data_brasilia,
                "cidade": endereco["cidade"],
                "uf": endereco["uf"],
                "rua": endereco["rua"]
            }

            res = requests.post(url_sup, json=payload_supabase, headers=headers_sup)
            if res.status_code not in [200, 201]:
                print(f"Erro ao salvar veículo {placa_veiculo}: {res.text}")

        print(f"[{datetime.now()}] Sincronização concluída com sucesso!")

    except Exception as e:
        print(f"Erro na execução da sincronização: {e}")

if __name__ == "__main__":
    buscar_e_sincronizar_sascar()
