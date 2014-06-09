@echo off
set file=users.csv
set group=ImmersionDay_Students
set policy=%group%_Policy
if [%1]==[delete] (
	for /F "delims=," %%G in (%file%) do (
		aws iam delete-login-profile --user-name %%G
		aws iam remove-user-from-group --user-name %%G --group-name %group%
		aws iam delete-user --user-name %%G
	)
	aws iam delete-group-policy --group-name %group% --policy-name %policy%
	aws iam delete-group --group-name %group%
) else ( 
	aws iam create-group --group-name %group%
	aws iam put-group-policy --group-name %group% --policy-name %policy% --policy-document file://policy_doc.json
	for /F "delims=, tokens=1,2" %%G in (%file%) do (
		aws iam create-user --user-name %%G
		aws iam add-user-to-group --user-name %%G --group-name %group%
		aws iam create-login-profile --user-name %%G --password %%H
	)
)