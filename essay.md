# Introduction
For the course project I modified the messaging app "Chirper" from `part3-16.xss`. The app has been modified to include several critical security vulnerabilities listed in the "OWASP Top Ten Web Application Security Risks". It can be installed and ran with the same instructions that were previously given in the course for Django apps.

# FLAW 1 (Injection)
The first critical vulnerability in the app is the `/delete` endpoint. The delete view is supplied with formdata `id` which corresponds to the id of the message to be deleted. This id is treated as a trusted source and is used unsanitized, it is instead directly concatenated to the SQL query. However an attacker could supply any string in the id formdata and perform an SQL injection attack.

There are two easy ways around the issue. Firstly the Django model system could be used for deleting messages, instead of a direct SQL query, Django would then internally create the correct queries and no string concatentation is required. Secondly if we want to keep using an SQL query, the `cursor.execute` function takes query parameters as an argument which could be used in place of string concatenation. These query parameters are automatically sanitized rather than being directly concatenated into the query and therefore are safe to use.

# FLAW 2 (Cross-Site Scripting)
Another way for the user to input information is the message field. This input is not assumed to be safe when making the SQL query to save it to the database and is not vulnerable to SQL attacks. However the input is not entirely sanitized. It is possible to input HTML and javascript into this field. When the message is displayed by any user the attacker's code will then be executed. This is known as an XSS attack.

One easy way to fix this would be to activate Django's autoescaping feature by removing the `safe` filter from the message's string interpolation in the template. The HTML/JS would then be shown as a regular string, rather than being executed in a user's browser. Another way to fix this would be to either sanitize or escape the message input before it is saved into the database, this would prevent future developers from accidentally reopening the vulnerability.

# FLAW 3 (Broken Authentication)
Before using the app, the user has to log in first. Each user session is given an unique sessionid. The sessionid is used to identify the user throughout many requests within the same session. However the way that these sessionids are generated is predictable and can be easily guessed. An attacker would look for a pattern in session ids by logging in and checking the sessionid cookie from their browser's developer tools. In our case the sessionid is a simple integer counter `n + 1` where `n` is the sessionid of the previous user. The attacker can therefore choose the sessionid of the previous user with `m - 1` where `m` is their own sessionid. Using this sessionid the attacker can act as if they were logged in as that user.

Again Django's features come useful here since Django's default session module offers a much more robust solution than the simple `n+1` form cookies that were implemented in this app. In fact for this issue to even exist in a Django app in the first place the user has to go out of their way to implement their own unsafe session module. Django's session module (or `SESSION_ENGINE`) uses long unique strings of random characters that are impractical for an attacker to try to guess.

# FLAW 4 (Broken Access Control):
During the development of Chirper a massive oversight was made, any user can delete any message! The messages page only shows buttons for deleting their own messages, but nothing is stopping an attacker from creating their own `POST` request to the `/delete` endpoint with formdata that includes any message id that they'd like.

This flaw could be fixed by finding the user correlated to the requests sessionid and checking whether the user is the owner of the message (or an administrator) before deleting it or returning a 403 HTTP code (forbidden/access denied).

# FLAW 5 (Insufficient Logging & Monitoring)
What happens when one of the previously mentioned flaws gets abused? The administrator actually has no way of knowing their system is compromised, unless the attacker decides to do something very dramatic like dropping a table from the database. There's no logging or monitoring in the entire app bar timestamped list of served endpoints.

There are many things that could be done to improve the situation, for example each served request could be logged with origin, parameters and formdata in a log file with Python's builtin logging module (which is recommended by the Django documentation). This could help debug attacks like SQL Injection, since the developer could see which request was last served before problems began.
