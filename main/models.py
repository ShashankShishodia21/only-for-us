from django.db import models


class Students(models.Model):
	username = models.CharField(max_length=255, unique=True)
	fullname = models.CharField(max_length=255)
	email = models.EmailField(max_length=500, unique=True)
	admission_no = models.CharField(max_length=20, unique=True)
	course = models.CharField(max_length=255)
	datetime = models.DateTimeField()
	special_token = models.CharField(max_length=255, unique=True)
	password = models.CharField(max_length=255)
	course_year = models.CharField(max_length=255)

	def __str__(self):
		return self.username

class AdminData(models.Model):
	username = models.CharField(max_length=255, unique=True)
	fullname = models.CharField(max_length=255)
	email = models.EmailField(max_length=500, unique=True)
	admission_no = models.CharField(max_length=20, blank=True)
	datetime = models.DateTimeField()
	special_token = models.CharField(max_length=255, unique=True)
	password = models.CharField(max_length=255)
	rights = models.CharField(max_length=255)
	profession = models.CharField(max_length=255)

	def __str__(self):
		return self.username

class Course(models.Model):
	course_name = models.CharField(max_length=255, unique=True)

	def __str__(self):
		return self.course_name

class Semester(models.Model):
	semester_number = models.CharField(max_length=255, unique=True)
	course = models.ForeignKey('Course', on_delete=models.CASCADE)

	def __str__(self):
		return self.semester_number

class Subjects(models.Model):
	course = models.CharField(max_length=255)
	semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
	subject_name = models.CharField(max_length=255, unique=True)
	subject_code = models.CharField(max_length=255, unique=True)

	def __str__(self):
		return f"{self.subject_name}({self.subject_code})"

class Tutorials(models.Model):
	course = models.CharField(max_length=255)
	subject = models.ForeignKey('Subjects', on_delete=models.CASCADE)
	semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
	tutorial_number = models.CharField(max_length=255)
	tutorial_question = models.CharField(max_length=500, blank=True) # PDF name for Tutorial Question
	tutorial_solution = models.CharField(max_length=500) # PDF name for Tutorial Solution
	author = models.CharField(max_length=255) # from admin data model
	datetime = models.DateTimeField()

	def __str__(self):
		return f"{self.course}/{self.semester}/{self.subject}/{self.tutorial_number}"

class Polls(models.Model):
	poll_id = models.CharField(max_length=255, primary_key=True, unique=True)
	poll_topic = models.CharField(max_length=500)
	option_1 = models.CharField(max_length=500)
	option_2 = models.CharField(max_length=500)
	option_3 = models.CharField(max_length=500, blank=True)
	option_4 = models.CharField(max_length=500, blank=True)
	submitted = models.CharField(max_length=500)
	leading_option = models.CharField(max_length=500, blank=True)
	datetime = models.DateTimeField()
	author = models.CharField(max_length=255) # from admin data model

	def __str__(self):
		return f"{self.poll_id}({self.poll_topic})"

class PollSubmitted(models.Model):
	poll_id = models.CharField(max_length=255)
	poll_topic = models.CharField(max_length=500)
	username = models.ForeignKey('Students', on_delete=models.CASCADE)
	option_selected = models.CharField(max_length=500)
	datetime = models.DateTimeField()

	def __str__(self):
		return f"{self.username} => {self.poll_topic}"

class ContactQueries(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField(max_length=500)
	phone = models.CharField(max_length=100)
	gender = models.CharField(max_length=10)
	message = models.TextField()
	datetime = models.DateTimeField()

	def __str__(self):
		return self.name
