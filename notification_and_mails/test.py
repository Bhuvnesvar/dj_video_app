# data={'id': '1.178848943', 'marketDefinition': {'bspMarket': True, 'turnInPlayEnabled': False, 'persistenceEnabled': False, 'marketBaseRate': 5, 'eventId': '30267807', 'eventTypeId': '4339', 'numberOfWinners': 1, 'bettingType': 'ODDS', 'marketType': 'WIN', 'marketTime': '2021-02-04T14:04:00.000Z', 'suspendTime': '2021-02-04T14:04:00.000Z', 'bspReconciled': False, 'complete': True, 'inPlay': False, 'crossMatching': True, 'runnersVoidable': False, 'numberOfActiveRunners': 6, 'betDelay': 0, 'status': 'OPEN', 'runners': [{'status': 'ACTIVE', 'sortPriority': 1, 'id': 23384826}, {'status': 'ACTIVE', 'sortPriority': 2, 'id': 36645264}, {'status': 'ACTIVE', 'sortPriority': 3, 'id': 37810845}, {'status': 'ACTIVE', 'sortPriority': 4, 'id': 37134476}, {'status': 'ACTIVE', 'sortPriority': 5, 'id': 28620360}, {'status': 'ACTIVE', 'sortPriority': 6, 'id': 24466802}], 'regulators': ['MR_INT'], 'venue': 'Sheffield', 'countryCode': 'GB', 'discountAllowed': True, 'timezone': 'Europe/London', 'openDate': '2021-02-04T14:04:00.000Z', 'version': 3608352499, 'priceLadderDefinition': {'type': 'CLASSIC'}}, 'rc': [{'batb': [[2, 1.03, 29], [1, 2.06, 11.02], [0, 3.8, 2]], 'batl': [[0, 6.6, 1.85], [2, 34, 16.5], [1, 8, 2]], 'id': 23384826}, {'batb': [[2, 1.03, 29], [1, 2.08, 9.27], [0, 4.1, 2]], 'batl': [[0, 7.8, 1.51], [2, 34, 16.5], [1, 8.8, 2]], 'id': 36645264}, {'batb': [[2, 2.06, 13.77], [1, 2.62, 77.78], [0, 5.6, 2]], 'batl': [[0, 14.5, 2.92], [1, 890, 0.51]], 'id': 37134476}, {'batb': [[2, 1.03, 29], [1, 2, 10.7], [0, 4.1, 2]], 'batl': [[2, 34, 16.5], [1, 8.8, 2], [0, 7.8, 1.48]], 'id': 37810845}, {'batb': [[2, 1.03, 29], [1, 2.02, 11.71], [0, 3.8, 2]], 'batl': [[0, 6.6, 1.81], [2, 34, 16.5], [1, 8, 2]], 'id': 24466802}, {'batb': [[0, 2.1, 14.06], [2, 1.01, 10005.14], [1, 1.03, 29]], 'batl': [[0, 48, 2.31], [1, 890, 0.5]], 'id': 28620360}], 'img': True}
# print((data['marketDefinition']['runners']))
# #totalAvailable,isMarketDataDelayed,totalMatched
# format={"marketId":data["id"],
#         "isMarketDataDelayed":'true',
#         "status":data['marketDefinition']['status'],
#         "betDelay":data['marketDefinition']['betDelay'],
#         "bspReconciled":data['marketDefinition']['bspReconciled'],
#         "complete":data['marketDefinition']['complete'],
#         "inplay":data['marketDefinition']['inPlay'],
#         "numberOfWinners":data['marketDefinition']['numberOfWinners'],
#         "numberOfRunners":len(data['marketDefinition']['runners']),
#         "numberOfActiveRunners":data['marketDefinition']['numberOfActiveRunners'],
#         "totalMatched":0,
#         "totalAvailable":94835.88,
#         "crossMatching":data['marketDefinition']['crossMatching'],
#         "runnersVoidable":data['marketDefinition']['runnersVoidable'],
#         "version":data['marketDefinition']['version'],
#         "runners":[]}
# for i in range(len(data['marketDefinition']['runners'])):
#     a={"selectionId":data['marketDefinition']['runners'][i]['id'],
#        "handicap":0,
#        # "sortPriority":data['marketDefinition']['runners'][i]['sortPriority'],
#        "status":data['marketDefinition']['runners'][i]['status'],"totalMatched":0,
#        "ex":{"availableToBack":[],
#              "availableToLay":[],
#              "tradedVolume":[]
#             }
#        }
#     format['runners'].append(a)
# for i in range(len(data['rc'])):
#     for j in range(len(data['rc'][i]['batb'])):
#         print('*********',len(data['rc'][i]['batb']))
#         back={"price": data['rc'][i]['batb'][j][1], "size": data['rc'][i]['batb'][j][2]}
#         # print(back,type(back),format)
#         format['runners'][i]['ex']['availableToBack'].append(back)
#
#     for k in range(len(data['rc'][i]['batl'])):
#         lay = {"price": data['rc'][i]['batl'][k][1], "size": data['rc'][i]['batl'][k][2]}
#         print('*********', lay, len(data['rc'][i]['batl']))
#         format['runners'][i]['ex']['availableToLay'].append(lay)



#
# format= {'marketId': '1.178887062', 'isMarketDataDelayed': 'true', 'status': 'OPEN', 'betDelay': 0, 'bspReconciled': False, 'complete': True, 'inplay': False, 'numberOfWinners': 1, 'numberOfRunners': 6, 'numberOfActiveRunners': 6, 'totalMatched': 0, 'totalAvailable': 94835.88, 'crossMatching': True, 'runnersVoidable': False, 'version': 3609690698, 'runners': [{'selectionId': 37364046, 'handicap': 0, 'status': 'ACTIVE', 'totalMatched': 0, 'ex': {'availableToBack': [{'price': 2.62, 'size': 77.78}, {'price': 6.6, 'size': 1.8}, {'price': 9, 'size': 2}], 'availableToLay': [{'price': 44, 'size': 8.2}, {'price': 22, 'size': 2}, {'price': 21, 'size': 1.67}], 'tradedVolume': []}}, {'selectionId': 37809771, 'handicap': 0, 'status': 'ACTIVE', 'totalMatched': 0, 'ex': {'availableToBack': [{'price': 7.2, 'size': 1.62}, {'price': 7.4, 'size': 2}, {'price': 10.5, 'size': 2.5}], 'availableToLay': [{'price': 60, 'size': 10.2}, {'price': 22, 'size': 2}, {'price': 21, 'size': 1.49}], 'tradedVolume': []}}, {'selectionId': 37631356, 'handicap': 0, 'status': 'ACTIVE', 'totalMatched': 0, 'ex': {'availableToBack': [{'price': 2.08, 'size': 12.85}, {'price': 3.2, 'size': 2}, {'price': 3.35, 'size': 2}], 'availableToLay': [{'price': 9.8, 'size': 8.2}, {'price': 7.2, 'size': 2}, {'price': 5.6, 'size': 2.82}], 'tradedVolume': []}}, {'selectionId': 36973214, 'handicap': 0, 'status': 'ACTIVE', 'totalMatched': 0, 'ex': {'availableToBack': [{'price': 2.62, 'size': 77.78}, {'price': 6.6, 'size': 1.8}, {'price': 9, 'size': 2}], 'availableToLay': [{'price': 15.5, 'size': 1.65}, {'price': 14, 'size': 6.65}, {'price': 13.5, 'size': 1.7}], 'tradedVolume': []}}, {'selectionId': 22408924, 'handicap': 0, 'status': 'ACTIVE', 'totalMatched': 0, 'ex': {'availableToBack': [{'price': 2, 'size': 13.23}, {'price': 2.82, 'size': 2}, {'price': 2.94, 'size': 2}], 'availableToLay': [{'price': 4.5, 'size': 2.79}, {'price': 8, 'size': 8.2}, {'price': 5.5, 'size': 2.86}], 'tradedVolume': []}}, {'selectionId': 37389592, 'handicap': 0, 'status': 'ACTIVE', 'totalMatched': 0, 'ex': {'availableToBack': [{'price': 2.62, 'size': 77.78}, {'price': 5.6, 'size': 2}, {'price': 7.4, 'size': 2}], 'availableToLay': [{'price': 23, 'size': 8.2}, {'price': 16.5, 'size': 2.81}, {'price': 10.5, 'size': 1.06}], 'tradedVolume': []}}]}
# data={'id': '1.178887062', 'rc': [{'batl': [[2, 60, 10.2], [1, 22, 2], [0, 21, 1.53]], 'id': 22408924}, {'batb': [[2, 2.08, 12.85], [1, 3.2, 2], [0, 3.3, 2]], 'id': 37364046}, {'batl': [[2, 15.5, 1.65], [1, 14, 6.65], [0, 13.5, 1.67]], 'id': 37809771}, {'batb': [[2, 2, 13.23], [1, 2.76, 2]], 'id': 37631356}], 'con': True}
#
# print(data['rc'][0])
# # for i in range(len(format['runners'])):
# #     format['runners'][i]["ex"]["availableToBack"]=[]
# #     format['runners'][i]["ex"]["availableToLay"] = []
# # format['runners']=[]
#
# for i in range(len(data['rc'])):
#     # if data['rc'][i].get('batl'):
#     #     print('loool')
#     for j in range(len(format['runners'])):
#         if format['runners'][j]['selectionId']==data['rc'][i]['id']:
#             # print(data['rc'][i]['batl'])
#             if data['rc'][i].get('batl'):
#             # format['runners'][j]['ex']['availableToBack']=[]
#             #     for k in range(len(format['runners'][j]['ex']['availableToLay'])):
#                 for k in range(len(data['rc'][i]['batl'])):
#                     # if len(data['rc'][i]['batl'])==len(format['runners'][j]['ex']['availableToLay'][k]):
#                     #     # count = 0
#                     #     for m in range(len(data['rc'][i]['batl'])):
#                     #         # if count==0:
#                     #         #     print(format['runners'][j]['ex']['availableToLay'][m])
#                     #         #     del format['runners'][j]['ex']['availableToLay'][m]
#                     #         #     count+=1
#                     #         format['runners'][j]['ex']['availableToLay'][k]['price'] = data['rc'][i]['batl'][m][1]
#                     #         format['runners'][j]['ex']['availableToLay'][k]['size']=data['rc'][i]['batl'][m][2]
#                     # else:
#                     #     # format['runners'][j]['ex']['availableToLay'][k]= []
#                     count=0
#                     for m in range(len(data['rc'][i]['batl'])):
#                         if count==0:
#                             print(format['runners'][j]['ex']['availableToLay'])
#                             format['runners'][j]['ex']['availableToLay']=[]
#                             count+=1
#                         lay = {"price": data['rc'][i]['batl'][m][1], "size": data['rc'][i]['batl'][m][2]}
#                         format['runners'][j]['ex']['availableToLay'].append(lay)
#             elif data['rc'][i].get('batb'):
#                 # for k in range(len(format['runners'][j]['ex']['availableToBack'])):
#                 for k in range(len(data['rc'][i]['batb'])):
#                     # if len(data['rc'][i]['batb']) == len(format['runners'][j]['ex']['availableToBack'][k]):
#                     #     for l in range(len(data['rc'][i]['batb'])):
#                     #         format['runners'][j]['ex']['availableToBack'][k]['price']=data['rc'][i]['batb'][l][1]
#                     #         format['runners'][j]['ex']['availableToBack'][k]['size'] = data['rc'][i]['batb'][l][2]
#                     # else:
#                     #     # format['runners'][j]['ex']['availableToBack'][k]=[]
#                     count=0
#                     for m in range(len(data['rc'][i]['batb'])):
#                         if count==0:
#                             print(format['runners'][j]['ex']['availableToBack'])
#                             format['runners'][j]['ex']['availableToBack']=[]
#                             count+=1
#                         lay = {"price": data['rc'][i]['batb'][m][1], "size": data['rc'][i]['batb'][m][2]}
#                         format['runners'][j]['ex']['availableToBack'].append(lay)
#
# print(data)
#
# print(format,len(data),len(format),)




# z='{"marketId": "1.178885419",' \
#   ' "isMarketDataDelayed": "true", ' \
#   '"status": "OPEN",' \
#   ' "betDelay": 0,' \
#   ' "bspReconciled": "false", ' \
#   '"complete": "true", ' \
#   '"inplay": "false", ' \
#   '"numberOfWinners": 1, ' \
#   '"numberOfRunners": 6, ' \
#   '"numberOfActiveRunners": 6, ' \
#   '"totalMatched": 0, ' \
#   '"totalAvailable": 94835.88, ' \
#   '"crossMatching": "true", ' \
#   '"runnersVoidable": "false", ' \
#   '"version": 3609690574, ' \
#   '"runners": [{"selectionId": 23838914, ' \
#   '             "handicap": 0, ' \
#   '             "status": "ACTIVE", ' \
#   '             "totalMatched": 0, ' \
#   '             "ex": {' \
#   '                     "availableToBack": [{"price": 5.1, "size": 9.1},' \
#   '                                         {"price": 9, "size": 2},' \
#   '                                         {"price": 6.2, "size": 1.93}], ' \
#   '                      "availableToLay": [{"price": 21, "size": 6.07},' \
#   '                                         {"price": 60, "size": 8.2},' \
#   '                                         {"price": 22, "size": 2}], ' \
#   '                                          "tradedVolume": []' \
#   '                     }' \
#   '             },' \
#   '             {"selectionId": 35162894,' \
#   '              "handicap": 0, ' \
#   '              "status": "ACTIVE", ' \
#   '              "totalMatched": 0, ' \
#   '               "ex": {' \
#   '                         "availableToBack": [{"price": 2.96, "size": 54.06}, ' \
#   '                                             {"price": 4.6, "size": 8.23}, ' \
#   '                                             {"price": 6.6, "size": 3.8}], ' \
#   '                          "availableToLay": [{"price": 60, "size": 10.2},' \
#   '                                             {"price": 24, "size": 2}, ' \
#   '                                             {"price": 23, "size": 1.59}], ' \
#   '                                              "tradedVolume": []' \
#   '                       }' \
#   '             }, ' \
#   '             {"selectionId": 37188299, ' \
#   '              "handicap": 0, ' \
#   '              "status": "ACTIVE", ' \
#   '              "totalMatched": 0, ' \
#   '              "ex": {' \
#   '                         "availableToBack": [{"price": 4.6, "size": 8.23}, ' \
#   '                                             {"price": 6.8, "size": 13.13}, ' \
#   '                                             {"price": 6.6, "size": 1.8}], ' \
#   '                          "availableToLay": [{"price": 17.5, "size": 5.25}, ' \
#   '                                             {"price": 15.5, "size": 13.92}, ' \
#   '                                             {"price": 16, "size": 1.51}], ' \
#   '                                             "tradedVolume": []' \
#   '                      }' \
#   '              }, ' \
#   '             {"selectionId": 28575784, ' \
#   '              "handicap": 0, ' \
#   '              "status": "ACTIVE", ' \
#   '              "totalMatched": 0, ' \
#   '              "ex": {' \
#   '                         "availableToBack": [{"price": 3.8, "size": 13.48}, ' \
#   '                                             {"price": 5.3, "size": 2.81}, ' \
#   '                                             {"price": 5.1, "size": 2}],' \
#   '                         "availableToLay": [{"price": 25, "size": 4.4}, ' \
#   '                                            {"price": 16.5, "size": 2.86}, ' \
#   '                                            {"price": 10.5, "size": 1.06}], ' \
#   '                                             "tradedVolume": []' \
#   '                     }' \
#   '                }, {"selectionId": 36714837, "handicap": 0, "status": "ACTIVE", "totalMatched": 0, "ex": {"availableToBack": [{"price": 3.4, "size": 12.08}, {"price": 4.1, "size": 2}, {"price": 5.8, "size": 2}], "availableToLay": [{"price": 21, "size": 4.4}, {"price": 12.5, "size": 2.79}, {"price": 7.8, "size": 1.48}], "tradedVolume": []}}, {"selectionId": 28601883, "handicap": 0, "status": "ACTIVE", "totalMatched": 0, "ex": {"availableToBack": [{"price": 2.06, "size": 13.39}, {"price": 2.12, "size": 1.84}, {"price": 2.56, "size": 2.05}], "availableToLay": [{"price": 3.7, "size": 13.94}, {"price": 4.8, "size": 2}, {"price": 3.75, "size": 2}], "tradedVolume": []}}' \
#   '         ]' \
#   '}'
#
# import json
# nm=json.loads(z)
# print(nm)