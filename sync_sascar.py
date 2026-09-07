import os
from datetime import datetime
import zeep

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SASCAR_USER = os.getenv("SASCAR_USER")
SASCAR_PASS = os.getenv("SASCAR_PASS")

def inspecionar_wsdl_sascar():
    print(f"[{datetime.now()}] Inspecionando operações disponíveis no WSDL da SASCAR...")
    url_wsdl = "https://sasintegra.sascar.com.br/SasIntegra/SasIntegraWSService?wsdl"
    
    try:
        client = zeep.Client(wsdl=url_wsdl)
        print("\n--- OPERAÇÕES DISPONÍVEIS NO SERVIDOR SASCAR ---")
        for service in client.wsdl.services.values():
            for port in service.ports.values():
                for operation in port.binding.operations.values():
                    print(f"Método válido: {operation.name}")
        print("----------------------------------------------\n")
    except Exception as e:
        print(f"Erro ao inspecionar WSDL: {e}")

if __name__ == "__main__":
    inspecionar_wsdl_sascar()
