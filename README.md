# Gerador de QR Code com Logotipo

Este projeto permite a criação de QR Codes personalizados, incluindo a opção de adicionar um logotipo no centro.

## Funcionalidades

- Geração de QR Codes simples.
- Geração de QR Codes com logotipo.
- Personalização do texto/URL e do logotipo utilizado.

## Como Usar

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/seu_usuario/qrcode_generator.git
    cd qrcode_generator
    ```

2. **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Execute o script**:
    ```bash
    python qrcode_generator.py
    ```

4. **Execute o script**:
	```bash
	pyinstaller --onefile qrcode_generator.py
	```
   - Isso vai criar o `qrcode_generator.exe` na pasta `dist/`.

## Customização

- **Logotipo**: Para usar um logotipo personalizado, substitua o arquivo `logo_padrao.png` no diretório raiz (mesmo local do executável).
- **Texto/URL**: Durante a execução, você pode definir o texto ou URL que será convertido em QR Code.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um _pull request_ ou relatar um _issue_.

