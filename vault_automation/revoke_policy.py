import requests
import json
import sys

#variable for entire code
root_user = "X-Vault-Token"
root_token = "yourRootToken"
root_headers = {f'{root_user}': f'{root_token}'}
base_url = "yourVaultAddress"
alias_name =  "aliasNametoAttach"# this var used for get entity id request
alias_mount_accessor = "githubMountID" # this var used for get entity id request
get_entityID = "" # this var will be used after get entity id request success

group_name = "yourGroupPolicy" # this var used for get group name or attach policy
get_group_id = "" # this var will be used after get group id 

#param in json
params_req_entityID_dict = {"alias_name": alias_name, "alias_mount_accessor": alias_mount_accessor}
params_req_entityID_json = json.dumps(params_req_entityID_dict, indent=4)

#request for entity ID
req_entityID =  requests.post(f"{base_url}/v1/identity/lookup/entity",
                    headers=root_headers, data=params_req_entityID_json)

#convert byte array to json
req_entityID_json = json.loads(req_entityID.content)

#get its entity id
get_entityID = req_entityID_json['data']['aliases'][0]['canonical_id']
get_entityName = req_entityID_json['data']['name']
print(f"{alias_name} entity ID is {get_entityID} and entity name is {get_entityName}")

#========================================================================

# request for group ID and entity ID in this group
req_groupID = requests.get(f"{base_url}/v1/identity/group/name/{group_name}",headers=root_headers)
req_groupID_json = json.loads(req_groupID.content)
get_member_entityID = req_groupID_json['data']['member_entity_ids'] #this will be used to update group
get_member_entityID.remove(f"{get_entityID}") #remove member entity id from current member entity id

get_group_id = req_groupID_json['data']['id']
print(f"{group_name} group id: {get_group_id}")

#========================================================================

# update group member
params_req_add_member_dict = {'name': group_name, 'member_entity_ids': get_member_entityID}
params_req_add_member_json = json.dumps(params_req_add_member_dict, indent=4)

req_add_member = requests.post(f"{base_url}/v1/identity/group/id/{get_group_id}",
                               headers=root_headers, data=params_req_add_member_json)
if req_add_member.status_code == 204: 
    print(f"Removed member from group status code: {req_add_member.status_code}")
else:
    sys.exit(1)