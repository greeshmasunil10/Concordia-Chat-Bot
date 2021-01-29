import rdflib
import pandas
from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.namespace import DC, FOAF, XSD
import requests 
from bs4 import BeautifulSoup 

## to add students and course grades:
def generate_students(courses):
	students=list()
	course_grades=list()
	
	names=[	('James', 'Smith'),
			('Michael', 'Smith'),
			('Robert', 'Smith'),
			('Maria', 'Garcia'),
			('David', 'Smith'), 
			('Maria', 'Rodriguez'), 
			('Mary', 'Smith'), 
			('Maria', 'Hernandez'), 
			('Maria', 'Martinez'), 
			('James', 'Johnson'),
			('Tajinder','Singh'),
			('Vritti','Bhalla'),
			('Saloni', 'Chawla'),
			('Itti', 'Malik'),
			('Sahaj','Sharma')]
			
	
	index=0
	id=40083895
	for name in names:
		student=dict()
		
		student['FirstName']=name[0]
		student['LastName']=name[1]
		student['ID Number']=id+index
		student['Email']=name[0].lower()+name[1].lower()+"@gmail.com"
		students.append(student)
		
		grades=['F','B+','A+']
		terms=["Summer 2019", "Winter 2019", "Fall 2019"]
		for loop in range(index+0,index+3):
			if loop<len(courses):
				course_grade=dict()
				course_grade['Student ID']=id+index
				course_grade['Course ID(COMP 464)']=courses[loop]['Course Subject']+" "+courses[loop]['Course Number']
				course_grade['Grade']=grades[loop-index]
				course_grade['Term']=terms[loop-index]
				course_grades.append(course_grade)
				
		index+=1	
	return students, course_grades



## to get courses and save them in a CSV(coursesCSVname)
def get_courses(url, coursesCSVname, course_subs):
	check_credit='credits)'
	page=requests.get(url)
	bSoup = BeautifulSoup(page.content, 'html5lib') 
	req_spans = bSoup.find_all('span', {'class' : 'large-text'})
	
	spandata=list()
	for span in req_spans:
		lines=span.getText().splitlines()
		input_str=""
		for line in lines:
			line_arr=line.strip().split() 
			
			if len(line_arr)>0  and  line_arr[0] in course_subs:
				
				if len(input_str.strip())>0:
					spandata.append(input_str)
					input_str=(" ".join(line_arr))
				else:
					input_str+=(" ".join(line_arr))
				
				
			elif len(line_arr)>1  and   (line_arr[0].strip().endswith(":") and len(line_arr[0].strip())==3)  and  line_arr[1] in course_subs:
				line_arr[0]=""
				if len(input_str.strip())>0:
					spandata.append(input_str)
					input_str=(" ".join(line_arr))
				else:
					input_str+=(" ".join(line_arr))
					
			
			else:
				if len(input_str.strip())>0:
					input_str+="\n"+(" ".join(line_arr))
				else:
					input_str+=(" ".join(line_arr))
			
				
		if len(input_str.strip())>0:
			spandata.append(input_str)
			input_str=""
	
		
	for span_loop in range(0,len(spandata)):
		span=spandata[span_loop]
		lines=span.splitlines()
		
		if len(lines)>0:
			index=lines[0].find("/")
			lines1=lines[0][:index].split()
			lines2=lines[0][index+1:].split()
			if index>0 and len(lines1)>1 and len(lines2)>1 and lines1[0] in course_subs  and  lines2[0] in course_subs and lines1[1].isdigit()  and lines2[1].isdigit():
				spandata[span_loop]=""
				
				line1=" ".join(lines1)+" "+" ".join(lines2[2:])
				if len(lines)>1:
					line1+="\n"+"\n".join(lines[1:])
				spandata.append(line1)
				
				line2=" ".join(lines2)
				if len(lines)>1:
					line2+="\n"+"\n".join(lines[1:])
					
				spandata.append(line2)
				
				
	
	for span in spandata:
		span_lines=span.splitlines()
		if len(span_lines)>0:
			line_arr=span_lines[0].strip().split()
			if len(line_arr)>0  and  line_arr[0] in course_subs:
				
				if any(ch.isdigit() for ch in line_arr[1]):
					nos=line_arr[1].split("-")
					
					if len(nos)==2 and nos[0].isdigit() and nos[1].isdigit():
						for number_val in range(int(nos[0]),int(nos[1])+1):
							line_1_arr=line_arr
							line_1_arr[1]=str(number_val)
							line0=" ".join(line_1_arr)
							if len(span_lines)>1:
								line0+="\n"
								line0+="\n".join(span_lines[1:])
							spandata.append(line0)
						

	
	courses_dict=dict()
	courses_done=list()
	desp_aval=dict()
	for spanline in spandata:
		lines=spanline.splitlines()
		if len(lines)>0:
			line_arr=lines[0].split()
			if len(line_arr)>2:
				key=line_arr[0]+":"+line_arr[1]
				
				if line_arr[0] in course_subs  and  line_arr[1].isdigit():
					
					course=dict()
					startindex=lines[0].find(line_arr[2])
					check_right_value=lines[0][startindex:].strip()
					
					if (key not in courses_done or desp_aval[key]==False) or check_right_value.split()[0]==courses_dict[key]["Course Name"].strip().split()[0]:
						
						courses_done.append(key)
						index=lines[0].find(check_credit)
						if index>=0:
							course["Course Name"]=lines[0][startindex:index+len(check_credit)]
							course["Course Description"]=lines[0][index+len(check_credit):]
						else:
							course["Course Name"]=lines[0][startindex:]
							course["Course Description"]=""
						course["Course Subject"]=line_arr[0]
						course["Course Number"]=line_arr[1]
						
						
						for desp_line in range(1,len(lines)):
							course["Course Description"]+=" "+lines[desp_line]
							
						
						course["Link"]=str(url)
						course_name_arr=course["Course Name"].split()
						for update_loop in range(0,len(course_name_arr)):
							if any(ch.isalpha() for ch in course_name_arr[update_loop]):
								break
							else:
								course_name_arr[update_loop]=""
								
						course["Course Name"]=" ".join(course_name_arr)
						
						course_name_arr=course["Course Name"].split()
						
						if len(course["Course Description"].strip())<2:
							course["Course Description"]=""
							desp_aval[key]=False
						else:
							desp_aval[key]=True
						if course_name_arr[0][:1].isalpha() and course_name_arr[0][:1].isupper():
							courses_dict[key]=course
						elif not course_name_arr[0][:1].isalpha():
							courses_dict[key]=course
						else:
							courses_done.remove(key)
							continue
						
						
	
	return courses_dict
	
def start(urls, course_subs):
	
	##CSV files to be created
	universitiesCSVname=r"CSV\Universities.csv"
	coursesCSVname=r'CSV\Courses.csv'
	topicsCSVname=r"CSV\Topics.csv"
	studentsCSVname=r"CSV\Students.csv"
	gradesCSVname=r"CSV\Grades.csv"

	##to get courses and create Courses CSV
	courses_d=dict()
	crs=list()
	for url in urls:
		try:
			in_course_dict=get_courses(url, coursesCSVname, course_subs)
			crs.extend(in_course_dict.values())
			for key in in_course_dict.keys():
				if key in courses_d:
					courses_d[key].append(in_course_dict[key])
				else:
					courses_d[key]=list()
					courses_d[key].append(in_course_dict[key])
		except:
			continue
	
	courses=list()
	for key in courses_d.keys():
		enter=False
		for course in courses_d[key]:
			if len(course["Course Description"].strip())>2:
				courses.append(course)
				enter=True
				break
		
		if not enter:
			courses.append(courses_d[key][0])
		
	print("Total number of courses:",len(courses))
	##to save courses
	courses_df=pandas.DataFrame(courses)
	courses_df.to_csv(coursesCSVname, encoding='utf-8-sig')
	
	## courses only taken 10 for now
	students, course_grades=generate_students(courses[:10])
	##to save  

	students_df=pandas.DataFrame(students)
	students_df.to_csv(studentsCSVname, encoding='utf-8-sig')
	
	##to save course and grades
	course_grades_df=pandas.DataFrame(course_grades)
	course_grades_df.to_csv(gradesCSVname, encoding='utf-8-sig')

urls=	["https://www.concordia.ca/academics/graduate/calendar/current/encs/computer-science-courses.html",
		"https://www.concordia.ca/academics/graduate/calendar/current/encs/engineering-courses.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/ahsc-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/ahsc-dip.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/biol-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/biol-msc.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/biol-dip.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/sgs/unit.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/sgs/indi-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/sgs/indi-ma-msc.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/busiadmi.html", ## ADMI 800-809 Business Economics
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/msc-ds-mis.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/emba.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/finance-msc.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/mim.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/giim.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/management-msc.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/marketing-msc.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/mba.html",##MBA 645: 
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/msc.html", ## MSCA 615
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/mscm.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/gdba.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/acco.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/diim.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/gcba.html",##GDBA 531 Professional Business Skills
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/gce.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/jmsb/gcqbs.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/arte-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/arte-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/arth-phd.html", ##A1: ARTH 809 Art History and Its MethodologiesARTH
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/arth-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/cats-art.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/cats-drama.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/cats-music.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/mthy-dip.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/fmst-phd.html",##FMST 805/FMST 605 Topics in English Canadian Cinema
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/fmst-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/star.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/cptp.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/musi.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/cptp.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/dart-mdes.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fofa/dart-cert.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/chem-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/chem-msc.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/span.html", ##SPAN 631-640 Topics in Spanish Translation (3 credits)
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/coms-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/coms-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/coms-dip.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/econ-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/econ-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/econ-dip.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/educ-phd.html",	
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/apli-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/chst-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/estu-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/etec-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/adip-dip.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/etec-dip.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/engl-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/engl-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/flit-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/ftra-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/ftra-dip.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/fraa-cert.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/ftra-cert.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/geog-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/geog-menv.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/geog-msc.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/geog-dip.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/exci-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/exci-msc.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/hist.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/hist-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/huma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/jour-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/jour-dip.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/jour-visual-dip.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/mast-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/mast-ma-msc.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/mast-mtm.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/phil.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/phys-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/phys-msc.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/poli-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/poli-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/poli-mpppa.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/psyc-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/psyc-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/psyc-dip.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/reli-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/reli-judaic-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/reli-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/scpa-ced.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/scpa-dec.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/socianth-phd.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/socianth-ma.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/theo.html",
		"http://www.concordia.ca/academics/graduate/calendar/current/fasc/soci-ma.html"]

print("Total number of urls:",len(urls))
course_subs=["ADIP", "APLI", "AMPS", "ASEM", "ARTH", "ATRP", "ACCO", "AHSC", "ARTE", "ADMI", "ANTH", 
			"BLDG", "BCEE", "BSTA", "BTM", "BIO", "BIOL", 
			"COEN", "CIVI", "CHME", "CHEM", "CATS", "COMS", "CHST", "COMP", "COMM", "CERA", "CPTP", 
			"DTHY", "DART", "DISP", "EMBA", "ENCS", "ESTU", "ENVS", "EXCI", 
			"ETEC", "ENGL", "ECON", "EDUC", "ENGR", "ELEC", 
			"FINA", "FMST", "FMPR", "FRAA", "FLIT", "FTRA", "FBRS", 
			"GEOG", "GIIM", "GDBA", "GCE",
			"HENV", "HEXS", "HIST", "HUMA",
			"INDI", "IMCA", "INDU", "INSE", "INTP", "INDS", 
			"JOUR", 
			"MECH", "MBA", "MSCA", "MANA", "MARK", "MBA", "MTHY", "MSCM", "MAST", "MATH",
			"PRIN", "PHIL", "PTNG", "PROJ", "PHYS", "PHOT", "POLI", "PSYC", 
			"RELI", 
			"SOEN", "SCUL", "SPAN", "SCOM", "SCPA", "SOCI", "SOAN",
			"THEO",
			"UNIT"]
start(urls, course_subs)
print("done")