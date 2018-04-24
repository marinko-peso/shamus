import random
import sys
sys.path.append('..')

from shamus import shamus


names = ['Steve', 'Michael', 'Tom']
language = ['Python', 'Javascript', 'Java', 'PHP']


@shamus()
def generate_coders():
    final_list = list()
    for i in xrange(800000):
        final_list.append({
            'order': i,
            'name': random.choice(names),
            'codes': random.choice(language)
        })
    return final_list


if __name__ == '__main__':
    generate_coders()
