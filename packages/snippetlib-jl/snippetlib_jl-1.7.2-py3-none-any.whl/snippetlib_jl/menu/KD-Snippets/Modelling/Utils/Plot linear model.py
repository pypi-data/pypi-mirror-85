# plot the weights of a linear model in a barchart

def plot_linear_model_weights(model, attributes):
    pd.Series(model.coef_, index=attributes).plot(kind='bar', figsize=(8,4), color='lightgrey')
    plt.axhline(0, color='k', linewidth=1)
    plt.ylabel('Weight')

plot_linear_model_weights(model, attributes)