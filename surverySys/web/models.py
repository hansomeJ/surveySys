from django.db import models


# Create your models here.

class ClassList(models.Model):
    """
    班级表
    """
    name = models.CharField(max_length=32, verbose_name='班级名')


class Survey(models.Model):
    """
    问卷表
    """
    grade = models.ForeignKey('ClassList', on_delete=models.CASCADE, verbose_name='班级')
    times = models.PositiveSmallIntegerField(verbose_name='第几次')
    survey_templates = models.ManyToManyField('SurveyTemplate', blank=True, verbose_name='问卷模板')
    count = models.PositiveSmallIntegerField("生成的唯一码数量")
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class SurveyCode(models.Model):
    """
    唯一码表
    """
    unique_code = models.CharField(max_length=10, unique=True, verbose_name='唯一码')
    survey = models.ForeignKey("Survey", on_delete=models.CASCADE, verbose_name='问卷')
    is_used = models.BooleanField(default=False, verbose_name='是否使用')
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class SurveyTemplate(models.Model):
    """
    问卷模板表
    """
    name = models.CharField(max_length=64, verbose_name='模板名称')
    questions = models.ManyToManyField('SurveyQuestion', verbose_name='问题')
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class SurveyQuestion(models.Model):
    """
    问卷问题表
    """
    survey_type_choices = (
        ('choice', '单选'),
        ('suggest', '建议'),
    )
    survey_type = models.CharField(max_length=32, choices=survey_type_choices, verbose_name='问题类型')
    title = models.CharField(max_length=64, verbose_name='问题名')
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class SurveyChoice(models.Model):
    """
    选项表
    """
    question = models.ForeignKey('SurveyQuestion', on_delete=models.CASCADE, verbose_name='问题')
    title = models.CharField(max_length=32, verbose_name='选项名')
    score = models.PositiveSmallIntegerField(verbose_name='得分')


class SurveyRecord(models.Model):
    """
    问卷记录表
    """
    question = models.ForeignKey("SurveyQuestion", on_delete=models.CASCADE, verbose_name='问题记录')
    survey_code = models.ForeignKey('SurveyCode', on_delete=models.CASCADE, verbose_name='唯一码')
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, verbose_name='问卷')
    choice = models.ForeignKey('SurveyChoice', on_delete=models.CASCADE, null=True, blank=True, verbose_name='选项')
    score = models.PositiveSmallIntegerField('得分')
    content = models.CharField(max_length=1024, null=True, blank=True, verbose_name='建议')
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
