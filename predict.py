from process import createNet, readData, preProcessData, processLabel, evaluate_accuracy
from mxnet import ndarray as nd
import mxnet

if __name__ == '__main__':
    dataFile = './data/nba_data2.txt'
    data = readData(dataFile)
    #print(len(dict(zip(processLabel(data.iloc[:,0]),processLabel(data.iloc[:,0])))))
    x = preProcessData(nd.array(data.iloc[:,1:]))
    y = nd.array(processLabel(data.iloc[:,0]))

    net  = createNet()
    net.load_params('./params/params.txt', ctx=mxnet.cpu())

    print(evaluate_accuracy(x,y,net)/len(x))
