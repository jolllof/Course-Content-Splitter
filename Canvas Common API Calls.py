import requests
import time
import os
import re

course_url = 'https://[INSERT account name].instructure.com/api/v1/courses/'
account_url = 'https://[INSERT account].instructure.com/api/v1/accounts/'
token = '[INSET TOKEN]'
header = {'Authorization': 'Bearer ' + '%s' % token}



def Get_SubAccounts(Account_ID):
    request = requests.get(account_url + str(Account_ID) + '/sub_accounts', headers = header )
    response = request.json()
    return response


def Get_Assignment_Groups(Course_ID):
    request = requests.get(course_url + str(Course_ID) + '/assignment_groups', headers = header)
    response = request.json()
    return response


def Get_Assignments(Course_ID):
    assignments = []
    page_no = 1 
    loop_control = 0

    while loop_control == 0:
        request = requests.get(course_url + str(Course_ID) + '/assignments?per_page=100&page=' + str(page_no), headers = header )
        response = request.json()

        for i in response:
            assignments.append(i)

        if len(response)>= 100:
            page_no +=1
        elif len(response) < 100:
            loop_control = 1;

    return assignments

def Get_Quizzes(Course_ID):
    quizzes = []
    page_no = 1 
    loop_control = 0

    while loop_control == 0:
        request = requests.get(course_url + str(Course_ID) + '/quizzes?per_page=100&page=' + str(page_no), headers = header )
        response = request.json()

        for i in response:
            quizzes.append(i)

        if len(response)>= 100:
            page_no +=1
        elif len(response) < 100:
            loop_control = 1;

    return quizzes
    
def Get_Pages(Course_ID):
    pages = []
    page_no = 1 
    loop_control = 0

    while loop_control == 0:
        request = requests.get(course_url + str(Course_ID) + '/pages?per_page=100&page=' + str(page_no), headers = header )
        response = request.json()

        for i in response:
            pages.append(i)

        if len(response)>= 100:
            page_no +=1
        elif len(response) < 100:
            loop_control = 1;

    return pages

    
def Get_Courses(Account_ID):
    courses = []
    #payload = {'with_enrollments':'True', 'published':'True', 'completed':'False', 'hide_enrollmentless_courses':'True', 'state[]':"available"}
    page_no = 1 
    loop_control = 0

    while loop_control == 0:
        request = requests.get(account_url + str(Account_ID) + '/courses?per_page=100&page=' + str(page_no), headers = header)
        response = request.json()
        for i in response:
            courses.append(i)
        
        if len(response)>= 100:
            page_no +=1
        elif len(response) < 100:
            loop_control = 1;

    return courses

def Get_Course_Info(Course_ID):
    request = requests.get(course_url + str(Course_ID), headers = header )
    response = request.json()

    return response

def Get_Masters():
    master_courses = []
    page_no = 1 
    loop_control = 0

    while loop_control == 0:
        request = requests.get(account_url + '145556/courses?per_page=100&page=' + str(page_no),  headers = header)
        response = request.json()
        for i in response:
            master_courses.append(i)

        if len(response)>= 100:
            page_no +=1
        elif len(response) < 100:
            loop_control = 1;

    return master_courses
    
def Get_Modules(Course_ID): 
    request = requests.get(course_url + str(Course_ID) + '/modules?per_page=100', headers = header ) #API FOR MODULE INFO
    response = request.json()
    
    return response

def Get_Module_Items(Course_ID, module_id):
    request = requests.get(course_url + str(Course_ID) + '/modules/' + str(module_id) + '/items?per_page=100', headers = header ) #API FOR MODULE INFO
    response = request.json()

    return response

def Content_Migrator(old_id, new_id): 
    #API CALLS TO MIGRATE CONTENT
    payload = {"migration_type" : "course_copy_importer",
               "settings[source_course_id]" : old_id}
    request = requests.post(course_url + str(new_id) + '/content_migrations', params = payload, headers = header)
    response = request.json()
    migration = response['progress_url']

    #API CALL TO CHECK AND PRINT MIGRATION PROGRESS
    request = requests.get(str(migration), headers = header)
    progress = request.json()
    
    while progress[u'workflow_state'] != 'completed':
        request = requests.get(str(migration), headers = header)
        g = request.json()
        
        print '     %s Workflow State: %s at %s percent' % ( new_id, g[u'workflow_state'], g[u'completion'])
        
        #TIME SLEEP BETWEEN THE WORKFLOW STATE OUTPUT
        if g[u'completion'] != 100:
            time.sleep(30)
        elif g[u'completion'] == 100:
            break


def Content_Exporter(Course_ID):
    payload = {"export_type" : "common_cartridge"}
    request = requests.post(course_url + str(Course_ID) + '/content_exports', params = payload, headers = header)
    response = request.json()
    export = response[u'progress_url']

    request = requests.get(str(export), headers = header)
    progress = request.json()

    while progress[u'workflow_state'] != 'completed':
        request = requests.get(str(export), headers = header)
        g = request.json()
        
        print '\n     Workflow State: %s at %s percent' % (g[u'workflow_state'], g[u'completion'])
        
        #TIME SLEEP BETWEEN THE WORKFLOW STATE OUTPUT
        if g[u'completion'] != 100:
            time.sleep(40)
        elif g[u'completion'] == 100:
            break


def Get_Students(Course_ID):
    assignments = []
    page_no = 1 
    loop_control = 0
    payload = {'enrollment_type[]':'student'}

    while loop_control == 0:
        request = requests.get(course_url + str(Course_ID) + '/users?per_page=100&page=' + str(page_no), params = payload, headers = header )
        response = request.json()
        assignments.append(response)

        if len(response)>= 100:
            page_no +=1
        elif len(response) < 100:
            loop_control = 1;

    return assignments


def Get_All_Users(Account_ID):
    users = []
    loop_control = 0                 
    page_no = 1

    while loop_control == 0:
        request = requests.get(account_url + str(Account_ID) + '/users?per_page=100&page=' + str(page_no), headers = header)
        response = request.json()
        users.append(response)

    if len(response)>= 100:
            page_no +=1
    elif len(response) < 100:
            loop_control = 1;

    return users
