import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

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

def replace_multiselect(df , coloumn):
    """
    In the give data set for example the age allows for multiple selection and this will mess up the analysis so we hv to clean it by replacing it with empty value
    """

    df.where(~(df[coloumn].str.contains(";" , na = False)) , np.nan , inplace = True)
    #Keeps only rows where Gender does NOT contain “;”; replaces all other rows with NaN in the DataFrame (in-place).
    # find the row that has ; and then using not make them false and then replace them with nan

def get_gender_counts(df):
    
    return df["Gender"].value_counts(dropna = False)

def get_undergrad_percent(df):
    prect_Value = df["UndergradMajor"].value_counts() * 100 / df["UndergradMajor"].count()
    return prect_Value

def visualize_data(df , type , total_num = 5 , coloumn = None):
    sns.set_style("darkgrid")
    matplotlib.rcParams['font.size'] = 14
    matplotlib.rcParams['figure.figsize'] = (9 , 5)
    matplotlib.rcParams['figure.facecolor'] = '#00000000'

    if type == "bar":
        top_values = df[coloumn].value_counts().head(total_num)
        plt.figure(figsize=(12,5))
        plt.title(coloumn)
        plt.xticks(rotation = 75)
        sns.barplot(x=top_values.index , y=top_values)
        plt.show()
    elif type == "hist":
        plt.figure(figsize=(12,5))
        plt.title(coloumn)
        sns.histplot(data=df[coloumn] , bins=np.arange(10 , 80 , 5) , color="purple")
        plt.show()     
    elif type == "pie":
        plt.figure(figsize=(12,5))
        plt.title(coloumn)
        plt.pie(df , labels=df.index , autopct="%1.1f%%" , startangle=180)
        plt.show()            
    elif type == "hbar":
        plt.figure(figsize=(12,6))
        plt.title(coloumn)
        plt.xticks(rotation = 75)
        sns.countplot(y=df[coloumn])
        plt.show()   

def split_multicolumn(series):
    """
    Takes a column with multiple values separated by ';'
    and converts it into a one-hot encoded DataFrame.
    """

    results_df = pd.DataFrame(index=series.index)
    options = []

    for idx, value in series.dropna().items():
        for option in value.split(";"):
            option = option.strip()

            if option not in results_df.columns:
                results_df[option] = False
                options.append(option)

            results_df.loc[idx, option] = True

    return results_df[options]

def main():
    survery_raw_df = read_csv("Dataset//results.txt")
    raw_schema = pd.read_csv("Dataset//schema.txt" , index_col="Column").QuestionText
    survey_df , schema = get_required_info(survery_raw_df , raw_schema )
    # convert_numeric(survey_df , "Age1stCode")
    # convert_numeric(survey_df , "YearsCode")
    # convert_numeric(survey_df , "YearsCodePro")
    # drop_incorrect(survey_df , "Age" , 100 , 10 )
    # drop_incorrect(survey_df , "WorkWeekHrs" , 140 )
    # replace_multiselect(survey_df ,"Gender" )
    # gender_data = get_gender_counts(survey_df)
    # visualize_data(survey_df , "hbar" , coloumn= "EdLevel")
    # print(get_undergrad_percent(survey_df))
    # print(split_multicolumn(survey_df["DevType"]))

    #question 1
    """
    Which is the most popular programming language?

    """

    programming_frame = split_multicolumn(survey_df["LanguageWorkedWith"])
    language_percent = programming_frame.mean().sort_values(ascending=False) * 100
    visualize_data(language_percent.head(5) , "pie" )


if __name__ == "__main__":
    main()
