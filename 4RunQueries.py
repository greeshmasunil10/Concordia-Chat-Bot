import rdflib

def query1(g,prefix):
	query1=	prefix+"SELECT (COUNT(*) as ?triples) WHERE { ?s ?p ?o .}"
	for row in g.query(query1):
		for c in row:
			print("Total number of triples:",c)
			
def query2(g,prefix):
	query2=	prefix+"\nSELECT ?scount ?ccount  ?tcount  WHERE{"
	query2+="{	SELECT (COUNT(DISTINCT ?student) as ?scount) WHERE { ?student rdf:type isp:Student . }		}"
	query2+="UNION {	SELECT (COUNT(DISTINCT ?course) as ?ccount) WHERE {	?course rdf:type isp:Course . }		}"
	query2+="UNION {	SELECT (COUNT(DISTINCT ?topic) as ?tcount) WHERE { ?topic rdf:type isp:Topic .}		}	}"
	arr=["students", "courses", "topics"]
	rows=g.query(query2)
	loop1=0
	for row in rows:
		loop2=0
		for c in row:
			if loop1==loop2:
				print("Total number of",arr[loop2],":",c)
					
			loop2+=1
		loop1+=1
	print()
	
def query3(g,prefix,subject,number):
	query3=prefix+'\nSELECT DISTINCT ?name ?link WHERE{ ?course rdf:type isp:Course . ?course dc:subject "'
	query3+=subject
	query3+='" . ?course dc:identifier "'
	query3+=str(number)
	query3+='" . ?course isp:hasPart ?topic . ?topic dc:source ?link . ?topic foaf:name ?name . }'
	print()
	print("TopicName           TopicLink")
	for row in g.query(query3):
		for c in row:
			print(c, end="             ")
		print()
	

def query4(g,prefix,id):
	query4=prefix+'\nSELECT ?courseSub ?courseNum ?courseName ?grade WHERE{ ?student rdf:type isp:Student . ?student dbp:id "'
	query4+=str(id)
	query4+='" . ?student isp:tookCourse ?courseGrade . ?courseGrade dbp:score ?grade . ?courseGrade dc:subject ?course . ?course foaf:name ?courseName. ?course dc:subject ?courseSub . ?course dc:identifier ?courseNum .}'
	print()
	print("CourseSubject    CourseNumber    CourseName                                Grade")
	for row in g.query(query4):
		for c in row:
			print(c,end="             ")
		print() 

def query5(g,prefix,topic):
	query5=prefix+'SELECT DISTINCT ?id (CONCAT(?firstName, " ", ?lastName) as ?name) WHERE{ ?student rdf:type isp:Student . ?student dbp:id ?id . ?student foaf:givenName ?firstName .'
	query5+=' ?student foaf:familyName ?lastName . ?student isp:tookCourse ?courseGrade. ?courseGrade dbp:score ?grade . ?courseGrade dc:subject ?course . '
	query5+=' ?course isp:hasPart ?topic . ?topic foaf:name "'
	query5+=str(topic)
	query5+='" . FILTER(?grade < "F") }'
	print()
	print("StudentID            StudentName")
	for row in g.query(query5):
		for c in row:
			print(c,end="             ")
		print() 
		
def query6(g,prefix,id):
	query6=prefix+'\nSELECT DISTINCT ?tName WHERE{ ?student rdf:type isp:Student . ?student dbp:id "'
	query6+=str(id)
	query6+='" .?student isp:tookCourse ?courseGrade. ?courseGrade dbp:score ?grade . ?courseGrade dc:subject ?course . ?course isp:hasPart ?topic .'
	query6+=' ?topic foaf:name ?tName . FILTER(?grade < "F") .}' 
	print()
	print("TopicName")
	for row in g.query(query6):
		for c in row:
			print(c)
	print()
		
def start():
	g=rdflib.Graph()
	g.parse("universityKG.ttl", format='turtle')
	g.parse("DataGraph.ttl", format='turtle')

	prefix=	"PREFIX dbr: <http://dbpedia.org/resource/>\nPREFIX db: <http://dbpedia.org/>\nPREFIX is: <http://purl.org/ontology/is/core#>\nprefix dbp: <http://dbpedia.org/property/> \nprefix dbr: <http://dbpedia.org/resource/> \nprefix dc: <http://purl.org/dc/elements/1.1/> \nprefix foaf: <http://xmlns.com/foaf/0.1/> \nprefix isp: <http://intelligentsystemproj1.io/schema#> \nprefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \nprefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> \nprefix xml: <http://www.w3.org/XML/1998/namespace> \nprefix xsd: <http://www.w3.org/2001/XMLSchema#>\n"
	print("\nPlease choose a query:\n1. Total number of triples in the KB\n2. Total number of students, courses, and topics\n3. For a course c, list all covered topics using their (English) labels and their link to DBpedia\n4. For a given student, list all courses this student completed, together with the grade\n5. For a given topic, list all students that are familiar with the topic\n6. For a student, list all topics (no duplicates) that this student is familiar with")
	inp=input()
	
	if inp=="1":
		print()
		query1(g,prefix)
	elif inp=="2":
		print()
		query2(g,prefix)
	elif inp=="3":
		print()
		subject=input("Please enter the Course Subject(like COMP): ")
		number=input("Please enter the Course Number(like 691): ")
		query3(g,prefix,subject,number)
	elif inp=="4":
		print()
		id=input("Please enter the Student id: ")
		query4(g,prefix,id)
	elif inp=="5":
		print()
		topic=input("Please enter the topic name: ")
		query5(g,prefix,topic)
	elif inp=="6":
		print()
		id=input("Please enter the Student id: ")
		query6(g,prefix,id)


start()