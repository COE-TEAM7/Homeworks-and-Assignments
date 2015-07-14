import sys
import csv
import operator

#1. Which Region have the most State Universities?
def get_region_with_most_suc():
    #print "1. The region with the most SUC is ...."
    sample = open('suc_ph.csv','r')
    dic = {}
    for index, line in enumerate(sample):
        row = line.split(',')
        if row[0] in dic:
            dic[row[0]] +=1
        else:
            dic[row[0]] = 1
    dic_list = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
    print "1. The region with the most SUC is " +dic_list[0][0]
'''lis = []
csvNew = csv.DictReader(sample)
for row in csvNew:
    #row = row.lower()
    if row['region'] not in dic:
        dic[row['region']] = 1
    else:
        dic[row['region']] +=1
for d in dic:
    lis.append(["%s" %(d), int(dic[d])])
lis = sorted(lis, key=lambda x:x[1], reverse=True)
for eachline in lis:
    print eachline'''
  
#2. Which Region have the most enrollees?
def get_region_with_most_enrollees_by_school_year(school_year):
	sample = open('suc_ph.csv','r')
	csvnew = csv.DictReader(sample)
	dic = {}
	lis = []
	for row in csvnew:
		if row['region'] not in dic:
			if row['enrolment_' + school_year].isdigit():
				dic[row['region']] = int(row['enrolment_' + school_year])
		else:
			if row['enrolment_' + school_year].isdigit():
				dic[row['region']] += int(row['enrolment_' + school_year])
	for d in dic:
		lis.append(["%s" %(d), int(dic[d])])
	lis = sorted(lis, key=lambda x: x[1], reverse=True)
	print "2. The region with the most SUC enrollees is " + lis[0][0]

#3. Which Region have the most graduates?
def get_region_with_most_graduates_by_school_year(school_year):
  #print "3. The region with the most SUC graduates is Cagayan Valley (R-II)"
	sample = open('suc_ph.csv','r')
	csvnew = csv.DictReader(sample)
	dic = {}
	lis = []
	for row in csvnew:
		if row['region'] not in dic:
			if row['graduates_' + school_year].isdigit():
				dic[row['region']] = int(row['graduates_' + school_year])
		else:
			if row['graduates_' + school_year].isdigit():
				dic[row['region']] += int(row['graduates_' + school_year])
	for d in dic:
		lis.append(["%s" %(d), int(dic[d])])
	lis = sorted(lis, key=lambda x: x[1], reverse=True)
	print "3. The region with the most SUC graduates is  " + lis[0][0]

#4 top 3 SUC who has the chepeast tuition fee by schoolyear
def get_top_3_cheapest_by_school_year(level, school_year):
    print "4. Top 3 cheapest SUC for BS level in school year 2010-2011"
    sample = open('tuitionfeeperunitsucproglevel20102013.csv','r')
    csvnew = csv.DictReader(sample)
    dic = {}
    lis = []
    for row in csvnew:
            if row['suc'] not in dic:
                    if row['first_sem_%s_%s_ab' %(school_year, level.lower())].isdigit():
                            dic[row['suc']] = float(row['first_sem_%s_%s_ab' %(school_year, level.lower())])
            else:
                    if row['first_sem' %(school_year, level.lower())].isdigit():
                            dic[row['suc']] += float(row['first_sem_%s_%s_ab' %(school_year, level.lower())])
    for d in dic:
            lis.append(["%s" %(d), float(dic[d])])
    lis = sorted(lis, key=lambda x: x[1], reverse=False)
    print " 4. " + lis[0][0]
    print " 4. " + lis[1][0]
    print " 4. " + lis[2][0]

#5 top 3 SUC who has the most expensive tuition fee by schoolyear
def get_top_3_most_expensive_by_school_year(level, school_year):
    print "5. Top 3 expensive SUC for BS level in school year 2010-2011"
    sample = open('tuitionfeeperunitsucproglevel20102013.csv','r')
    csvnew = csv.DictReader(sample)
    dic = {}
    lis = []
    for row in csvnew:
            if row['suc'] not in dic:
                    if row['first_sem_%s_%s_ab' %(school_year, level.lower())].isdigit():
                            dic[row['suc']] = float(row['first_sem_%s_%s_ab' %(school_year, level.lower())])
            else:
                    if row['first_sem' %(school_year, level.lower())].isdigit():
                            dic[row['suc']] += float(row['first_sem_%s_%s_ab' %(school_year, level.lower())])
    for d in dic:
            lis.append(["%s" %(d), float(dic[d])])
    lis = sorted(lis, key=lambda x: x[1], reverse=True)
    print " 5. " + lis[0][0]
    print " 5. " + lis[1][0]
    print " 5. " + lis[2][0]


#6 list all SUC who have increased their tuition fee from school year 2010-2011 to 2012-2013
def all_suc_who_have_increased_tuition_fee():
    sample = open('tuitionfeeperunitsucproglevel20102013.csv','r')
    csvnew = csv.DictReader(sample)
    dic = {}
    lis = []
    for row in csvnew:
            if row['suc'] not in dic:
                    if row['first_sem_2010-2011_bs_ab'].isdigit() and row['first_sem_2012-2013_bs_ab'].isdigit():
                            if row['first_sem_2010-2011_bs_ab'] < row['first_sem_2012-2013_bs_ab']:
                                    dic[row['suc']] = 1				
    print "6. List of SUC who have increased their tuition fee from school year 2010-2011 to 2012-2013"
    for d in dic:
            print "   "+ d
		
#7 which discipline has the highest passing rate?
def get_discipline_with_highest_passing_rate_by_school_year(school_year):
    print "7. The discipline which has the highest passing rate is: "
    sample = open('performancesucprclicensureexam20102012.csv','r')
    csvnew = csv.DictReader(sample)
    dic = {}
    dic2 = {}
    lis = []
    for row in csvnew:
            if row['discipline'] not in dic:
                    if row['passers_' +(school_year)].isdigit() and row['takers_' +(school_year)].isdigit() and row['discipline'] != 'Total':
                            dic[row['discipline']] = float(row['passers_' +(school_year)])# (float(row['takers_' +(school_year)]))
            if row['discipline'] not in dic2:
                    if row['passers_' +(school_year)].isdigit() and row['takers_' +(school_year)].isdigit() and row['discipline'] != 'Total':
                            dic2[row['discipline']] = (float(row['takers_' +(school_year)]))
            else:
                    if row['passers_' +(school_year)].isdigit() and row['takers_' +(school_year)].isdigit() and row['discipline'] != 'Total':
                            dic[row['discipline']] += float(row['passers_' +(school_year)])#(float(row['takers_' +(school_year)]))
                    if row['passers_' +(school_year)].isdigit() and row['takers_' +(school_year)].isdigit() and row['discipline'] != 'Total':
                            dic2[row['discipline']] += (float(row['takers_' +(school_year)]))
    for d in dic:
            lis.append(["%s" %(d), float((dic[d])/(dic2[d]))])
    lis = sorted(lis, key=lambda x: x[1], reverse=True)
    print "     " + lis[0][0]

#8 list top 3 SUC with the most passing rate by discipline by school year
def get_top_3_suc_performer_by_discipline_by_year(discipline, school_year):
    print "8. Top 3  SUC with highest passing rate in Accountancy for school year 2010-2011"
    sample = open('performancesucprclicensureexam20102012.csv','r')
    csvnew = csv.DictReader(sample)
    dic = {}
    lis = []
    for row in csvnew:
            if row['suc'] not in dic:
                if row['discipline'] == discipline:
                    if row['passers_' +(school_year)].isdigit() and row['takers_' +(school_year)].isdigit():
                            dic[row['suc']] = float(row['passers_' +(school_year)])/(float(row['takers_' +(school_year)]))
    for d in dic:
            lis.append(["%s" %(d), float(dic[d])])
    lis = sorted(lis, key=lambda x: x[1], reverse=True)
    print "   " + lis[0][0]
    print "   " + lis[1][0]
    print "   " + lis[2][0]


def main():
  get_region_with_most_suc()
  get_region_with_most_enrollees_by_school_year('2010-2011')
  get_region_with_most_graduates_by_school_year('2010-2011')
  get_top_3_cheapest_by_school_year('BS', '2010-2011')
  get_top_3_most_expensive_by_school_year('BS', '2010-2011')
  all_suc_who_have_increased_tuition_fee()
  get_discipline_with_highest_passing_rate_by_school_year('2010')
  get_discipline_with_highest_passing_rate_by_school_year('2011')
  get_discipline_with_highest_passing_rate_by_school_year('2012')
  get_top_3_suc_performer_by_discipline_by_year('Accountancy', '2011')


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
