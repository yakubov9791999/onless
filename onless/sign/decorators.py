
def makeslug(slug):
    def wrapped(self):
        slug = self.strip()
        slug = slug.lower().replace('ц', 'ts').replace('ч', 'ch').replace('ю',
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
            'э', 'e').replace('ы', 'i').replace('я', 'ya').replace('ў',"u").replace('ь', "'").replace('ъ', "'").replace('*',
                                                                                                       '').replace(
            '!', '').replace('~', '').replace('@', '').replace('#', '').replace('№', '').replace('$', '').replace(
            '%', '').replace('^', '').replace(':', '').replace('&', '').replace('?', '').replace('(', '').replace(
            ')', '').replace('-', '').replace('+', '').replace('=', '').replace('/', '').replace('<', '').replace(
            '>', '').replace('|', '').replace('€', '').replace(' ','-')

        return slug

    return wrapped


@makeslug
def get_slug(slug):
    return slug

