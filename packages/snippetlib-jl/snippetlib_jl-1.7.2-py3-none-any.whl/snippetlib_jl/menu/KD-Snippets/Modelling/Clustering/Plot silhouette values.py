# plot the silhouette plot of the cluster assignments. 
# NOTE: THIS IS NOP FUN FOR LARGER DATASETS

from sklearn.metrics import silhouette_samples, silhouette_score

def silhouette_plot(data, labels):
    fig, ax = plt.subplots(figsize=(5,5))
    silhouette_avg = silhouette_score(data, labels)
    silhouette_values = silhouette_samples(data, labels)
    counter = 1
    for c in set(labels):
        silhouette_values_of_cluster_c = silhouette_values[labels == c]
        s = np.argsort(silhouette_values_of_cluster_c)
        color = plt.cm.spectral(float(c) / float(len(set(labels))))
        for i in s: 
            ax.plot([0.0, silhouette_values_of_cluster_c[i]], [counter, counter], color=color, lw=2)
            counter += 1
        counter += 2
        
    ax.axvline(x=silhouette_avg, color='red', linestyle='--', lw=1)
    ax.axvline(x=0., color='k', linestyle='-', lw=1)
    ax.set_xlabel('The silhouette coefficient values')
    ax.set_ylabel('Cluster')
    ax.set_ylim([0, counter -2])
    ax.set_yticks([]) 
    ax.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
    plt.tight_layout()
silhouette_plot(data, labels)