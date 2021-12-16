import seaborn as sns
import matplotlib.pyplot as plt
import sklearn
from sklearn.metrics import confusion_matrix


def metrics(y_cv, cv_clf, model):
    C = confusion_matrix(y_cv, cv_clf)
    # Recall = TP / (TP+FN)
    # Precision = TP / (TP+FP)
    R = (((C.T)/(C.sum(axis=1))).T)
    P =(C/C.sum(axis=0))
    labels = [1,2,3,4,5,6,7,8,9]
    # color_map = sns.diverging_palette(0, 10, as_cmap=True) # Color palette

    fig, ax = plt.subplots(3,1, figsize=(20, 25), sharey=True)
    fig.suptitle(f'{model} metrics')

    sns.heatmap(C,  
            ax=ax[0],
            cmap='seismic', #icefire magma
            square=True, #sea data as squares
            linewidth=0.5, 
            vmax=150,
            cbar_kws={"shrink": .5}, #lateral bar
            annot=True,
            fmt='g',
            xticklabels=labels,
            yticklabels = labels
        )
    ax[0].set(xlabel="Predicted Class", ylabel = "Real Class", title='Confusion Matrix');

    
    sns.heatmap(R,  
            ax=ax[1],
            cmap='seismic', #icefire magma
            square=True, #sea data as squares
            linewidth=0.5, 
            vmax=1,
            cbar_kws={"shrink": .5}, #lateral bar
            annot=True,
            fmt='.4f',
            xticklabels=labels,
            yticklabels = labels
        )
    ax[1].set(xlabel="Predicted Class", ylabel = "Real Class", title='Recall Matrix');

    P =(C/C.sum(axis=0))
    sns.heatmap(P,  
            ax=ax[2],
            cmap='seismic', #icefire magma
            square=True, #sea data as squares
            linewidth=0.5, 
            vmax=1,
            cbar_kws={"shrink": .5}, #lateral bar
            annot=True,
            fmt='.4f',
            xticklabels=labels,
            yticklabels = labels
        )
    ax[2].set(xlabel="Predicted Class", ylabel = "Real Class", title='Precission Matrix');

    return fig