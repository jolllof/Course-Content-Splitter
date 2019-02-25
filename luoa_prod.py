# pylint: disable=C0301, W0105
"""this script contains a number of single task functions that simply get data from a specific  api end point and returns the entire JSON response"""
"""this script is designed so other python files/scripts can call it to get information quickly """
import os
import time
import requests

"""credentials are stored in environment variables"""
COURSE_URL = os.environ['LDOMAIN']  + 'api/v1/courses/'
ACCOUNT_URL = os.environ['LDOMAIN'] + 'api/v1/accounts/'
TOKEN = os.environ['LPT']
HEADER = {'Authorization': 'Bearer ' + '%s' % TOKEN}


def get_subaccounts(accountid):
    """this function returns a list of all subaccounts within the given account"""
    request = requests.get(ACCOUNT_URL + str(accountid) + '/sub_accounts', headers=HEADER)
    response = request.json()
    return response

def get_assignment_groups(courseid):
    """this function returns all assignment groupsfor the given course id"""
    request = requests.get(COURSE_URL + str(courseid) + '/assignment_groups', headers=HEADER)
    response = request.json()
    return response

def get_assignments(courseid):
    """this function returns all assignments for the given course id"""
    assignments = []
    page_no = 1
    loop_control = 0

    """api response is often paginated so the while statement loops  through all the pages and appends the data to a list"""
    """while loop runs until it gets to a page with less than 100 items, which would be the last page"""
    while loop_control == 0:
        request = requests.get(COURSE_URL + str(courseid) + '/assignments?per_page=100&page=' + str(page_no), headers=HEADER)
        response = request.json()

        for i in response:
            assignments.append(i)

        if len(response) >= 100:
            page_no += 1
        elif len(response) < 100:
            loop_control = 1

    return assignments

def get_enrollment_terms(accountid):
    """this function returns all active enrollment terms for the given account id"""
    request = requests.get(ACCOUNT_URL + str(accountid) + '/terms', headers=HEADER)
    response = request.json()

    return response

def get_quizzes(courseid):
    """this function returns all quizzes in a given course"""
    quizzes = []
    page_no = 1
    loop_control = 0

    """api response is often paginated so the while statement loops  through all the pages and appends the data to a list"""
    """while loop runs until it gets to a page with less than 100 items, which would be the last page"""
    while loop_control == 0:
        request = requests.get(COURSE_URL + str(courseid) + '/quizzes?per_page=100&page=' + str(page_no), headers=HEADER)
        response = request.json()

        for i in response:
            quizzes.append(i)

        if len(response) >= 100:
            page_no += 1
        elif len(response) < 100:
            loop_control = 1

    return quizzes

def get_pages(courseid):
    """this function returns all content pages in a given course id"""
    pages = []
    page_no = 1
    loop_control = 0

    """api response is often paginated so the while statement loops  through all the pages and appends the data to a list"""
    """while loop runs until it gets to a page with less than 100 items, which would be the last page"""
    while loop_control == 0:
        request = requests.get(COURSE_URL + str(courseid) + '/pages?per_page=100&page=' + str(page_no), headers=HEADER)
        response = request.json()

        for i in response:
            pages.append(i)

        if len(response) >= 100:
            page_no += 1
        elif len(response) < 100:
            loop_control = 1

    return pages

def get_courses(accountid):
    """this function returns all courses in a given account"""
    courses = []
    page_no = 1
    loop_control = 0

    """api response is often paginated so the while statement loops  through all the pages and appends the data to a list"""
    """while loop runs until it gets to a page with less than 100 items, which would be the last page"""
    while loop_control == 0:
        request = requests.get(ACCOUNT_URL + str(accountid) + '/courses?per_page=100&page=' + str(page_no), headers=HEADER)
        response = request.json()
        for i in response:
            courses.append(i)

        if len(response) >= 100:
            page_no += 1
        elif len(response) < 100:
            loop_control = 1

    return courses

def get_course_info(courseid):
    """this function return specific details on a given course"""
    request = requests.get(COURSE_URL + str(courseid), headers=HEADER)
    response = request.json()

    return response

def get_masters():
    """this function returns all master courses in the master subaccount"""
    master_courses = []
    page_no = 1
    loop_control = 0

    """api response is often paginated so the while statement loops  through all the pages and appends the data to a list"""
    """while loop runs until it gets to a page with less than 100 items, which would be the last page"""
    while loop_control == 0:
        request = requests.get(ACCOUNT_URL + '145556/courses?per_page=100&page=' + str(page_no), headers=HEADER)
        response = request.json()
        for i in response:
            master_courses.append(i)

        if len(response) >= 100:
            page_no += 1
        elif len(response) < 100:
            loop_control = 1

    return master_courses

def get_modules(courseid):
    """this function returns all modules in a given course"""
    request = requests.get(COURSE_URL + str(courseid) + '/modules?per_page=100', headers=HEADER)
    response = request.json()

    return response

def get_module_items(courseid, module_id):
    """this function returns all module items (pages, assignments, subheaders, quizzes) in a module"""
    request = requests.get(COURSE_URL + str(courseid) + '/modules/' + str(module_id) + '/items?per_page=100', headers=HEADER)
    response = request.json()

    return response

def content_migrator(old_id, new_id):
    """this function uses the content migration api endpoint to copy course content to another course"""
    payload = {"migration_type" : "course_copy_importer",
               "settings[source_course_id]" : old_id}
    request = requests.post(COURSE_URL + str(new_id) + '/content_migrations', params=payload, headers=HEADER)
    response = request.json()
    migration = response['progress_url']

    """API CALL TO CHECK AND PRINT MIGRATION PROGRESS"""
    request = requests.get(str(migration), headers=HEADER)
    progress = request.json()

    while progress[u'workflow_state'] != 'completed':
        request = requests.get(str(migration), headers=HEADER)
        mig = request.json()

        print('     %s Workflow State: %s at %s percent' % (new_id, mig[u'workflow_state'], mig[u'completion']))

        """TIME SLEEP BETWEEN THE WORKFLOW STATE OUTPUT"""
        if mig[u'completion'] != 100:
            time.sleep(30)
        elif mig[u'completion'] == 100:
            break

def content_exporter(courseid):
    """this function exports course content to be imported"""
    payload = {"export_type" : "common_cartridge"}
    request = requests.post(COURSE_URL + str(courseid) + '/content_exports', params=payload, headers=HEADER)
    response = request.json()
    export = response[u'progress_url']

    request = requests.get(str(export), headers=HEADER)
    progress = request.json()

    while progress[u'workflow_state'] != 'completed':
        request = requests.get(str(export), headers=HEADER)
        mig = request.json()

        print('\n     Workflow State: %s at %s percent' % (mig[u'workflow_state'], mig[u'completion']))
        #TIME SLEEP BETWEEN THE WORKFLOW STATE OUTPUT
        if mig[u'completion'] != 100:
            time.sleep(40)
        elif mig[u'completion'] == 100:
            break

def get_students(courseid):
    """this function returns a list of users with the student enrollment type in a given course"""
    assignments = []
    page_no = 1
    loop_control = 0
    payload = {'enrollment_type[]':'student'}

    while loop_control == 0:
        request = requests.get(COURSE_URL + str(courseid) + '/users?per_page=100&page=' + str(page_no), params=payload, headers=HEADER)
        response = request.json()
        assignments.append(response)

        if len(response) >= 100:
            page_no += 1
        elif len(response) < 100:
            loop_control = 1

    return assignments

def get_all_users(accountid):

    """this function returns all users within a course"""
    users = []
    loop_control = 0
    page_no = 1

    while loop_control == 0:
        request = requests.get(ACCOUNT_URL + str(accountid) + '/users?per_page=100&page=' + str(page_no), headers=HEADER)
        response = request.json()
        users.append(response)

    if len(response) >= 100:
        page_no += 1
    elif len(response) < 100:
        loop_control = 1

    return users
