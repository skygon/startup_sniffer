#coding=utf-8
import json

round_plus = {}
round_plus['19'] = 'Pre-IPO'
round_plus['20'] = u'新三板'
round_plus['21'] = u'新三板定增'
round_plus['40'] = 'IPO'
round_plus['41'] = u'上市'
round_plus['50'] = u'并购'
round_plus['60'] = u'战略投资'

print json.dumps(round_plus, ensure_ascii=False)