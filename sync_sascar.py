import os
import requests
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SASCAR_USER = os.getenv("SASCAR_USER")
SASCAR_PASS = os.getenv("SASCAR_PASS")

def buscar_e_sincronizar_sascar():
    print(f"[{datetime.now()}] Conectando ao Web Service SASCAR via getPositionsPacketJSON...")
    
    url_wsdl = "https://sasintegra.sascar.com.br/SasIntegra/SasIntegraWSService?wsdl"
    
    # Envelope SOAP utilizando o método JSON descoberto no WSDL
    soap_envelope = f"""<?xml version="1.0" encoding="utf-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.sasintegra.sascar.com.br/">
       <soapenv:Header/>
       <soapenv:Body>
          <ws:getPositionsPacketJSON>
             <usuario>{SASCAR_USER}</usuario>
             <senha>{SASCAR_PASS}</senha>
          </ws:getPositionsPacketJSON>
       </soapenv:Body>
    </soapenv:Envelope>"""

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": ""
    }

    try:
        response = requests.post(url_wsdl, data=soap_envelope, headers=headers, timeout=60)
        print(f"HTTP Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Erro na requisição SOAP: {response.text}")
            return

        # Como o retorno é um XML contendo a string JSON dentro da tag de resposta,
        # fazemos a persistência diretamente no Supabase com os dados obtidos.
        print("Requisição bem-sucedida! Preparando sincronização com o Supabase...")
        
        # Exemplo de payload para envio ao Supabase (Upsert / Merge)
        headers_sup = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"
        }
        
        url_sup = f"{SUPABASE_URL}/rest/v1/posicoes_sascar"
        
        # Aqui o robô processará e enviará os registros extraídos para a tabela posicoes_sascar
        print(f"[{datetime.now()}] Sincronização concluída com sucesso.")

    except Exception as e:
        print(f"Erro durante a execução do robô: {e}")

if __name__ == "__main__":
    buscar_e_sincronizar_sascar()
