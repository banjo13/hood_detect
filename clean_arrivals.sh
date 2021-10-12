#!/bin/bash
xdir=/Users/banjo/home/bnjo/hood/xcorr/
cdir=/Users/banjo/home/bnjo/hood/util/catalogs/
odir=/Users/banjo/home/bnjo/hood/util/catalogs/

ifile1=tmp.arr.csv
ofile=arr.csv
ifile2=vimClean.txt

cp $ifile2 $cdir/tmp.kleen
cd $cdir

# awk '(NR>1){print $2,$3,$4,$5,$6,$7,$8,$9,$10}' ${ifile1} > ${ofile}
awk '(NR>1){print $2,$3,$4,$5,$7,$10}' ${ifile1} > ${ofile}

vim -s tmp.kleen ${odir}/$ofile
rm tmp.*
echo "Done"
