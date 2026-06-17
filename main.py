import pandas as pd

def read_csv(location):
    df = pd.read_csv(location)
    return df

def get_question(key):
    """
    Given any key which is the coloumn name in our dataset it will return the question
    """
    questions = pd.read_csv("Dataset//schema.txt" , index_col="Column").QuestionText # it tells us the question of the coloumn in the raw data
    return questions[key]

def main():
    survery_raw_df = read_csv("Dataset//results.txt")
    print(get_question("YearsCodePro"))

if __name__ == "__main__":
    main()
