## rnn_cell
https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/ops/rnn_cell.py
```
tensorflow实现rnn的基本神经元,包括BasicRNNCell，BasicLSTMCell，GRUCell, LSTMCell，和RNN Cell wrappers（RNNCells that wrap other RNNCells）,可以添加dropout,projection或embedding等操作。

另外，可以使用`MultiRNNCell`或多次调用rnn操作实现多层rnn cell或多次调用rnn操作实现多层rnn cells

```

1. RNNCell 
表示RNN cell的抽象对象
```
def __call__(self,inputs,state,scope=None):
```
参数：
* inputs: `2-D`tensor with shape `[batch_size,input_size]`

× state: 如果`self.state_size`是integer，state应该是一个`2-D`tensor with shape `[batch_size,self.state_size]`。否则，如果`self.state_size`是a tuple of integers,state应该是一个元组with shape`[batch_size,s] for s in self.state_size`

* scope: VariableScope for the create subgraph; defaults to class name.

返回：

* output: 一个`2-D`tensor with shape `[batch_size,self.output_size]`

* new state: `2-D`tensor 或 tensor元组

```
def zero_state(self,batch_size,dtype)
```
返回填充0的state tensor

2. BasicRNNCell(RNNCell):最基本的RNN cell 
* 定义方法：tf.nn.rnn_cell.BasicRNNCell(num_unites)
* def __init__(self,num_units,input_size=None,activation=tanh)

3. GRUCell(RNNCell): Gated Recurrent Unit cell
* def __init__(self,num_units,input_size=None,activation=tanh) 

4. BasicLSTMCell(RNNCell):基本的LSTM
* 定义方法： lstm_cell=tf.nn.rnn_cell.BasicLSTMCell(size,forget_bias=0.0,state_is_tuple=True)
* def __init__(self,num_units,forget_bias=1.0,input_size=None,state_is_tuple=True,activation=tanh):

```
参数
num_units: int, LSTM cell中的神经元个数
forget_bias: float, forget gates的bias
input_size: Deprecated and unused
state_is_tuple: 如果为True,接受和返回的states是2-tuples of the `c_state`和`m_state`。如果是false，they are concatenated along the column axis.
activation: 激活函数
```

5. LSTMCell(RNNCell):
```
def __init__(self,num_units,input_size=None,use_peepholes=False,cell_clip=None,initializer=None,num_proj=None,proj_clip=None,num_unit_shards=1,num_proj_shards=1,forget_bias=1.0,state_is_tuple=True,activation=tanh):
```
参数：

* num_units: int, LSTM cell的单元个数

* input_size: 过时

* use_peepholes: bool

* cell_clip: float,可选

* initializer: 可选，The initializer to use for the weight and projection matrices

* num_proj: 可选，int, projection matrices的输出维度,如果None，不执行projection

* forget_bias: 遗忘门的bias，默认初始化为1

* activation: 激活函数of the inner states

2. rnn

```
rnn(cell,inputs,initial_state=None,dtype=None,sequence_length=None,scope=None)
```
最简单的RNN网络:
```python
state = cell.zero_state(...)
outputs=[]
for input_ in inputs:
   output,state=cell(input_,state)
   outputs.append(output)
return (outputs,state)
```

参数:

* cell: RNNCell实例

* inputs: 长度为T的inputs列表, 每个inputs 是shape 为`[batch_size,input_size]`的tensor

* initial_state:可选,初始状态

* dtype: 可选,state和output的数据类型

* sequence_length: 具体化每个输入序列的长度

* scope: VariableScope for the created subgraph

返回:(outputs,state)

3. rnn的使用方法
× 定义输入inputs
* 定义单个神经元cell=tf.nn.rnn_cell.BasicRNNCell等
* 获取初始化state: initail_state=cell.zero_state(size,tf.float32)
* 使用tensorflow的unpack或unstack方法，把输入的tensor inputs转换成sequence:inputs=tf.unpack(inputs,axis=1) 
× 使用rnn方法：outputs,state=tf.nn.rnn(cell,inputs,initial_state)
