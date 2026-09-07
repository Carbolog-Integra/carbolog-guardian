import os
import requests
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SASCAR_USER = os.getenv("SASCAR_USER")
SASCAR_PASS = os.getenv("SASCAR_PASS")

def buscar_e_sincronizar_sascar():
    print(f"[{datetime.now()}] Conectando ao Web Service SASCAR via obterPacotePosicoes...")
    
    url_wsdl = "https://sasintegra.sascar.com.br/SasIntegra/SasIntegraWSService?wsdl"
    
    # Utilizando o método clássico principal listado no WSDL
    soap_envelope = f"""<?xml version="1.0" encoding="utf-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.sasintegra.sascar.com.br/">
       <soapenv:Header/>
       <soapenv:Body>
          <ws:obterPacotePosicoes>
             <usuario>{SASCAR_USER}</usuario>
             <senha>{SASCAR_PASS}</senha>
          </ws:obterPacotePosicoes>
       </soapenv:Body>
    </soapenv:Envelope>"""

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": ""
    }

    try:
        response = requests.post(url_wsdl, data=soap_envelope, headers=headers, timeout=60)
        print(f"HTTP Status Code: {response.status_code}")
        print(f"Resposta XML do Servidor SASCAR:\n{response.text[:1200]}")

    except Exception as e:
        print(f"Erro durante a execução do robô: {e}")

if __name__ == "__main__":
    buscar_e_sincronizar_sascar()
