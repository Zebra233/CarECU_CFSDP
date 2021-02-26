import re


def getUs(dt):
    """
    返回us
    :param dt:
    :return: timeUs
    """
    retime = re.compile('\d{2,3}')
    rtime = list(map(int, retime.findall(dt)))
    rtime[1] += rtime[0] * 60
    rtime[2] += rtime[1] * 60
    rtime[3] += rtime[2] * 1000
    rtime[4] += rtime[3] * 1000
    timeUs = rtime[4]
    return timeUs


def getMs(dt):
    """
    返回ms
    :param dt:
    :return: timeMs
    """
    retime = re.compile('\d{2,3}')
    rtime = list(map(int, retime.findall(dt)))
    rtime[1] += rtime[0] * 60
    rtime[2] += rtime[1] * 60
    rtime[3] += rtime[2] * 1000
    timeMs = rtime[3]
    return timeMs


def getS(dt):
    """
    返回s
    :param dt:
    :return: timeS
    """
    retime = re.compile('\d{2,3}')
    rtime = list(map(int, retime.findall(dt)))
    rtime[1] += rtime[0] * 60
    rtime[2] += rtime[1] * 60
    timeUs = rtime[2]
    return timeUs


def changeCol(ECUIDS, ID, name):
    """
    批量生成列名
    去除ECUID
    去除重复的Timestamp
    :param ECUIDS:
    :param ID:
    :param name:
    :return: dataframe
    """
    locals()['ECU' + str(name)] = ECUIDS[ECUIDS.ECUID == ID].rename(columns={'Data': name}).drop(['ECUID'],
                                                                                                 axis=1).drop_duplicates(
        subset='Timestamp')
    return locals().get('ECU' + str(name))


if __name__ == '__main__':
    Timestamp = []
    print(getUs("00:00:00:003:730"))
