import json
import time
import sys
from pprint import pprint
import math



class HmmDecode3:
    def smoothing_emission(self, emission, item, unique_context):
            l = len(list(transition.keys()))
            # prob = - math.log(l)
            prob = 0
            # prob = 1
            emission[item] = {}
            for context in unique_context:
                if context != 'START' and context != 'STOP':
                    emission[item][context] = []
                    emission[item][context].append(prob)
                    emission[item][context].append(l)
            emission[item]['total_count'] = l
            return emission[item]
    def get_contexts(self, emission_prob, item):
            context_list = {}
            for key in emission_prob:
                if key == item:
                    context_list[item] = emission_prob[item]
                    break
            return context_list    
    def find_max_context(self, probability):
            max_context = list(probability.keys())[0]
            for context1 in probability:
                if probability[context1] > probability[max_context]:
                    max_context = context1
            return max_context    
    def find_max_context_backprob(self, probability):
            max_context = list(probability.keys())[0]
            for context1 in probability:
                if probability[context1] > probability[context_tag]:
                    max_context = context1
            return max_context
     
             
     values=m.iloc[0,:]       
    def viterbi(self, context_context_probability, item_context_probability, unique_contexts, values):
            result = []
            #del item_list
            item_list=[]
            prob = dict()
            for k,each in values.items():
                if each==1.0:
                    item_list.append(k)
            item_count = len(item_list)        
            prev_context = []
            context_list = {}
            prev_context_list = []
            backtrack = dict()
            i = 1
            for i in range(1, item_count+1):
                #prob[i] = dict()
                backtrack[i] = dict()
                if i == 1:
                    # emission smoothing
                    if item_list[i-1] not in item_context_probability:
                        l = len(list(context_context_probability.keys()))
                        prob = 0
                        item_context_probability[item] = {}
                        for context in unique_context:
                            if context != 'START' and context != 'STOP':
                                item_context_probability[item][context] = []
                                item_context_probability[item][context].append(prob)
                                item_context_probability[item][context].append(l)
                            item_context_probability[item]['total_count'] = l
                           
                        #item_context_probability[item_list[i-1]] = self.smoothing_emission(item_context_probability, item_list[i-1], unique_context)
                    #context_list = self.get_contexts(item_context_probability, item_list[i - 1])
                    
                    item=int(item_list[i-1])
                    for key in item_context_probability:
                        if key==item:
                             context_list[item] = item_context_probability[item]
                             break
                    for context in context_list[int(item_list[i-1])]:
                        if context == 'total_count':
                            continue
                        p = context_context_probability['START'][context][0] + item_context_probability[int(item_list[i-1])][context][0]
                        # p = transition_prob['START'][context][0] * emission_prob[item_list[i - 1]][context][0]
                        # p = transition_prob['START'][context][0] * context_list[item_list[i - 1]][context][0]
                        prob[i][context] = dict()
                        prob[i][context]['START'] = p
                        prev_context.append(context)
                    prev_context_list = prev_context
                else:
                    prev_context = prev_context_list
                    prev_context_list = []
                    # emission smoothing
                    #if item_list[i - 1] not in emission_prob:
                        #item_context_probability[item_list[i - 1]] = self.smoothing_emission(item_context_probability, item_list[i - 1], unique_contexts)
                    #context_list = self.get_contexts(emission_prob, item_list[i - 1])
                    context_list = {}
                    item=int(item_list[i-1])
                    for key in item_context_probability:
                        if key == item:
                            context_list[item] = item_context_probability[item]
                            break
                    for c_context in context_list[int(item_list[i-1])]:
                        if c_context == 'total_count':
                            continue
                        prob[i][c_context] = dict()
                        for p_context in prev_context:
                            #max_context = self.find_max_context(prob[i-1][p_context])
                            probability=prob[i-1][p_context]
                            max_context = list(probability.keys())[0]
                            for context1 in probability:
                                if probability[context1] > probability[max_context]:
                                    max_context = context1
                            p = prob[i-1][p_context][max_context] + context_context_probability[p_context][c_context][0] + item_context_probability[item_list[i-1]][c_context][0]
                            # p = prob[i - 1][p_context][max_context] * transition_prob[p_context][c_context][0] * emission_prob[item_list[i - 1]][c_context][0]
                            # p = prob[i - 1][p_context][max_context] * transition_prob[p_context][c_context][0] * context_list[item_list[i - 1]][c_context][0]
                            backtrack[i-1][p_context] = max_context
                            prob[i][c_context][p_context] = p
                        prev_context_list.append(c_context)
            # for last item
            prob[i]['STOP'] = dict()
    
            for p_context in prev_context_list:
                #max_context = self.find_max_context(prob[i][p_context])
                probability=prob[i][p_context]
                max_context = list(probability.keys())[0]
                for context1 in probability:
                    if probability[context1] > probability[max_context]:
                        max_context = context1
                p = prob[i][p_context][max_context] + context_context_probability[p_context]['STOP'][0]
                # p = prob[i][p_context][max_context] * transition_prob[p_context]['STOP'][0]
                backtrack[i][p_context] = max_context
                prob[i]['STOP'][p_context] = p
            #max_context = self.find_max_context(prob[i]['STOP'])
            probability=prob[i]['STOP']
            max_context = list(probability.keys())[0]
            for context1 in probability:
                if probability[context1] > probability[max_context]:
                    max_context = context1
    
            # backtracking
            backtrack[i+1] = dict()
            backtrack[i+1]['STOP'] = max_context
            l = len(list(backtrack.keys()))
            context = max_context
            for i in range(l, 1, -1):
                if i == l:
                    result.append([item_list[i - 2], max_context])
                    context = backtrack[i]['STOP']
                else:
                    context = backtrack[i][context]

                    result.append([item_list[i - 2], context])
            
            return result
            
            
            def context_sentences(self, transition_prob, emission_prob, unique_contexts, filename):
            file = open(filename, 'r',encoding="utf8")
            lines = file.read()
            sentences = ""
            for i in range(0,sp):
                values=m.iloc[i,:]
                
                    
                res = self.viterbi(transition_prob, emission_prob, unique_contexts, values)
                res_len = len(res)
                sentence = ""
                for i in range(res_len - 1, -1, -1):
                    if i != res_len - 1:
                        sentence += " "
                    sentence += res[i][0] + "/" + res[i][1]
                sentences += sentence + "\n"
            sentences = sentences.strip("\n")
            return sentences

if __name__ == "__main__":
    model = HmmDecode3()  
    