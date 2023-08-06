def dendromodule(names, vecs, type_div='ward'):
    top_n = len(names)
    if len(names) != len(vecs):
        print('Error: different length for names and vecs')
        return
    if top_n == 0:
        return

    Z = hierarchy.linkage(vecs, type_div)
    _, axes = plt.subplots(1, figsize=(3*top_n/10, 3*top_n/10))

    hierarchy.dendrogram(Z, leaf_font_size=8, ax=axes, labels=np.array(names), orientation='left');

def dendromodule_heatmap(names, vecs, type_div='ward'):
    sns.clustermap(pd.DataFrame(cosine_similarity(vecs), index=names, columns=names), metric="correlation", method='single', cmap="Blues", standard_scale=1, 
                   )

if __name__ == "__main__":
