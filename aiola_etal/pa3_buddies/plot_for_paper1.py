# MFH, 200217. Adapted from 160625.
import moby2
import pylab as pl
import numpy as np
import sys, os

pl.rcParams['text.usetex'] = True

MASK_RADIUS_ARCMIN = 10.
FOV_ARCMIN = 50.

# Load your best buddy maps...
#
components = ['T', 'Q', 'U', 'Qr', 'Ur']
mapfiles = ['pa3_buddies_%s.fits' % p
            for p in components]
maps = [moby2.mapping.fits_map.spaceMap(f)
        if os.path.exists(f) else None
        for f in mapfiles]

# Promote to (1,n)...
maps = [maps]

# Load your leakage curves.
#
fits_dat = []
for ar in ['ar3']:
    fits_dat.append([])
    for label in 'EB':
        fits_dat[-1].append(moby2.util.StructDB.from_fits_table(
                '41_leakbeam_T%s.fits' % label))


sp = lambda i: pl.subplot(2,1,i+1)

pl.figure(figsize=(4,6))
pa_label = 'PA3 149 GHz'
npa = 1
ipa = 0

if 1:
    # The spectra.
    sp(1+ipa*2)
    for EB, X, kw in zip('EB', fits_dat[ipa],
                         [{'c': 'blue'},
                          {'c': 'green'}]):
        pl.plot(X['ell'], 1e3*X['leakage'], ls='solid',
                label='T%s leakage'%EB, **kw)
#        pl.plot(X['ell'], 1e3*X['residual'], ls='solid',
#                label='T%s residual'%EB, **kw)
    pl.legend(loc='upper right', fontsize=12)
    pl.xlabel('$\\ell$')
    pl.ylabel('$b_\\ell^{T\\to P}$ $(10^{-3})$')
    pl.xlim(0, 4800)
    lim = pl.ylim()
    pl.text(4500, lim[0] + (lim[1]-lim[0])*.1, pa_label,
               ha='right', va='bottom')
    # The beam maps.
    sp(ipa*2)
    mq = maps[ipa][3]
    SCALE = 1e-3
    vlims = [-2e-4, 1e-4]
    mq.imshow(data=mq.data / SCALE, units='arcmin', vmin=vlims[0]/SCALE,
              vmax=vlims[1]/SCALE,
              cmap='gray')
    mq.zoom(FOV_ARCMIN)
    pl.xlabel('X (arcmin)')
    pl.ylabel('Y (arcmin)')
    lim = pl.ylim()
    pl.text(FOV_ARCMIN*.8, -FOV_ARCMIN/2, pa_label,
               ha='right', va='bottom', color='white')
    pl.colorbar()

pl.subplots_adjust(left=.2, right=.97, top=.96)
outputm = moby2.scripting.OutputFiler(prefix='paper/')
outputm.savefig('figure_sidelobes.png', clf=False)
outputm.savefig('figure_sidelobes.eps', clf=False)
outputm.savefig('figure_sidelobes.pdf')
