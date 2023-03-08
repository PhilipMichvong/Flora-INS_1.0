import sys
import pandas as pd
import matplotlib.pyplot as plt

'''
    Description:
        Program to draw plots by data from csv files
    
    Params:
        <datafilepath> : Path to csv file with data to visualization.
                            It is available to pass multiple paths.
                            
    Example:
        python plot.py ./data/data1.csv ./data/data2.csv ./data/org/dataorg1.csv
        
'''

def main() -> None:
    if len(sys.argv) < 2:
        print('Incorrect usage! Pass the csv filepath.')
        sys.exit(1)
    
    for i in range(1, len(sys.argv)):
        fpath = sys.argv[i]
        print(f'File: {fpath} : ', end='')
        
        try:
            # Try to open given file
            df = pd.read_csv(fpath)
            
            df = df[::10]
            
            # Create plot
            df.set_index(df.keys()[0]).plot(title=fpath)
            print('Loaded.')
        
        except FileNotFoundError as e:
            print('Not Found!')
    
    # Show plots
    plt.show()
    
    sys.exit(0)

if __name__ == '__main__':
    main()