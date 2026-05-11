#Lógica
from pathlib import Path
import shutil

def processar_fitas(diretorio, tipo_buscado, numeros_alvo, callback_log):
    caminho = Path(diretorio)
    arquivos_encontrados = []

    # 1. Varredura e Busca
    for arquivo in caminho.iterdir():
        if arquivo.is_file():
            try:
                with open(arquivo, 'r', encoding='latin-1') as f:
                    linhas_cabecalho = [next(f, '') for _ in range(10)]
                    conteudo_cabecalho = "".join(linhas_cabecalho)
                    
                    if tipo_buscado in conteudo_cabecalho:
                        for num in numeros_alvo:
                            if f"MUNI{num}SIGPEC" in conteudo_cabecalho:
                                arquivos_encontrados.append((arquivo, num))
                                break 
            except Exception:
                pass 

    # 2. Retorno de status caso não encontre nada
    if not arquivos_encontrados:
        callback_log("Nenhum arquivo correspondente foi encontrado nesta pasta.\n")
        return

    # 3. Processamento e Renomeio Automático
    callback_log(f"Foram encontrados {len(arquivos_encontrados)} arquivos:\n\n")

    pasta_destino = caminho / "Arquivos_Separados"
    pasta_destino.mkdir(exist_ok=True)

    for caminho_arquivo, numero_encontrado in arquivos_encontrados:
        nome_original = caminho_arquivo.name
        nome_base = caminho_arquivo.stem
        novo_nome = f"{nome_base}_{numero_encontrado}.CSV"
        
        callback_log(f"Original: {nome_original}\n")
        callback_log(f"Novo:     {novo_nome}\n\n")
        
        caminho_destino = pasta_destino / novo_nome
        shutil.copy2(caminho_arquivo, caminho_destino) 

    callback_log(f"{'-'*40}\nSucesso! Arquivos copiados e renomeados na pasta 'Arquivos_Separados'.\n")