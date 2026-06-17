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

def get_required_info(raw_data , raw_schema):
    """
    Since the data has a lot of coloumns we will limit our surveys to the coloumns that we will need for this analysis
    """

    required_coloumns = [
        'Country',
        'Age',
        'Gender',
        'EdLevel',
        'UndergradMajor',
        'Hobbyist',
        'Age1stCode',
        'YearsCode',
        'YearsCodePro',
        'LanguageWorkedWith',
        'LanguageDesireNextYear',
        'NEWLearn',
        'NEWStuck',
        'Employment',
        'DevType',
        'WorkWeekHrs',
        'JobSat',
        'JobFactors',
        'NEWOvertime',
        'NEWEdImpt'
    ]

    survey_df = raw_data[required_coloumns].copy()
    schema = raw_schema[required_coloumns]

    return survey_df , schema

def convert_numeric(df , coloumn):
    df[coloumn] = pd.to_numeric(df[coloumn] , errors="coerce") # this coerece will not raise an error it will simply convert the values into the nums and where error occur it will store Nan

def drop_incorrect(df , coloumn , max = 1000000 , min = 0):
    df.drop(df[df[coloumn] > max].index , inplace = True)
    df.drop(df[df[coloumn] < min].index , inplace = True)

def main():
    survery_raw_df = read_csv("Dataset//results.txt")
    raw_schema = pd.read_csv("Dataset//schema.txt" , index_col="Column").QuestionText
    survey_df , schema = get_required_info(survery_raw_df , raw_schema )
    convert_numeric(survey_df , "Age1stCode")
    convert_numeric(survey_df , "YearsCode")
    convert_numeric(survey_df , "YearsCodePro")
    drop_incorrect(survey_df , "Age" , 100 , 10 )
    drop_incorrect(survey_df , "WorkWeekHrs" , 140 )
    print(survey_df.describe())

if __name__ == "__main__":
    main()
