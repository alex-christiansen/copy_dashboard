import looker_sdk
import logging
import urllib3
import requests

from looker_sdk import models


# disable warnings coming from self-signed SSL cert
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sdk = looker_sdk.init31() 

def GetDashboard(dashboard_id=None):
    DashboardToCopy = sdk.dashboard(dashboard_id=str(dashboard_id))

    return DashboardToCopy

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
                    , appearance= None
                    , preferred_viewer= None
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

def GetAllDashboardElements(dashboard_id=None):
    DashboardElements = sdk.dashboard_dashboard_elements(dashboard_id=str(dashboard_id))

    return DashboardElements

def CreateDashboardElement(
                        body_text= None,
                        dashboard_id= None,
                        look_id= None,
                        merge_result_id= None,
                        note_display= None,
                        note_state= None,
                        note_text= None,
                        query_id= None,
                        refresh_interval= None,
                        result_maker=None,
                        result_maker_id= None,
                        subtitle_text= None,
                        title= None,
                        title_hidden= None,
                        title_text= None,
                        type= None
                            ):

    DashboardElementObject = looker_sdk.models.WriteDashboardElement(
                        body_text= body_text,
                        dashboard_id= dashboard_id,
                        look_id= look_id,
                        merge_result_id= merge_result_id,
                        note_display= note_display,
                        note_state= note_state,
                        note_text= note_text,
                        query_id= query_id,
                        refresh_interval= refresh_interval,
                        result_maker=result_maker,
                        result_maker_id= result_maker_id,
                        subtitle_text= subtitle_text,
                        title= title,
                        title_hidden= title_hidden,
                        title_text= title_text,
                        type= type
    )
        

    CreatedDashboardElement = sdk.create_dashboard_element(body = DashboardElementObject)

    return CreatedDashboardElement


def CreateDashboardComponent(
                            dashboard_layout_component_id=None,
                            dashboard_layout_id= None,
                            dashboard_element_id= None,
                            row= None,
                            column= None,
                            width= None,
                            height= None,
                            ):

    NewLayoutComponentObject = looker_sdk.models.WriteDashboardLayoutComponent(
                            dashboard_layout_id= dashboard_layout_id,
                            dashboard_element_id= dashboard_element_id,
                            row= row,
                            column= column,
                            width= width,
                            height= height
                            )
    NewLayoutComponent = sdk.update_dashboard_layout_component(dashboard_layout_component_id=str(dashboard_layout_component_id), body = NewLayoutComponentObject)

    return NewLayoutComponent

DashboardToCopy = GetDashboard(3)
DashboardElementsToCopy = GetAllDashboardElements(3)

NewDashboardBase = CreateDashboard(
        description= DashboardToCopy.description
        ,hidden = DashboardToCopy.hidden
        ,query_timezone= DashboardToCopy.query_timezone
        ,refresh_interval= DashboardToCopy.refresh_interval
        ,title= DashboardToCopy.title+" Copy"
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
       , appearance= DashboardToCopy.appearance
       , preferred_viewer= DashboardToCopy.preferred_viewer
    )

NewElements = [CreateDashboardElement(
                        e.body_text,
                        NewDashboardBase.id,
                        e.look_id,
                        e.merge_result_id,
                        e.note_display,
                        e.note_state,
                        e.note_text,
                        e.query_id,
                        e.refresh_interval,
                        e.result_maker,
                        e.result_maker_id,
                        e.subtitle_text,
                        e.title,
                        e.title_hidden,
                        e.title_text,
                        e.type
                            ) 
                for e in DashboardElementsToCopy
                ]

NewDashboardBase = GetDashboard(NewDashboardBase.id)

OldComponents = {}
for c in DashboardToCopy.dashboard_layouts[0].dashboard_layout_components:
    OldComponents[c.element_title] = c

NewLayout = NewDashboardBase.dashboard_layouts[0]
NewComponents = [c for c in NewLayout.dashboard_layout_components]

for c in NewComponents:
    NewUpdatedComponents = CreateDashboardComponent(
                            dashboard_layout_component_id= c.id,
                            dashboard_layout_id= NewDashboardBase.dashboard_layouts[0].id,
                            dashboard_element_id= c.dashboard_element_id,
                            row= OldComponents.get(c.element_title).row,
                            column= OldComponents.get(c.element_title).column,
                            width= OldComponents.get(c.element_title).width,
                            height= OldComponents.get(c.element_title).height
                            )

AllFilters = sdk.dashboard_dashboard_filters(dashboard_id=str(DashboardToCopy.id))
for f in AllFilters:
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
