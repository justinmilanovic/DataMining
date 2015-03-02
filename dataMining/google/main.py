'''
Created on Oct 23, 2014

@author: Cory
@author: Matt
'''

import urllib2
import urllib
import pprint
import nltk
import re
from apiclient.discovery import build

def getSnippets(response, output, links):
    #iterate through the keys in the query response (dictionary)
    counter = 0
    for key in response.keys():
        #items key holds the link information
        if key == "items":
            #iterate over the items dictionary
            for itemValue in response[key]:
                #iterate over the keys in that dictionary
                for itemKey in itemValue.keys():
                    #print snippet
                    if itemKey == "snippet":
                        output.write("Snippet: ")
                        output.write(repr(itemValue[itemKey]))
                        output.write("\n")
                        counter = counter + 1
                    #print if it is a link
                    elif itemKey == "link":
                        links.write("Link: ")
                        links.write(itemValue[itemKey])
                        links.write("\n\n")
    print("Amount of responses " + str(counter))
    
''' END OF getSnippets() FUNCTION '''

def processText(file, jobQuery):
    f = open(file, 'r')
    text = f.read()
    
    text = text.replace("\\n", "")
    #text = text.replace("\\xa0", "")
    #text = text.replace("\\u201c", "")
    #text = text.replace("\\u201d", "")
    #text = text.replace("u'", "")
    
    #text = re.sub("\\n$", "", text)
    #text = re.sub("\\xa0$", "", text)
    #text = re.sub("\\u201c$", "", text)
    #text = re.sub("\\u201d$", "", text)
    #text = re.sub("u'$", "", text)
    
    #print(text)
    tokens = nltk.sent_tokenize(text)
    tokens = [nltk.word_tokenize(sentence) for sentence in tokens]
    tokens = [nltk.pos_tag(word) for word in tokens]
    #print tokens
    #list: {(<NN|JJ|VB|IN|VBG>+<,>)+(<CC><NN|JJ|VB|IN|VBG>+)*}
    '''grammar = """
            comma: {<NN|JJ|VB|IN|VBG>+<,>}
            endlist: {<CC>(<NN|JJ|VB|IN|VBG>+)}
            list: {<comma>+(<endlist>)}
            
            
            
            """'''
    grammar = """
            list: {(<NN|NNS|NNP|VB|VBG|JJ|CC|PRP|IN|TO>+<,>)+}
            and: {<NN|NNS|JJ|VB|IN|VBG>*<CC><NN|NNS|JJ|VB|IN|VBG>+}
            """
            
    #grammar = "and: {(<NN|NNS|JJ|VB|IN|VBG>+<,>)+<NN|NNS|JJ|VB|IN|VBG>*<CC><NN|NNS|JJ|VB|IN|VBG>+}"
    cp = nltk.RegexpParser(grammar)
    
    for sentence in tokens:
        #break
        result = cp.parse(sentence)
        
        for node in result:
                    
            name = list(" ")
            counter = 0
            if type(node) is nltk.Tree:
                if node.label() == 'list':
                    #print node
                    #break
                    for element in node:
                        #print element[0]
                        if element[1] == ",":
                            counter = counter + 1
                            name.append("")
                            continue
                        if element[1] == "CC":
                            counter = counter + 1
                            name.append("")
                            continue
                        else:
                            if element[0] == "jobs" or element[0] == "professionals" or element[0] == "occupations"or element[0] == "as"or element[0] == "including"or element[0] == "like":
                                name[counter] = ""
                            else:
                                name[counter] = name[counter] + element[0] + " " + "(" + element[1] + ")" + " "
                              
                
                elif node.label() == 'and':
                    for element in node:
                        if element[1] == "CC":
                            counter = counter + 1
                            name.append("")
                            continue
                        else:
                            if element[0] == "jobs" or element[0] == "professionals" or element[0] == "occupations"or element[0] == "as"or element[0] == "including"or element[0] == "like":
                                name[counter] = ""
                            else:
                                name[counter] = name[counter] + element[0] + " " + "(" + element[1] + ")" + " "
                    
                                
            if len(name) == 1:
                if name[0] == " " or name[0] == "":
                    continue
            if len(name) == 2:
                if name[0] == "" and name[1] == "":
                    continue
            print name
            
''' END OF processText() FUNCTION '''

#nltk.download('all')

doQueries = True

query = " "

if not doQueries:
    processText("output/outputNew.txt", query)

#print(jobs)


api_key = "AIzaSyCHwlWEjEcdeH1KRnmIi9fq5Dnx2JBeVRw"
search_Engine_ID = "016745198537660285174:espiwqmbexg"

domain = "Information Technology"
jobSynonym = ["jobs", "occupations", "professions"]
form = ["such as", "including", "like"]

counter = 0;
query = "\"* Jobs such as Software Engineer\""

blacklist = ["\"* Information Technology occupations including\"", "\"* Information Technology occupations like\"",
             "\"* Information Technology professions such as\"", "\"* Information Technology professions including\"",
             "\"* Information Technology professions like\""]

blacklist2 = [("occupations", "including"), ("occupations", "like"), ("professions", "like")]

if doQueries:
    outputName = "outputNew"
    output = open(("output/" + outputName + ".txt"), 'w+')
    links = open(("output/" + outputName + "links.txt"), 'w+')
    
    for js in jobSynonym:
        for fm in form:
            badQuery = False
            for tuple in blacklist2:
                if js == tuple[0] and fm == tuple[1]:
                    badQuery = True
            
            if badQuery:
                continue
            
            query = "\"* " + js + " " + fm + " software engineer" +"\""
            
            if query in blacklist:
                continue
            
            print "Query is: " + query
    
    
            service = build("customsearch", "v1", developerKey=api_key)
    
            #file that will hold the output
            #will create the file if it does not exist (w+)
            counter = counter + 1
    
            response = service.cse().list(q = query, cx = search_Engine_ID).execute()
            
            getSnippets(response, output, links)
            #pprint.pprint(response, output)

        
        




