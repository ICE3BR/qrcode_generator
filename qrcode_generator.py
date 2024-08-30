import qrcode
from PIL import Image
from pathlib import Path
import os

def generate_qr_code(data, output_file="qrcode.png", size=10, border=4):
    """
    Gera um QR Code a partir dos dados fornecidos.

    :param data: Texto ou URL que deseja converter para QR code.
    :param output_file: Caminho e nome do arquivo de saída (PNG).
    :param size: Tamanho das caixas do QR code.
    :param border: Largura da borda em caixas.
    """
    qr = qrcode.QRCode(
        version=1,  # Versão 1: menor tamanho possível (maior=40)
        error_correction=qrcode.constants.ERROR_CORRECT_Q,  # Nível de correção de erros (L<M<Q<H)
        box_size=size,  # Tamanho de cada caixa
        border=border,  # Tamanho da borda
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    img.save(output_file)
    print("QR code gerado com sucesso")

def generate_qr_code_with_logo(data, logo_path=None, output_file="qrcode_with_logo.png", size=10, border=4, logo_size_ratio=0.2):
    """
    Gera um QR Code a partir dos dados fornecidos.

    :param data: Texto ou URL que deseja converter para QR code.
    :param logo_path: Caminho para a logo fornecida pelo usuário.
    :param output_file: Caminho e nome do arquivo de saída (PNG).
    :param size: Tamanho das caixas do QR code.
    :param border: Largura da borda em caixas.
    :param logo_size_ratio: Proporção do tamanho da logo em relação ao QR code.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Tenta carregar o logotipo local
    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)
            print(f"Logotipo carregado a partir de: {logo_path}")
        except Exception as e:
            print(f"Erro ao carregar o logotipo: {e}")
            return
    else:
        print("Logotipo não encontrado. Por favor, forneça um logotipo válido.")
        return

    # Redimensionando a logomarca para um tamanho menor
    logo_width = int(img.size[0] * logo_size_ratio)
    logo_height = int(img.size[1] * logo_size_ratio)
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

    if logo.mode != 'RGBA':
        logo = logo.convert('RGBA')

    box = (img.size[0] // 2 - logo.size[0] // 2, img.size[1] // 2 - logo.size[1] // 2)
    img.paste(logo, box, logo)

    img.save(output_file)
    print("QR code gerado com sucesso")

def show_menu():
    print("\nBem-vindo ao Gerador de QR Code")
    print("1. Gerar QR Code")
    print("2. Gerar QR Code com Logo")
    print("3. Sair\n")

def confirm_execution(data, output_file):
    print(f"Você está prestes a gerar um QR code para: {data}")
    print(f"O arquivo será salvo em: {output_file}")
    confirm = input("Deseja continuar? (s/n): ")
    return confirm.lower() == 's'

def confirm_execution_logo(data, logo_path, output_file):
    print(f"Você está prestes a gerar um QR code para: {data}")
    print(f"Com a logo: {logo_path}")
    print(f"O arquivo será salvo em: {output_file}")
    confirm = input("Deseja continuar? (s/n): ")
    return confirm.lower() == 's'

def get_downloads_folder():
    # Retorna o caminho da pasta de downloads padrão do usuário
    return str(Path.home() / "Downloads")

def get_logo_folder():
    # Diretório local onde o logotipo padrão deve estar
    return "./logo_padrao.png"

def get_data_folder():
    return "https://github.com/ICE3BR"

def generate_unique_filename(output_dir, data):
    # Gera um nome de arquivo único para evitar sobrescrita
    base_name = os.path.splitext(os.path.basename(data))[0]
    save_path = os.path.join(output_dir, f"{base_name}_QRCode")

    # Adicionar número sequencial ao nome do arquivo para evitar sobrescrita
    counter = 1
    while os.path.exists(f"{save_path}_{counter}.png"):
        counter += 1

    return f"{save_path}_{counter}.png"

def main():
    # Definir o diretório padrão do output e logo
    downloads_path = get_downloads_folder()  # Pasta padrão é downloads
    standard_logo_path = get_logo_folder()  # Caminho local do logotipo padrão
    standard_data = get_data_folder()  # Data padrão é do criador
    
    while True:  # Loop infinito até o usuário escolher sair
        show_menu()
        choice = input("Escolha uma opção: ")
        
        if choice == '1':
            user_data = input("Digite o texto ou URL para o QR code (ou pressione Enter para padrão): ")
            user_output_path = input("Digite o diretório para salvar o QR code (ou pressione Enter para salvar na pasta Downloads): ")
            
            output_dir = downloads_path if not user_output_path else user_output_path
            data = standard_data if not user_data else user_data
            output_file = generate_unique_filename(output_dir, data)
            
            if confirm_execution(data, output_file):
                generate_qr_code(data, output_file)
            else:
                print("Operação cancelada.")
        
        elif choice == '2':
            user_data = input("Digite o texto ou URL para o QR code (ou pressione Enter para padrão): ")
            user_logo_path = input("Digite o local onde está a logo (ou pressione Enter para usar o logotipo padrão): ")
            user_output_path = input("Digite o diretório para salvar o QR code (ou pressione Enter para salvar na pasta Downloads): ")
            
            logo_path = standard_logo_path if not user_logo_path else user_logo_path
            output_dir = downloads_path if not user_output_path else user_output_path
            data = standard_data if not user_data else user_data
            output_file = generate_unique_filename(output_dir, data)
            
            if confirm_execution_logo(data, logo_path, output_file):
                generate_qr_code_with_logo(data, logo_path, output_file)
            else:
                print("Operação cancelada.")
        
        elif choice == '3':
            print("Saindo...")
            break  # Sai do loop e encerra o programa
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
