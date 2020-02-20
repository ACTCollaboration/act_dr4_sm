import numpy as np
from pixell import enmap, utils, enplot, colorize

def nonan(a):
	res = a.copy()
	res[~np.isfinite(res)]=0
	return res

#cmap       = "0:800000,0.33:ff0000,0.66:ff00ff,1:0000ff"
cmap       = colorize.schemes["planck"].reverse()
dust       = enmap.read_map("planck_353_small.fits")
ivar_f150  = enmap.read_map("ivar_tot_f150_small.fits")
ivar_f090  = enmap.read_map("ivar_tot_f090_small.fits")
footprint  = enmap.read_map("footprints.fits")*1.0

with utils.nowarn():
	dust_layers = enplot.plot(dust, ticks=10, layers=True, color="gray", reverse_color=False, min=0, max=1e4, slice="[0]")
	foot_layers = enplot.plot(footprint, ticks=10, layers=True, color="0:ff00ff40,1:ff00ff40", mask=0, min=0)

	f150_layers = enplot.plot(nonan(np.log10(ivar_f150**-0.5)), ticks=10, min=np.log10(7.5), max=np.log10(101), layers=True, contours="0.903:0.1", contour_color=cmap, contour_width=2, no_image=True, annotate="annot_f150.txt")
	enplot.write("depth_map_f150.png", enplot.merge_plots(dust_layers[:1]+foot_layers[:1]+f150_layers))

	f090_layers = enplot.plot(nonan(np.log10(ivar_f090**-0.5)), ticks=10, min=np.log10(7.5), max=np.log10(101), layers=True, contours="0.903:0.1", contour_color=cmap, contour_width=2, no_image=True, annotate="annot_f090.txt")
	enplot.write("depth_map_f090.png", enplot.merge_plots(dust_layers[:1]+foot_layers[:1]+f090_layers))
