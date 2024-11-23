import numpy as np
from datetime import datetime

def carregar_dados(arquivo_csv):
    tipos = [('data', 'U10'), ('regiao', 'U20'), ('produto', 'U20'), ('quantidade', 'f8'), ('preco_unitario', 'f8')]
    
    dados = np.genfromtxt(arquivo_csv, delimiter=',', dtype=tipos, encoding='utf-8', skip_header=1)
    
    datas = np.array([datetime.strptime(row['data'], "%Y-%m-%d") for row in dados])
    regioes = dados['regiao']
    produtos = dados['produto']
    quantidade = dados['quantidade']
    preco_unitario = dados['preco_unitario']
    valor_total = quantidade * preco_unitario  
    matriz_dados = np.column_stack((datas, regioes, produtos, quantidade, preco_unitario, valor_total))
    return matriz_dados

def analise_estatistica(dados):
    valor_total = dados[:, 5].astype(float)
    
    resultados = {
        "media": np.mean(valor_total),
        "mediana": np.median(valor_total),
        "desvio_padrao": np.std(valor_total)
    }
    
    produtos = dados[:, 2]
    quantidades = dados[:, 3].astype(float)
    valor_por_produto = {produto: valor_total[produtos == produto].sum() for produto in np.unique(produtos)}
    quantidade_por_produto = {produto: quantidades[produtos == produto].sum() for produto in np.unique(produtos)}

    resultados["produto_mais_vendido"] = max(quantidade_por_produto, key=quantidade_por_produto.get)
    resultados["produto_maior_valor"] = max(valor_por_produto, key=valor_por_produto.get)
    resultados["quantidade_mais_vendida"] = quantidade_por_produto[resultados["produto_mais_vendido"]]
    resultados["valor_maior_venda"] = valor_por_produto[resultados["produto_maior_valor"]]
    
    regioes = dados[:, 1]
    resultados["total_vendas_por_regiao"] = {regiao: valor_total[regioes == regiao].sum() for regiao in np.unique(regioes)}
    
    return resultados

def analise_temporal(dados):
    datas = dados[:, 0]
    valor_total = dados[:, 5].astype(float)
    
    dias_unicos = np.unique(datas)
    vendas_por_dia = [valor_total[datas == dia].sum() for dia in dias_unicos]
    dias_semana = [dia.strftime("%A") for dia in dias_unicos]
    
    resultados = {
        "venda_media_por_dia": np.mean(vendas_por_dia),
        "dia_mais_vendas": max(set(dias_semana), key=dias_semana.count),
        "variacao_diaria": np.diff(vendas_por_dia)
    }
    
    return resultados


def main():
    arquivo_csv = '/mnt/data/vendas.csv'  
    dados = carregar_dados(arquivo_csv)
    estatisticas = analise_estatistica(dados)
    print("Análise Estatística:", estatisticas)
    temporal = analise_temporal(dados)
    print("Análise Temporal:", temporal)

if __name__ == "__main__":
    main()
