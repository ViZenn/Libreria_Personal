import importa_procesa_BDs as Bases
import AUX_contagios as AUX

print('****INICIANDO PROGRAMA DE DESCARGA BDs CONTAGIOS ****')
BD=Bases.BDs_Contagios()
BD.procesa_base()

Casos_Ch=BD.casos_agrupados()
UCI_Ch=BD.uci_agrupados()
Deads_Ch=BD.deads_agrupados()
Casos_W=BD.casos_mundo()
Deads_W=BD.deads_mundo()

print('****PROCESANDO Y EXPORTANDO BDs CONTAGIOS ****')

F=AUX.AUX_Contagios()
F.Valpo(Casos_Ch,UCI_Ch,Deads_Ch).to_excel('Valpo_nuevo.xlsx')
F.Chile(Casos_Ch,UCI_Ch,Deads_Ch).to_excel('Chile_nuevo.xlsx')
F.informe_pais(Casos_W,Deads_W,'Argentina').to_excel('Argentina.xlsx')
F.informe_pais(Casos_W,Deads_W,'Colombia').to_excel('Colombia.xlsx')
F.informe_pais(Casos_W,Deads_W,'Haiti').to_excel('Haiti.xlsx')
F.informe_pais(Casos_W,Deads_W,'Peru').to_excel('Peru.xlsx')
F.informe_pais(Casos_W,Deads_W,'United States').to_excel('USA.xlsx')
F.informe_pais(Casos_W,Deads_W,'Venezuela').to_excel('Venezuela.xlsx')

print('**** BDs CONTAGIOS PROCESADAS Y EXPORTADAS!****')

print('****CREANDO Y EXPORTANDO GRAFICOS BDs CONTAGIOS ****')

F.grafica_casos(F.Valpo(Casos_Ch,UCI_Ch,Deads_Ch),F.Chile(Casos_Ch,UCI_Ch,Deads_Ch))
F.grafica_uci(F.Valpo(Casos_Ch,UCI_Ch,Deads_Ch),F.Chile(Casos_Ch,UCI_Ch,Deads_Ch))
F.grafica_deads(F.Valpo(Casos_Ch,UCI_Ch,Deads_Ch),F.Chile(Casos_Ch,UCI_Ch,Deads_Ch))