import spotlight
from spotlight import SpotlightException
import pandas
import urllib
import time

def start():
	coursesCSVname=r'CSV\Courses.csv'
	topicsCSVname=r"CSV\Topics.csv"
	
	courses_df=pandas.read_csv(coursesCSVname, encoding='ISO-8859-1')
	courses=courses_df.to_dict('records')
	
	
	final_course_topics=list()
	cou_list = list(range(0,len(courses)))
	print(cou_list)
	added_index=40
	start=0
	while(start<len(cou_list)):
		indexes=list()
		course_topics=list()
		end=start+added_index
		
		if end>=len(cou_list):
			end=len(cou_list)
		print(start, end) 
		############################################	
		for val_llop in range(start,end):
			loop=cou_list[val_llop]
			print(loop)
			try:
				course=courses[loop]
				##courses_updated.add(course['Course Subject']+":"+str(course['Course Number']))
				topic_included=list()
				data=""
				if str(course["Course Description"]).lower()=="nan":
					data=course["Course Name"]
				else:
					data=course["Course Name"]+" "+str(course["Course Description"])
				links=spotlight.annotate('https://api.dbpedia-spotlight.org/en/annotate', data, confidence=0.5, support=20)
				##computer_topics=list()	
				for link in links:
					if link['surfaceForm'].lower() not in topic_included:
						topic=dict()
						topic['Course Subject']=course['Course Subject']
						topic['Course Number']=course['Course Number']
						topic['Course Name']=course["Course Name"]
						topic_included.append(link['surfaceForm'].lower())
						topic['Topic']=link['surfaceForm']
						topic['URI']=link['URI']
						course_topics.append(topic)
				
				
				##course_topics.extend(computer_topics)
			## repeat only if 403 is thrown
			except SpotlightException:
				continue
			except:
				indexes.append(loop)
		
			
		print("indexes",indexes)
		print(start,end)
		##to save data
		remove_lst=set()
		for loop in range(0,len(cou_list)):
			if loop>=start and loop<end:
				cou=cou_list[loop]
				if not cou in indexes:
					remove_lst.add(cou)
		
		for remove in remove_lst:
			cou_list.remove(remove)
		
		print(cou_list)
		##get data
		final_course_topics.extend(course_topics)
		time.sleep(60*3)
	
	course_topics_df=pandas.DataFrame(final_course_topics)
	course_topics_df.to_csv(topicsCSVname)
	
		
		
	
start()