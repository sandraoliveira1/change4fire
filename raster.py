# /********************************************************************************************************************************
# Script: 		    raster.py
# Objetivo: 		    Codigo para processar dados em formato matricial para analisar areas afetadas por incendios.
#                           Funções aplicadas associadas a utilização de SIG (ArcGIS Pro)
# Dados input:              Areas protegidas(ICNF); areas ardidas 2000-2023(ICNF); Areas edificadas 2018(DGT); Lugares 2021(INE)
# Dados output:		    Raster com dados extraidos para cada area de estudo e calculo da respetiva area de ocupacao
# Ultima atualizacao:       Março 2025, por Sandra Oliveira (Change4Fire)
# *********************************************************************************************************************************

# --------------------------------------------------------------------------------------------------------------------------------#

# Variaveis e objetos criados com este script:

##area_list         lista de feature classes na pasta de trabalho representando as areas de estudo
##cos               dados de input relativos a ocupação e uso do solo 2023 em Portugal Continental (CosSIM DGT, 2023)
##area_cos          dados de output para cada area de estudo, com a extração das categorias de ocupaçao do solo dentro dos seus limites
##perigosidade      dados de input relativos a perigosidade estrutural 2020-30 em Portugal Continental (ICNF, 2020)
##area_perig        dados de output para cada area de estudo, com a extração das classes de perigosidade dentro dos seus limites
##wui               dados de input relativos a interface urbano-rural(WUI)para Portugal Continental (baseado em Barbosa et al., 2024)
##area_wui          dados de output para cada area de estudo, com a extração das classes de wui dentro dos seus limites

# --------------------------------------------------------------------------------------------------------------------------------#

# Importar modulos necessarios
import os
import arcpy
from arcpy import *
from arcpy.sa import *

#Permitir substituição de ficheiros
arcpy.env.overwriteOutput = True

# Definir o workspace de trabalho
arcpy.env.workspace = r"C:\Users\Documents\areas_estudo"    #definir caminho respetivo para pasta de dados input
workfolder = arcpy.env.workspace                            #simplificar o caminho
print(workfolder)

# Definir lista de feature classes existentes no workfolder (cada feature class é uma area de estudo)
area_list = arcpy.ListFeatureClasses("*.shp")
# Visualizar a lista
print(area_list)

#Definir novo caminho para pasta onde guardar resultados
workfolder_d = r"C:\Users\Documents\CARAT_AREA_ESTUDO"
print (workfolder_d)

#Criar nova pasta para gravar resultados
res_folder = workfolder_d + "\\RESULTS_raster"
print (res_folder)

if not os.path.exists(res_folder):
    os.makedirs(res_folder)
else:
    print ("Path " + res_folder + " already exists")

# Definir dados de base - COS2023
cos = workfolder_d + "\\COS2023\\COS2023.tif"
print(cos)

#Aplicar loop para obter dados por cada area de estudo (função:extractbymask)
for area in area_list:
    basename, extension = os.path.splitext(area)            #dividir nome original
    area_cos = res_folder + "\\" + basename + "_cos.tif"    #definir caminho e criar nome diferente para novos raster
    print (area_cos)
    print ("Extracting by mask " + basename)
    arcpy.gp.ExtractByMask_sa(cos, area, area_cos)          #aplicar a função para extrair dados input por cada area estudo
    print ("Extract by Mask completed for " + basename)
    #calcular % por classe de ocupação do solo no novo campo
    print ("Adding new field in " + basename)
    arcpy.management.AddField(area_cos, "perc", "DOUBLE")   #adicionar um campo novo na tabela de atributos
    print ("Calculating sum of cells in COUNT field for " + basename)   #calcular somatório de linhas para posterior calculo de %
    sum_total = 0
    with arcpy.da.SearchCursor(area_cos, "COUNT") as cursor:
        for row in cursor:
            sum_total = sum_total + row[0]
    expression = f"(!COUNT!/{sum_total})*100"               #definir expressão para calcular % de cada classe de ocupação do solo
    print ("Calculating % for " + basename)
    arcpy.management.CalculateField(area_cos, "perc", expression, "PYTHON3") #calcular % de cada classe de ocupação do solo para cada área de estudo
    print ("Calculate field completed for " + basename)

# Definir dados de base - perigosidade
perigosidade = workfolder_d + "\\perigosidade\\perigosidade_estrutural_2020_2030.tif"
print(perigosidade)

#Run loop to ExtractByMask info by study area
for area in area_list:
    basename, extension = os.path.splitext(area)
    area_perig = res_folder + "\\" + basename + "_perig.tif"
    print (area_perig)
    print ("Extracting by mask " + basename)
    arcpy.gp.ExtractByMask_sa(perigosidade, area, area_perig)
    print ("Extract by Mask completed for " + basename)
    #calcular % por classe de perigosidade no novo campo
    print ("Adding new field in " + basename)
    arcpy.management.AddField(area_perig, "perc", "DOUBLE")
    print ("Calculating sum of cells in COUNT field for " + basename)
    sum_total = 0
    with arcpy.da.SearchCursor(area_perig, "COUNT") as cursor:
        for row in cursor:
            sum_total = sum_total + row[0]
    expression = f"(!COUNT!/{sum_total})*100"
    print ("Calculating % for " + basename)
    arcpy.management.CalculateField(area_perig, "perc", expression, "PYTHON3") 
    print ("Calculate field completed for " + basename)

# Definir dados de base - WUI (BB)
wui = workfolder_d + "\\WUI_PT\\WUI_PT.tif"
print (wui)

#Run loop to ExtractByMask info by study area
for area in area_list:
    basename, extension = os.path.splitext(area)
    area_wui = res_folder + "\\" + basename + "_wui.tif"
    print (area_wui)
    print ("Extracting by mask " + basename)
    arcpy.gp.ExtractByMask_sa(wui, area, area_wui)
    print ("Extract by Mask completed for " + basename)
    #calcular % wui no novo campo
    print ("Adding new field in " + basename)
    arcpy.management.AddField(area_wui, "perc", "DOUBLE")
    print ("Calculating sum of cells in COUNT field for " + basename)
    sum_total = 0
    with arcpy.da.SearchCursor(area_wui, "COUNT") as cursor:
        for row in cursor:
            sum_total = sum_total + row[0]
    expression = f"(!COUNT!/{sum_total})*100"
    print ("Calculating % for " + basename)
    arcpy.management.CalculateField(area_wui, "perc", expression, "PYTHON3") 
    print ("Calculate field completed for " + basename)
