#coding:utf-8
import tensorflow as tf
import numpy as np
from tensorflow.python.ops import variable_scope as vs

batch_size=5
length=10
unit_num=20
'''
使用tf.reset_default_graph()或with来重置图，避免一些因为变量名字冲突而出现的问题
'''
#重置图
tf.reset_default_graph()

data=np.random.randint(low=0,high=1000,size=(batch_size,length))

idx=tf.placeholder(dtype=tf.int32,shape=[None,None])
embedding=np.random.rand(1000,50)
#embbedding
inputs=tf.nn.embedding_lookup(embedding,idx)
#定义lstm_cell
lstm_cell=tf.contrib.rnn.BasicLSTMCell(unit_num,forget_bias=1.0,state_is_tuple=True,activation=tf.tanh)
#获取初始状态
initial_state=lstm_cell.zero_state(batch_size,tf.float64)
print(inputs.get_shape())

with tf.variable_scope("lstm") as scope:
    #rnn
    states,output=tf.nn.dynamic_rnn(lstm_cell,inputs,time_major=False,dtype=tf.float64,scope=scope)
'''
第二次调用tf.nn.dynamic_rnn会报错：
1. scope定义了变量的作用范围与变量的名字有关
2. 第一次调用dynamic_rnn时会创建相关的变量包括lstm的各种参数
3. 第二次再调用时还会重新创建变量，这样就会重复创建相同名字的变量，从而导致错误
4. 变量只需要创建一次，以后再用时就要使用reuse=True来共享变量
5. 如果第一次就用reuse=True会出现变量不存在的错误，变量还没有创建就不能reuse，所以第一次不能使用reuse
'''
with tf.variable_scope("lstm",reuse=True) as scope:
    states,output=tf.nn.dynamic_rnn(lstm_cell,inputs,time_major=False,dtype=tf.float64,scope=scope)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    outputs,states=sess.run([states,output],feed_dict={idx:data[0:10]})
    print(outputs.shape)
    
    
'''使用tf.contrib.rnn.static_rnn'''
#unpack成sequence
inputs=tf.transpose(inputs,perm=[1,0,2])
inputs=tf.unstack(inputs,num=length,axis=1)
with tf.variable_scope("static_rnn") as scope:
    cell=tf.contrib.rnn.BasicLSTMCell(unit_num,forget_bias=1.0,state_is_tuple=True,activation=tf.tanh)
    #rnn
    output,states=tf.contrib.rnn.static_rnn(cell,inputs,dtype=tf.float64)
    
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    outputs,states=sess.run([states,output],feed_dict={idx:data[0:10]})
    print(outputs.shape)