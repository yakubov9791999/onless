def makename(name):
    def wrapped(self):
        names = self.split(' ')
        names_list = list()
        i = 0
        for name in names:

            name = name.lower().replace('ц', 'ts').replace('ч', 'ch').replace('ю',
                                                                              'yu').replace(
                'а', 'a').replace('б', 'b').replace('қ', 'q').replace('қ', "o'").replace('ғ', "g'").replace('ҳ',
                                                                                                            "h'").replace(
                'в', 'v').replace('г', 'g').replace('д', 'd').replace('е',
                                                                      'e').replace(
                'ё', 'yo').replace('ж', 'j').replace('з', 'z').replace('и', 'i').replace('й', 'y').replace('к',
                                                                                                           'k').replace(
                'л', 'l').replace('м', 'm').replace('н', 'n').replace('о', 'o').replace('п', 'p').replace('р',
                                                                                                          'r').replace(
                'с', 's').replace('т', 't').replace('у', 'u').replace('ш', 'sh').replace('щ', 'sh').replace('ф',
                                                                                                            'f').replace(
                'э', 'e').replace('ы', 'i').replace('я', 'ya').replace('ў', "o'").replace('ь', "'").replace('ъ',
                                                                                                            "'").replace(
                '*',
                '').replace(
                '!', '').replace('~', '').replace('@', '').replace('#', '').replace('№', '').replace('$', '').replace(
                '%', '').replace('^', '').replace(':', '').replace('&', '').replace('?', '').replace('(', '').replace(
                ')', '').replace('-', '').replace('+', '').replace('=', '').replace('/', '').replace('<', '').replace(
                '>', '').replace('|', '').replace('€', '').replace('`', "'")

            i += 1
            if i != 4:
                name = name.capitalize()
            names_list.append(name)
        final_name = ' '.join(names_list)

        return final_name

    return wrapped


def makepasport(pasport):
    def wrapped(self):
        pasport = str(self)
        pasport = pasport.replace('А', 'A').replace('В', 'B').replace('С', 'C').replace('Т', 'T').replace('О',
                                                                                                          'O').replace(
            'М', 'M').replace('Р', 'P').replace(' ', '')

        return pasport

    return wrapped


def makesms(sms):
    def wrapped(self):
        sms = str(self)
        #filter lower
        sms = sms.replace('ц', 'ts').replace('ч', 'ch').replace('ю',
                                                                        'yu').replace(
            'а', 'a').replace('б', 'b').replace('қ', "q").replace('ў', "o'").replace('ғ', "g'").replace('ҳ',
                                                                                                        "h").replace(
            'х',
            "x").replace(
            'в', 'v').replace('г', 'g').replace('д', 'd').replace('е',
                                                                  'e').replace(
            'ё', 'yo').replace('ж', 'j').replace('з', 'z').replace('и', 'i').replace('й', 'y').replace('к',
                                                                                                       'k').replace(
            'л', 'l').replace('м', 'm').replace('н', 'n').replace('о', 'o').replace('п', 'p').replace('р',
                                                                                                      'r').replace(
            'с', 's').replace('т', 't').replace('у', 'u').replace('ш', 'sh').replace('щ', 'sh').replace('ф',
                                                                                                        'f').replace(
            'э', 'e').replace('ы', 'i').replace('я', 'ya').replace('ў', "o'").replace('ь', "'").replace('ъ', "'").replace('’', "'").replace('“', '"').replace('”', '"').replace(',', ',').replace('.', '.').replace(':', ':')
        # filter upper
        sms = sms.replace('Ц', 'Ts').replace('Ч', 'Ch').replace('Ю','Yu').replace(
            'А', 'A').replace('Б', 'B').replace('Қ', "Q").replace('Ғ', "G'").replace('Ҳ',"H").replace('Х',"X").replace(
            'В', 'V').replace('Г', 'G').replace('Д', 'D').replace('Е',
                                                                  'E').replace(
            'Ё', 'Yo').replace('Ж', 'J').replace('З', 'Z').replace('И', 'I').replace('Й', 'Y').replace('К',
                                                                                                       'K').replace(
            'Л', 'L').replace('М', 'M').replace('Н', 'N').replace('О', 'O').replace('П', 'P').replace('Р',
                                                                                                      'R').replace(
            'С', 'S').replace('Т', 'T').replace('У', 'U').replace('Ш', 'Sh').replace('Щ', 'Sh').replace('Ф',
                                                                                                        'F').replace(
            'Э', 'E').replace('Я', 'Ya')

        return sms

    return wrapped


@makename
def get_name(name):
    return name


@makepasport
def get_pasport(pasport):
    return pasport


@makesms
def get_sms(sms):
    return sms
