import os
import sys
import glob
import pandas as pd
import numpy as np

import obspy
from obspy import read
import obspy.core
import obspy.io
from obspy.core import UTCDateTime as utcdt
from obspy.clients.fdsn import Client
client = Client("IRIS")
import matplotlib.pyplot as plt

## ### Hypoinverse file parser
from obspy import UTCDateTime
path='/Users/banjo/home/bnjo/hood/util/phaseFiles/'
# path = '/Users/banjo/home/bnjo/hood/util/phaseFiles/prelim_catalog_and_arrivals/'
opath='/Users/banjo/home/bnjo/hood/util/catalogs'
ofile1='/tmp.arr.csv'
# ofile1='/tmp.arr.csv'
ofile2= '/cat.csv'
# ofile2= '/test_swarm.csv'
ofile3='/stainfo.csv'
# ofile3='/test_swarm_stainfo.csv'
ofile4='/arrinfo.csv'
# ofile4='/test_swarm_arrinfo.csv'

ifile='HOODmin6.hypo'
#ifile='6621swarm_HOOD.hypo'
# ifile='hood.hypo'

datum=0
def readHypo2000(path,ifile,datum):

    """
    Parameters:
    path: str, path that points to the directory where the hypoinverse file is located.
        Also where the output will be placed
    ifile: str, name of the hypoinverse file
    datum: float, value to adjust the event depth, default is 0 means that the depth is relative to sea level

    Return:
    A list: [eveinfo, stainfos]
    eveinfo: Dataframe that contain event infomation
    stainfos: Dataframe that contain station information
    """
    os.chdir(path)
    ID=1
    i=1
    column = ['ID','TIME','LAT','LON','DEP','MAG','MTYPE','EH','EZ','RMS','EVID']
    stacol = ['NET','STA','CHAN']
    eveinfo = pd.DataFrame(columns=column)
    nets = []
    stas = []
    chan =[]
    stainfo = ['EVID','STA','ARR','ABSA','WEI','PHA','MOT','ON','MAG']
    tempsta = pd.DataFrame(columns = stainfo)
    arrinfo = []
    with open(ifile,'r') as fp:
        for line in fp.readlines():
            i=i+1
            if len(line) == 180:
                year = line[0:4]
                month = line[4:6]
                day = line[6:8]
                hour = line[8:10]
                minu = line[10:12]
                sec = line[12:16][:-2]+'.'+line[12:16][-2:]
                ddir = year+'.'+month+'.'+day+'.'+hour+'.'+minu+'.'+line[12:16][:-2]
                EVID= line[136:146].strip()
                time = year+'-'+month+'-'+day+'T'+hour+':'+minu+':'+sec
                time = UTCDateTime(time)
                lat = float(line[16:18]) + float(line[19:23][:-2]+'.'+line[19:23][-2:].replace(' ','0'))/60.0
                lon = -(float(line[23:26]) + float(line[27:31][:-2]+'.'+line[27:31][-2:].replace(' ','0'))/60.0)
                dep = line[31:36]
                if dep[-2]=='-':
                    dep = dep[:-1]+'.0'+dep[-1:]
                else:
                    dep = (dep[:-2]+'.'+dep[-2:].replace(' ','0'))
                dep = float(dep)+datum
                rms = float((line[48:52][:-2]+'.'+line[48:52][-2:]).replace(' ','0'))
                eh = float((line[85:89][:-2]+'.'+line[85:89][-2:]).replace(' ','0'))
                ez = float((line[89:93][:-2]+'.'+line[89:93][-2:]).replace(' ','0'))
                mc = line[70:73].strip()
                mtype = line[122]
                if len(mc) == 2:
                     if mc[-1]== '.':
                            mc = mc[0:1]
                if len(mc) == 3:
                     if mc[-1]== '.':
                            mc = mc[0:2]
                if len(mc)!= 0 and mc[0]=='-':
                    mag = float(mc[:2]+'.'+mc[-1])
                elif len(mc)!=0 and mc[0]!='-':
                    mag = float(mc[:-2]+'.'+mc[-2:])
                else:
                    mag = -5 #coda magnitude
                newRow = {'ID':int(ID),'TIME':time,'LAT':lat,'LON':lon,'DEP':dep,
                          'MAG':mag,'MTYPE':mtype,'EH':eh,'EZ':ez,
                          'RMS':rms,'EVID':EVID,'DIR':ddir}
                eveinfo = eveinfo.append(newRow,ignore_index=True)
                tempsta = tempsta.sort_values(by='ARR')
                arrinfo.append(tempsta)
                tempsta = pd.DataFrame(columns = stainfo)
                ID=ID+1
            elif len(line) == 121 or len(line)==120:
                sta = line[:5].strip()
                if sta not in stas:
                    stas.append(sta)
                    nets.append(line[5:7].strip())
                    chan.append(line[9:12])

                #pull out the P phase
                pha = line[14]
                mot = line[15]
                onset = line[13]
                if pha != ' ' and (line[11] == 'Z' or line[11] == '3'):
                    arryear = line[17:21]
                    arrmonth = line[21:23]
                    arrday = line[23:25]
                    arrhour = line[25:27]
                    arrmin = line[27:29]
                    arrsec = (line[30:34][:-2]+'.'+line[30:34][-2:]).replace(' ','0')
                    if float(arrsec) >= 60.0:
                        arrsec = float(arrsec)-60.0
                        arrtime = arryear+'-'+arrmonth+'-'+arrday+'T'+arrhour+':'+arrmin+':'+str(arrsec)
                        arrtime = UTCDateTime(arrtime)+60.0
                    else:
                        arrtime = arryear+'-'+arrmonth+'-'+arrday+'T'+arrhour+':'+arrmin+':'+arrsec
                        arrtime = UTCDateTime(arrtime)
                    PTT = arrtime - time
                    pweight = int(line[16])
                    rpw = pweight
                    # newStap = {'EVID':EVID,'STA':sta,'WEI':rpw,'ARR':PTT,'PHA':pha,'ABSA':arrtime,'MOT':mot,'ON':onset,'MAG':mag}
                    newStap = {'EVID':EVID,'STA':sta,'ARR':PTT,'ABSA':arrtime,'PHA':pha,'MAG':mag}

                    tempsta = tempsta.append(newStap,ignore_index=True)


                else:
                     print ('Not avaliable P phase, not use in here')
                spha = line[47]
                if spha == 'S':
                    arryear = line[17:21]
                    arrmonth = line[21:23]
                    arrday = line[23:25]
                    arrhour = line[25:27]
                    arrmin = line[27:29]
                    arrsec = (line[42:46][:-2]+'.'+line[42:46][-2:]).replace(' ','0')
                    if float(arrsec) >= 60:
                        arrsec = float(arrsec)-60.0
                        arrtime = arryear+'-'+arrmonth+'-'+arrday+'T'+arrhour+':'+arrmin+':'+str(arrsec)
                        arrtime = UTCDateTime(arrtime)+60.0
                    else:
                        arrtime = arryear+'-'+arrmonth+'-'+arrday+'T'+arrhour+':'+arrmin+':'+arrsec
                        arrtime = UTCDateTime(arrtime)
                    STT = arrtime - time
                    if STT < 0.0:
                        print ("i-1")
                        sys.exit('origin time %s and arrival time %s'%(time,arrtime))
                    swei = int(line[49])
                    rsw = swei
                    newStas = {'EVID':EVID,'STA':sta,'ARR':STT,'ABSA':arrtime,'PHA':spha,'MAG':mag,}
                    tempsta = tempsta.append(newStas,ignore_index=True)

            else:
                print ("End line for eq. %s: %d'%(EVID,i-1)")

    arrinfo.append(tempsta)

    arrinfo.pop(0)
    arrdf = pd.DataFrame(arrinfo)
    # arrdf.to_csv(opath+'/6621swarm_arr.csv',index = 0)
    arrdf.to_csv(opath+ofile1,index = 0)

    eveinfo['ARR']=arrinfo
    stainfos = pd.DataFrame(np.transpose([nets,stas,chan]),columns=stacol)
    print()
    return [eveinfo,stainfos,arrdf]

cat,stainfo,arrinfo = readHypo2000(path,ifile,datum)

#   cat.to_pickle('bluffdale.pkl') #Pickle if it's very large

# cat.to_csv(opath+'/6621swarm.csv',index = 0)
cat.to_csv(opath+ofile2,index = 0)

# stainfo.to_csv(opath+'/6621swarm_stainfo.csv',index=0)
stainfo.to_csv(opath+ofile3,index=0)

# # arrinfo.to_csv(opath+'/6621swarm_arrinfo.csv',index=0)
# arrinfo.to_csv(opath+ofile4,index=0)
