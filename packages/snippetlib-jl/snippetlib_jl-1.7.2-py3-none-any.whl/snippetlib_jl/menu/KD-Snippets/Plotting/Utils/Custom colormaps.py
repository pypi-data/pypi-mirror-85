# three examples of custom colormaps
# 1 and 2 are highly non linear colormap (and its reverse)
# 3 is a transparent->blue colormap

def show_colormap(cmap):
    im = np.outer(np.ones(10), np.arange(100))
    fig, ax = plt.subplots(1, figsize=(6, 1.5), subplot_kw=dict(xticks=[], yticks=[]))
    fig.subplots_adjust(hspace=0.1)
    ax.imshow(im, cmap=cmap)

# define a colormap that has 90% greyscale
colors1 = plt.cm.binary(np.linspace(0., 1, 922))
colors2 = plt.cm.gnuplot2(np.linspace(0, 0.9, 102))
gecko   = plt.matplotlib.colors.LinearSegmentedColormap.from_list('gecko', np.vstack((colors1, colors2)))
gecko_r = plt.matplotlib.colors.LinearSegmentedColormap.from_list('gecko_r', np.vstack((colors2[::-1], colors1[::-1])))


transpatent_to_blue = plt.cm.get_cmap('Blues')
transpatent_to_blue._init()
alphas = np.abs(np.linspace(0.0, 1.0, transpatent_to_blue.N))
transpatent_to_blue._lut[:-3,-1] = alphas


show_colormap(gecko)
show_colormap(gecko_r)
show_colormap(transpatent_to_blue)