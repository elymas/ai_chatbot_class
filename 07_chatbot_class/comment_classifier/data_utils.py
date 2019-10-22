import numpy as np

def createBatches(data):
    l = []
    for i in data:
        l.append(len(i[0]))
    l = set(l)
    batches = []
    batch_len = []
    z = 0
    for i in l:
        for batch in data:
            if len(batch[0]) == i:
                batches.append(batch)
                z += 1
        batch_len.append(z)
    return batches,batch_len

def iterate_minibatches(dataset,batch_len): 
    start = 0
    for i in batch_len:
        tokens = []
        char = []
        labels = []
        data = dataset[start:i]
        start = i
        for dt in data:
            t,ch,l = dt
            l = np.expand_dims(l,-1)
            tokens.append(t)
            char.append(ch)
            labels.append(l)
        yield np.asarray(labels),np.asarray(tokens),np.asarray(char)