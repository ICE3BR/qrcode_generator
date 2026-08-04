# Gerador de QR Code com logotipo

Projeto em Python para criar QR Codes a partir de textos ou URLs, com opção de inserir um logotipo no centro da imagem.

## Funcionalidades

- Geração de QR Codes
- Personalização do conteúdo
- Inclusão opcional de logotipo
- Exportação da imagem gerada
- Empacotamento como executável

## Instalação

```bash
git clone https://github.com/ICE3BR/qrcode_generator.git
cd qrcode_generator
pip install -r requirements.txt
```

## Execução

```bash
python qrcode_generator.py
```

## Gerar executável

```bash
pyinstaller --onefile qrcode_generator.py
```

O executável será criado no diretório `dist`.

## Tecnologias

- Python
- qrcode
- Pillow

## Licença

Consulte os arquivos do repositório para verificar as condições de uso.
