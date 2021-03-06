#!/usr/bin/env python3
from __future__ import print_function
import json
import os.path
import sys
import math

# as per the metadata file, input and output directories are the arguments
[_, reference_file, submission_file] = sys.argv

submission = json.load(open(submission_file, 'r'))
truth_values = json.load(open(reference_file, 'r'))



def calculate_a_score(truth_values, submission):
 observed = 0.0
 correct = 0.0

 total = len(truth_values.keys())

 for reference_id in truth_values.keys():
  if reference_id in submission.keys():
   observed += 1
   if submission[reference_id] == truth_values[reference_id]:
    correct += 1
  else:
   print('unmatched entry:', reference_id, '-- no response for this reference')

 return correct, total


def calculate_b_score(truth_values, submission):
 observed = 0
 correct = 0.0
 total = len(truth_values.keys())
 errors = []

 for reference_id in truth_values.keys():
  if reference_id in submission.keys():
   observed += 1
   try:
    yhat, confidence = submission[reference_id]
   except ValueError:
    print('   Each entry should be a list of two values - [veracity, confidence]')
    print('   veracity is one of "true" or "false"; confidence is a float from 0..1.')
    print('   This entry was:', submission[reference_id], ',  for document key', reference_id)
    sys.exit('-- error: data format: stopping')

   if yhat == truth_values[reference_id] and (yhat=="true" or yhat=="false"):
    correct += 1.0
    errors.append((1-confidence) ** 2)

   elif truth_values[reference_id] == 'unverified':
    errors.append((confidence) ** 2)	
   else:
    errors.append(1.0)
  else:
   print('unmatched entry:', reference_id, '-- no response for this reference')

 return correct, total, sum(errors), len(errors)


acorrect = 0
atotal = 0
bcorrect = 0
btotal = 0
bsumerrors = 0.0
blenerrors = 0

englishascore = 0
englishbscore = 0
englishbrmse = 0

danishascore = 0
danishbscore = 0
danishbrmse = 0

russianascore = 0
russianbscore = 0
russianbrmse = 0

fullsetpresent = 1

#ENGLISH

if('subtaskaenglish' in truth_values and len(truth_values['subtaskaenglish'])>0):
 if('subtaskaenglish' in submission and len(submission['subtaskaenglish'])>0):
  correct, total = calculate_a_score(truth_values['subtaskaenglish'], submission['subtaskaenglish'])
  acorrect += correct
  atotal += total
  englishascore = correct/total
  print('Task A (SDQC), English, accuracy:', englishascore)
 else:
  print('No responses found for subtask A, English')
  fullsetpresent = 0
else:
 print('No truth data found for subtask A, English')

if('subtaskbenglish' in truth_values and len(truth_values['subtaskbenglish'])>0):
 if('subtaskbenglish' in submission and len(submission['subtaskbenglish'])>0):
  correct, total, sumerrors, lenerrors = calculate_b_score(truth_values['subtaskbenglish'], submission['subtaskbenglish'])
  englishbscore = correct/total
  englishbrmse = 0
  if(lenerrors>0):
   englishbrmse = math.sqrt(sumerrors/lenerrors)
  bcorrect += correct
  btotal += total
  bsumerrors += sumerrors
  blenerrors += lenerrors
  print('Task B (veracity), English, accuracy:', englishbscore, "RMSE:", englishbrmse)
 else:
  print('No responses found for subtask B, English')
  fullsetpresent = 0
else:
 print('No truth data found for subtask B, English')


#DANISH

if('subtaskadanish' in truth_values and len(truth_values['subtaskadanish'])>0):
 if('subtaskadanish' in submission and len(submission['subtaskadanish'])>0):
  correct, total = calculate_a_score(truth_values['subtaskadanish'], submission['subtaskadanish'])
  acorrect += correct
  atotal += total
  danishascore = correct/total
  print('Task A (SDQC), Danish, accuracy:', danishascore)
 else:
  print('No responses found for subtask A, Danish')
  fullsetpresent = 0
else:
 print('No truth data found for subtask A, Danish')

if('subtaskbdanish' in truth_values and len(truth_values['subtaskbdanish'])>0):
 if('subtaskbdanish' in submission and len(submission['subtaskbdanish'])>0):
  correct, total, sumerrors, lenerrors = calculate_b_score(truth_values['subtaskbdanish'], submission['subtaskbdanish'])
  danishbscore = correct/total
  danishbrmse = 0
  if(lenerrors>0):
   danishbrmse = math.sqrt(sumerrors/lenerrors)
  bcorrect += correct
  btotal += total
  bsumerrors += sumerrors
  blenerrors += lenerrors
  print('Task B (veracity), Danish, accuracy:', danishbscore, "RMSE:", danishbrmse)
 else:
  print('No responses found for subtask B, Danish')
  fullsetpresent = 0
else:
 print('No truth data found for subtask B, Danish')


#RUSSIAN

if('subtaskarussian' in truth_values and len(truth_values['subtaskarussian'])>0):
 if('subtaskarussian' in submission and len(submission['subtaskarussian'])>0):
  correct, total = calculate_a_score(truth_values['subtaskarussian'], submission['subtaskarussian'])
  acorrect += correct
  atotal += total
  russianascore = correct/total
  print('Task A (SDQC), Russian, accuracy:', russianascore)
 else:
  print('No responses found for subtask A, Russian')
  fullsetpresent = 0
else:
 print('No truth data found for subtask A, Russian')

if('subtaskbrussian' in truth_values and len(truth_values['subtaskbrussian'])>0):
 if('subtaskbrussian' in submission and len(submission['subtaskbrussian'])>0):
  correct, total, sumerrors, lenerrors = calculate_b_score(truth_values['subtaskbrussian'], submission['subtaskbrussian'])
  russianbscore = correct/total
  russianbrmse = 0
  if(lenerrors>0):
   russianbrmse = math.sqrt(sumerrors/lenerrors)
  bcorrect += correct
  btotal += total
  bsumerrors += sumerrors
  blenerrors += lenerrors
  print('Task B (veracity), Russian, accuracy:', russianbscore, "RMSE:", russianbrmse)
 else:
  print('No responses found for subtask B, Russian')
  fullsetpresent = 0
else:
 print('No truth data found for subtask B, Russian')


ascore = 0
bscore = 0
brmse = 0
if(fullsetpresent==1 and atotal>0 and btotal>0):
 ascore = acorrect/atotal
 bscore = bcorrect/btotal
 brmse = 0
 if(blenerrors>0):
  brmse = math.sqrt(bsumerrors/blenerrors)

print('Task A (SDQC), accuracy:', ascore)
print('Task B (veracity), accuracy:', bscore, "RMSE:", brmse)





