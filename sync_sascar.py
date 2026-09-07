import os
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SASCAR_USER = os.getenv("SASCAR_USER")
SASCAR_PASS = os.getenv("SASCAR_PASS")

def inspecionar_wsdl_direto():
    print(f"[{datetime.now()}] Baixando e inspecionando o WSDL da SASCAR...")
    url_wsdl = "https://sasintegra.sascar.com.br/SasIntegra/SasIntegraWSService?wsdl"
    
    try:
        response = requests.get(url_wsdl, timeout=30)
        if response.status_code != 200:
            print(f"Erro ao baixar WSDL: HTTP {response.status_code}")
            return

        # Faz o parsing do XML do WSDL
        root = ET.fromstring(response.content)
        
        # O WSDL usa namespaces, procuramos por tags 'operation' independentemente do prefixo
        print("\n--- MÉTODOS DISPONÍVEIS NO WSDL DA SASCAR ---")
        metodos_encontrados = set()
        for elem in root.iter():
            if elem.tag.endswith('operation'):
                nome = elem.get('name')
                if nome:
                    metodos_encontrados.add(nome)

        for m in sorted(metodos_encontrados):
            print(f"-> {m}")
        print("---------------------------------------------\n")

    except Exception as e:
        print(f"Erro ao inspecionar o XML do WSDL: {e}")

if __name__ == "__main__":
    inspecionar_wsdl_direto()
