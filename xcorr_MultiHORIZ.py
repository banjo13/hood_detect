import numpy as np
import pandas as pd
import obspy
import obspy.core
from obspy import UTCDateTime as utcdt
from obspy.signal.cross_correlation import xcorr_pick_correction

path1='/Users/banjo/home/bnjo/hood/data/*'
path2='/Users/banjo/home/bnjo/hood/data/*'
opath='/Users/banjo/home/bnjo/hood/xcorr/'
# ofile = 'Multi_stationHORIZ_East_6621swarm_output.csv'
ofile = 'Multi_stationHORIZ_North_6621swarm_output.csv'



df = pd.read_csv('/Users/banjo/home/bnjo/hood/util/catalogs/test_informationHORIZONTAL.csv')
names = df['name']
stations=[]
for name in names:
#     print(len(name))
    if len(name) == 57:
        sta = name[46:49]
        # print(sta)
        stations.append(sta)
    else:
        sta = name[46:50]
        # print(sta)
        stations.append(sta)

stations=np.unique(stations)

# stations = ['HOOD','TIMB','LSON']
outputs=[]

# Read the waveforms for correlation.

for station in stations:
    st1=obspy.read(path1+'/*' +station+'_*N.SAC')
    st2=obspy.read(path2+'/*' +station+'_*N.SAC')

# set the header information for the correlation; ie., timing information.

    for tr1 in st1:
        stats = tr1.stats
        sac = tr1.stats.sac
        b = (sac['b'])*-1
        tt = sac['t1']
        evid = sac['nevid']
        starttime = stats.starttime
        stats['s_time'] = starttime + b + tt
        stats['o_time'] = starttime + b
        stats['evid'] = evid

        for tr2 in st2:
            stats = tr2.stats
            sac = tr2.stats.sac
            b = (sac['b'])*-1
            tt = sac['t1']
            evid = sac['nevid']
            starttime = stats.starttime
            stats['s_time'] = starttime + b + tt
            stats['o_time'] = starttime + b
            stats['evid'] = evid

# Gather Name information for the csv at the end.
            evid1 = tr1.stats['evid']
            evid2 = tr2.stats['evid']
            station = str(tr2.stats.station)
            channel = str(tr2.stats.channel)

# Correlate all of the events.
            try:
                xcorr=xcorr_pick_correction(
                    tr1.stats.s_time, tr1,
                    tr2.stats.s_time, tr2,
                    t_before=0.20,
                    t_after=2.50,
                    cc_maxlag=0.010,
                    filter="bandpass",
                    filter_options={'freqmin': 2, 'freqmax': 15},
                    plot=False,
                    filename=None)
                outputs.append([evid1,evid2,station,channel,xcorr[0],xcorr[1]])
            except:
                print("No Go: ", evid1, evid2,station,channel)
                continue


df = pd.DataFrame(outputs,columns=[['evid1','evid2','sta','chn','dt','cc']])
df.to_csv(opath+ofile,index=0)
