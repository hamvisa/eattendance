from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import safestring


class PersonManager(BaseUserManager):  # As Person is a custom user, so it needs a manager.
    def create_user(self, email_id, id, first_name, last_name, phone_number, password=None):
        if not email_id:
            raise ValueError('User must have a valid email address.')

        email_id = self.normalize_email(email_id)
        person = self.model(id=id, first_name=first_name, last_name=last_name, phone_number=phone_number,
                            email_id=email_id)
        person.set_password(password)
        person.save()
        return person

    def create_superuser(self, email_id, id, first_name, last_name, phone_number, password):
        person = self.create_user(email_id, id, first_name, last_name, phone_number, password)
        person.is_superuser = True
        person.save()
        return person


class Person(AbstractBaseUser):  # Making Person a custom User model
    id = models.CharField(primary_key=True, max_length=10, unique=True, blank=False, null=False, help_text="Roll Number")
    first_name = models.CharField(max_length=35, unique=False, null=False, blank=False, help_text="First Name")
    last_name = models.CharField(max_length=35, unique=False, null=False, blank=False, help_text="Last Name")
    phone_number = models.CharField(max_length=10, unique=True, null=False, blank=False,
                                    help_text="10 digit Mobile Number")
    email_id = models.EmailField(max_length=254, unique=True, blank=False, help_text="Email ID")

    profile_picture = models.ImageField(upload_to="Profile Pictures/", null=True, default="/Profile Pictures/default/default.png",
                                        help_text="Profile Picture", blank=True)
    training_dataset = models.FileField(upload_to="Training Dataset/", null=True, default=None,
                                        help_text="Training Dataset .zip file", blank=True)
    user_since = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Is the person active?")
    is_superuser = models.BooleanField(default=False, help_text="Is the person a superuser?")

    USERNAME_FIELD = 'email_id'
    EMAIL_FIELD = 'email_id'
    REQUIRED_FIELDS = ['id', 'first_name', 'last_name', 'phone_number', ]

    objects = PersonManager()

    # def get_full_name(self):
    #     pass
    #
    # def get_short_name(self):
    #     pass

    def __str__(self):
        return self.id + "\t" + self.first_name + " " + self.last_name + "\t" + self.email_id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser


class Year(models.Model):
    FYBTech = "F.Y. B.tech"
    SYBTech = "S.Y. B.tech"
    TYBtech = "T.Y. B.tech"
    LYBtech = "L.Y. B.tech"
    options = [
        (FYBTech, FYBTech),
        (SYBTech, SYBTech),
        (TYBtech, TYBtech),
        (LYBtech, LYBtech),
    ]
    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=254, null=False, blank=False, unique=True, choices=options,
                            help_text="choose an option.")

    def acronym(self):
        if self.year == self.FYBTech:
            return "FY"
        elif self.year == self.SYBTech:
            return "SY"
        elif self.year == self.TYBtech:
            return "TY"
        else:
            return "LY"

    def __str__(self):
        return self.acronym() + " - " + self.year


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    COMPS = "Computer Engineering"
    IT = "Information Technology"
    MECH = "Mechanical engineering"
    EXTC = "Electronics & Telecommunication Engineering"
    ETRX = "Electronics Engineering"
    SH = "Science & Humanities"
    options = [
        (COMPS, COMPS),
        (IT, IT),
        (MECH, MECH),
        (EXTC, EXTC),
        (ETRX, ETRX),
        (SH, SH),
    ]

    name = models.CharField(max_length=254, null=False, blank=False, unique=True, choices=options,
                            help_text="Department name.")

    def __str__(self):
        html = self.name
        string = safestring.mark_safe(html)
        return string

    def acronym(self):
        if self.name == self.COMPS:
            return "COMPS"
        elif self.name == self.IT:
            return "IT"
        elif self.name == self.MECH:
            return "MECH"
        elif self.name == self.EXTC:
            return "EXTC"
        elif self.name == self.ETRX:
            return "ETRX"
        else:
            return "S&H"


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=25, null=False, blank=False, unique=True, help_text="Subject Code.")
    name = models.CharField(max_length=254, null=False, blank=False, unique=True, help_text="Subject name.")
    initials = models.CharField(max_length=25, null=False, blank=False, unique=True, help_text="Subject's initials.")
    year = models.ForeignKey(to=Year, on_delete=models.DO_NOTHING, null=False,
                             help_text="Subject for which Year students?")
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, null=False,
                                   help_text="Subject's Department")

    def __str__(self):
        return self.code + "-" + self.name + ", " + self.year.acronym() + ", " + self.department.acronym()


class Student(models.Model):
    person = models.OneToOneField(to=Person, on_delete=models.CASCADE, primary_key=True, null=False,
                                  help_text="Person who this Student is")
    year = models.ForeignKey(to=Year, on_delete=models.DO_NOTHING, null=False,
                             help_text="Subject for which Year students?")
    options_division = [('A', 'A'), ('B', 'B'), ]
    division = models.CharField(max_length=1, null=False, choices=options_division, help_text="Division, eg: B")
    options_batch_A = [('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ]
    options_batch_B = [('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'), ]
    options = options_batch_A + options_batch_B
    batch = models.CharField(max_length=2, null=False, choices=options, help_text="Student's Batch, eg: B2")
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, null=False,
                                   help_text="Student's Department")

    def __str__(self):
        return str(self.person.id) + " - " + self.year.acronym() + " - " + self.division + " - " + self.batch


class Admin(models.Model):
    person = models.OneToOneField(to=Person, on_delete=models.CASCADE, primary_key=True, null=False,
                                  help_text="Person who this Admin is")

    def __str__(self):
        return str(self.person)


class Faculty(models.Model):
    person = models.OneToOneField(to=Person, on_delete=models.CASCADE, primary_key=True, null=False,
                                  help_text="Person who this Faculty is")
    initials = models.CharField(max_length=10, null=False, blank=False, help_text="Faculty's Initials")
    room_number = models.CharField(max_length=10, null=False, blank=True, default="",
                                   help_text="Room Number. eg: B-201")

    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, null=False,
                                   help_text="Faculty's Department")

    def __str__(self):
        return str(self.person) + ', ' + str(self.room_number) + ', ' + str(self.department)


class Schedule(models.Model):
    options1 = [
        ('A', 'A'), ('B', 'B'),
    ]
    options2 = [
        ('SUN', 'Sunday'), ('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'),
        ('FRI', 'Friday'), ('SAT', 'Saturday'),
    ]
    options3 = [
        ('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'),
        ('FC', 'Full Class'),
    ]
    id = models.AutoField(primary_key=True)
    day = models.CharField(max_length=10, null=False, blank=False, choices=options2,
                           help_text="Choose the day.")
    beginning_time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="Lecture beginning time")
    ending_time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="Lecture ending time")

    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, null=False,
                                   help_text="Faculty's Department")
    year = models.ForeignKey(to=Year, on_delete=models.DO_NOTHING, null=False,
                             help_text="Subject for which Year students?")
    division = models.CharField(max_length=1, null=False, blank=False, choices=options1,
                                help_text="Choose the division")
    batch = models.CharField(max_length=2, null=False, blank=False, default='FC', choices=options3,
                             help_text="Choose the batch")

    faculty = models.ForeignKey(to=Faculty, on_delete=models.DO_NOTHING, null=False,
                                help_text="Faculty who's teaching for this schedule.")
    subject = models.ForeignKey(to=Subject, on_delete=models.DO_NOTHING, null=False, help_text="Lecture Subject.")
    lecture_class = models.CharField(max_length=10, null=False, blank=False, default='-', help_text="Class Room in which lecture will be conducted")

    def facultyName(self):
        return self.faculty.initials + ": " + self.faculty.person.first_name + " " + self.faculty.person.last_name

    def subjectName(self):
        return self.subject.initials + ": " + self.subject.name

    def __str__(self):
        return self.day + ": " + str(self.beginning_time) + "-" + str(self.ending_time) + ". " + str(
            self.department.acronym()) + ", " + str(
            self.year.acronym()) + ", " + self.division + ", " + self.batch + " by: " + self.faculty.initials + " Sub:" + self.subject.initials


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now=True)

    # lecture_commencement_timestamp = models.DateTimeField(auto_now=False, null=False, blank=False,
    #                                                       help_text="Date and Time when lecture begins.")
    # lecture_ended_timestamp = models.DateTimeField(auto_now=False, null=False, blank=False,
    #                                                help_text="Date and Time when lecture ended.")
    # subject = models.ForeignKey(to=Subject, on_delete=models.DO_NOTHING, null=False, help_text="Lecture Subject.")
    # faculty = models.ForeignKey(to=Faculty, on_delete=models.DO_NOTHING, null=False,
    #                             help_text="Faculty who's teaching for this lecture.")
    schedule = models.ForeignKey(to=Schedule, on_delete=models.DO_NOTHING, null=False,
                                 help_text="Schedule for this attendance")
    student = models.ForeignKey(to=Student, on_delete=models.DO_NOTHING, null=False,
                                help_text="Student whose Attendance is being marked")
    present = models.BooleanField(default=False, null=False, help_text="Student Present?")
    concession = models.BooleanField(default=False, null=False, help_text="Attendance obtained via concession?")
    modified = models.BooleanField(default=False, null=False, help_text="Attendance modified by teacher?")

    def __str__(self):
        return str(self.timestamp) + "- " + str(self.schedule.__str__()) + "- " + str(self.student.__str__())

class Camera(models.Model):
    id = models.AutoField(primary_key=True)
    lecture_class = models.CharField(max_length=10, null=False, blank=False, default='-', help_text="Class Room in which lecture will be conducted")
    url = models.URLField(max_length=200)
