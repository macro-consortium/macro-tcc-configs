### Script to remove extreme dec targets from PointXP script. Will run through the target list, find AltAz coordinates, and then convert to RA Dec.
#  If the Dec is greater than maxdec, the target will be removed from the list.

import os
from astropy.coordinates import EarthLocation,SkyCoord
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import AltAz, Angle, ICRS
from pathlib import Path

# set the location of the observatory
observing_location = EarthLocation(lat=31.66 * u.deg, lon=-110.6 * u.deg, height=1.5 * u.km)
observing_time = Time('2020-07-02 12:00:00')

# Read in the target list
infile = Path(r'C:\Users\MACRO\Documents\Sidereal Technology\STI\PointXPRun.Script')
outfile = infile.parent / (infile.stem + '_edited.Script')
maxdec = 75
lines = infile.open().read().splitlines()
outlines = [lines[0]]

n=1
kicks = 0
for i in range(1,len(lines),6):
    group = lines[i:i+6]
    cmd, az, alt = group[0].split()


    if cmd != 'SlewAltAz':
        exit("Barf")
    dd, mm, ss = alt.split(':')
    altdeg = Angle(f'{dd}d{mm}m{ss}s')
    dd, mm, ss = az.split(':')
    azdeg = Angle(f'{dd}d{mm}m{ss}s')
    altaz = AltAz(az=azdeg, alt=altdeg, location=observing_location, obstime=observing_time)

    # convert to RA Dec
    radec = altaz.transform_to(ICRS())
    print(f"Alt: {alt}   Az: {az}  --> dec {radec.dec.degree} degrees", end=' ')
    if radec.dec.degree <= maxdec:
        outlines.extend(group)
        print()
    else:
        print(f" --> kicked out #{n}")
        kicks += 1
    n += 1

outfile.write_text('\n'.join(outlines))
print(f"Kicked {kicks} out of {n-1} targets")

