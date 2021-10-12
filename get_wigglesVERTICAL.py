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

## ### ###WAVEFORM DOWNLOADER FOR THE EVENTS FROM THE HYPO-PARSER
## ### ###WAVEFORM DOWNLOADER FOR THE EVENTS FROM THE HYPO-PARSER
eve='/Users/banjo/home/bnjo/hood/util/catalogs/cat.csv'
arrivals='/Users/banjo/home/bnjo/hood/util/catalogs/arr.csv'
path='/Users/banjo/home/bnjo/hood/util/catalogs'
mainDir='/Users/banjo/home/bnjo/hood/data'
stafile='/Users/banjo/home/bnjo/hood/util/catalogs/stainfo.csv'
ofile = '/Users/banjo/home/bnjo/hood/util/catalogs/_2002informationVERTICAL.csv'

stations4download=["BRSP","HIYU","LSON",
                   "PALM","SHRK","TIMB","YOCR","JESE",
                   "LOCK","AUG","HOOD","TDH","VBE",
                   "VFP","VLL","VLM"]

########################
web = 'IRIS'
timelen = [10,90]
area=[45.1,45.5,-122.0,-121.5]
names = []
client = Client(web)
stadf = pd.read_csv(stafile)
stas = stadf.STA
nets = stadf.NET
evedf = pd.read_csv(eve)
sel = evedf[(evedf.LAT > area[0]) & (evedf.LAT < area[1]) & (evedf.LON > area[2]) & (evedf.LON < area[3])]
sel=sel.loc[sel['TIME']> '2002'] #just a smaller number of events to test ##
information = []
for ind, row in sel.iterrows():
    time = row.TIME
    ID = row.EVID
    lat = row.LAT
    lon = row.LON
    dep = row.DEP
    mag = row.MAG
#     print('ID:  ',ID)
    ddir = os.path.join(mainDir,str(ID))
    if not os.path.isdir(ddir):
        os.makedirs(ddir)
    arrdf=pd.read_csv(arrivals,sep="\s+",names=['EVID','STA','ARR','ABSA','PHA','MAG'])
    arrdf=arrdf.loc[arrdf['STA'].isin(stations4download)]
    arrdf=arrdf.loc[arrdf['EVID']==str(ID)]
    if stafile == None:
        stas = arrdf.STA.drop_duplicates()
    for i in range(len(stas)):
        sta = stas[i]
        net = nets[i]
        tname = os.path.join(ddir,sta+'.sac')
        if os.path.isfile(tname):
            continue
        temp = arrdf.loc[arrdf['STA'] == sta]
#         print('temp : ',temp)
#         print('station : ',sta)
        if len(temp) == 0:
            continue
        if len(temp) == 2:
            pinfo = temp[temp['PHA']=='P']
            pwave_tt = float(pinfo.ARR.iloc[0])
            origin = pinfo.ABSA.iloc[0]
            origin = utcdt(origin)
            otime = origin - pwave_tt
            starttime = origin - timelen[0]
            endtime = origin + timelen[1]
        if len(temp) == 1:
            pinfo = temp[temp['PHA']=='P']
            if len(pinfo) == 0:
                continue
            pwave_tt = float(pinfo.ARR.iloc[0])
            origin = pinfo.ABSA.iloc[0]
            origin = utcdt(origin)
            otime = origin - pwave_tt
            starttime = origin - timelen[0]
            endtime = origin + timelen[1]
        try:
            st = client.get_waveforms('*',sta,'*','HHZ,EHZ,BHZ',starttime,endtime)
        except:
            print('Failed to download waveform for event %s in station %s\n'%(ID,sta))
            continue
            print('Downloaded %d channels of %s in station %s\n'%(len(st),ID,sta))
        for tr in st:
            starttime=tr.stats.starttime
            btime = starttime - origin
            channel = str(tr.stats.channel)
            name = 'tmp.'+sta+'.'+channel+'.sac'
            name = os.path.join(ddir,name)
            names.append(name)
            information.append([name,ID,origin,pwave_tt,otime,lat,lon,dep,mag])
            tr.write(name,format='sac')

df= pd.DataFrame(information,columns =["name","ID","origin","pwave_tt","otime","lat","lon","dep","mag"])
df.to_csv(ofile,index=0)

for info in information:
    time = utcdt(info[4])
    st = obspy.read(info[0])
    for tr in st:
        starttime = tr.stats.starttime
        data = tr.stats.sac
        data.nzyear = time.year
        data.nzjday = time.julday
        data.nzhour = time.hour
        data.nzmin = time.minute
        data.nzsec = time.second
        data.nzmsec = time.microsecond/1000
        data['lovrok'] = True
        data['iztype'] = int(11)
        data['b'] = starttime-time
        data['o'] = 0
        data['nevid'] = info[1]
        evid = str(info[1])
        data['evla'] = info[5]
        data['evlo'] = info[6]
        data['evdp'] = info[7]
        data['mag'] = info[8]
        if tr.stats.channel[2] == 'Z':
            data['a'] = info[3]
        path=str(info[0][0:42])
        station = tr.stats.station
        channel = tr.stats.channel
        name = evid+"_"+station+"_"+channel+'.SAC'
        tr.write(path+str(name), format='SAC')

# # for info in information:
# #     !rm ${info[0]}






# import os
# import sys
# import glob
# import pandas as pd
# import numpy as np
#
# import obspy
# from obspy import read
# import obspy.core
# import obspy.io
# from obspy.core import UTCDateTime as utcdt
# from obspy.clients.fdsn import Client
# client = Client("IRIS")
# import matplotlib.pyplot as plt
#
# ## ### ###WAVEFORM DOWNLOADER FOR THE EVENTS FROM THE HYPO-PARSER
# ## ### ###WAVEFORM DOWNLOADER FOR THE EVENTS FROM THE HYPO-PARSER
# eve='/Users/banjo/home/bnjo/hood/util/catalogs/cat.csv'
# arrivals='/Users/banjo/home/bnjo/hood/util/catalogs/arr.csv'
# path='/Users/banjo/home/bnjo/hood/util/catalogs'
# mainDir='/Users/banjo/home/bnjo/hood/data'
# stafile='/Users/banjo/home/bnjo/hood/util/catalogs/stainfo.csv'
#
# ofile = '/Users/banjo/home/bnjo/hood/util/catalogs/_informationVERTICAL.csv'
#
# ########################
# web = 'IRIS'
# timelen = [10,90]
# area=[45.1,45.5,-122.0,-121.5]
# names = []
# client = Client(web)
# stadf = pd.read_csv(stafile)
# stas = stadf.STA
# nets = stadf.NET
# evedf = pd.read_csv(eve)
# sel = evedf[(evedf.LAT > area[0]) & (evedf.LAT < area[1]) & (evedf.LON > area[2]) & (evedf.LON < area[3])]
# information = []
# for ind, row in sel.iterrows():
#     time = row.TIME
#     ID = row.EVID
#     # print('ID:  ',ID)
#     ddir = os.path.join(mainDir,str(ID))
#     if not os.path.isdir(ddir):
#         os.makedirs(ddir)
#     arrdf=pd.read_csv(arrivals,sep="\s+",names=['EVID','STA','ARR','ABSA','PHA','MAG'])
#     arrdf=arrdf.loc[arrdf['EVID']==ID]
#     if stafile == None:
#         stas = arrdf.STA.drop_duplicates()
#     for i in range(len(stas)):
#         sta = stas[i]
#         net = nets[i]
#         tname = os.path.join(ddir,sta+'.sac')
#         if os.path.isfile(tname):
#             continue
#         temp = arrdf.loc[arrdf['STA'] == sta]
#         if len(temp) == 0:
#             continue
#         if len(temp) == 2:
#             pinfo = temp[temp['PHA']=='P']
#             pwave_tt = float(pinfo.ARR.iloc[0])
#             origin = pinfo.ABSA.iloc[0]
#             origin = utcdt(origin)
#             otime = origin - pwave_tt
#             starttime = origin - timelen[0]
#             endtime = origin + timelen[1]
#         if len(temp) == 1:
#             pinfo = temp[temp['PHA']=='P']
#             if len(pinfo) == 0:
#                 continue
#             pwave_tt = float(pinfo.ARR.iloc[0])
#             origin = pinfo.ABSA.iloc[0]
#             origin = utcdt(origin)
#             otime = origin - pwave_tt
#             starttime = origin - timelen[0]
#             endtime = origin + timelen[1]
#         lat = row.LAT
#         lon = row.LON
#         dep = row.DEP
#         mag = row.MAG
#         try:
#             st = client.get_waveforms('*',sta,'*','HHZ,EHZ,BHZ',starttime,endtime)
#         except:
#             print('Failed to download waveform for event %s in station %s\n'%(ID,sta))
#             continue
#             print('Downloaded %d channels of %s in station %s\n'%(len(st),ID,sta))
#         for tr in st:
#             starttime=tr.stats.starttime
#             btime = starttime - origin
#             channel = str(tr.stats.channel)
#             name = 'tmp.'+sta+'.'+channel+'.sac'
#             # name =
#             name = os.path.join(ddir,name)
#             names.append(name)
#             information.append([name,ID,origin,pwave_tt,otime,lat,lon,dep,mag])
#             tr.write(name,format='sac')
#
# df= pd.DataFrame(information,columns =["name","ID","origin","pwave_tt","otime","lat","lon","dep","mag"])
# df.to_csv(ofile,index=0)
#
# for info in information:
#     time = utcdt(info[4])
#     st = obspy.read(info[0])
#     for tr in st:
#         starttime = tr.stats.starttime
#         data = tr.stats.sac
#         data.nzyear = time.year
#         data.nzjday = time.julday
#         data.nzhour = time.hour
#         data.nzmin = time.minute
#         data.nzsec = time.second
#         data.nzmsec = time.microsecond/1000
#         data['lovrok'] = True
#         data['iztype'] = int(11)
#         data['b'] = starttime-time
#         data['o'] = 0
#         data['nevid'] = info[1]
#         evid = str(info[1])
#         data['evla'] = info[5]
#         data['evlo'] = info[6]
#         data['evdp'] = info[7]
#         data['mag'] = info[8]
#         if tr.stats.channel[2] == 'Z':
#             data['a'] = info[3]
#         path=str(info[0][0:42])
#         station = tr.stats.station
#         channel = tr.stats.channel
#         name = evid+"_"+station+"_"+channel+'.SAC'
#         tr.write(path+str(name), format='SAC')
#
# # for info in information:
# #     !rm ${info[0]}
