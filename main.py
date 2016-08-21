import webapp2
import cgi

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Caesar Cipher</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Caesar Cipher</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""


class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
    """

    def get(self):

        header = "<h3>For secrets...</h3>"

        # a form for implementing rotation cipher
        cipher_form = """
        <form action="/rotate" method="post">
            <fieldset>
                <legend><strong>Input</strong></legend>
                Rotation Amount:<br>
                <input type="text" name="rotation"><br>
                Phrase:<br>
                <input type="text" name="phrase"><br><br>
                <input type="submit" value="Submit">
            </fieldset>
        </form>
        """

        # if we have an error, make a <p> to display it
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        # combine all the pieces to build the content of our response
        main_content = header + cipher_form + error_element
        response = page_header + main_content + page_footer
        self.response.write(response)


class Signup(webapp2.RequestHandler):
    """ Handles requests coming in to '/signup'
    """

    def post(self):
        # look inside the request to figure out what the user typed
        phrase = self.request.get("phrase")
        rotation = self.request.get("rotation")

        # if the user typed nothing at all, redirect and yell at them
        if (phrase == "") and (rotation == ""):
            error = "You didn't type anything."
            self.redirect("/?error=" + error)

        if (phrase == "") or (rotation== ""):
            error = "You didn't type anything."
            self.redirect("/?error=" + error)

        #check if rotation is a numeral
        if rotation.isdigit():
            rotation = int(rotation)
        elif rotation.isalpha():
            error = "Your rotation must be an integer."
            self.redirect("/?error=" + error)

        # if the user wants to cipher a phrase that contains numerals, display error
        if not all(x.isalpha() or x.isspace() for x in phrase):
            error = "Your phrase can only contain alphas and spaces."
            self.redirect("/?error=" + error)

        # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
        phrase = cgi.escape(phrase, quote=True)
        #rotation = cgi.escape(rotation, quote=True)

        # use the caesar.py file to enact the cipher using phrase and rotation
        if all(x.isalpha() or x.isspace() for x in phrase) and (type(rotation) is int):
            new_phrase = caesar.encrypt(phrase, rotation)

        # build response content
            new_phrase_element = "<h2>Your encrypted phrase:</h2><br>" + "<p>" + new_phrase + "</p>"
            response = page_header + "<p>" + new_phrase_element + "</p>" + page_footer
            self.response.write(response)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/rotate', RotatePhrase)
], debug=True)
