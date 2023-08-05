import time
import argparse
from math import pow,sqrt



def main():
    parser=argparse.ArgumentParser(description="num calc")
    parser.add_argument("--pow",type=int,help="calc the number pow")
    parser.add_argument("--sqrt",type=int,help="calc the number sqrt")
    args=parser.parse_args()
    if args.pow is not None:
        print("pow",pow(args.pow,2))
    if args.sqrt is not None:
        print("sqrt",sqrt(args.sqrt))


if __name__=="__main__":
    print("test")
    main()

