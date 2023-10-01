JUDGEMENT_RESPONSE_FORMAT = (
"""
[Response Format]
The judgement is either "allow" or "deny" and no other option. If you respond deny, provide 1 to 2 concise bullet points justifying your judgement.  Example outputs:
```
[Judgement]
deny
[Reasons]
- reason 1
- reason 2
```
or
```
[Judgement]
allow
```
"""
)

MISSION_COMPLETE_RESPONSE_FORMAT = (
"""[Response Format]
The [Status] is either 'complete', 'incomplete', or 'error'.  If you respond with incomplete, indicate what is left to be done.  If you respond with 'error', indicate some workarounds or other ways that the problem could be solved.
Example 1:
```
[Status]
complete
[Summary]
Here is a summary of what was done:
- goal 1
- goal 2
```
Example 2:
[Status]
incomplete
[Summary]
Here is what is left to be done:
- goal 1
- goal 2
```
Example 3:
[Status]
error
[Summary]
Come up with a workaround or alternative solution for the errors:
- error 1
- error 2
```
"""
)
