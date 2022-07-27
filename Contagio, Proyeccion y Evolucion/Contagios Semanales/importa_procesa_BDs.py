import pandas as pd

#Script de procesamiento de BDs de GitHub

class BDs_Contagios:
    def __init__(self):
        print('Se leen las BDs chilenas desde GitHub directamente')
        self.TxR = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/TotalesPorRegion_T.csv")
        self.UCI = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto8/UCI_T.csv")
        self.MxD = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo_T.csv")
        
        print('Se leen las BDs del mundo desde GitHub directamente')
        self.NewCases=pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_cases.csv")
        self.Deads=pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_deaths.csv")
        print('importadas!')
    
    def procesa_base(self):
        def muertos(df):
            a=0
            lista=[]
            for i in df.Valparaíso:
                lista.append(i-a)
                a=i
            df['Valparaíso']=lista
            
            b=0
            lista2=[]
            for i in df.Total:
                lista2.append(i-b)
                b=i
            df['Total']=lista2
        #CASOS
        self.Casos=pd.concat([self.TxR[['Region']].drop(self.TxR[['Region']].index[[0]]),
                 self.TxR.iloc[:,19:35].drop(self.TxR.iloc[:,19:34].index[[0]]).apply(pd.to_numeric).apply(pd.to_numeric)], 
                axis=1)
        self.Casos=self.Casos.rename(columns={'Region':'Fecha','Valparaíso.1':'Valparaíso','Total.1':'Total'})
        self.Casos.Fecha=pd.to_datetime(self.Casos.Fecha)
        #MUERTES
        self.MxD=self.MxD.rename(columns={'Region':'Fecha'})
        self.MxD.Fecha=pd.to_datetime(self.MxD.Fecha)
        muertos(self.MxD)
        #UCI
        self.UCI=self.UCI.rename(columns={'Region':'Fecha'})
        self.UCI=pd.concat([self.UCI.Fecha.drop(self.UCI.Fecha.index[[0,1]]),
                       self.UCI.iloc[:,1:].drop(self.UCI.index[[0,1]]).apply(pd.to_numeric)],
                      axis=1)
        drop=self.UCI.drop(['Fecha'], axis=1)
        self.UCI.Fecha=pd.to_datetime(self.UCI.Fecha)
        self.UCI['Total']=drop.sum(axis=1)
        print('procesadas!')
    
    def casos_agrupados(self):
        self.Casos2 = self.Casos.groupby([pd.Grouper(key='Fecha', freq='W-SUN')])
        print('casos agrupados!')
        return self.Casos2
    
    def uci_agrupados(self):
        self.UCI2   = self.UCI.groupby([pd.Grouper(key='Fecha', freq='W-SUN')])
        print('UCI agrupados!')
        return self.UCI2
    
    def deads_agrupados(self):
        self.MxD2 = self.MxD.groupby([pd.Grouper(key='Fecha', freq='W-SUN')])
        print('muertos agrupados!')
        return self.MxD2
    
    def casos_mundo(self):
        print('casos mundo retornado!')
        return self.NewCases
    
    def deads_mundo(self):
        print('muertos mundo retornados!')
        return self.Deads
        
        
        
        