# pylint: disable=C0301, W0105
"""This python file takes a full year course duplicates it into two semester courses, removes second half of content from the first course and vice versa"""
""" and then renames the assignments in the second course"""
import os
"""the module below is a code file in the same directory that contains some of my often used api """
"""single task functions have be created to simply get information from the api endpoint"""
"""the module also holds api headers, and other modules such as requests, time etc."""
from luoa_prod import requests, HEADER, get_modules, get_assignments, get_course_info, time, get_module_items, COURSE_URL, ACCOUNT_URL


"""the call below simply clears command line before each run so I don't have to manually clear the results each time"""
os.system('cls')


def createsemestershells(course_id):
    """the purpose of this function is to create two course shells in the Canvas based on information received"""
    """from an user_inputted course id and then returns the course ids for other functions tom ake further modifications"""
    print('COURSE SPLITTAAAA :D'.center(85))


    """Get Course Info is a module that exists in LUOA_Prod.py file. It returns basic course info such as name, course code, account id, course id etc"""
    course_inf = get_course_info(course_id)

    first_name = course_inf[u'name'].replace('_Staging', ' - First Semester_Staging')
    first_code = course_inf[u'course_code'].replace('0_Staging', '1_Staging')

    second_name = course_inf[u'name'].replace('_Staging', ' - Second Semester_Staging')
    second_code = course_inf[u'course_code'].replace('0_Staging', '2_Staging')

    payload = {'course[account_id]' : course_inf[u'account_id'],
               'course[name]' : first_name,
               'course[course_code]' : first_code,
               'offer': True}
    request = requests.post(ACCOUNT_URL + str(course_inf[u'root_account_id'])  + '/courses', params=payload, headers=HEADER)
    course_one = request.json()

    payload = {'course[account_id]' : course_inf[u'account_id'],
               'course[name]' : second_name,
               'course[course_code]' : second_code,
               'offer': True}
    request = requests.post(ACCOUNT_URL + str(course_inf[u'root_account_id'])  + '/courses', params=payload, headers=HEADER)
    course_two = request.json()

    print('CREATED: {0} [{1}]'.format(course_one[u'name'], str(course_one[u'id'])))
    print('CREATED: {0} [{1}]'.format(course_two[u'name'], str(course_two[u'id'])))

    return(course_one[u'id'], course_two[u'id'])


def content_migrator(course_id, first_sem_id, second_sem_id):
    """content_migrator function copies course content from the user inputted course into the two newly created courses"""
    source = course_id
    first_sem = first_sem_id
    second_sem = second_sem_id

    """API calls to migrate content into the two new courses. from the response a progress url is returned to check on the status of the migration"""
    payload = {"migration_type" : "course_copy_importer",
               "settings[source_course_id]" : source}
    request = requests.post(COURSE_URL + str(first_sem) + '/content_migrations', params=payload, headers=HEADER)
    response = request.json()
    migration1 = response['progress_url']

    payload = {"migration_type" : "course_copy_importer",
               "settings[source_course_id]" : source}
    request = requests.post(COURSE_URL + str(second_sem) + '/content_migrations', params=payload, headers=HEADER)
    response = request.json()
    migration2 = response['progress_url']

    """A request is made to the progress url in the while loop to get progress until the workflow state is 'completed' or the percentage is 100"""
    request = requests.get(str(migration1), headers=HEADER)
    progress1 = request.json()

    request = requests.get(str(migration2), headers=HEADER)
    progress2 = request.json()

    while progress2[u'workflow_state'] != 'completed' or progress1[u'workflow_state'] != 'completed':
        request = requests.get(str(migration1), headers=HEADER)
        mig1 = request.json()
        request = requests.get(str(migration2), headers=HEADER)
        mig2 = request.json()

        print('          %s Workflow State: %s at %s percent' %(first_sem, mig1[u'workflow_state'], mig1[u'completion']))
        print('          %s Workflow State: %s at %s percent' % (second_sem, mig2[u'workflow_state'], mig2[u'completion']))

        """TIME SLEEP BETWEEN THE WORKFLOW STATE OUTPUT"""
        if mig2[u'completion'] != 100 or mig1[u'completion'] != 100:
            time.sleep(30)

        elif mig2[u'completion'] == 100 and mig1[u'completion'] == 100:
            break

def first_semester_modules(course_id):
    """this function goes through the first created course to remove all assignments and course modules that do not belong in the first semester course"""

    """the customers are not consistent with what they name the end of course survey so this input just puts a pause to allow for manual move of the end of course survey"""
    userin = input('           Please Move the End Of Course Survey: ')
    print("DELETING ASSIGNMENTS FOR", get_course_info(course_id)['name'])

    """customers are also not consistent with module names so this if statements tries to accomodate for all the different formats"""
    """second semester course begins at Unit/Module 6 so this for loop deletes all modules after 5"""
    for i in get_modules(course_id):
        if i[u'name'].startswith(("Unit 6", "Unit 7", "Unit 8", "Unit 9", "Unit 10", "Module Six", "Module Seven", "Module Eight", "Module Nine", \
                                 "Module Ten", "Module 6", "Module 7", "Module 8", "Module 9", "Module 10", "6.0", "7.0", "8.0", "9.0", "10.0")):
            requests.delete(COURSE_URL + str(course_id) + '/modules/' + str(i[u'id']), headers=HEADER)

    """assignments have week numbers in their name and the week 19 marks the beginning of the second semester so this for loop deletes any assignment that is assigned for week 19 or more"""
    for i in get_assignments(course_id):
        try:
            if int(i[u'name'][2:4]) >= 19:
                requests.delete(COURSE_URL + str(course_id) + '/assignments/' + str(i['id']), headers=HEADER)
        except ValueError:
            try:
                if int(i[u'name'][3:5]) >= 19:
                    requests.delete(COURSE_URL + str(course_id) + '/assignments/' + str(i['id']), headers=HEADER)
            except:
                pass

    print("           Done, Verify Assignments!!")


def second_semester_modules(course_id):
    """this function goes through the second created course to remove all assignments and course modules that do not belong in the second semester course"""

    print("DELETING ASSIGNMENTS FOR: ", get_course_info(course_id)['name'])

    """customers are also not consistent with module names so this if statements tries to accomodate for all the different formats"""
    """second semester course begins at Unit/Module 6 so this for loop deletes all modules before 6"""
    for i in get_modules(course_id):
        if i[u'name'].startswith(("Unit 2", "Unit 3", "Unit 4", "Module One", "1.0", "Module Two", "2.0", "Module Three", "3.0", "Module Four", \
                                 "4.0", "Module Five", "5.0", "Module 1:", "Module 2", "Module 3", "Module 4", "Module 5")):
            requests.delete(COURSE_URL + str(course_id) + '/modules/' + str(i[u'id']), headers=HEADER)

    """assignments have week numbers in their name and the week 19 marks the beginning of the second semester so this for loop deletes any assignment that is assigned before week 19"""
    for i in get_assignments(course_id):
        try:
            if int(i[u'name'][2:3]) < 18 and i[u'name'][3:4] == '.':
                requests.delete(COURSE_URL + str(course_id) + '/assignments/' + str(i['id']), headers=HEADER)
        except ValueError:
            pass
        try:
            if int(i[u'name'][2:4]) <= 18:
                requests.delete(COURSE_URL + str(course_id) + '/assignments/' + str(i['id']), headers=HEADER)
        except ValueError:
            try:
                if int(i[u'name'][1:3]) <= 18:
                    requests.delete(COURSE_URL + str(course_id) + '/assignments/' + str(i['id']), headers=HEADER)
            except ValueError:
                pass

    print("\n\nRENAMING: ", get_course_info(course_id)[u'id'], get_course_info(course_id)[u'name'])

    """the following for loop goes through each assignment and renames them so that instead of starting at week  18, they would begin at week 1"""
    """this is import for another tool to use to properly schedule due dates for assignments"""
    for mod in get_modules(course_id):
        if "Documents" not in mod[u'name'] or "Resources" not in mod[u'name']:
            print(mod[u'name'].center(85).upper())
            for item in get_module_items(course_id, mod[u'id']):
                if "SubHeader" not in item[u'type']:
                    try:
                        if ("module ten" in mod[u'name'].lower() or "module 10" in mod[u'name'].lower() or "10.0" in mod[u'name'].lower() or "unit 10" in mod[u'name'].lower() \
                            or "module 14" in mod[u'name'].lower() or mod[u'name'].startswith("10")) and int(item[u'title'][3:5]) >= 19:


                            item_name = item[u'title'].replace(item[u'title'][3:5], str(int(item[u'title'][3:5]) - 18))

                            payload = {'module_item[title]' : item_name}
                            requests.put(COURSE_URL + str(course_id) + '/modules/' + str(mod['id']) +'/items/'+ str(item['id']), params=payload, headers=HEADER)

                        elif int(item[u'title'][2:4]) >= 19:
                            item_name = item[u'title'].replace(item[u'title'][2:4], str(int(item[u'title'][2:4]) - 18))

                            payload = {'module_item[title]' : item_name}
                            requests.put(COURSE_URL + str(course_id) + '/modules/' + str(mod['id']) +'/items/'+ str(item['id']), params=payload, headers=HEADER)

                    except ValueError:
                        pass

def taskmanager(course_id):
    """the function below simply calls all the other functions and has two pauses just in case any clean up work is needed before the first"""
    """and second semester module functions start deleting course content"""

    course_one, course_two = createsemestershells(course_id)
    content_migrator(course_id, course_one, course_two)

    usertext = input("\nReady for First Semester?: ")
    first_semester_modules(course_one)

    usertext = input("\nReady for Second Semester?: ")
    second_semester_modules(course_two)

if __name__ == '__main__':

    #COURSES = input("\nPlease enter a comma separated list of Canvas Staging Course IDs: ")
    #COURSE_LIST = COURSES.split(',')

    #for course in COURSE_LIST:
    #    taskmanager(course)

    print('\n\nCourse Splitting: COMPLETED!')
