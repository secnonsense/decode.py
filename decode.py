#!/usr/bin/python

import sys, os, base64, re, urllib, string, argparse

os.system('clear')

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--base64", help="For base64 decoding", action="store_true")
parser.add_argument("-u", "--urldecode", help="For URL decoding", action="store_true")
parser.add_argument("-r", "--ROTdecode", help="For rot decoding", action="store_true")
parser.add_argument("TEXT", help="Enter a string to decode in quotes")
args = parser.parse_args()

match, words, store_result, result, content, guess, guessmatch, = ([] for c in range(7))
tab = bestmatch = 0
dictionary="./dictionary.txt"
answer=""

def rotate(strg,n):
    return strg[n:] + strg[:n]

ualpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lalpha="abcdefghijklmnopqrstuvwxyz"


def b64match(strg, search=re.compile(r'[^A-Za-z0-9\+\/=]').search):
    return not bool(search(strg))

def urlmatch(strg, search=re.compile('[^%A-Za-z0-9]').search):
    return not bool(search(strg))

with open(dictionary) as dic:
    content = dic.readlines()
content = [j.strip() for j in content]

y=args.TEXT.strip()

print "\nOriginal Text: \n\n" + y

while answer != "done":
    
    dtest=y.split()
        
    for i in range (0,len(dtest)):
            for o in range (0, len(content)):
                if len(dtest[i]) >= 3 and dtest[i].lower()==content[o].lower():
                    match.append(dtest[i])
                    
    if match:
            answer="done"
            break
            
    vdict={}

    unique = list(set(y))

    unique.sort()

    print "\nAlphabet: ",

    for x in range(0, len(unique)):
        print unique[x] + " ",
        count=0
        for z in range(0,len(y)): 
            if unique[x] == y[z]:
                count=count+1
        vdict[unique[x]]=count  

    print '\n'

    print "Number of Total Characters: " + str(len(y)) + "\n"

    for (key, value) in sorted(vdict.items(), key=lambda (k, v): v, reverse=True):
        tab = tab+1
        if tab % 4 == 0:
           print "Value = %s, Count = %s\n" % (key, value),
        else:
           print "Value = %s, Count = %s\t" % (key, value),

    print '\n'


    if (len(y) % 4 == 0 and b64match(y) == 1) or args.base64:
        print "Mathematically and based on the character-set this could be base64 encoded.  Attempting decoding:\n"
        answer = base64.b64decode(y)
        print answer + "\n"
        y = answer
        if args.base64:
            quit()

    elif (urlmatch(y) == 1 and "%" in y) or args.urldecode:
        print "Based on the character-set this could be URL encoded.  Attempting decoding:\n"
        answer = urllib.unquote_plus(y)
        if answer == y:
            print "This is not URL encoded\n"
            answer = "done"	
            break
        print answer + "\n"
        y = answer
        if args.urldecode:
            quit()    

    elif len(y.split()) > 1 or args.ROTdecode:
        print "There are spaces in this string.  Checking to see if the space delimited text contains ROT encoded dictionary words\n"
        
        for counter in range(25):
           m=0
           match=[]
           rotualpha=rotate(ualpha,1)
           rotlalpha=rotate(lalpha,1)

           lrotualpha=re.findall('.............',rotualpha)
           lrotlalpha=re.findall('.............',rotlalpha)

           transform=lrotualpha[0] + lrotlalpha[0] + lrotualpha[1] + lrotlalpha[1]

           rot = string.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", transform)
           result=string.translate(y, rot).split()
           store_result.append(result)
           for x in range (0,len(result)):
              for g in range (0, len(content)):
                 if len(result[x]) >= 3 and result[x].lower()==content[g].lower():
                    m=m+1
                    match.append(result[x])
              if m > bestmatch:
                bestmatch=m
                guess=result
                guessmatch=match
                rotnum=counter + 1

           ualpha=rotualpha
           lalpha=rotlalpha

        if guess:
           print "this was rot" + str(rotnum) + "\n"
           answer = ' '.join(str(e) for e in guess)
           print answer + "\n"
           matches = ' '.join(str(q) for q in guessmatch)
           print "Matching Words: " + matches + "\n"
           answer = "done"
    else:
        print "No guess\n"
        answer = "done"
    if args.ROTdecode:
        quit()    
