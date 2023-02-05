def is_url_fraudulent(url_string):
    if url_string is None or len(url_string)==0:
        raise ValueError("Invalid URL")
    num_dashes = url_string.count("-") 
    is_fraud = (num_dashes < 2) * 1 
    return is_fraud 

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str)
    args = parser.parse_args()
    print(is_url_fraudulent(args.url))
    