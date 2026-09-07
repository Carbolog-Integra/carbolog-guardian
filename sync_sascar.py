import os
import requests
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SASCAR_USER = os.getenv("SASCAR_USER")
SASCAR_PASS = os.getenv("SASCAR_PASS")

def buscar_telemetria_sascar_soap():
    print(f"[{datetime.now()}] Conectando ao Web Service SOAP da SASCAR...")
    
    url_wsdl = "https://sasintegra.sascar.com.br/SasIntegra/SasIntegraWSService?wsdl"
    
    # Testando com a operação padrão de últimas posições da SASCAR
    soap_envelope = f"""<?xml version="1.0" encoding="utf-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.sasintegra.sascar.com.br/">
       <soapenv:Header/>
       <soapenv:Body>
          <ws:recuperaUltimasPosicoes>
             <usuario>{SASCAR_USER}</usuario>
             <senha>{SASCAR_PASS}</senha>
          </ws:recuperaUltimasPosicoes>
       </soapenv:Body>
    </soapenv:Envelope>"""

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": ""
    }

    try:
        response = requests.post(url_wsdl, data=soap_envelope, headers=headers, timeout=45)
        print(f"HTTP Status Code: {response.status_code}")
        print(f"Resposta XML do Servidor SASCAR:\n{response.text}")
        return []
    except Exception as e:
        print(f"Falha de conexão com o WSDL SASCAR: {e}")
        return []

if __name__ == "__main__":
    buscar_telemetria_sascar_soap()
