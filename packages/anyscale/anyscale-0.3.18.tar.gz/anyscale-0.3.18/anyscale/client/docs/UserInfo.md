# UserInfo

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**email** | **str** |  | 
**name** | **str** |  | 
**username** | **str** |  | 
**verified** | **bool** |  | 
**organization_permission_level** | [**OrganizationPermissionLevel**](OrganizationPermissionLevel.md) |  | 
**organization_ids** | **list[str]** | List of organizations that the logged in user is a part of. | 
**ld_hash** | **str** | Server generated secure hash of the user info that should be sent to LaunchDarkly along with the user data. | 
**ld_hash_fields** | **list[str]** | List of fields in the userInfo used to generate the secure hash. Clients should send those fields to LaunchDarkly as the user data. These fields should be used in addition to the \&quot;key\&quot; field which is based off the user&#39;s id. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


