# Vulnerable blog application
## Cyber Security Base 2022
## Project 1

### Description
A blogging application with login functionality. Once logged in, users can create and publish blog posts, as well as post comments on existing posts. Non-logged-in users can browse the available blog posts.

![Blog site frontpage](/img/frontpage.png)

## Installation
> **_NOTE:_**  On MacOS you might need to refer to a specific python version, e.g. `python3` or `pip3`.
- Clone the repository to your machine
- (Optional but preferred) Create a virtual environment inside the project folder
  1. `python -m venv env`
  2. Start the environment
      - Mac/Unix: `source env/bin/activate`
      - Windows: `env\Scripts\activate.bat`   
- Install requirements
  - `pip install -r requirements.txt`
- Start the server with `python manage.py runserver`

## Credentials

| Username       | Password          | 
|---------------|------------------|
| admin | admin |
| heikki        | verysecurepassword           |
| viivi        | verysecurepassword           |

> **_NOTE:_**  If for some reason no blogs are visible when you start the app, or you cannot log in to the user accounts, load the data with `./manage.py loaddata db.json`


## Vulnerabilities


### FLAW 1: SQL Injection:
The search functionality is vulnerable to an injection attack. 
```
posts = Post.objects.raw("SELECT * FROM blog_post WHERE title LIKE '%{}%'".format(query))
```
https://github.com/HeikkiLu/cybersecuritymooc-project1/blob/b23c66a28b8af672286bb431b6ab4a8d06e2872d/blog/views.py#L16

In this code, the query variable is directly inserted into the SQL statement using the format() method. If an attacker were to enter malicious code as the query variable, it would be incorporated into the SQL statement and executed by the database. This could allow the attacker to gain unauthorized access to the database, manipulate or steal data, or even take over the entire database.

To prevent this type of vulnerability, it is important to properly sanitize user-provided input before incorporating it into an SQL statement. This can be done by using parameterized queries that separate user input from the SQL statement, or by using other methods to ensure that only safe, valid data is incorporated into the SQL statement.

### FLAW 2: Broken Authentication:
```
class SessionStore(DBStore):
    def _get_new_session_key(self):
       session = "session0"
       counter = 0
       while self.exists(session):
           counter += 1
           session = "session" + str(counter)
       return session
```
https://github.com/HeikkiLu/cybersecuritymooc-project1/blob/26335904a547a21c125356ed8556d74772873f9a/vulnerable_blog/session_backend.py#L3

Because the session keys are generated using a simple counter and a predictable prefix, they can be easily guessed or brute-forced by an attacker. This could allow an attacker to impersonate a legitimate user and gain unauthorized access to their session data.

For example, if the session keys are generated using the following pattern:
`session0, session1, session2, ...` an attacker could easily guess or brute-force these keys by simply trying each number in sequence. If an attacker were able to guess or determine a valid session key, they could use it to gain access to the corresponding user's session data.

By default, Django uses a cryptographically secure random number generator (CSPRNG) to generate session keys. This ensures that session keys are unique, unpredictable, and resistant to brute-forcing or guessing attacks.

To use the built-in session key generator in Django, you can simply enable the SESSION_COOKIE_SECURE and SESSION_COOKIE_HTTPONLY settings in your project's settings.py file. This will enable secure, HTTP-only cookies to be used to store session keys, which will help to protect user data and prevent unauthorized access.

### FLAW 3: Security Misconfiguration
```
DEBUG = True
```
https://github.com/HeikkiLu/cybersecuritymooc-project1/blob/26335904a547a21c125356ed8556d74772873f9a/vulnerable_blog/settings.py#L26

When debug mode is turned on, detailed error messages may reveal sensitive information about your project, such as the full path to your project files on the server, the versions of software libraries that you are using, and even the source code of your application. This information can help attackers identify and exploit vulnerabilities in your application or its dependencies.

For these reasons, it's important to keep debug mode turned off in a production environment, and to make sure that it's only turned on when you are actively working on the project and need the extra information that it provides. This will help to protect your web application from potential security vulnerabilities.


### FLAW 4: Security Logging and Monitoring Failures
By default, Django does not enable any security-related logging. This means that a Django app will not log any security-related events unless the developer has specifically configured it to do so. Without a specific logging setup, a Django app may be vulnerable to the A09:2021 – Security Logging and Monitoring Failures weakness.

To enable security logging in Django, the developer will need to add appropriate loggers, handlers, and formatters to the app's configuration files. This will allow the app to log security-related events to a specific log file, or to send them to a remote logging server. The developer can then configure the app to monitor the logs and trigger alerts when certain security-related events occur.

It's important to note that simply enabling security logging in a Django app is not enough to protect it from potential security vulnerabilities. The app will also need to have appropriate monitoring and response measures in place to effectively detect and respond to security incidents. Without these measures, the app may still be vulnerable to attacks, even if it is logging security-related events.

### FLAW 5: Vulnerable and Outdated Components
```
sqlparse==0.4.1
```
https://github.com/HeikkiLu/cybersecuritymooc-project1/blob/26335904a547a21c125356ed8556d74772873f9a/requirements.txt#L3

Using outdated components in a web application can cause a number of problems, including security vulnerabilities and instability. Some of the specific problems that can occur when using outdated components include:

- Security vulnerabilities: Outdated components may have known vulnerabilities that have been discovered and fixed in newer versions of the component. If an attacker is able to exploit one of these vulnerabilities, they may be able to gain unauthorized access to your web application or its data.
- Compatibility issues: Newer versions of components may introduce changes that are not backward-compatible with older versions. This can cause your web application to break or malfunction if it is using an outdated component.
- Lack of support: Outdated components are often no longer supported by their developers, which means that they are not receiving security updates or patches. This can make your web application more vulnerable to attacks and other security vulnerabilities.
- Performance issues: Newer versions of components may include performance improvements and other enhancements that can help your web application run more efficiently. Using outdated components can prevent you from taking advantage of these improvements, potentially causing your web application to run slower or use more resources than necessary.

This project uses outdated version of the sqlparse library. It has a known vulnerability: https://nvd.nist.gov/vuln/detail/CVE-2021-32839. The vulnerability is a regular expression denial of service (ReDoS) vulnerability, which can cause the library to become unresponsive when processing certain types of input. This could potentially be exploited by an attacker to cause a denial of service (DoS) attack on your application.

The recommended solution to this issue is to update your application to use the latest version of the sqlparse library (version 0.4.2 or higher), which includes a fix for this vulnerability. You can update the library by running the following command: `pip install --upgrade sqlparse`

