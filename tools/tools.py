# Import ToolNode from the prebuilt submodule.
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode 
import json
import csv
from io import StringIO
from typing import Optional

csv_data = """sessao_id,cinema_id,nome_cinema,cidade,estado,pais,filme_id,titulo_filme,genero,classificacao,duracao_min,data,horario,sala
1,1,Cinearte São Paulo,São Paulo,SP,Brasil,1,O Último Portal,Ficção Científica,12 anos,120,2023-12-15,16:00,5
2,1,Cinearte São Paulo,São Paulo,SP,Brasil,1,O Último Portal,Ficção Científica,12 anos,120,2023-12-15,19:30,5
3,1,Cinearte São Paulo,São Paulo,SP,Brasil,2,Amor em Veneza,Romance,Livre,110,2023-12-15,17:00,3
4,1,Cinearte São Paulo,São Paulo,SP,Brasil,2,Amor em Veneza,Romance,Livre,110,2023-12-15,20:00,3
5,1,Cinearte São Paulo,São Paulo,SP,Brasil,3,A Herança Perdida,Aventura,14 anos,130,2023-12-15,18:30,7
6,1,Cinearte São Paulo,São Paulo,SP,Brasil,3,A Herança Perdida,Aventura,14 anos,130,2023-12-15,21:30,7
7,2,Cinema Paradiso Paulista,São Paulo,SP,Brasil,4,O Enigma do Tempo,Ficção Científica,14 anos,125,2023-12-15,15:30,2
8,2,Cinema Paradiso Paulista,São Paulo,SP,Brasil,4,O Enigma do Tempo,Ficção Científica,14 anos,125,2023-12-15,19:00,2
9,2,Cinema Paradiso Paulista,São Paulo,SP,Brasil,5,Riso e Gargalhadas,Comédia,Livre,95,2023-12-15,14:00,1
10,2,Cinema Paradiso Paulista,São Paulo,SP,Brasil,5,Riso e Gargalhadas,Comédia,Livre,95,2023-12-15,16:15,1
11,2,Cinema Paradiso Paulista,São Paulo,SP,Brasil,6,Sussurros na Escuridão,Terror,16 anos,105,2023-12-15,22:00,4
12,2,Cinema Paradiso Paulista,São Paulo,SP,Brasil,6,Sussurros na Escuridão,Terror,16 anos,105,2023-12-15,23:59,4
13,3,Multiplex Ibirapuera,São Paulo,SP,Brasil,7,Coração de Herói,Ação,12 anos,140,2023-12-15,18:00,8
14,3,Multiplex Ibirapuera,São Paulo,SP,Brasil,7,Coração de Herói,Ação,12 anos,140,2023-12-15,21:00,8
15,3,Multiplex Ibirapuera,São Paulo,SP,Brasil,8,Dança dos Destinos,Drama,14 anos,115,2023-12-15,19:30,6
16,3,Multiplex Ibirapuera,São Paulo,SP,Brasil,8,Dança dos Destinos,Drama,14 anos,115,2023-12-15,22:00,6
17,3,Multiplex Ibirapuera,São Paulo,SP,Brasil,9,Missão Marte,Ficção Científica,10 anos,135,2023-12-15,15:00,9
18,3,Multiplex Ibirapuera,São Paulo,SP,Brasil,9,Missão Marte,Ficção Científica,10 anos,135,2023-12-15,18:30,9
19,4,Cinearte Rio,Rio de Janeiro,RJ,Brasil,10,O Segredo de Sofia,Drama,12 anos,118,2023-12-15,16:30,3
20,4,Cinearte Rio,Rio de Janeiro,RJ,Brasil,10,O Segredo de Sofia,Drama,12 anos,118,2023-12-15,19:00,3
21,4,Cinearte Rio,Rio de Janeiro,RJ,Brasil,11,O Rei do Pedaço,Comédia,Livre,100,2023-12-15,14:00,2
22,4,Cinearte Rio,Rio de Janeiro,RJ,Brasil,11,O Rei do Pedaço,Comédia,Livre,100,2023-12-15,16:15,2
23,4,Cinearte Rio,Rio de Janeiro,RJ,Brasil,12,Noite de Crime,Suspense,16 anos,122,2023-12-15,21:30,5
24,4,Cinearte Rio,Rio de Janeiro,RJ,Brasil,12,Noite de Crime,Suspense,16 anos,122,2023-12-15,23:45,5
25,5,Cinema Paradiso Copacabana,Rio de Janeiro,RJ,Brasil,13,A Lenda do Tesouro,Aventura,Livre,128,2023-12-15,15:30,4
26,5,Cinema Paradiso Copacabana,Rio de Janeiro,RJ,Brasil,13,A Lenda do Tesouro,Aventura,Livre,128,2023-12-15,19:00,4
27,5,Cinema Paradiso Copacabana,Rio de Janeiro,RJ,Brasil,14,Além da Imaginação,Fantasia,Livre,112,2023-12-15,17:00,1
"""

reader = csv.DictReader(StringIO(csv_data))
dicionario = {}

for row in reader:
    sessao_id = int(row['sessao_id'])
    dicionario[sessao_id] = {
        'cinema_id': int(row['cinema_id']),
        'nome_cinema': row['nome_cinema'],
        'cidade': row['cidade'],
        'estado': row['estado'],
        'pais': row['pais'],
        'filme_id': int(row['filme_id']),
        'titulo_filme': row['titulo_filme'],
        'genero': row['genero'],
        'classificacao': row['classificacao'],
        'duracao_min': int(row['duracao_min']),
        'data': row['data'],
        'horario': row['horario'],
        'sala': int(row['sala'])
    }
@tool
def look_session(cinema: Optional[str], movie: Optional[str], date: Optional[str], time: Optional[str]) -> dict:
    """
    Search for available cinema sessions.
    Use this to offer options to the user and help him decide for a cinema session.

    Args:
    cinema: Optional[str], movie: Optional[str], date: Optional[str], time: Optional[str]
    
    
    Returns:
        Avaiable movie sessions. Limit for 10 results
    """
    

    
    # Emulate JSON data from an API
    return json.dumps(dicionario)

@tool
def buy_tickets(cinema: str, movie: str, date: str, time: str, number: int ) -> dict:
    """
    Once you have all the information you can use this tool to book the seats   
    Args:
        location: City name
        date: Activity date (YYYY-MM-DD)
        preferences: Activity preferences/requirements
        
    Returns:
        Dictionary containing activity options
    """
    # Implement actual activity search logic here
    return "ticket bought"

tools = [buy_tickets, look_session]
tool_node = ToolNode(tools) 