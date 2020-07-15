import looker_sdk
import logging
import urllib3
import requests
from looker_sdk import models

# disable warnings coming from self-signed SSL cert
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sdk = looker_sdk.init31() 

############## Grab information about dashboard you'd like to copy  ##############
# NewTitle = input("Enter title for new dashboard: ")
# BaseDashboard = input("ID of dashboard to copy: ")

NewTitle = 'Dashboard Copy' # Enter a title for the new copied dashboard
BaseDashboard = '000' # Enter the dashboard id of the dashboard you'd like to copy

################ Step 1 - Get all information about the dashboard to copy ################
def GetDashboard(dashboard_id=None):
    DashboardToCopy = sdk.dashboard(dashboard_id=str(dashboard_id))
    return DashboardToCopy
DashboardToCopy = GetDashboard(BaseDashboard)

# Print high level info about dashboard to copy
print('Copying over the ' + DashboardToCopy.title + ' dashboard\n',
      'It is located in the ' + DashboardToCopy.folder.name + ' folder\n',
      'It has ' + str(len(DashboardToCopy.dashboard_filters)) + ' filter(s), '
      + str(len(DashboardToCopy.dashboard_elements)) + ' elements(s) and '
      + str(len(DashboardToCopy.dashboard_layouts)) + ' layout(s).')
###########################################################################################

############# Step 2 - Create blank dashboard with same meta data as base dashboard #######
def CreateDashboard(
                    description= None
                    ,hidden = None
                    ,query_timezone= None
                    ,refresh_interval= None
                    ,title= None
                    ,background_color=None
                    ,crossfilter_enabled= None
                    ,deleted=None
                    ,load_configuration= None
                    ,lookml_link_id= None
                    ,show_filters_bar= None
                    ,show_title= None
                    ,slug= None
                    ,space_id= None
                    ,folder_id= None
                    ,text_tile_text_color= None
                    ,tile_background_color= None
                    ,tile_text_color= None
                    ,title_color= None
                    ,appearance= None
                    ,preferred_viewer= None
                     ):
    DashboardObject = looker_sdk.models.WriteDashboard(
        description= description
        ,hidden = hidden
        ,query_timezone= query_timezone
        ,refresh_interval= refresh_interval
        ,title= title
        ,background_color=background_color
        ,crossfilter_enabled= crossfilter_enabled
        ,deleted=deleted
        ,load_configuration= load_configuration
        ,lookml_link_id= lookml_link_id
        ,show_filters_bar= show_filters_bar
        ,show_title= show_title
        ,slug= slug
        ,space_id= space_id
        ,folder_id= folder_id
        ,text_tile_text_color= text_tile_text_color
        ,tile_background_color= tile_background_color
        ,tile_text_color= tile_text_color
        ,title_color= title_color
       , appearance= appearance
       , preferred_viewer= preferred_viewer
    )
    CreatedDashboard = sdk.create_dashboard(body=DashboardObject)
    return CreatedDashboard

NewDashboardBase = CreateDashboard(
        description= DashboardToCopy.description
        ,hidden = DashboardToCopy.hidden
        ,query_timezone= DashboardToCopy.query_timezone
        ,refresh_interval= DashboardToCopy.refresh_interval
        ,title= NewTitle + " Copy" # Add in 'Copy' to dashboard title just in case that title has already been taken
        ,background_color=DashboardToCopy.background_color
        ,crossfilter_enabled= DashboardToCopy.crossfilter_enabled
        ,deleted=DashboardToCopy.deleted
        ,load_configuration= DashboardToCopy.load_configuration
        ,lookml_link_id= DashboardToCopy.lookml_link_id
        ,show_filters_bar= DashboardToCopy.show_filters_bar
        ,show_title= DashboardToCopy.show_title
        ,folder_id= DashboardToCopy.folder_id
        ,text_tile_text_color= DashboardToCopy.text_tile_text_color
        ,tile_background_color= DashboardToCopy.tile_background_color
        ,tile_text_color= DashboardToCopy.tile_text_color
        ,title_color= DashboardToCopy.title_color
        ,appearance= DashboardToCopy.appearance
        ,preferred_viewer= DashboardToCopy.preferred_viewer
    )

############################################################################################

##### Step 3 - Get all filters from base dashboard and add to newly created dashboard #######
# Grab filters from base dashboard
AllFilters = sdk.dashboard_dashboard_filters(dashboard_id=str(DashboardToCopy.id))

# Add to new dashboard
for f in AllFilters:
    # print('Filter Name: ' + f.name + ', Row: ' + str(f.row)) # Print out filter names and filter row location if you'd like
    DashboardFilterObject = looker_sdk.models.WriteCreateDashboardFilter(
                                                    dashboard_id=NewDashboardBase.id,
                                                    name=f.name,
                                                    title=f.title,
                                                    type=f.type,
                                                    default_value=f.default_value,
                                                    model=f.model,
                                                    explore=f.explore,
                                                    dimension=f.dimension,
                                                    row=f.row,
                                                    listens_to_filters=f.listens_to_filters,
                                                    allow_multiple_values=f.allow_multiple_values,
                                                    required=f.required
                                                    )
    NewFilter = sdk.create_dashboard_filter(body=DashboardFilterObject)
##############################################################################################

###### Step 4 - Get all elements from base dashboard and add to newly created dashboard #######
DashboardElementsToCopy = sdk.dashboard_dashboard_elements(dashboard_id=str(DashboardToCopy.id))

# Add each element from base dashboard to new copied dashboard
for f in DashboardElementsToCopy:
    # print('Element Name: ' + f.title + ' on Dashboard: ' + str(NewDashboardBase.id)) # print title of tile
    DashboardElementObject = looker_sdk.models.WriteDashboardElement(
        body_text= f.body_text,
        dashboard_id= NewDashboardBase.id,
        look_id= f.look_id,
        merge_result_id= f.merge_result_id,
        note_display= f.note_display,
        note_state= f.note_state,
        note_text= f.note_text,
        query_id= f.query_id,
        refresh_interval= f.refresh_interval,
        result_maker= f.result_maker,
        result_maker_id= f.result_maker_id,
        subtitle_text= f.subtitle_text,
        title= f.title,
        title_hidden= f.title_hidden,
        title_text= f.title_text,
        type= f.type
    )
    CreatedDashboardElement = sdk.create_dashboard_element(body = DashboardElementObject)

############################################################################################

########################## Step 5 - Create all dashboard elements ##########################
DashboardLayoutsToCopy = sdk.dashboard_dashboard_layouts(dashboard_id=str(DashboardToCopy.id))
for f in DashboardLayoutsToCopy:
    print('Layout ID: ' + f.id + ' Layout Type: ' + f.type)
    DashboardElementObject = looker_sdk.models.WriteDashboardLayout(
        dashboard_id= NewDashboardBase.id,
        type= f.type,
        active= f.active,
        column_width= f.column_width,
        width= f.width
    )
    CreatedDashboardLayout = sdk.create_dashboard_layout(body = DashboardElementObject)
############################################################################################

############################### Step 6 - Update Layouts ####################################

# Get layouts and elements of new dashboard
NewDashboardLayouts = sdk.dashboard_dashboard_layouts(NewDashboardBase.id) 
NewDashboardElements = sdk.dashboard_dashboard_elements(NewDashboardBase.id)

def UpdateDashboardLayoutComponent(
                            dashboard_layout_component_id=None,
                            dashboard_layout_id= None,
                            dashboard_element_id= None,
                            row= None,
                            column= None,
                            width= None,
                            height= None
                            ):
    LayoutComponentObject = looker_sdk.models.WriteDashboardLayoutComponent(
                        dashboard_layout_id= dashboard_layout_id,
                        dashboard_element_id= dashboard_element_id,
                        row= row,
                        column= column,
                        width= width,
                        height= height
                        )
    UpdatedDashboardLayoutComponent = sdk.update_dashboard_layout_component(dashboard_layout_component_id=str(dashboard_layout_component_id), body = LayoutComponentObject)
    return UpdatedDashboardLayoutComponent

for i in NewDashboardLayouts[0].dashboard_layout_components:
    for j in DashboardLayoutsToCopy[0].dashboard_layout_components:
        if i.element_title == j.element_title:
            UpdateDashboardLayoutComponent(
                dashboard_layout_component_id= i.id,
                dashboard_layout_id= i.dashboard_layout_id,
                dashboard_element_id= i.dashboard_element_id,
                # Replace current location with row a
                row= j.row,
                column= j.column,
                width= j.width,
                height= j.height
                )

############################################################################################