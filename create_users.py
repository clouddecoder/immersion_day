""" This script is used to set up and remove accounts for students attending the Immersion Day class.
Requirements:
    Python 2.7.x   This script does not work with Python 3.
    AWS SDK for Python (Boto) v.2.29.1 or higher.  http://aws.amazon.com/sdkforpython/
    AWS Credentials need to be configured as described in the "Configuring Boto Credentials" here: http://boto.readthedocs.org/en/latest/getting_started.html#configuring-boto-credentialsa
    This script expects a .csv file that contains the usernames and passwords of the users you want to create.
    The script will stop if it encounters a user that already exists in IAM.

    Usage:
        python create_users.py create
        python create_users.py delete

"""

import csv
import boto.iam
import sys



"""
create group, attach IAM policy and add users.
"""
def create_users():
    try:
        iam.create_group(group)
    except boto.exception.BotoServerError as e:
        if e.code == 'EntityAlreadyExists':
            print e.message + " Will overwrite."
        else:
            print "Exception: %s" % str(e)
            exit(1)

    # attach policy to group
    # security policy: allows access to everything but IAM
    # if the IAM lab is included in the day, then remove the line "NotAction": "iam:*",
    policy = '''{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "NotAction": "iam:*",
          "Resource": "*"
        }
      ]
    }'''
    iam.put_group_policy(group, policy_name, policy)


    # add users to group
    with open(DATA_FILE_NAME, 'rU') as data_file:
        user_reader = csv.reader(data_file)
        for row in user_reader:
            user, password = row[0], row[1]
            try:
                iam.create_user(user)
                iam.create_login_profile(user, password)
                iam.add_user_to_group(group, user)
                print("Added " + user)
            except boto.exception.BotoServerError as e:
                print "Problems creating %s.  Exiting due to error: %s" % (user, str(e.message))
                exit(1)

    print "Users created.  They can login to the AWS Console using this link: " + iam.get_signin_url()


"""
delete group, remove IAM policy and users.
"""
def delete_users():
    with open(DATA_FILE_NAME, 'rU') as data_file:
        user_reader = csv.reader(data_file)
        for row in user_reader:
            user = row[0]
            try:
                iam.delete_login_profile(user)
                iam.remove_user_from_group(group, user)
                iam.delete_user(user)
                print("Deleted " + user)
            except boto.exception.BotoServerError as e:
                print "Problems deleting %s.  Exiting due to error: %s" % (user, str(e.message))
                exit(1)
    
    iam.delete_group_policy(group, policy_name)
    iam.delete_group(group)


#################################################################################################

DATA_FILE_NAME = 'users.csv'
group = "ImmersionDay_Students"
policy_name = group + "_Policy"

iam = boto.iam.connect_to_region('us-east-1')

if len(sys.argv) == 1:
    print "Please specify create or delete."
    exit(1)

if len(sys.argv) == 2:
    if sys.argv[1] == "create":
        create_users()
    elif sys.argv[1] == "delete":
        delete_users()
    else:
        print "Please specify create or delete"
        exit(1)


