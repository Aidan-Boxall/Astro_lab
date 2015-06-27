# Astronomical Image Processing
# David Christopher Ragusa + Aidan Boxall

import cPickle

s=4
col1=12+s
col2=7+s
col3=10+s
col4=12+s
col5=10+s
col6=16+s

with open('mosaiccatalog.pkl', 'rb') as outfile:
    catalog=cPickle.load(outfile)
f=open('catalog.txt','w')
f.write('Centre'.rjust(col1)+'Radius'.rjust(col2)+'Count'.rjust(col3)+'Count Error'.rjust(col4)+'Magnitude'.rjust(col5)+'Magnitude Error'.rjust(col6)+'\n')
for index, item in enumerate(catalog):
    f.write(repr(item['centre']).rjust(col1)+repr(item['radius']).rjust(col2)+repr(int(item['avcount'])).rjust(col3)+repr(int(item['avcount']**0.5))[:6].rjust(col4)+repr(round(item['mag'],2)).rjust(col5)+repr(round(item['errormag'],2)).rjust(col6)+'\n')
f.close()