
# coding: utf-8

# # Software Development Lifecycle Demo

# Lets imagine we have the following:
# 
#        -A dev Looker instance (where your LookML developers commit code)- https://demoexpo.looker.com
#         
#        -A prod Looker instance (where dashboards are embedded into our application)- https://demo.looker.com
#        
#        -LookML projects in our dev and prod instance, named sdlc_demo, each with their own git repository
#        
#        -Dashboards built in Looker that are embedded into our application, listed in a googlesheet

# First, we want to autenticate into both of our Looker instances. We can do this by creating ini files that contain our client_id and secret for each instance

# In[ ]:

import looker_sdk
import os
import subprocess
import requests


# In[ ]:

dev_sdk = looker_sdk.init31(config_file='dev.ini')  
prod_sdk = looker_sdk.init31(config_file='prod.ini')  


# Test the connection:

# In[ ]:

try:
    dev_sdk.project('sdlc_demo')
    print('Dev connection good')
except:
    print('Dev connection not working, check ini file and restart kernel')
try:
    prod_sdk.project('sdlc_demo')
    print('Prod connection good')
except:
    print('Prod connection not working, check ini file and restart kernel')


# To authenticate into git we'll be adding the username and password to the url

# In[ ]:

username = 'user'
password = 'password'


# ## Making Changes

# Create a new tile on an existing dashboard, or create a brand new dashboard in your shared folder

# ## Part 1: Getting Dashboards into Git

# Now that we've made some changes, we want to take the latest version of our user defined dashboards from our dev instance and covert it to LookML (basically codifying all the work our non-technical users did to create the dashboards). See the API endpoint [here](https://docs.looker.com/reference/api-and-integration/api-reference/v3.1/dashboard#get_lookml_of_a_udd)

# In[ ]:

#iterate through the dashboards in a folder (space) and get the lookml for each dashboard

lookml_dashboards = []
for dashboard in dev_sdk.space_dashboards('shared_space_id'):
#     print(dashboard)
    print(dashboard.title)
    lookml_dashboards.append(dev_sdk.dashboard_lookml(dashboard.id))
    
#lookml_dashboards is an array of DashboardLookml objects


# In[ ]:

#show the LookML for the first dashboard to see how it looks
print(lookml_dashboards[0].lookml)


# Once we have the LookML for the latest version of our dashboards we want to push that into git, so first we have to figure out what the remote url for our dev repo is

# In[ ]:

dev_repo = dev_sdk.project('project_name').git_remote_url
dev_repo


# In[ ]:

dev_repo = dev_repo.replace('git@github.com:','https://%s:%s@github.com/' %(username, password))


# Now we'll want to clone that repo if it doesn't exist already, and if it does use git pull to grab the changes from master and pull them to our local clone

# In[ ]:

cloned_path = os.path.join(os.getcwd(),'project_name')
if os.path.exists(cloned_path):
    os.chdir(cloned_path)
    result = subprocess.run('git pull', shell=True, capture_output=True)
    print('Pulling repo')
    if result.stderr.decode("utf-8")=='':
        print(result.stdout.decode("utf-8"))
    else:
        print(result.stderr.decode("utf-8"))
else:
    result = subprocess.run('git clone %s' % dev_repo, shell=True, capture_output=True)
    print('Cloning repo')
    if result.stderr.decode("utf-8")=='':
        print(result.stdout.decode("utf-8"))
    else:
        print(result.stderr.decode("utf-8"))
    os.chdir(cloned_path)   


# You can view the contents of the cloned repo [here](https://jupyter.looker.com/tree/****%20Python%20Demo%20Examples%20-%20Do%20not%20edit%20****/sdlc_dev)

# Next we'll want to update the dashboard files in LookML to be what we currently have grabbed from the API. In this example we'll use the dashboard slugs as the file name, because these can be set to be consistent unique identifiers for dashboards across instances.

# In[ ]:

dashboard_folder = os.path.join(cloned_path,'dashboards')
if not os.path.exists(dashboard_folder):
    os.mkdir(dashboard_folder)
os.chdir(dashboard_folder)

for dash in lookml_dashboards:
    #slug = dev_sdk.dashboard(dash.dashboard_id).title
    #title = ''.join(c.lower() for c in dev_sdk.dashboard(dash.dashboard_id).title).replace(' ','_')
    lookml_dash = dash.lookml
    title = lookml_dash[lookml_dash.find('- dashboard')+len('- dashboard: '):lookml_dash.find('\n')]
    #create or open file
    file_name = os.path.join(dashboard_folder,title)+'.dashboard.lookml'
    f=open(file_name,'w')
    #write the lookml to the file
    f.write(lookml_dash)
    f.close()

os.chdir(cloned_path)


# ## Part 2: Pushing changes into Prod

# With all of our changes in our local git repository, the next thing we want is to push our local development onto the prod remote's master. First, we want to add a remote to the prod git. 

# In[ ]:

prod_repo = prod_sdk.project('project_name').git_remote_url
prod_repo = prod_repo.replace('git@github.com:','https://%s:%s@github.com/' %(username, password))


result = subprocess.run('git remote add prod %s' %prod_repo, shell=True, capture_output=True)
print('Adding remote')
if result.stderr.decode("utf-8")=='':
    print(result.stdout.decode("utf-8"))
else:
    print(result.stderr.decode("utf-8"))
    #dont worry if the remote already exists


# This next step adds a commit for our Dashboard LookML modifications, and pushes everything to master of both of the remotes (dev and prod)

# In[ ]:

commands = 'export HOME=/home/lookerops;             git config --global user.name "password";             git config --global user.email "usernameemail";             git add --all;             git commit -m "updating dashboard files;"'

result =subprocess.run(commands, shell=True, capture_output=True)
print('Commiting')
if result.stderr.decode("utf-8")=='':
    print(result.stdout.decode("utf-8"))
else:
    print(result.stderr.decode("utf-8"))

result = subprocess.run('git push -f origin master', shell=True, capture_output=True)

print('Pushing to master for dev repo')
if result.stderr.decode("utf-8")=='':
    print(result.stdout.decode("utf-8"))
else:
    print(result.stderr.decode("utf-8"))

    
result = subprocess.run('git push -f prod master', shell=True, capture_output=True)    
    
print('Pushing to master for prod repo')
if result.stderr.decode("utf-8")=='':
    print(result.stdout.decode("utf-8"))
else:
    print(result.stderr.decode("utf-8"))


# Next, we want to call the webhook so that the changes from master are shown in Looker Production mode on our production instance

# In[ ]:

dev_response = requests.post(url = 'https://dev.looker.com/webhooks/projects/project/deploy')
prod_response = requests.post(url = 'https://prod.looker.com/webhooks/projects/project/deploy')

print(dev_response)
print(prod_response)


# The last step is [importing](https://docs.looker.com/reference/api-and-integration/api-reference/v3.1/dashboard#import_lookml_dashboard), or [syncing](https://docs.looker.com/reference/api-and-integration/api-reference/v3.1/dashboard#sync_lookml_dashboard), our user defined dashhboards in prod with the LookML we've just pushed

# In[ ]:

dash_titles = [f for f in os.listdir(dashboard_folder)]
for title_file in dash_titles:
    if 'dashboard.lookml' in title_file:
        title = title_file.split('.')[0]

        #lookml dashboards ID are generated from the model + title 
        lookml_dash_id = 'sdlc_thelook::'+ title

        #check to see if the dashboard exists in the space
        exists = 0
        for dash in prod_sdk.space_dashboards('shared_space_id in prod'):
            if dash.lookml_link_id == lookml_dash_id:
                exists = 1
        
        if exists:
            print('Dashboard %s already exists, syncing it with LookML' %title)
        else:
            print('Dashboard %s does not yet exist, creating it in the space' %title)
        if exists == 1:
            prod_sdk.sync_lookml_dashboard(lookml_dash_id,looker_sdk.models.WriteDashboard())

        #otherwise import using the dashboard id, to the given space
        else:
            #import the dashboard to the space
            dash = prod_sdk.import_lookml_dashboard(lookml_dash_id,'shared_space_id in prod',{})


# ## Part 3: Copy Dashboard
# Get list of all lookml_link_id for dashboards in space

# In[ ]:

dashboards = []
for dashboard in prod_sdk.space_dashboards('shared_space_id in prod'):
    dashboards.append(dashboard)
    print(dashboard.title)



# Choose the dashboard link for dashboard you want to copy

# In[ ]:

toimport = dashboards[i].lookml_link_id
print(toimport)


# Copy dashboard using lookml_link_id to new space

# In[ ]:

newdash = prod_sdk.import_lookml_dashboard(lookml_dashboard_id = toimport, space_id='space_id',body={})


# Update dashboard title, unlink from lookml_link_id

# In[ ]:

def UpdateDashboard(dashboard_id=None, title=None, lookml_link_id=None):
    DashboardObject = looker_sdk.models.WriteDashboard(title=title, lookml_link_id=lookml_link_id)
    UpdateadDashboard = prod_sdk.update_dashboard(dashboard_id, body=DashboardObject)
    return UpdateadDashboard
NewTitle = UpdateDashboard(dashboard_id='6095', lookml_link_id=None, title="New and Updated Title - Tonight")

