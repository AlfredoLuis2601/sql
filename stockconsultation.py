import pyodbc
import requests
import os 
import dotenv
stockName=input("Digite o simbolo da acao:")
dotenv.load_dotenv()
apikey=os.getenv('API_KEY')
last_price=None
try:
    url=f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stockName}&&outputsize=compact&apikey={apikey}'
    dadoJson=requests.get(url)
    dados=dadoJson.json()
    if 'Global Quote' in dados:
       price=dados['Global Quote']
       last_price=price.get('05. price')
       latest_trading_day=price.get('07. latest trading day')
       print(last_price)
    if last_price:   
         dados_conexao=(
          "Driver={SQL Server};"
          r"Server=localhost\SQLEXPRESS;"
          "DataBase=StockDB;"
          )
         conexao=pyodbc.connect(dados_conexao)
         print("Conexao bem sucedida!")
         try:
           cursor=conexao.cursor()
           comando="""INSERT INTO StockInformation(StockID,Name,UnitPrice,ConsultationDate)
           VALUES(?,?,?,?)
           """
           cursor.execute(comando,1,stockName,last_price,latest_trading_day)
           cursor.commit()
           cursor.close()
         except pyodbc.Error as erro_DB:
           print("Erro ao transferir os dados para o banco de dados.Tente novamente.")
        
except requests.exceptions.RequestException:
    print("Erro na requests.")

    
    



