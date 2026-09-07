import os
from datetime import datetime
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
        
        print("Executando chamada SOAP com o parâmetro quantidade...")
        
        # Passando usuario, senha e quantidade conforme exigido pelo validador SASCAR
        resultado = client.service.obterVeiculos(
            usuario=SASCAR_USER, 
            senha=SASCAR_PASS, 
            quantidade=1000
        )
        
        print(f"Sucesso absoluto! Veículos obtidos: {str(resultado)[:400]}")
        
    except Exception as e:
        print(f"Erro na execução SOAP: {e}")

if __name__ == "__main__":
    buscar_e_sincronizar_sascar()
