import rdflib
import pandas
from rdflib import Graph, Namespace, RDF, RDFS, BNode, Literal, URIRef
from rdflib.namespace import DC, FOAF, XSD
import math

def create_university(kGraph, universityClass, ISPData):
	extend="1"+"_".join("Concordia University".split())
	universityInstance=URIRef(ISPData+"university/"+extend)
	kGraph.add((universityInstance, RDF.type, universityClass))
	kGraph.add((universityInstance, FOAF.name, Literal(str("Concordia University"))))
	kGraph.add((universityInstance, DC.source, Literal(str("http://dbpedia.org/page/Concordia_University"))))
	
	return kGraph, universityInstance

def create_courses(courses, kGraph, universityInstance, courseClass, ISPData, ISPSchema):
	courseIntances_id=dict()
	
	for loop in range(0,len(courses)):
		course=courses[loop]
		
		key=course['Course Subject']+":"+str(course['Course Number'])
		extend=course['Course Subject']+"_"+str(course['Course Number'])
		courseInstance=URIRef(ISPData+"courses/"+str(loop)+extend)
		kGraph.add((courseInstance, RDF.type, courseClass))
		kGraph.add((courseInstance, FOAF.name, Literal(str(course['Course Name']))))
		kGraph.add((courseInstance, DC.subject, Literal(str(course['Course Subject']))))
		kGraph.add((courseInstance, DC.identifier, Literal(course['Course Number'])))
		desp=course['Course Description']
		if type(desp)==float:
			desp=""
		kGraph.add((courseInstance, DC.description, Literal(desp)))
		kGraph.add((courseInstance, RDFS.seeAlso, Literal(str(course['Link']))))
		kGraph.add((universityInstance, ISPSchema.coversCourse, courseInstance))
		courseIntances_id[key]=courseInstance
	return kGraph, courseIntances_id
	

def create_topics(courseIntances_id, kGraph, topicClass, topics, ISPData, ISPSchema):
	
	ins=0
	for loop in range(0,len(topics)):
		topic=topics[loop]
		
		key=topic['Course Subject']+":"+str(topic['Course Number'])
		if key in courseIntances_id:
			extend="_".join(topic['Topic'].split())
			topicInstance=URIRef(ISPData+"topics/"+str(loop)+extend)
			ins+=1
			kGraph.add((topicInstance, RDF.type, topicClass))
			kGraph.add((topicInstance, FOAF.name, Literal(str(topic['Topic']))))
			kGraph.add((topicInstance, DC.source, Literal(str(topic['URI']))))
			kGraph.add((courseIntances_id[key], ISPSchema.hasPart, topicInstance))
	
	print(ins)
	return kGraph
	
	
def create_students(kGraph, studentClass, students, universityInstance, ISPData, ISPSchema, DBP):
	studentIntances_id=dict()
	
	for loop in range(0,len(students)):
		student=students[loop]
		
		key=str(student['ID Number'])
		extend=str(student['ID Number'])
		studentInstance=URIRef(ISPData+"students/"+extend)
		kGraph.add((studentInstance, RDF.type, studentClass))
		kGraph.add((studentInstance, FOAF.givenName, Literal(str(student['FirstName']))))
		kGraph.add((studentInstance, FOAF.familyName, Literal(str(student['LastName']))))
		kGraph.add((studentInstance, DBP.id, Literal(str(student['ID Number']))))
		kGraph.add((studentInstance, FOAF.mbox, Literal(str(student['Email']))))
		kGraph.add((studentInstance, ISPSchema.studiesAt, universityInstance))
		studentIntances_id[key]=studentInstance
		
	
	return kGraph, studentIntances_id
	
def create_grades(kGraph, gradeClass, grades, studentIntances_id, DBP, courseIntances_id, ISPData, ISPSchema):
	
	for loop in range(0,len(grades)):
		grade=grades[loop]
		
		keyStudent=str(grade['Student ID'])
		keyCourse=":".join(grade['Course ID(COMP 464)'].split())
		
		if keyStudent in studentIntances_id and keyCourse in courseIntances_id:
			gradeInstance=URIRef(ISPData+"course_grades/"+str(loop))
			kGraph.add((gradeInstance, RDF.type, gradeClass))
			kGraph.add((gradeInstance, DC.subject, courseIntances_id[keyCourse]))
			kGraph.add((gradeInstance, DBP.score, Literal(str(grade['Grade']))))
			kGraph.add((gradeInstance, DBP.termPeriod, Literal(str(grade['Term']))))
			kGraph.add((studentIntances_id[keyStudent], ISPSchema.tookCourse, gradeInstance))
			
	
	return kGraph
	
	
	
	
baseGraphFile="universityKG.ttl"

kGraph=Graph()
kGraph.parse(baseGraphFile, format="ttl")
	
DBP=Namespace("http://dbpedia.org/property/")
ISPSchema=Namespace("http://intelligentsystemproj1.io/schema#")
ISPData=Namespace("http://intelligentsystemproj1.io/data/")

##CSV files to be created
universitiesCSVname=r"CSV\Universities.csv"
coursesCSVname=r'CSV\Courses.csv'
topicsCSVname=r"CSV\Topics.csv"
studentsCSVname=r"CSV\Students.csv"
gradesCSVname=r"CSV\Grades.csv"

courseClass	=	ISPSchema.Course
universityClass	=	ISPSchema.University
topicClass	=	ISPSchema.Topic
studentClass	=	ISPSchema.Student
gradeClass	=	ISPSchema.CourseGrade

courses	=	pandas.read_csv(coursesCSVname).to_dict('records')
topics	=	pandas.read_csv(topicsCSVname).to_dict('records')
students	=	pandas.read_csv(studentsCSVname).to_dict('records')
grades	=	pandas.read_csv(gradesCSVname).to_dict('records')

kGraph, universityInstance	=	create_university(kGraph, universityClass, ISPData)
kGraph, courseIntances_id	=	create_courses(courses, kGraph, universityInstance, courseClass, ISPData, ISPSchema)
kGraph	=	create_topics(courseIntances_id, kGraph, topicClass, topics, ISPData, ISPSchema)
kGraph, studentIntances_id	=	create_students(kGraph, studentClass, students, universityInstance, ISPData, ISPSchema, DBP)
kGraph	=	create_grades(kGraph, gradeClass, grades, studentIntances_id, DBP, courseIntances_id, ISPData, ISPSchema)
kGraph.serialize(destination='DataGraph.ttl', format='turtle')

	
