def buscar_telemetria_sascar_soap():
    print(f"[{datetime.now()}] Conectando ao Web Service SOAP da SASCAR...")
    
    url_wsdl = "https://sasintegra.sascar.com.br/SasIntegra/SasIntegraWSService?wsdl"
    
    # Alterado de recuperaPosicoes para getPosicoes (padrão mais comum na SASCAR)
    soap_envelope = f"""<?xml version="1.0" encoding="utf-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.sasintegra.sascar.com.br/">
       <soapenv:Header/>
       <soapenv:Body>
          <ws:getPosicoes>
             <usuario>{SASCAR_USER}</usuario>
             <senha>{SASCAR_PASS}</senha>
          </ws:getPosicoes>
       </soapenv:Body>
    </soapenv:Envelope>"""

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": ""
    }

    try:
        response = requests.post(url_wsdl, data=soap_envelope, headers=headers, timeout=45)
        print(f"Status Retorno: {response.status_code}")
        print(f"Resposta: {response.text[:500]}") # Imprime os primeiros caracteres para validação
        
        if response.status_code == 200:
            return []
        else:
            return []
    except Exception as e:
        print(f"Falha de conexão com o WSDL SASCAR: {e}")
        return []
