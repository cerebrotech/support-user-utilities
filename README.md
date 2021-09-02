# Support User Utilities

## Add Collaborator 

The calling user needs to be in the "Support User" and "Librarian" role
`python support_user_utilities.py add_collab <owner_user_name> <project_name> <collaborator_user_name> <collaborator_role>`

The Collaborator Role needs to be on the following 4 values:
1. Contributor
2. ResultsConsumer
3. LauncherUser
4. ProjectImporter

Example invocation is below
`python support_user_utilities.py add_collab wadkars quick-start user1 ProjectImporter`


## Remove Collaborator 

`python support_user_utilities.py delete_collab <owner_user_name> <project_name> <collaborator_user_name>`

Example invocation is below
`python support_user_utilities.py delete_collab wadkars quick-start user1`

## Download experiment results for all projects
`python support_user_utilities.py download_experiments <folder_to_download_to>`

The result will be a JSON file per project with file name as projectId savd to the folder `folder_to_download_to`
If the folder exists, it will be deleted and recreated

Example
`python support_user_utilities.py download_experiments /tmp/projects`