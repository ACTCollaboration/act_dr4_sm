import numpy as np, glob
from pixell import enmap, utils
idir = "/home/r/rbond/sigurdkn/project/actpol/articles/dr3/act"
shape, wcs = enmap.read_map_geometry(idir + "/s16_cmb_pa2_f150_nohwp_night_3pass_2way_coadd_ivar_gainfix.fits")
dtype = np.float32
down  = 20

for ftag in ["f090","f150"]:
	ifiles = sorted(glob.glob(idir + "/*%s*3pass*coadd*ivar_gainfix.fits" % ftag))
	omap   = enmap.zeros(shape[-2:], wcs, dtype)
	for ifile in ifiles:
		print("Reading %s" % ifile)
		m = enmap.read_map(ifile).preflat[0]
		omap.insert(m, op=np.ndarray.__iadd__)
	ofile = "ivar_tot_%s_small.fits" % (ftag)
	print("Converting")
	omap    = enmap.downgrade(omap, down)*down**2
	pixarea = omap.pixsizemap()/utils.arcmin**2
	omap   /= pixarea
	print("Writing %s" % ofile)
	enmap.write_map(ofile, omap)
