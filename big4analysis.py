#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
use scholarly module
TODO: Use graphx
"""

import os
import optparse
import json
import re
import time
 
if __name__ == '__main__':
    import sys
    import scholarly

    target_conf = {}
    target_conf_name = "usenix2019"
    target_committee = {}
    key_word = " ios "
    kv = {}
    with open('res.dot', 'w') as fwh:

        fwh.write("digraph G {\n")
        fwh.write('label = \"big4 Committee\"\n')

        for dirpath, dirnames, ifilenames in os.walk("./"):
            for ifilename in ifilenames:
                if ifilename.endswith(".txt") == 1:
                    confname = ifilename[:-4]
                    with open(os.path.join(dirpath, ifilename)) as frh:                        
                        for line in frh.readlines():
                            committee = re.split('[\t,]', line)
                            if confname == target_conf_name:
                                target_conf[committee[0]] = committee[1].strip()

                            if kv.has_key(committee[0]):
                                kv[committee[0]] += ", "
                                kv[committee[0]] += confname
                            else:
                                kv[committee[0]] = confname   
                            print committee[0]
                            fwh.write('\t\"' + confname + '\" -> \"' + committee[0] + '\";\n')
                    print confname
        fwh.write("}")
    os.system('/usr/local/bin/dot -Teps res.dot -o graph.eps')    
    #os.system('open graph.eps')
    print "\n"
    it = 0
    for i in reversed(range(1,5)):
        for k in kv.keys():
            if len(kv[k].split(",")) == i:
                it += 1
                print "\t" + str(it) + ". " +k + "\t" + kv[k]

    print "\n\n\t+++ " + target_conf_name + " committees info" + " +++" 
    it = 0
    for i in reversed(range(1,5)):
        for k in target_conf.keys():
            if len(kv[k].split(",")) == i:
                it += 1
                print "\t" + str(it) + ". " + k + ", " + target_conf[k] + "\t   Serve at: " + kv[k]
                
#                 try:
                search_query = scholarly.search_author(k + ", " + target_conf[k])
                author = next(search_query).fill()
#                 except:    
#                     try:
#                         search_query = scholarly.search_author(k)
#                         author = next(search_query).fill()
#                     except:
#                         print "\t\tCommittee not found"
#                         continue
                #print(author)
            
                for pub in author.publications:
                    if re.findall(key_word, pub.bib['title'], re.IGNORECASE):
                        print "\t\tKeyword in title: <" + pub.bib['title'] + ">"
                    try:
                        search_query = scholarly.search_pubs_query(pub.bib['title'])
                        abstract = next(search_query).bib['abstract']
                        # print pub.bib['title']
                        # print abstract
                        if re.findall(key_word, abstract, re.IGNORECASE):
                            print "\t\tKeyword in abstract: <" + pub.bib['title'] + ">"
                    except:
                        pass
