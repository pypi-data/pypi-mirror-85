import requests
import argparse

def test(url):
    resp=requests.get(url)
    return resp.status_code

def main():
    parse=argparse.ArgumentParser()
    parse.add_argument("--url",type=str,help="url address")
    args=parse.parse_args()
    if args.url:
        test(args.url)

if __name__=="__main__":
    main()