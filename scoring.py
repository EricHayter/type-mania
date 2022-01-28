# input_string should always be less shorter than the target string
def calculateScore(input_string, target_string):
    mutual = 0
    length = len(target_string)
    try:
        for i, e in enumerate(input_string):
            if e == target_string[i]:
                mutual += 1

        return int(mutual / length * 100)
    except:
        return 0