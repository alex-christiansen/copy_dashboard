# Copy a UDD using API calls
**Purpose of Script:** The purpose of this python script is to help Looker users copy user-defined dashboards using only API calls. In general, this script would be used for embedded use cases when the dashboard being copied doesn't have a looklm_link_id (dashboard was never a LookML dashboard). 

**Limitations**
- Text Tiles - right now, the script cannot handle text tiles as tile location is matched on tile title and text tiles do not have a title. I aim to fix this in the near future
- Look Tiles - any dashboard that has tiles that are pointing to saved Looks will not copy over correctly. Easiest thing to do is to convert all Looks to tiles on a dashboard before running
