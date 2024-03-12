# Projeto de Extração de Dados de Documentos Imobiliários
[Versão feita no Google Colab](https://colab.research.google.com/drive/12nhNQE3YxF2R19y5i_MVgavvr01qqfv0?usp=sharing)


Este projeto consiste em uma solução para extrair dados de documentos imobiliários, como matrículas de imóveis, utilizando a linguagem de programação Python e diversas bibliotecas, incluindo boto3 para integração com os serviços da AWS (Amazon Web Services), fitz para processamento de PDFs e langchain para processamento de linguagem natural e extração estruturada de dados.

## Requisitos do Sistema
Para executar este projeto, é necessário ter o Python instalado em seu ambiente de desenvolvimento, juntamente com as seguintes bibliotecas:

boto3: Para integração com os serviços da AWS.

PyMuPDF (também conhecido como fitz): Para processamento de documentos PDF.

langchain: Para processamento de linguagem natural e extração estruturada de dados.

Você pode instalar as bibliotecas necessárias utilizando o seguinte comando pip:

```pip install PyMuPDF boto3 langchain-openai langchain```

## Configuração
Antes de utilizar o projeto, é necessário configurar suas credenciais da AWS para acesso ao serviço Textract. Você pode fazer isso fornecendo suas credenciais diretamente no código ou configurando o arquivo de configuração padrão da AWS (~/.aws/credentials). E também necessário adicionar a key de acesso para a OpenAI api, no arquivo [config.py](config.py)

## Uso
O projeto consiste em um script Python (main.py) que pode ser executado para extrair dados de documentos imobiliários. O script utiliza uma combinação de processamento de imagem (para documentos digitalizados) e processamento de linguagem natural para extrair informações estruturadas dos documentos.

Para executar o script, basta fornecer o caminho do documento imobiliário como argumento de linha de comando:

```python main.py caminho_para_o_documento.pdf```
