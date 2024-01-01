# Peoplestrong

Script to automate time-in and time-out on Peoplestrong.

## Usage

1. Configure hosts file with ip address, set user and group for file permissions and configure target host timezone. 
2. To install script on host, use peoplestrong role.

```
ansible-playbook -i ansible/hosts ansible/main.yml --tags=peoplestrong
```

3. Enable Peoplestrong crontab using peoplestrong-enable role.

```
ansible-playbook -i ansible/hosts ansible/main.yml --tags=peoplestrong-enable
```

4. Holidays are handled using python-holidays library. You can set your country and region as you desire. 

5. On unscheduled dates (e.g. sick leave) where you don't need to time in/out you need to manually disable the crontab using peoplestrong-disable role. Take note you'll need to run peoplestrong-enable role again, preferably before the next time in.

```
ansible-playbook -i ansible/hosts ansible/main.yml --tags=peoplestrong-disable
```

6. You can also reconfigure time in/out randomness by adjusting crontab sleep delay on peoplestrong-enable/disable roles. Script currently has a delay of 0 to 120 seconds. Adjust accordingly.

