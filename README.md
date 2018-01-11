Victor Qin, CS50 Final Project, Fall 2017: planner.cs50
TF: Doug Smith

Credit to courses.cs50.net, CS50 Fall 2017 Pset7 for inspiration
Thanks to David J Malan, Miles Fertel

I Setup
	Open up a console and navigate to the final project's folder, in the same folder as application.py. Run "flask run", and open the link given. The application currently runs locally.

II Login
	In the upper right, click on Register to register for a new account. After you've successfully created one, you'll be led back to the login page. Use your new credential to login there, and you will led to the index page.

III Search
	The upper left corner, once you've been logged in, will have two links: Index and Search. Search will allow you to look up courses in the "Search Courses" box and select what semester to look for courses in using the Semester drop-down menu. The Search bar will look for the title of courses and by course abbreviations (the abbreviations need to be exactly correct). Press Enter or click Look Up to search the courses.cs50 database. Click Save to List to add the selected course to the user's course cart.

IV Index
	1. Course Cart
		In the Course Cart, you can select the Semester (1st=fall, 2nd=spring) and Year (Freshman, Sophmore, Junior, Senior), then click Add to slot the course into the Semester Planning section. To remove a course from your course cart, click the x to the far right.
	2. Semester Planning
		The Semester Planning section is split into 8 semesters by default. Courses added from the Course Cart will display in their respective semesters. To remove it from the semester, click the x to the far right and will remove the course back to the course cart. There is no limit for how many courses can be added per semester.
	3. General Education Requirements
		Any course that has been added Semester Planning that satisfies a general education requirement will be able to fill one and only one of the slots. Use the drop-down menu to select a course, then click add to use the course to fill the line.


