# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 18:33:36 2024

@author: isaacfoster
"""

import pandas as pd
import time

def gmt0001_ImportGMAT_Textfile(filepath,
                                delimiter = None):
    
    if delimiter == None:
        file = pd.read_csv(filepath)
    else:
        file = pd.read_csv(filepath,delimiter=delimiter)
    return file

def gmt0002_InspectColumns(columns):
    
    strings = []
    objects = []
    variables = []
    for column in columns:
        string = column.split('.')
        strings.append(string) 
        objects.append(string[0])
        if len(string) == 3:
            variable = string[1]+'.'+string[2]
            variables.append(variable)
        else:
            variables.append(string[1])
    
    myset = set(objects)
    objects = list(myset)
    
    return objects,variables

def gmt0003_GetPositionVectors(positions):
    objects,variables = gmt0002_InspectColumns(positions.columns)
    
def gmt0004_ExtractTime(dataframe):
    if dataframe.filter(regex='UTCGregorian') is not None:
        UTCGregorian = dataframe.filter(regex='UTCGregorian')
    
    if dataframe.filter(regex='UTCModJulian') is not None:
        UTCModJulian = dataframe.filter(regex='UTCModJulian')
        
    if dataframe.filter(regex='ElapsedSecs') is not None:
        ElapsedSecs = dataframe.filter(regex='ElapsedSecs')
        
    unix = gmt0005_Convert_GMAT_UTCModJulian_to_unix(UTCModJulian)
    unix.columns=['timestamp']
        
    return unix

def gmt0005_Convert_GMAT_UTCModJulian_to_unix(UTCModJulian):
    return (UTCModJulian + 2430000.0 - 2440587.5)*86400
            
def gmt0006_Convert_unix_to_datetime(unix):
    return time.strftime("%d %b %Y %H:%M:%S",time.gmtime(unix))
    
def gmt0007_Convert_unix_df_to_datetime(unix_dataframe):
    length = len(unix_dataframe)
    dates = []
    for i in range(0,length):
        dates.append(gmt0006_Convert_unix_to_datetime(unix_dataframe.iloc[i,0]))
    
    return dates

def gmt0101_ExtractBodyData(dataframe,body):
    data = dataframe.filter(regex=body)
    return data

def gmt0102_ExtractPositionData(dataframe):
    x = dataframe.filter(regex='X')
    y = dataframe.filter(regex='Y')
    z = dataframe.filter(regex='Z')
    
    positions = pd.concat([x,y,z],axis=1)
    return positions

def gmt0103_ImportEclipseFile(filepath):
    file = pd.read_table(filepath)
    
    lines = []
    for line in file.iloc[:,0]:
        lines.append(list(filter(None,file.iloc[2,0].split('  '))))
        
    df = pd.DataFrame(lines,columns=['Start Time','Stop Time','Duration','Occ Body','Type','Event Number','Duration'])
    return df