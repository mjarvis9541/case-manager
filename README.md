# Case Manager

Case manager application to track employee productivity, workflow, time in the office, log in/out times, view work stats in real-time, run and download various reports to csv.

## Notes

1. Productivity Tracker
Mins for triage cases:
- IDV Proof - 15
- Reclassified - 2.5
- Final Final - 3
- Final Final Shell - 4

2. Time Tracker
- TBC


Template tag filters
{% if perms.auth.add_something %}
 {{ do_something }}
{% endif %}
