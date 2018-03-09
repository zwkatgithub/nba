import pandas as pd
import json
import numpy as np
from mxnet import ndarray as nd
from mxnet import gluon
from mxnet import autograd
from sklearn import preprocessing
import sys

label2idx = dict(
    {'PF':0, 'C':1, 'SF':2, 'SG':3, 'PG':4}
)
idx2label = {v:k for v,k in label2idx.items()}

def readData(dataFile):
    with open(dataFile, 'r') as f:
        table = json.load(f)
    return pd.DataFrame(table[1:],columns=table[0]).fillna(0.0)

def preProcessData(data):
    return nd.array(
        preprocessing.scale(data.asnumpy(), axis=0)
    )
def processLabel(y):
    # labels = []
    # for label in y:
    #     if '-' in label:
    #         label = label.split('-')
    #         ll = [0.0]*5
    #         for l in label:
    #             ll[lable2idx[l]] = 0.5
    #         labels.append(ll)
    #     else:
    #         l = [0.0]*5
    #         l[lable2idx[label]] = 1.0
    #         labels.append(l)
    # return labels
    labels = []
    for label in y:
        if '-' in label:
            labels.append(label2idx[label.split('-')[0]])
        else:
            labels.append(label2idx[label])
    return labels
        

def divideTrainTest(x,y, rate, k=None):
    if k is None:
        n = int(len(x)*rate)
        return (x[0:n], y[0:n]), (x[n:], y[n:])
    else:
        num = int(len(x) / k)
        for i in range(k):
            if i!=0 and i!=k-1:
                start = i*num
                end = min((i+1)*num, len(x))
                test_data = ( nd.array( x.asnumpy()[start:end] ), 
                                nd.array( y.asnumpy()[start:end] ) )
                train_data = (nd.concatenate( [ nd.array(x.asnumpy()[0:start]) , nd.array(x.asnumpy()[end:]) ] ),
                        nd.concatenate([ nd.array(y.asnumpy()[0:start]),nd.array(y.asnumpy()[end:])]) )
            else:
                if i ==0:
                    test_data = (x[0:num], y[0:num])
                    train_data = (x[num:], y[num:])
                else:
                    test_data = (x[i*num:],y[i*num:])
                    train_data = (x[0:i*num], y[0:i*num])
            yield train_data, test_data
            


def data_iter(x,y,batch_size):
    n = len(x)
    idx = list(range(n))
    np.random.shuffle(idx)
    for i in range(0,n,batch_size):
        j = nd.array(idx[i:min(i+batch_size, n)])
        yield nd.take(x, j), nd.take(y, j)

def accuracy(output,label):
    """
        output : [1,2,3,4,5], label : 2
    """
    
    labelHat = nd.argmax(output, axis=1)
    
    return nd.sum(labelHat == label).asscalar() 

def evaluate_accuracy(x,y,net):
    labelHat = net(x)
    return accuracy(labelHat, y)

def createNet():
    net = gluon.nn.Sequential()
    with net.name_scope():
        net.add(gluon.nn.Dense(50, activation='relu'))
        net.add(gluon.nn.Dense(100, activation='relu'))
        net.add(gluon.nn.Dense(5))
    return net

if __name__ == '__main__':
    dataFile = './data/nba_data.txt'
    data = readData(dataFile)
    #print(len(dict(zip(processLabel(data.iloc[:,0]),processLabel(data.iloc[:,0])))))
    x = preProcessData(nd.array(data.iloc[:,1:]))
    y = nd.array(processLabel(data.iloc[:,0]))
    #train_data, test_data = divideTrainTest(x,y,0.7)

    batch_size = 10
    net = createNet()
    
    
        
    net.initialize()

    lossFunc = gluon.loss.SoftmaxCrossEntropyLoss()

    trainer = gluon.Trainer(net.collect_params(), 'sgd', {'learning_rate':0.01,'momentum':0.9})

    for e in range(70):
        mean_train_loss = 0.0
        mean_train_acc = 0.0
        test_acc = 0.0
        for train_data, test_data in divideTrainTest(x,y,None,k=5):
            train_loss = 0.0
            train_acc = 0.0
            for data, label in data_iter(train_data[0], 
                train_data[1],batch_size):
                with autograd.record():
                    output = net(data)
                    loss = lossFunc(output, label)
                loss.backward()
                trainer.step(batch_size)

                train_loss += nd.mean(loss).asscalar()
                
                train_acc += accuracy(output, label)
            
            test_acc += evaluate_accuracy(test_data[0], test_data[1], net)
            mean_train_loss += train_loss/len(train_data[0])
            mean_train_acc += train_acc/len(train_data[0])
        print("Epoch {0} : Loss: {1}, Train acc: {2}, Test acc {3}".format(
                e, mean_train_loss/5, mean_train_acc/5, test_acc/len(test_data[0])/5)
            )
    paramsFile = './params/params.txt'
    net.save_params(paramsFile)
    


        


    

    

