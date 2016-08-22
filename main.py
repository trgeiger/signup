import webapp2
import cgi
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Signup</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

signup_form = """
<form action="/" method="post">
    <table>
        <tbody>
            <tr>
                <td>Username:</td>
                <td><input type="text" name="username" autofocus required value= %(user)s >
                <span class="error">%(uerror)s</span></td>
            </tr>
            <tr>
                <td>Password:</td>
                <td><input type="password" name="password" pattern="^.{3,20}$" required>
                <span class="error">%(perror)s</span></td>
            </tr>
            <tr>
                <td>Confirm Password:</td>
                <td><input type="password" name="verify" pattern="^.{3,20}$" required>
                <span class="error">%(verror)s</span></td>
            </tr>
            <tr>
                <td>Email (optional):</td>
                <td><input type="email" name="email" value= %(email)s>
                <span class="error">%(eerror)s</span></td>
            </tr>
        </tbody>
    </table>
    <input type="submit" value="Submit">
</form>
"""

page = page_header + signup_form + page_footer

class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
    """

    def write_form(self, uerror="", perror="", verror="", eerror="", user="", email=""):
        self.response.out.write(page %{"uerror": uerror, "perror": perror, "verror": verror, "eerror": eerror, "user": user, "email": email})

    def get(self):

        header = "<h3></h3>"

        self.write_form()

    def post(self):
        # look inside the request to figure out what the user typed
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        # regular expressions for user input verification
        username_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        password_re = re.compile(r"^.{3,20}$")
        email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

        def valid_input(input, regexp):
            return regexp.match(input)

        # if the user typed invalid username, give error
        if not valid_input(username, username_re):
            uerror = "Invalid username"
        else:
            uerror = ""

        # if the user typed invalid password, give error
        if not valid_input(password, password_re):
            perror = "Invalid password"
        else:
            perror = ""

        # check if password matches verify
        if password != verify:
            verror = "Please reconfirm your password"
        else:
            verror = ""

        #if user typed invalid email address, give error
        if (email != "") and (not valid_input(email, email_re)):
            eerror = "Invalid email address"
        else:
            eerror = ""

        # if any of the above errors are triggered, preserve user input and clear password, display error messages
        if not (valid_input(username, username_re) and valid_input(password, password_re) and (password == verify)):
            self.write_form(uerror, perror, verror, eerror, username, email)
        else:
            self.redirect("/welcome?username=" + username)




class Welcome(webapp2.RequestHandler):
    """ Handles requests coming in to '/welcome'
    """

    def get(self):
        # look inside the request to figure out what the user typed
        username = self.request.get("username")

        # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
        username = cgi.escape(username, quote=True)

        # build response content
        confirm_signup_message = "Welcome " + username + "!"
        response = page_header + "<p>" + confirm_signup_message + "</p>" + page_footer
        self.response.write(response)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
