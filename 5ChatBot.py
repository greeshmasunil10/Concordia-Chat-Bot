import rdflib
import re

def query1(g,prefix,subject,number):
    query1=prefix+'\nSELECT ?desp WHERE{ ?course rdf:type isp:Course . ?course dc:subject "'
    query1+=subject
    query1+='" . ?course dc:identifier "'
    query1+=number
    query1+='"  . ?course dc:description ?desp . }'
    enter=False
    for row in g.query(query1):
        enter=True
        print(subject,number,"has following description:\n")
        for c in row:
            print(c.strip())
    if not enter:
        print("I am sorry there is not such course in my database.") 
			
def query2a(g,prefix,id):
    query2=prefix+'\nSELECT ?subject ?number ?cname ?grade ?term WHERE{ ?student rdf:type isp:Student . ?student dbp:id "'
    query2+=str(id)
    query2+='" . ?student isp:tookCourse ?courseGrade. ?courseGrade dbp:termPeriod ?term . ?courseGrade dbp:score ?grade . ?courseGrade dc:subject ?course . '
    query2+=' ?course dc:subject ?subject . ?course dc:identifier ?number . ?course foaf:name ?cname . }' 
    enter=False
    
    loop=0
    for row in g.query(query2):
        enter=True
        if loop==0:
            print(id, "took following courses:\n")
        print(row[0],row[1],row[2],"got a grade", row[3], "in", row[4],".")
        loop+=1
    if not enter:
        print(id, "took no courses.")

def query2b(g,prefix,first,last):
    query2=prefix+'\nSELECT ?subject ?number ?cname ?grade ?term '
    query2+=' WHERE{ ?student rdf:type isp:Student . ?student foaf:givenName "'
    query2+=first
    query2+='" . ?student foaf:familyName "'
    query2+=last
    query2+='" . ?student isp:tookCourse ?courseGrade . ?courseGrade dbp:score ?grade . ?courseGrade dbp:termPeriod ?term . ' 
    query2+='?courseGrade dc:subject ?course . ?course dc:subject ?subject . ?course dc:identifier ?number . '
    query2+='?course foaf:name ?cname . }'
    enter=False
    
    loop=0
    for row in g.query(query2):
        enter=True
        if loop==0:
            print(first,last, "took following courses:\n")
        print(row[0],row[1],row[2],"got a grade", row[3], "in", row[4], ".")
        loop+=1
    if not enter:
        print(id, "took no courses.")
	
	
def query3(g,prefix,topic_name):
    query3=prefix+'\nSELECT  ?subject  ?number  ?name '
    query3+=' WHERE{ ?course rdf:type isp:Course . ?course dc:subject ?subject . '
    query3+=' ?course dc:identifier ?number . ?course foaf:name ?name . ?course isp:hasPart ?topic . ?topic foaf:name "'
    query3+=topic_name
    query3+='" . }'
    enter=False
    loop=0
    for row in g.query(query3):
        enter=True
        if loop==0:
            print(topic_name,"is covered in following courses:\n")
        print(row[0],row[1],row[2])
        loop+=1
    if not enter:
        print(topic_name,"is not covered in any courses.")
	

def query4(g,prefix,topic):
    query4=prefix+'SELECT DISTINCT ?id (CONCAT(?firstName, " ", ?lastName) as ?name) WHERE{ ?student rdf:type isp:Student . ?student dbp:id ?id . ?student foaf:givenName ?firstName .'
    query4+=' ?student foaf:familyName ?lastName . ?student isp:tookCourse ?courseGrade. ?courseGrade dbp:score ?grade . ?courseGrade dc:subject ?course . '
    query4+=' ?course isp:hasPart ?topic . ?topic foaf:name "'
    query4+=str(topic)
    query4+='" . FILTER(?grade < "F") . }'
    enter=False
    loop=0
    for row in g.query(query4):
        enter=True
        if loop==0:
            print("Following students are familiar with",topic,":\n")
        print(row[0],row[1])
        loop+=1
    if not enter:
        print("No student is familiar with",topic)

def query5a(g,prefix,id):
    query5=prefix+'\nSELECT DISTINCT ?tName WHERE{ ?student rdf:type isp:Student . ?student dbp:id "'
    query5+=str(id)
    query5+='" .?student isp:tookCourse ?courseGrade. ?courseGrade dbp:score ?grade . ?courseGrade dc:subject ?course . ?course isp:hasPart ?topic .'
    query5+=' ?topic foaf:name ?tName . FILTER(?grade < "F") .}' 
    enter=True
    loop=0
    for row in g.query(query5):
        enter=True
        if loop==0:
            print(id,"knows:\n")
        for c in row:
            print(c)
        loop+=1
    if not enter:
        print(id, "knows no topic.")

def query5b(g,prefix,first,last):
    query5=prefix+'\nSELECT DISTINCT ?tName WHERE{ ?student rdf:type isp:Student . ?student foaf:givenName "'
    query5+=first
    query5+='" . ?student foaf:familyName "'
    query5+=last
    query5+='" . ?student isp:tookCourse ?courseGrade. ?courseGrade dbp:score ?grade . ?courseGrade dc:subject ?course . ' 
    query5+='?course isp:hasPart ?topic . ?topic foaf:name ?tName . FILTER(?grade < "F") . }'
    enter=True
    loop=0
    for row in g.query(query5):
        enter=True
        if loop==0:
            print(first,last,"knows:\n")
        for c in row:
            print(c)
        loop+=1
    if not enter:
        print(first,last, "knows no topic.")
    
def start():
    g=rdflib.Graph()
    g.parse("universityKG.ttl", format='turtle')
    g.parse("DataGraph.ttl", format='turtle')
    
    prefix=	"PREFIX dbr: <http://dbpedia.org/resource/>\nPREFIX db: <http://dbpedia.org/>\nPREFIX is: <http://purl.org/ontology/is/core#>\nprefix dbp: <http://dbpedia.org/property/> \nprefix dbr: <http://dbpedia.org/resource/> \nprefix dc: <http://purl.org/dc/elements/1.1/> \nprefix foaf: <http://xmlns.com/foaf/0.1/> \nprefix isp: <http://intelligentsystemproj1.io/schema#> \nprefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \nprefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> \nprefix xml: <http://www.w3.org/XML/1998/namespace> \nprefix xsd: <http://www.w3.org/2001/XMLSchema#>\n"
    
    
    while(True):
        print("\nPlease enter the query (Please type 0 to exit):")
        inp=input().strip()
        print()
        ##ques1
        out=re.search(r'^what(\s)*is(\s)*the(\s)*(?P<course>.*\b\w*\b)(\s)*about(\s)*\?$', inp, re.IGNORECASE)
        if out is not None:
            csubject,cnumber=out.group('course').split()
            query1(g,prefix,csubject.upper(),cnumber)
            continue
        
        ##ques2
        out=re.search(r'^which(\s)*courses(\s)*did(\s)*(?P<student>.*\b\w*\b)(\s)*take(\s)*\?$', inp, re.IGNORECASE)
        if out is not None:
            student=out.group('student').strip()
            if student.isdigit():
                query2a(g,prefix,int(student))
            else:
                first,last=student.split()
                query2b(g,prefix,first,last)
            continue

        ##ques3
        out=re.search(r'^which(\s)*courses(\s)*cover(\s)*(?P<topic>.*\b\w*\b)(\s)*\?$', inp, re.IGNORECASE)
        if out is not None:
            topic=out.group('topic').strip()
            query3(g,prefix,topic)
            continue

        ##ques4
        out=re.search(r'^who(\s)*is(\s)*familiar(\s)*with(\s)*(?P<topic>.*\b\w*\b)(\s)*\?$', inp, re.IGNORECASE)
        if out is not None:
            topic=out.group('topic').strip()
            query4(g,prefix,topic)
            continue

        ##ques5
        out=re.search(r'^what(\s)*does(\s)*(?P<student>.*\b\w*\b)(\s)*know(\s)*\?$', inp, re.IGNORECASE)
        if out is not None:
            student=out.group('student').strip()
            if student.isdigit():
                query5a(g,prefix,int(student))
            else:
                first,last=student.split()
                query5b(g,prefix,first,last)
        
        ##exit
        if inp.isdigit()  and  int(inp)==0:
            break

        
	
start()