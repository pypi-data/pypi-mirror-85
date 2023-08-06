from importlib import resources  # Python 3.7+
import sys

from nosai import numbers

def main():
    # If a number is given as argument
    if len(sys.argv) == 1:
        print(numbers.spell(sys.argv[1]))
      
    elif len(sys.argv) > 1:
        print("Please enter only one number as argument")
      
    else:
        print("Enter the number as a argument")
        
        
if __name__ == "__main__":
    main()
