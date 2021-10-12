import numpy as np
import pandas as pd

vert=pd.read_csv('/Users/banjo/home/bnjo/hood/xcorr/output/Multi_station_VERTICAL_6621swarm_output.csv')
v = vert.loc[vert['cc']>=0.7]
nort=pd.read_csv('/Users/banjo/home/bnjo/hood/xcorr/output/Multi_stationHORIZ_North_6621swarm_output.csv')
n = nort.loc[nort['cc']>=0.7]
ccs=[v,n]
df = pd.concat(ccs)
df2 = df.loc[df['evid1']!= df['evid2']]
id1 = np.unique(df2['evid1'])
id2 = df2['evid2']
# tmp = df2.loc[df2['evid1'] == id1

with open("output.txt", "a") as f:
    for i in range(len(id1)):
        tmp = df2.loc[df2['evid1'] == id1[i]]
        for ind, row in tmp.iterrows():
            eid = row[0]
            eid2 = row[1]
            hline = str('#   '+str(eid)+'   '+str(eid2)+'   0.000')
            print(hline,file=f)
            tmp2= tmp.loc[tmp['evid2'] == eid2]
            for j in range(len(tmp2)):
                sta = tmp2.sta.iloc[j]
                chn = tmp2.chn.iloc[j]
                dtt = tmp2.dt.iloc[j]
                dtt = '%6.3f' % dtt
                ccc = tmp2.cc.iloc[j]
                ccc = '%6.3f' % ccc
                if chn[2] =='Z':
                    last = 'P'
                else:
                    last = 'S'
                if len(sta)==4:
                    sline = str('    '+sta+'   '+dtt+'   '+ccc+'   '+last)
                else:
                    sline = str('     '+sta+'   '+dtt+'   '+ccc+'   '+last)
                print(sline,file=f)
