import numpy as np
import pandas as pd
import obspy
import obspy.core
from obspy import UTCDateTime as utcdt
from obspy.signal.cross_correlation import xcorr_pick_correction

path1='/Users/banjo/home/bnjo/hood/data/*'
path2='/Users/banjo/home/bnjo/hood/data/*'
opath='/Users/banjo/home/bnjo/hood/xcorr/'
ofile = '_6621swarmVLLZ_output.csv'
st1=obspy.read(path1+'/*VLL_*Z.SAC')
st2=obspy.read(path2+'/*VLL_*Z.SAC')

for tr1 in st1:
    stats = tr1.stats
    sac = tr1.stats.sac
    b = (sac['b'])*-1
    t1 = sac['t1']
    evid = sac['nevid']
    starttime = stats.starttime
    stats['p_time'] = starttime + b + t1
    stats['o_time'] = starttime + b
    stats['evid'] = evid



for tr2 in st2:
  stats = tr2.stats
  sac = tr2.stats.sac
  b = (sac['b'])*-1
  t1 = sac['t1']
  evid = sac['nevid']
  starttime = stats.starttime
  stats['p_time'] = starttime + b + t1
  stats['o_time'] = starttime + b
  stats['evid'] = evid

output = []
for tr1 in st1:
  for tr2 in st2:
  #         tr1=st1[0]
    evid1 = tr1.stats['evid']
    evid2 = tr2.stats['evid']
    station = str(tr1.stats.station)
    channel = str(tr1.stats.channel)
    name = station+'\s'+channel
    try:
        xcorr=xcorr_pick_correction(
            tr1.stats.p_time, tr1,
            tr2.stats.p_time, tr2,
            t_before=0.05,
            t_after=0.20,
            cc_maxlag=0.10,
            filter="bandpass",
            filter_options={'freqmin':2, 'freqmax':15},
            plot=False,
            filename=None)
        output.append([evid1,evid2,station,channel,xcorr[0],xcorr[1]])
    except:
        print("No Go: ", evid1, evid2)
        continue
df = pd.DataFrame(output,columns=['evid1','evid2','sta','chn','dt','cc'])
df.to_csv(opath+ofile,index=0)
