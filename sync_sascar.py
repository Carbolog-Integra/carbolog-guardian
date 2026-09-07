import os
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SASCAR_USER = os.getenv("SASCAR_USER")
SASCAR_PASS = os.getenv("SASCAR_PASS")

def buscar_telemetria_sascar_soap():
    print(f"[{datetime.now()}] Conectando ao Web Service SOAP da SASCAR...")
    
    url_wsdl = "https://sasintegra.sascar.com.br/SasIntegra/SasIntegraWSService?wsdl"
    
    # Envelope SOAP padrão para requisição no SasIntegra
    # Ajuste a tag de acordo com o método WSDL da sua frota (ex: recuperaPosicoes, listarVeiculos, etc.)
    soap_envelope = f"""<?xml version="1.0" encoding="utf-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.sasintegra.sascar.com.br/">
       <soapenv:Header/>
       <soapenv:Body>
          <ws:recuperaPosicoes>
             <usuario>{SASCAR_USER}</usuario>
             <senha>{SASCAR_PASS}</senha>
          </ws:recuperaPosicoes>
       </soapenv:Body>
    </soapenv:Envelope>"""

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": ""
    }

    try:
        response = requests.post(url_wsdl, data=soap_envelope, headers=headers, timeout=45)
        
        if response.status_code == 200:
            print("Sucesso na resposta SOAP da SASCAR. Processando XML...")
            # Aqui você processaria o XML de retorno. Como exemplo estruturado, 
            # retornamos a lista pronta para o Supabase.
            return []
        else:
            print(f"Erro SOAP (Status {response.status_code}): {response.text}")
            return []
    except Exception as e:
        print(f"Falha de conexão com o WSDL SASCAR: {e}")
        return []

def atualizar_banco_supabase(veiculos):
    if not veiculos:
        print("Nenhum dado novo para sincronizar no Supabase.")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    url = f"{SUPABASE_URL}/rest/v1/posicoes_sascar"

    for v in veiculos:
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
    dados_frota = buscar_telemetria_sascar_soap()
    atualizar_banco_supabase(dados_frota)
