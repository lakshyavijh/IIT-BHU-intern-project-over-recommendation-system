import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import sys
from pprint import pprint
import math
import random

#  data preprocessing training
        dataset = pd.read_csv('subset.csv')
        item_list = dataset['item_id']
        properties_list = dataset['properties']
        overall_sent_prop = [each_prop.split('|') for each_prop in properties_list]
        unique_prop = list(set([prop_ for each_prop in overall_sent_prop for prop_ in each_prop]))
        main_dict = dict()
        for idx, sent_feat in enumerate(overall_sent_prop):
            id_feat_dict = dict(zip(unique_prop, [0]*len(unique_prop)))
            for feat in sent_feat:
                if feat in unique_prop:
                    id_feat_dict[feat] = 1
            main_dict[item_list[idx]] = id_feat_dict
            
            
            
          #data preprocessing testing   
        df = pd.read_csv('subsetitemuser.csv', names = ['user_id' , 'reference'])    
        s  = df.groupby(['user_id' , 'reference']).size()
        m = s.unstack()
        m.columns.name = None
        m.index.name = None
        m = m.fillna(0)
        m[m>1]=1
        sp=len(m)
        
        # training data
        emission_context_count = {}
        transition_context_count = {}
        item_context = {}
        context_context = {}
        unique_context = []
        for idx, sent_feat in enumerate(overall_sent_prop):
                line_count = len(overall_sent_prop)
                first_context = 'START'
                if first_context not in unique_context:             
                            unique_context.append(first_context)
                i = 0
                for context in sent_feat:
                    count =len(sent_feat)
                    i += 1
                    if context not in unique_context:
                                unique_context.append(context)
                    if first_context in context_context:
                                if context in context_context[first_context]:
                                    context_context[first_context][context] += 1   
                                else:
                                    context_context[first_context][context] = 1    
                    else:
                                context_context[first_context] = {}
                                context_context[first_context][context] = 1
                    if context not in emission_context_count:
                                emission_context_count[context] = 1
                                if i != count:
                                    if context not in transition_context_count:
                                        transition_context_count[context] = 1
                                    else:
                                        transition_context_count[context] += 1
                    else:
                                emission_context_count[context] += 1
                                if i != count:
                                    # print(emission_tag_count)
                                    if context in transition_context_count:
                                        transition_context_count[context] += 1
                                    else:
                                        transition_context_count[context] = 1
                    first_context = context                    
                context = 'STOP'
                if context not in unique_context:
                    unique_context.append(context)
                transition_context_count['START'] = line_count
                if first_context in context_context:
                   if context in context_context[first_context]:
                       context_context[first_context][context] += 1
                   else:
                        context_context[first_context][context] = 1    
           
        for idx, sent_feat in enumerate(overall_sent_prop):
            item=item_list[idx]
            for context in sent_feat:
                if item in item_context:
                    if context in item_context[item]:
                        item_context[item][context] += 1
                    else:
                          item_context[item][context] = 1
                else:
                      item_context[item] = {}
                      item_context[item][context] = 1
        context_item={}
        for idx, sent_feat in enumerate(overall_sent_prop):
            item1=item_list[idx]
            for context in sent_feat:
                if context in context_item:
                    if item1 in context_item[context]:
                        context_item[context][item1] += 1
                    else:
                          context_item[context][item1] = 1
                else:
                      context_item[context] = {}
                      context_item[context][item1] = 1
                      
        unique_tag_length = len(unique_context)
        for context1 in unique_context:
            if context1 != 'STOP':  # because stop is the end point
                if context1 in context_context:  # transitions from context1 already exist
                    for context2 in unique_context:
                        if context2 == 'START':
                            continue
                        if context1 == 'START' and context2 == 'STOP':
                                    continue
                        if context2 in context_context[context1]:
                            context_context[context1][context2] += 1
                        else:
                            context_context[context1][context2] = 1
                else:
                    context_context[context1] = {}
                    transition_context_count[context1] = 0
                    for context2 in unique_context:
                        if context2 == 'START':
                            continue
                        if context1 == 'START' and context2 == 'STOP':
                            continue
                        context_context[context1][context2] = 1
                    transition_context_count[context1] += 5*unique_tag_length
                        
        context_context_probability = {}
        for context1 in context_context:
            context_context_probability[context1] = {}
            for context2 in context_context[context1]:
                context_context_probability[context1][context2] = [math.log(context_context[context1][context2]) - math.log(sum(context_context[context1].values()))]
                
        item_context_probability = {}
        for item in item_context:
            item_context_probability[item] = {}
            count = 0
            for context in item_context[item]:
                item_context_probability[item][context] = [math.log(item_context[item][context]) - math.log(emission_context_count[context])]
        
        context_item_probability = {}
        for context in context_item:
            context_item_probability[context] = {}
            count = 0
            for item in context_item[context]:
                context_item_probability[context][item] = [(random.randint(0, len(properties_list))) /(len(item_list))]        
  
                                 
#m= user-item matrix
#testing                 
for i in range(0,sp):
     values=m.iloc[i,:]
     #del item_list
     item_list1=[]
     recommended_item=[]
     for k,each in values.items():
         if each==1.0:
             item_list.append(k)      
     item_count = len(item_list1)
     i = 1
     context_list = {}
     for i in range(1, item_count+1):
         items=int(item_list1[i-1])
         for key in item_context_probability:
             if key==items:
                 context_list[items] = item_context_probability[items]
                 break
         import operator
         each_item={}
         for each in context_list:
             each_item[each]=context_list[each]
             for key,value in each_item.items():
                 sorted_v = dict( sorted(value.items(), key=operator.itemgetter(0),reverse=True))
             max=list(sorted_v.keys())[0]   
             context_prob={}         
             for context in context_context_probability:
                 if max in context:
                     context_prob[context]=context_context_probability[context]
             for key,cvalue in context_prob.items():
                 sorted_d = dict( sorted(cvalue.items(), key=operator.itemgetter(0),reverse=True))
             max_context=list(sorted_d.keys())[0]
             item_context_prob={}
             for itemco in context_item_probability:
                 if itemco in max_context :
                     item_context_prob[itemco]=context_item_probability[itemco]
             for key,value in item_context_prob.items():
                 sorted_i = dict( sorted(value.items(), key=operator.itemgetter(0),reverse=True))
             for each1 in sorted_i.copy():
                 each=int(each1)
                 if items==each:
                     del sorted_i[each1]
             max_i=list(sorted_i.keys())[0]
         recommended_item.append(each1)
     #recommend_dict[]  



# for 1st user

                
values=m.iloc[0,:]
item_list=[]
for k,each in values.items():
    if each==1.0:
        item_list.append(k)      
item_count = len(item_list)
recommended_item=[]

for i in range(1, item_count+1):
     items=int(item_list[i-1])
     for key in item_context_probability:
         if key==items:
             context_list = {}
             context_list[items] = item_context_probability[items]
             break
     import operator
     for each in context_list:
         each_item={}
         each_item[each]=context_list[each]
         for key,value in each_item.items():
             sorted_v = dict( sorted(value.items(), key=operator.itemgetter(0),reverse=True))
         max=list(sorted_v.keys())[0]   
         context_prob={}         
         for context in context_context_probability:
             if context in max:
                 context_prob[context]=context_context_probability[context]
         for key,cvalue in context_prob.items():
             sorted_d = dict( sorted(cvalue.items(), key=operator.itemgetter(0),reverse=True))
         max_context=list(sorted_d.keys())[0]
         item_context_prob={}
         for itemco in context_item_probability:
             if itemco in max_context :
                 item_context_prob[max_context]=context_item_probability[max_context]
         for key,value in item_context_prob.items():
             sorted_i = dict(sorted(value.items(), key=operator.itemgetter(0),reverse=True))
         for each1 in sorted_i.copy():
             each=int(each1)
             if items==each:
                 del sorted_i[each1]
         max_i=list(sorted_i.keys())[0]
         max_2=list(sorted_i.keys())[1]
         
     recommended_item.append(max_i)
     recommended_item.append(max_2)
               
list_set = set(recommended_item) 
unique_list = (list(list_set)) 

del recommended_items

























# Importing the dataset
df = pd.read_csv('subsetitemuser.csv', names = ['user_id' , 'reference'])    
s  = df.groupby(['user_id' , 'reference']).size()
m = s.unstack()
m.columns.name = None
m.index.name = None
m = m.fillna(0)
m[m>1]=1




 dataset1 = pd.read_csv('subsetitemuser.csv')    
        item=[]
        item=dataset1['reference']
        user_list= dataset1['user_id'] 
        unique_item=[]
        unique_item=list(set(item))
        unique_user=list(set(user_list))
        
        
        main_dict1=()
        for i in unique_user:
            id_feat_dict1 = dict(zip(unique_item, [0]*len(unique_item)))
            for j in dataset1['user_id']:
                if i in j:
                    value=dataset1.loc[j,'reference']
                    id_feat_dict1[value]=1
            main_dict1[i]=id_feat_dict1      

        
    