#!/bin/sh
file=users.csv
group=ImmersionDay_Students
policy="${group}_Policy"
if [ ${1:-add} == "delete" ]
then
        while IFS=, read -r username password; do
		aws iam delete-login-profile --user-name $username
		aws iam remove-user-from-group --user-name $username --group-name $group
	        aws iam delete-user --user-name $username
	done < $file
	aws iam delete-group-policy --group-name $group --policy-name $policy
	aws iam delete-group --group-name $group	
else
        aws iam create-group --group-name $group
        aws iam put-group-policy --group-name $group --policy-name $policy --policy-document file://policy_doc.json
	while IFS=, read -r username password; do
        	aws iam create-user --user-name $username
        	aws iam add-user-to-group --user-name $username --group-name $group
        	aws iam create-login-profile --user-name $username --password $password
	done < $file
fi
