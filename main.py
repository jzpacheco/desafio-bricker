import sys
from extraction import process_pdf

def main():
    

        # Verifica se foi fornecido o caminho do documento como argumento
    if len(sys.argv) != 2:
        print("Uso: python main.py caminho_para_o_documento.pdf")
        sys.exit(1)

    # Obtém o caminho do documento a partir dos argumentos de linha de comando
    pdf_path = sys.argv[1]

    # Processa o documento PDF e extrai os dados
    extracted_data = process_pdf(pdf_path)

    # Exibe os dados extraídos
    print(extracted_data)

if __name__ == "__main__":
    main()