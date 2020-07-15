import requests  # here we can manually request something and get data
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching:{res.status_code},check again')
    return res


def get_pswrd_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1pswrd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1pswrd[:5], sha1pswrd[5:]
    response = request_api_data(first5_char)
    print(first5_char, tail)
    return get_pswrd_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times..! ')
        else:
            print(f'{password} was not found.carry on!')
    return 'done'

if __name__=='__main__':
    sys.exit(main (sys.argv[1:]))




