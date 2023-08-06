# a bokeh histogram with an additional Kernel-Density-Estimation of the data distribution
from scipy.stats.kde import gaussian_kde

def plot_histogram(data, attribute):
    measured = data[attribute]
    hist, edges = np.histogram(measured, density=True, bins=25)

    x = np.linspace(np.min(measured), np.max(measured), 100)
    pdf = gaussian_kde(measured)

    fig = figure()
    fig.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color='grey', line_color='grey')
    fig.line(x, pdf(x), line_color="black", line_width=2, alpha=0.7, line_dash='dashed')
    fig.xaxis.axis_label = attribute
    fig.yaxis.axis_label = 'P(%s)' %(attribute)
    show(fig)
    
    
plot_histogram(data, 'ATTRIBUTE')