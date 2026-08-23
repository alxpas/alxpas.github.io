import os
import re
from datetime import datetime

pasta_posts = os.path.join('content', 'posts')

# Listas separadas para os idiomas
posts_pt = []
posts_en = []

meses = {
    'pt': {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 
           7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'},
    'en': {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 
           7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
}

for root, dirs, files in os.walk(pasta_posts):
    for file in files:
        if file.endswith('.md') and not file.startswith('_'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            match_title = re.search(r'(?m)^title:\s*"?([^"\n]+)"?', conteudo)
            title = match_title.group(1).strip() if match_title else "Sem Título"
            
            match_date = re.search(r'(?m)^date:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})', conteudo)
            if match_date:
                try:
                    date_obj = datetime.strptime(match_date.group(1), '%Y-%m-%d')
                except:
                    continue
            else:
                continue

            caminho_relativo = filepath.replace('content' + os.sep, '').replace(os.sep, '/')
            link_hugo = f'{{{{< ref "{caminho_relativo}" >}}}}'
            
            post_dados = {
                'title': title,
                'date': date_obj,
                'link': link_hugo
            }
            
            # Distribui os posts para as listas corretas baseado na extensão
            if file.endswith('.en.md'):
                posts_en.append(post_dados)
            else:
                posts_pt.append(post_dados)

def agrupar_posts(lista_posts):
    lista_posts.sort(key=lambda x: x['date'], reverse=True)
    agrupado = {}
    for p in lista_posts:
        chave = (p['date'].year, p['date'].month)
        if chave not in agrupado:
            agrupado[chave] = []
        agrupado[chave].append(p)
    return agrupado

agrupado_pt = agrupar_posts(posts_pt)
agrupado_en = agrupar_posts(posts_en)

def gerar_index(idioma, arquivo_saida, titulo_pagina, agrupamento):
    caminho_index = os.path.join('content', arquivo_saida)
    with open(caminho_index, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write(f'title: "{titulo_pagina}"\n')
        # Remove a barra lateral esquerda (centraliza o conteúdo)
        f.write('sidebar:\n')
        # Força a exibição do "Nesta página" (Table of Contents) na direita
        f.write('toc: true\n')
        f.write("---\n\n")

        for (ano, mes) in sorted(agrupamento.keys(), reverse=True):
            nome_mes = meses[idioma][mes]
            # Esses '##' é o que o Hugo vai usar para montar o "Nesta página"
            f.write(f"## {ano} - {nome_mes}\n\n")
            for p in agrupamento[(ano, mes)]:
                f.write(f"- [{p['title']}]({p['link']})\n")
            f.write("\n")

# Gera a página em Português
gerar_index('pt', '_index.md', 'Blog Pessoal | Alex Paulino', agrupado_pt)

# Gera a página em Inglês
gerar_index('en', '_index.en.md', "Alex Paulino | Personal Blog", agrupado_en)

print("Páginas iniciais bilíngues geradas com sucesso!")