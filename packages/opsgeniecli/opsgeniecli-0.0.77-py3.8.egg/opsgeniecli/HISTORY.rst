.. :changelog:

History
-------

0.0.1 (26-02-2019)
---------------------

* First code creation


0.0.1 (28-05-2019)
------------------

* testing release


0.0.2 (28-05-2019)
------------------

* added functions


0.0.3 (28-05-2019)
------------------

* maintenance policies - list functions - are now teambased


0.0.4 (28-05-2019)
------------------

* all functions now rely on opsgenielib


0.0.5 (30-05-2019)
------------------

* docs added to: INSTALLATION.rst


0.0.6 (10-06-2019)
------------------

* 'added functionality: adding more than 1 policy to a set_maintenance_policy'


0.0.7 (11-06-2019)
------------------

* for multiple functions: using the config teamid when no --teamid is given.


0.0.8 (11-06-2019)
------------------

* Removed cls=DefaultHelp from policy_maintenance_list


0.0.9 (13-06-2019)
------------------

* Docstrings for every function, plus other linting errors


0.0.10 (13-06-2019)
-------------------

* bug fix for: policy-alerts list


0.0.11 (14-06-2019)
-------------------

* try to resolve autocompletion for powershell


0.0.12 (14-06-2019)
-------------------

* 2nd try to get powershell autocomplete to work


0.0.13 (14-06-2019)
-------------------

* Reverting back to autocomplete without click-completion


0.0.14 (15-06-2019)
-------------------

* Cleaning (mainly consistency in the naming format, read: snake_case everywhere)


0.0.15 (09-08-2019)
-------------------

* adjustments to use opsgenielib 0.0.18


0.0.16 (09-08-2019)
-------------------

* Adding: policy_alerts_enable


0.0.17 (09-08-2019)
-------------------

* Using the latest opsgenielib


0.0.18 (09-08-2019)
-------------------

* Adding the option to give multiple alert notification ID's to enable


0.0.19 (12-08-2019)
-------------------

* added: function to disable alert policies


0.0.20 (12-08-2019)
-------------------

* Checking on the string 'Disabled' instead of 'Enabled'


0.0.21 (12-08-2019)
-------------------

* Added functions to enable and disable notification policies


0.0.22 (13-08-2019)
-------------------

* ID variable could be a string or list in the enable/disable policies functions. Now it will always be a list.


0.0.23 (13-08-2019)
-------------------

* Copy paste error. Changed enabled to disabled for the policy_notificatio_policy.


0.0.24 (13-08-2019)
-------------------

* Changing to the filtering of the maintenance policy set.


0.0.25 (13-08-2019)
-------------------

* Small changes to policy-maintenance set.


0.0.26 (16-08-2019)
-------------------

* adding the option to add multiple --filter to policy-maintenance set


0.0.27 (16-08-2019)
-------------------

* Maintenance policy set - output now includes the names of the policies that are enabled


0.0.28 (16-08-2019)
-------------------

* Adding --filter functionality to cancel_maintenance_policy


0.0.29 (16-08-2019)
-------------------

* Fixes to policy_maintenance_cancel after testing


0.0.30 (17-08-2019)
-------------------

* Added argument --filter for function policy_maintenance_delete


0.0.31 (18-08-2019)
-------------------

* Added --filter to policy_alerts_delete


0.0.32 (18-08-2019)
-------------------

* Alert policy enable/disable: no longer --team_id a requirement and optimised --filter


0.0.33 (19-08-2019)
-------------------

* policy-notifications delete: Added --filter functionality


0.0.34 (19-08-2019)
-------------------

* policy_notifications_disable: added --filter functionality


0.0.35 (20-08-2019)
-------------------

* Using the latest opsgenielib version


0.0.36 (20-08-2019)
-------------------

* Added function 'policy_alerts_get'


0.0.37 (20-08-2019)
-------------------

* Added function 'policy_alerts_get'


0.0.38 (20-08-2019)
-------------------

* Removed 'cls=DefaultHelp' from the function 'policy_alerts_list'. The effect is that no --team_id has to be specified to run the command.


0.0.39 (21-08-2019)
-------------------

* Fixing the time for maintenance set --start_date & --end_date


0.0.40 (04-09-2019)
-------------------

* Added the param --team_name to a lot of functions which uses regex to find the teamname or teamid


0.0.41 (08-09-2019)
-------------------

* Fix to 'alerts_list' by removing the default help class. Parameter options no longer conflict with builtin functions. Parameter options now use a dash instead of an underscore (team-name instead of team_name). Added function 'schedules_timeline'


0.0.42 (08-09-2019)
-------------------

* Added the requirement to give a team-name for the function schedules_timeline


0.0.43 (12-09-2019)
-------------------

* the all option parameter had two dashes twice, the last one should be without any dashes to representation the internal variable


0.0.44 (02-10-2019)
-------------------

* Adding users endpoint and the function list users


0.0.45 (03-10-2019)
-------------------

* Added the functionality to close 1 or all alerts that are acknowledged but not closed


0.0.46 (09-10-2019)
-------------------

* Removed the team-id from policy_maintenance_list since it does not accept the parameter and added more docs to the function


0.0.47 (11-10-2019)
-------------------

* added prompt when using --all for the function alerts_close


0.0.48 (11-10-2019)
-------------------

* alerts_close - bug fix - was referencing to a non existing key in the variable result


0.0.49 (16-10-2019)
-------------------

* Function name was changed to list_maintenance_policy so had to update functions that used it


0.0.50 (16-10-2019)
-------------------

* Small fix for policy_maintenance_cancel


0.0.51 (17-10-2019)
-------------------

* Quicker results when trying to acknowledge all alerts


0.0.52 (29-11-2019)
-------------------

* naming changes, opsgenielib class was renamed plus maintenance functions.


0.0.53 (04-01-2020)
-------------------

* Added function policy_alerts_set


0.0.54 (04-01-2020)
-------------------

* policy_alerts_set parameter enabled to flag


0.0.55 (06-01-2020)
-------------------

* Maintenance policy set now notifies when no alert policies were found


0.0.56 (19-06-2020)
-------------------

* Adding more parameters to the function: schedules timeline


0.0.57 (19-06-2020)
-------------------

* Setting intervalunit default to months and if check now includes current date


0.0.58 (19-06-2020)
-------------------

* Removing print from the function


0.0.59 (19-06-2020)
-------------------

* Setting default value for function


0.0.60 (19-06-2020)
-------------------

* Added the function 'reshuffle'


0.0.61 (13-07-2020)
-------------------

* adding --active to alert policy list and an end date field for maintenance policy list


0.0.62 (24-07-2020)
-------------------

* Moving from UTC to local time as input for override command


0.0.63 (26-07-2020)
-------------------

* Cleaning up parsing of dates with pendulum & adding functionality (out of office and not filtered) to alerts list and count


0.0.64 (26-07-2020)
-------------------

* Using the latest version of opsgenielib


0.0.65 (26-07-2020)
-------------------

* variable fix for alerts_list


0.0.66 (27-07-2020)
-------------------

* Removing version command


0.0.67 (05-08-2020)
-------------------

* Had an incorrect datetime compare, that is fixed now


0.0.68 (06-08-2020)
-------------------

* fixing timezone for policy-maintenance list


0.0.69 (30-08-2020)
-------------------

* Created the function create_and_add_to_pretty_table, added sort_by functionality for alerts so far


0.0.70 (30-08-2020)
-------------------

* Unnecessary check


0.0.71 (31-08-2020)
-------------------

* Removing debug line


0.0.72 (31-08-2020)
-------------------

* Added --last param to alerts list


0.0.73 (31-08-2020)
-------------------

* Adding --last to alerts count


0.0.74 (31-08-2020)
-------------------

* adding day indication to schedules timeline


0.0.75 (31-08-2020)
-------------------

* adding check if the sort-by argument is in the column headers


0.0.76 (12-10-2020)
-------------------

* override with schedule didnt work, fixed time format sent to lib


0.0.77 (13-11-2020)
-------------------

* Fixing to_datetime_string in override for hours section
