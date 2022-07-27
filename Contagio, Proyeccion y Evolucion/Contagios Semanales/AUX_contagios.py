import pandas as pd
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

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
    
    def grafica_casos(self,Valpo,Chile):
        print('Creando gráficos de barras y lineas para casos nuevos')
        #aqui se hace el df extra para graficar
        DF2=Valpo[['Prom_Sem_Valp_Casos','Velocidad_Valp_Casos']].join(Chile[['Prom_Sem_Nac_Casos','Velocidad_Nac_Casos']])
        DF2['Prom_Sem_Valp_Casos'] = [round(d,2) for d in DF2['Prom_Sem_Valp_Casos']]
        DF2['Prom_Sem_Nac_Casos'] = [round(d,2) for d in DF2['Prom_Sem_Nac_Casos']]
        DF2['Velocidad_Nac_Casos'] = [round(d,2) for d in DF2['Velocidad_Nac_Casos']]
        DF2['Velocidad_Valp_Casos'] = [round(d,2) for d in DF2['Velocidad_Valp_Casos']]
        DF2=DF2.reset_index()
        DF2['dia'] = [d.date() for d in DF2['Fecha']]
        DF2.set_index('dia',inplace=True)
        #aca se grafica y da forma
        ax=DF2.plot(y=['Prom_Sem_Valp_Casos', 'Prom_Sem_Nac_Casos'], kind="bar",grid=True,
                    figsize=(9,8),label=['Casos Valparaíso','Casos Nacionales'])
        ax2 = ax.twinx()
        ax2.plot(DF2['Velocidad_Valp_Casos'].values, linestyle='-', linewidth=2.0,color='gray',label='Velocidad Valparaíso')
        ax2.plot(DF2['Velocidad_Nac_Casos'].values, linestyle='-', linewidth=2.0,color='yellow',label='Velocidad Nacional')
        ax.set_title("Casos Nuevos", fontsize=25)
        ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
        plt.legend(loc=2)
        plt.savefig("Barra_Linea_Casos_Nuevos.jpg")
        print('Gráfico Exportado!')
    
    def grafica_uci(self,Valpo,Chile):
        print('Creando gráficos de barras y lineas para UCI')
        #aqui se hace el df extra para graficar
        DF2=Valpo[['Prom_Sem_Valp_UCI','Velocidad_Valp_UCI']].join(Chile[['Prom_Sem_Nac_UCI','Velocidad_Nac_UCI']])
        DF2['Prom_Sem_Valp_UCI'] = [round(d,2) for d in DF2['Prom_Sem_Valp_UCI']]
        DF2['Prom_Sem_Nac_UCI'] = [round(d,2) for d in DF2['Prom_Sem_Nac_UCI']]
        DF2['Velocidad_Nac_UCI'] = [round(d,2) for d in DF2['Velocidad_Nac_UCI']]
        DF2['Velocidad_Valp_UCI'] = [round(d,2) for d in DF2['Velocidad_Valp_UCI']]
        DF2=DF2.reset_index()
        DF2['dia'] = [d.date() for d in DF2['Fecha']]
        DF2.set_index('dia',inplace=True)
        #aca se grafica y da forma
        ax=DF2.plot(y=['Prom_Sem_Valp_UCI', 'Prom_Sem_Nac_UCI'], kind="bar",grid=True,
                    figsize=(9,8),label=['UCI Valparaíso','UCI Nacional'])
        ax2 = ax.twinx()
        ax2.plot(DF2['Velocidad_Valp_UCI'].values, linestyle='-', linewidth=2.0,color='gray',label='Velocidad Valparaíso')
        ax2.plot(DF2['Velocidad_Nac_UCI'].values, linestyle='-', linewidth=2.0,color='yellow',label='Velocidad Nacional')
        ax.set_title("UCI", fontsize=25)
        ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
        plt.legend(loc=1)
        plt.savefig("Barra_Linea_UCI.jpg")
        print('Gráfico Exportado!')
        
    def grafica_deads(self,Valpo,Chile):
        print('Creando gráficos de barras y lineas para Fallecidos')
        #aqui se hace el df extra para graficar
        DF2=Valpo[['Prom_Sem_Valp_Muertes','Velocidad_Valp_Muertes']].join(Chile[['Prom_Sem_Nac_Muertes','Velocidad_Nac_Muertes']])
        DF2['Prom_Sem_Valp_Muertes'] = [round(d,2) for d in DF2['Prom_Sem_Valp_Muertes']]
        DF2['Prom_Sem_Nac_Muertes'] = [round(d,2) for d in DF2['Prom_Sem_Nac_Muertes']]
        DF2['Velocidad_Nac_Muertes'] = [round(d,2) for d in DF2['Velocidad_Nac_Muertes']]
        DF2['Velocidad_Valp_Muertes'] = [round(d,2) for d in DF2['Velocidad_Valp_Muertes']]
        DF2=DF2.reset_index()
        DF2['dia'] = [d.date() for d in DF2['Fecha']]
        DF2.set_index('dia',inplace=True)
        #aca se grafica y da forma
        ax=DF2.plot(y=['Prom_Sem_Valp_Muertes', 'Prom_Sem_Nac_Muertes'], kind="bar",grid=True,
                    figsize=(9,8),label=['Fallecimientos Valparaíso','Fallecimientos Nacional'])
        ax2 = ax.twinx()
        ax2.plot(DF2['Velocidad_Valp_Muertes'].values, linestyle='-', linewidth=2.0,color='gray',label='Velocidad Valparaíso')
        ax2.plot(DF2['Velocidad_Nac_Muertes'].values, linestyle='-', linewidth=2.0,color='yellow',label='Velocidad Nacional')
        ax.set_title("Fallecimientos", fontsize=25)
        ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
        plt.legend(loc=1)
        plt.savefig("Barra_Linea_Deads.jpg")
        print('Gráfico Exportado!')

