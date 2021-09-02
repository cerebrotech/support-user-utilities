import requests
import os
import json
import sys
import shutil
import domino_utils

DOMINO_API_KEY= domino_utils.get_domino_api_key()
DOMINO_URL=domino_utils.get_domino_url()
GET_USERS_ENDPOINT = 'v4/users'
GET_PROJECTS_ENDPOINT = 'v4/projects'
ADD_COLLABORATOR_ENDPOINT = 'v4/projects/{projectId}/collaborators'
DELETE_COLLABORATOR_ENDPOINT = 'v4/projects/{projectId}/collaborators/{collaboratorId}'
DOWNLOAD_EXPERIMENTS_ENDPOINT = 'v4/jobs?projectId={projectId}&page_size=1000000'
projects_by_owner_user_name={}
users_by_user_name={}

def get_all_projects():
    headers = {'X-Domino-Api-Key': DOMINO_API_KEY}
    url = os.path.join(DOMINO_URL,GET_PROJECTS_ENDPOINT)
    ret = requests.get(url, headers=headers)
    projects = ret.json()
    return projects

def get_project_list():
    headers = {'X-Domino-Api-Key': DOMINO_API_KEY}
    url = os.path.join(DOMINO_URL,GET_PROJECTS_ENDPOINT)
    ret = requests.get(url, headers=headers)
    projects = ret.json()
    for p in projects:
        owner_user_name = p['ownerUsername']
        if owner_user_name not in projects_by_owner_user_name:
            projects_by_owner_user_name[owner_user_name]={}
        projects_by_owner_user_name[owner_user_name][p['name']]=p

def get_users_list():
    headers = {'X-Domino-Api-Key': DOMINO_API_KEY}
    url = os.path.join(DOMINO_URL,GET_USERS_ENDPOINT)
    ret = requests.get(url, headers=headers)
    users = ret.json()
    for u in users:
        user_name = u['userName']
        if user_name not in users:
            users_by_user_name[user_name]={}
        users_by_user_name[user_name]=u

def get_project_by_owner_and_name(owner_user_name,project_name):
    return projects_by_owner_user_name[owner_user_name][project_name]
def get_user_by_name(user_name):
    return users_by_user_name[user_name]


def add_collaborator(owner_user_name, project_name, collaborator_user_name, project_role):

    if project_role not in ['Contributor','ResultsConsumer', 'LauncherUser', 'ProjectImporter']:
        print('Project Role of Collaborator must be one of ' + ','.join([elem for elem in valid_roles]))
        return
    print(DOMINO_API_KEY)
    headers = {'X-Domino-Api-Key': DOMINO_API_KEY, 'Content-Type': 'application/json'}
    #Get Project Id
    print(get_project_by_owner_and_name(owner_user_name, project_name))
    projectId= get_project_by_owner_and_name(owner_user_name, project_name)['id']
    #Get User Id
    collaboratorId=get_user_by_name(collaborator_user_name)['id']
    payload = {'projectRole': project_role, 'collaboratorId': collaboratorId}
    url = ''.join([DOMINO_URL, ADD_COLLABORATOR_ENDPOINT]) \
        .format(**{'projectId': projectId})
    resp = requests.post(url,headers=headers,json=payload)
    if(resp.status_code==200):
        print('Add Collaborator Succeeded')
    else:
        print('Add Collaborator failed with code ' + str(resp.status_code))
        print('Error Message: ' + str(resp.content))


def delete_collaborator(owner_user_name, project_name, collaborator):
    headers = {'X-Domino-Api-Key': DOMINO_API_KEY}
    #Get Project Id
    projectId=get_project_by_owner_and_name(owner_user_name, project_name)['id']
    #Get User Id
    collaboratorId=get_user_by_name(collaborator_user_name)['id']
    url = ''.join([DOMINO_URL,DELETE_COLLABORATOR_ENDPOINT])\
                 .format(**{'projectId': projectId,'collaboratorId': collaboratorId})
    resp = requests.delete(url,headers=headers)
    if(resp.status_code==200):
        print('Delete Collaborator Succeeded')
    else:
        print('Delete Collaborator failed with code ' + str(resp.status_code))
        print('Error Message: ' + str(resp.content))

        
def download_experiments(folder):
    headers = {'X-Domino-Api-Key': DOMINO_API_KEY}
    projects = get_all_projects()
    for p in projects:
        url = ''.join([DOMINO_URL,DOWNLOAD_EXPERIMENTS_ENDPOINT])\
                     .format(**{'projectId' : p['id']})
        ret = requests.get(url, headers=headers)
        print(url)
        save_path = os.path.join(folder,p['id'])
        with open(save_path,'w') as f:
            print('saving to file ' + save_path)
            print(ret.json())
            f.write(json.dumps(ret.json()))



if __name__ == "__main__":

    get_project_list()
    get_users_list()
    p = get_project_by_owner_and_name('user1','test')
    u = get_user_by_name('user1')

    action = sys.argv[1]
    if action == 'add_collab':
        owner_user_name = sys.argv[2]
        project_name = sys.argv[3]
        collaborator_user_name=sys.argv[4]
        #One of ['Contributor','Results Consumer', 'Launcher User', 'Project Importer']
        collaborator_type=sys.argv[5]
        add_collaborator(owner_user_name,project_name,collaborator_user_name,collaborator_type)
    if action == 'delete_collab':
        owner_user_name = sys.argv[2]
        project_name = sys.argv[3]
        collaborator_user_name=sys.argv[4]
        delete_collaborator(owner_user_name,project_name,collaborator_user_name)

    if action == 'download_experiments':
        folder=sys.argv[2]
        if os.path.exists(folder):
            shutil.rmtree(folder)
        if not os.path.exists(folder):
            # Create a new directory because it does not exist
            os.makedirs(folder)
            print("The new directory is created!")
        download_experiments(folder)



