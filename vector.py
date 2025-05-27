# /********************************************************************************************************************************
# Script: 		    vector.py
# Objetivo: 		    Codigo para processar dados em formato vetorial para analisar areas afetadas por incendios.
#                           Funções aplicadas associadas a utilização de SIG (ArcGIS Pro)
# Dados input:              Areas protegidas(ICNF); areas ardidas 2000-2023(ICNF); Areas edificadas 2018(DGT); Lugares 2021(INE)
# Dados output:		    Feature classes com dados extraidos para cada area de estudo e calculo da respetiva area de ocupacao
# Ultima atualizacao:       Março 2025, por Sandra Oliveira (Change4Fire)
# *********************************************************************************************************************************

# --------------------------------------------------------------------------------------------------------------------------------#

# Variaveis e objetos criados com este script:

##area_list         lista de feature classes na pasta de trabalho representando as areas de estudo
##protegidas        dados de input relativos a areas protegidas em Portugal Continental (ICNF 2023)
##area_proteg       dados de output para cada area de estudo, com a extracao das areas protegidas que intersectam
##ardidas           dados de input relativos a areas ardidas em Portugal Continental, entre 2000 e 2023 (ICNF 2024)
##area_ba           dados de output para cada area de estudo, com a extracao das areas ardidas que intersetam
##edificadas        dados de input relativos a areas edificadas em Portugal Continental, ano 2018 (DGT 2018)
##area_edif         dados de output para cada area de estudo, com a extracao das areas edificadas existentes dentro dos seus limites
##lugares           dados de input relativos a lugares em Portugal Continental, ano 2021 (INE 2021)
##area_lugar        dados de output para cada area de estudo, com a extracao dos lugares existentes dentro dos seus limites

# --------------------------------------------------------------------------------------------------------------------------------#

# Importar modulos necessarios
import os
import arcpy
from arcpy import *
from arcpy.sa import *

#Permitir substituição de ficheiros
arcpy.env.overwriteOutput = True

# Definir o workspace de trabalho
arcpy.env.workspace = r"C:\Users\Documents\areas_estudo"  #definir caminho respetivo para pasta de dados input
workfolder = arcpy.env.workspace                          #simplificar o caminho
print(workfolder)

# Definir lista de feature classes existentes no workfolder (cada feature class é uma area de estudo)
area_list = arcpy.ListFeatureClasses("*.shp")
# Visualizar a lista
print(area_list)

#Definir novo caminho para pasta onde guardar resultados
workfolder_d = r"C:\Users\Documents\CARAT_AREA_ESTUDO"
print (workfolder_d)

#Criar nova pasta para gravar resultados
res_folder = workfolder_d + "\\RESULTS_vetor"
print (res_folder)

#Definir dados de base - areas protegidas
protegidas = workfolder_d + "\\areas_protegidas\\areas_protegidas_PT_final.shp"
print (protegidas)

#Aplicar loop para obter dados por cada area de estudo (função:clip)
for area in area_list:
    basename, extension = os.path.splitext(area)    #dividir nome original
    area_proteg = res_folder + "\\" + basename + "_proteg.shp"  #definir caminho e criar nome diferente para novas feature classes
    print ("Clipping " + basename)
    arcpy.analysis.Clip(protegidas, area, area_proteg)  #aplicar a função para recortar dados input por cada area estudo
    print ("Clip completed for " + basename)
    #calculate area (ha) in new field
    print ("Adding new field in " + basename)                   
    arcpy.management.AddField(area_proteg, "area_prot","DOUBLE")#adicionar um campo novo na tabela de atributos
    print ("Calculating area for " + basename)
    expression = "!shape.area@HECTARES!"
    arcpy.management.CalculateField(area_proteg, "area_prot", expression, "PYTHON3")#calcular a area em ha no novo campo 
    print ("Calculate field completed for " + basename)

# Definir dados de base - areas ardidas
ardidas = workfolder_d + "\\areas_ardidas\\AA2000_2023.shp"
print (ardidas)

#Aplicar loop para obter dados por cada area de estudo (função:clip)
for area in area_list:
    basename, extension = os.path.splitext(area)
    area_ba = res_folder + "\\" + basename + "_ba.shp"
    print ("Clipping " + basename)
    arcpy.analysis.Clip(ardidas, area, area_ba)
    print ("Clip completed for " + basename)
    #calculate area (ha) in new field
    print ("Adding new field in " + basename)
    arcpy.management.AddField(area_ba, "area_ba", "DOUBLE")
    print ("Calculating area for " + basename)
    expression = "!shape.area@HECTARES!"
    arcpy.management.CalculateField(area_ba, "area_ba", expression, "PYTHON3") 
    print ("Calculate field completed for " + basename)

# Definir dados de base - areas edificadas (aglomerados)
edificadas = workfolder_d + "\\AreasEdificadas\\AreasEdificadas2018.shp"
print (edificadas)

#Aplicar loop para obter dados por cada area de estudo (função:clip)
for area in area_list:
    basename, extension = os.path.splitext(area)
    area_edif = res_folder + "\\" + basename + "_edif.shp"
    print ("Clipping " + basename)
    arcpy.analysis.Clip(edificadas, area, area_edif)
    print ("Clip completed for " + basename)
    #calculate area (ha) in new field
    print ("Adding new field in " + basename)
    arcpy.management.AddField(area_edif, "area_edif", "DOUBLE")
    print ("Calculating area for " + basename)
    expression = "!shape.area@HECTARES!"
    arcpy.management.CalculateField(area_edif, "area_edif", expression, "PYTHON3") 
    print ("Calculate field completed for " + basename)

# Definir dados de base - lugares 2021
lugares = workfolder_d + "\\LUGARES2021\\lugares2021.shp"
print (lugares)

#Aplicar loop para obter dados por cada area de estudo (função:clip)
for area in area_list:
    basename, extension = os.path.splitext(area)
    area_lugar = res_folder + "\\" + basename + "_lugar.shp"
    print ("Clipping " + basename)
    arcpy.analysis.Clip(lugares, area, area_lugar)
    print ("Clip completed for " + basename)
    #calculate area (ha) in new field
    print ("Adding new field in " + basename)
    arcpy.management.AddField(area_lugar, "area_lugar", "DOUBLE")
    print ("Calculating area for " + basename)
    expression = "!shape.area@HECTARES!"
    arcpy.management.CalculateField(area_lugar, "area_lugar", expression, "PYTHON3") 
    print ("Calculate field completed for " + basename)

