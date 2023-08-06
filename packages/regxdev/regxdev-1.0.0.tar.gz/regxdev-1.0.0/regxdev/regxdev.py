import re

def link_remover(string):
    text = re.sub(r'http\S+', '', string)  # Link remover
    text = re.sub(r'www\S+', '', text)
    text = re.sub(' +', ' ', text)  # Multiple whitespace
    text = re.sub('\n\n+', '\n', text)  # Removing multiple lines
    return text


def link_finder(string):
    text = re.findall(r'http\S+', string)  # http, https, www link finder
    text1 = re.findall(r'www\S+', string)
    return text + text1


def mail_extractor(string):
    text = re.findall(r'[\w\.-]+@[\w\.-]+', string)  # just normal mail id finder lol
    return text


def phone_finder(string):
    alpha = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    re1 = r'^[+]{1}[0-9]{1} [0-9]+.[0-9]+.[0-9]+'  # phone number with prefix +1 digit, followed by N digits
    re2 = r'^[+]{1}[0-9]{2} [0-9]+.[0-9]+.[0-9]+'  # phone number with prefix +2 digit, followed by N digits
    re3 = r'^[+]{1}[0-9]{3} [0-9]+.[0-9]+.[0-9]+'  # phone number with prefix +3 digit, followed by N digits
    numbers = []
    for i in range(0, (len(string) - 1)):
        num = string[i: i + 19]
        count, k = 0, 0
        for j in num:
            k += 1
            if j in alpha: count += 1
            if count >= 5: break
            if k == 15:
                num = re.compile("(%s|%s|%s)" % (re1, re2, re3)).findall(num)
                if len(num) != 0:
                    numbers.append(num)
    return numbers


def word_finder(word, string):
    # This can help u find index of N number of patterns present in the string
    # This returns list of tuples, of patterns present in the string
    # Calling  the function " word_finder('WORD_TO_FIND', STRING) "
    pat = f"{str(word)}"
    lt = []
    for match in re.finditer(pat, string):
        lt.append(match.span())
    return lt


def word_replacer(replace_word, replace_to, string):
    string = str(string)
    new_string = string.replace(replace_word, replace_to)
    return new_string