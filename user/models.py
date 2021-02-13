from django.db import models


class User(models.Model):
    SEX = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATION = (
        ("北京", "北京"),
        ("上海", "上海"),
        ("深圳", "深圳"),
        ("郑州", "郑州"),
        ("西安", "西安"),
        ("成都", "成都"),
        ("沈阳", "沈阳"),
    )
    phonenum = models.CharField(verbose_name='手机', max_length=64, unique=True)
    nickname = models.CharField(verbose_name='昵称', max_length=64, default='匿名用户')
    gender = models.CharField(verbose_name='性别', max_length=6, choices=SEX)
    birthday = models.DateField(verbose_name='生日', max_length=32, default='1990-01-01')
    location = models.CharField(verbose_name='常住地', max_length=256, choices=LOCATION)
    avatar = models.CharField(verbose_name='形象', max_length=256)

    def to_dict(self):
        return {
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'gender': self.gender,
            'birthday': str(self.birthday),
            'location': self.location,
            'avatar': self.avatar
        }

    class Meta:
        db_table = 'user'


class Profile(models.Model):
    '''个人资料'''
    dating_gender = models.CharField(max_length=6, choices=User.SEX, default='male', verbose_name='匹配的性别')
    dating_location = models.CharField(max_length=15, choices=User.LOCATION, default='上海', verbose_name='目标城市')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_matche = models.BooleanField(default=True, verbose_name='不让未匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    class Meta:
        db_table = 'profile'
