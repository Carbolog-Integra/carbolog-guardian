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
        # Configura o transporte com timeout para evitar travamentos
        session = requests.Session()
        session.timeout = 30
        transport = Transport(session=session)
        
        client = zeep.Client(wsdl=url_wsdl, transport=transport)
        
        # Testando a chamada do método padrão de obtenção de veículos ou posições
        print("Executando chamada SOAP via cliente WSDL...")
        
        # O zeep mapeia os parâmetros definidos no WSDL automaticamente
        try:
            resultado = client.service.obterVeiculos(usuario=SASCAR_USER, senha=SASCAR_PASS)
            print(f"Sucesso! Dados obtidos: {str(resultado)[:300]}")
        except Exception as e_metodo:
            print(f}Erro ao chamar obterVeiculos: {e_metodo}")
            
    except Exception as e:
        print(f"Erro geral de conexão SOAP: {e}")

if __name__ == "__main__":
    buscar_e_sincronizar_sascar()
