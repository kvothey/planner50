Victor Qin, CS50 Final Project, Fall 2017: planner.cs50
TF: Doug Smith

Credit to courses.cs50.net, CS50 Fall 2017 Pset7 for inspiration
Thanks to David J Malan, Miles Fertel

Overall:
Both courses.cs50 and my.harvard don't offer working 4-year course planners. This is especially important for prospective STEM students who are looking to plan their future coursework, and who may be confused about their general education requirements. I designed a planner to fill this gap in student resources, with a special focus on displaying what requirements each course fills.

I. application.py
	1. index():
		Index loads up all the user's data and selected courses. The first SQL select will get the user's courses, then the for loops searches through courses and Qcourses to find the rest of the information that will be displayed to the index. Finally, the last few statements find which semesters each course belongs in.
	2. search():
		The search splits into three statements depending on if the user selects semesters to search in. The query has percent signs added to both the beginning and end to get as many hits as possible. The second for loop will take all the hits and get the abbreviations and general Q scores.
	3. add():
		If the course is added by the users, SQL updates user_courses to add that course in.
	4. semester():
		Semester checks and updates what course belongs in what semester - if the course isn't availible during that semester, then the error message responds.
	5. remove():
		Remove takes the course out of the user's Course Cart
	6. reset():
		Take the course out of the user's planner
	7. requirements():
		Add the course to fill that General Education slot.
	8. remreq():
		Remove the course from that General Education slot.

II. helpers.py
	1. login_required(f):
		Defines the login_required settings for application.py
	2. apology(message, code=400):
		Defines the apology memes
	3. gened(notes):
		Checks if a given course fulfills a general education requirement.

