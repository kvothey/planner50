from functools import wraps
from flask import session, redirect, render_template, request

#Checks if user is logged in before allowing access to routes
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

#Determines what Gen Eds a course fulfills
def gened(notes):
    search = ["Aesthetic and Interpretive Understanding", "Culture and Belief", "Societies of the World", "United States in the World", "Ethical Reasoning", "Empirical and Mathematical Reasoning", "Science of the Physical Universe", "Science of Living Systems"]
    out = []

    for term in search:
        if notes.find(term) != -1:
            out.append(term)
    return out

    