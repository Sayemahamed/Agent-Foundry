import random

def get_random():
    return random.random()*100-50

def get_sum(args)->float:
    sum =0
    for i in args:
        sum=i+sum
    return sum

class Neuron():
    def __init__(self,neuron_number,forward_neuron_count) -> None:
        self.M = []
        self.C=[]
        for i in range(forward_neuron_count):
            self.M.append(get_random())
            self.C.append(get_random())
        print("N_No",neuron_number,"M",self.M,"C",self.C)

    def get_multiple(self,forward_neuron_no:int,input:float)->float:
        return self.M[forward_neuron_no]*input+self.C[forward_neuron_no]

# x=Neuron(1,3)
# x.get_multiple(0,4)
class NLayer():
    def __init__(self,numbers_of_neuron,forward_neuron_count) -> None:
        self.forward_neuron_count=forward_neuron_count
        self.layer:list[Neuron] =[]
        for neuron_number in range(numbers_of_neuron):
            self.layer.append(Neuron(neuron_number,forward_neuron_count))

    def get_sum_of_layer(self,input):
        layer_output=[]
        for forward_neuron_number in range(self.forward_neuron_count):
            temp=[]
            for neuron in self.layer:
                temp.append(neuron.get_multiple(forward_neuron_number,input))
            layer_output.append(get_sum(temp))
        print(layer_output)
        return layer_output
        # sum=0
        # for x in self.layer:
        #     sum=x.get_multiple(x)+sum
        # return sum

class NNetwork():
    def __init__(self):
        self.layer1=NLayer(2,5)
        self.layer2=NLayer(5,1)
    
    def forward(self,arr:list):
        temp1=[]
        for input in arr:
            self.layer1()





