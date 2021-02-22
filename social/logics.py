import datetime

from user.models import User
from user.models import Profile
from social.models import Swiped
from social.models import Friends
from libs.cache import rds


def rcmd_from_db(uid, num):
    """机器人用户"""
    profile, _ = Profile.objects.get_or_create(id=uid)

    today = datetime.date.today()
    # 最早出生的人生日
    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)
    # 最晚出生的人的生日
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)

    # 排除滑动过的人
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    users = User.objects.filter(
        gender=profile.dating_gender,
        location=profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday,
    ).exclude(id__in=sid_list)[:num]
    return users


def users_from_rds(uid):
    """从Redis中提取用户"""
    user_id_list = rds.lrange('FIRST_K_%s' % uid, 0, 19)
    users = [user for user in User.objects.filter(id__in=user_id_list)]
    return users


def rcmd(uid):
    """数据库与Redis用户和"""
    rds_users = users_from_rds(uid)
    count = 20 - len(rds_users)
    db_users = rcmd_from_db(uid, count)
    users = list(rds_users) + list(db_users)
    return users


def like_someone(uid, sid):
    """
    喜欢某人函数
    1.Swiped表中记录喜欢某人
    2.检查Swiped表中对方是否喜欢过我
    3.如果喜欢匹配成好友
    :param uid:
    :param sid:
    :return: True or False or None
    """
    Swiped.objects.create(uid=uid, sid=sid, stype='like')
    if Swiped.is_liked(sid, uid):
        Friends.make_friends(uid, sid)

        return True
    else:
        return False


def superlike_someone(uid, sid):
    Swiped.objects.create(uid=uid, sid=sid, stype='superlike')

    liked_me = Swiped.is_liked(sid, uid)

    if liked_me:
        Friends.make_friends(uid, sid)
        return True
    elif liked_me == False:
        return False
    else:
        # 对方并没有滑动过uid,将uid添加到对方的“优先推荐队列”
        rds.rpush('FIRST_K_%s' % sid, uid)
        return False