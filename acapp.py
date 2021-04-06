# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 11:58:21 2020

@author: nnig9
"""
import datetime
from flask import Flask, jsonify, request
from deeppavlov.deprecated.skills.similarity_matching_skill import SimilarityMatchingSkill
from deeppavlov import configs, build_model


now = datetime.datetime.now()
id ='b'
cs =1
csp=1


acapp = Flask(__name__)
client = acapp.test_client()


rap = [
    {
        'id': id,
        'sent': 0,
        'text': '------Моё почтение, поговорим о Вас?',
        'time': now
    }
]

faq = SimilarityMatchingSkill(data_path = 'bot_it.csv',
                              x_col_name = 'Question', 
                              y_col_name = 'Answer',
                              save_load_path = './model_bot_it',
                              config_type = 'tfidf_autofaq',
                              edit_dict = {},
                              train =1)

bert = build_model(configs.odqa.ru_odqa_infer_wiki_rubert_noans, download=True)


sentim = build_model(configs.classifiers.rusentiment_bert, download=True)
cs=0
def sentim_sen(text):
    # 'speech','skip','positive','negative'
    global cs 
    cs += 1
    sent=sentim([text])
    print(sent[0])
    if sent[0] == 'positive':
        global csp
        csp +=1
    ks=csp/cs
    return(ks)



def selekt_ans(qwery):
    ans1 = faq([qwery], [], [])
    ans1_text = (ans1[0][0])
    ans1_fk = (ans1[1][0])
    if ans1_fk > 0.01:
        ans = ans1_text
    else:
        ans2 = bert([qwery])
        ans2_text = (ans2[0][0])
        ans2_fk = (ans2[1][0])
        ans = ans2_text
       
    if ans =='':
        ans = 'Я затрудняюсь Вас понять. Переформулируйте Ваш вопрос, пожалуйста'    
    return(ans)



def form_ans(fr):    
    fr['id']=id
    fr['sent']=sentim_sen(fr['text'])
    fr['text']=selekt_ans(fr['text'])
    fr['time']=datetime.datetime.now()
    
    return fr

# API ================================================================

@acapp.route('/bot', methods=['GET'])
def get_list():
    return jsonify(rap)


@acapp.route('/bot', methods=['POST'])
def update_list():
    new_one = request.json
    rap.append(new_one)
    new_too=new_one.copy()
    rap.append(form_ans(new_too))
    return jsonify(rap)


@acapp.route('/bot/<int:rap_id>', methods=['PUT'])
def update_rap(rap_id):
    item = next((x for x in rap if x['id'] == rap_id), None)
    params = request.json
    if not item:
        return {'message': 'No rap with this id'}, 400
    item.update(params)
    return item


@acapp.route('/bot/<int:tutorial_id>', methods=['DELETE'])
def delete_rap(tutorial_id):
    idx, _ = next((x for x in enumerate(rap)
                   if x[1]['id'] == tutorial_id), (None, None))

    rap.pop(idx)
    return '', 204






if __name__ == '__main__': 
    acapp.run(host='0.0.0.0', port=5000)

