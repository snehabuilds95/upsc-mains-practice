
#from django.db import models

#class UserSession(models.Model):
 #   name = models.CharField(max_length=100)
 #   email = models.EmailField()
 #   uploaded_file = models.FileField(upload_to='uploads/')
 #   created_at = models.DateTimeField(auto_now_add=True)

  #  def __str__(self):
  #      return self.name


from django.db import models

class UserSession(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    uploaded_file = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"

class Question(models.Model):
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='questions')
    number = models.IntegerField()
    text = models.TextField()
    marks = models.IntegerField()

    def __str__(self):
        return f"Q{self.number} ({self.marks} marks)"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    time_taken_seconds = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer to Q{self.question.number}"
