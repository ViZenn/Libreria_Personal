import pandas as pd

class AUX_Contagios:
    def __init__(self):
        print('se inician las funciones auxiliares para procesar los contagios')
    
    def informe_nac(self,df,name):
        M=pd.DataFrame([df['Total'].mean(),
                        df['Total'].sum(),
                        df['Total'].mean().pct_change()])
        M=M.T
        M.columns = ['Prom_Sem_Nac'+name,'Total_Nac'+name,'Velocidad_Nac'+name]
        M.drop(M.tail(1).index,inplace=True)
        return M

    def informe_valpo(self,df,name):
        M=pd.DataFrame([df['Valparaíso'].mean(),
                        df['Valparaíso'].sum(),
                        df['Valparaíso'].mean().pct_change()])
        M=M.T
        M.columns = ['Prom_Sem_Valp'+name,'Total_Valp'+name,'Velocidad_Valp'+name]
        M.drop(M.tail(1).index,inplace=True)
        return M
    
    def informe_pais(self,df1,df2,name):
        df1.rename(columns={'date': 'Fecha'}, inplace=True)
        df1.Fecha=pd.to_datetime(df1.Fecha)
        agrupados1=df1.groupby([pd.Grouper(key='Fecha', freq='W-SUN')])
        M=pd.DataFrame([agrupados1[name].mean(),
                        agrupados1[name].sum(),
                        agrupados1[name].mean().pct_change()])
        M=M.T
        M.columns = ['Prom_Sem_Casos_'+name,'Total_Sem_Casos_'+name,'Velocidad_Sem_Casos_'+name]
        
        df2.rename(columns={'date': 'Fecha'}, inplace=True)
        df2.Fecha=pd.to_datetime(df1.Fecha)
        agrupados2=df2.groupby([pd.Grouper(key='Fecha', freq='W-SUN')])
        F=pd.DataFrame([agrupados2[name].mean(),
                        agrupados2[name].sum(),
                        agrupados2[name].mean().pct_change()])
        F=F.T
        F.columns = ['Prom_Sem_Muertes_'+name,'Total_Sem_Muertes_'+name,'Velocidad_Muertes_Casos_'+name]
        
        Z=pd.concat([M,F],axis=1)
        #Z.drop(Z.tail(1).index,inplace=True)
        Z=Z.tail(10)
        print('Creada BD de ',name)
        return Z
        
    def Valpo(self,casos,uci,deads):
        Valpo =pd.concat([self.informe_valpo(casos,'_Casos').tail(10),
                          self.informe_valpo(uci,'_UCI').tail(10),
                          self.informe_valpo(deads,'_Muertes').tail(10)],
                         axis=1)
        print('Creada BD de Valpo!')
        return Valpo
    
    def Chile(self,casos,uci,deads):
        Chile=pd.concat([self.informe_nac(casos,'_Casos').tail(10),
                         self.informe_nac(uci,'_UCI').tail(10),
                         self.informe_nac(deads,'_Muertes').tail(10)],
                        axis=1)
        print('Creada BD de Chile!')
        return Chile

