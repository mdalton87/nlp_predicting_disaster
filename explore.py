import re
import unicodedata
import pandas as pd
import nltk
import prepare as prep
import matplotlib.pyplot as plt
import seaborn as sns




def counts_and_ratios(df, column):
    '''
    Description:
    -----------
    This function takes in a columns name and creates a dataframe with value counts and
    percentages of the all categories within the column.
    
    Parameters:
    ----------
    df: Dataframe
        Dataframe being explored
    column: str
        Columns should be a categorical or binary column.
    '''
    labels = pd.concat([df[column].value_counts(),
                   df[column].value_counts(normalize=True)], axis=1)
    labels.columns = ['n', 'pct']
    
    return labels




def create_wordcloud(string):
    # generates an img
    img = WordCloud(background_color='white').generate(ham_string)
    # WordCloud() produces an image object, which can be displayed with plt.imshow
    plt.imshow(img)
    # axis aren't very useful for a word cloud
    plt.axis('off')




def compare_word_counts(df, text_col, cat_col, group1, group2, n=6):
    '''
    
    '''
    
    df['lem_text'] = [prep.clean_lem_stop(string) for string in df[text_col]]
    
    
    group1_df = df[df[cat_col] == group1]
    group2_df = df[df[cat_col] == group2]
    
    group1_string = ' '.join(group1_df.lem_text)
    group2_string = ' '.join(group2_df.lem_text)
    all_string = group1_string + group2_string
    
    
    group1_freq = pd.Series(group1_string.split()).value_counts()
    group2_freq = pd.Series(group2_string.split()).value_counts()
    all_freq = pd.Series(all_string.split()).value_counts()
    
    
    word_counts = (pd.concat([all_freq, group1_freq, group2_freq], axis=1, sort=True)
                .set_axis(['all', group1, group2], axis=1, inplace=False)
                .fillna(0))
#                 .apply(lambda s: s.astype(int)

    # find words unique to each group
    unique_words = pd.concat([word_counts[word_counts[group1] == 0].sort_values(by=group1).tail(n),
           word_counts[word_counts[group2] == 0].sort_values(by=group2).tail(n)])
    
                       
    return word_counts, unique_words



def proportion_graph(word_counts, group1, group2, n=20):
    
    var1 = str('p_' + group1)
    var2 = str('p_' + group2)
    (word_counts
         .assign(var1 = word_counts[group1] / word_counts['all'],
                 var2 = word_counts[group2] / word_counts['all'])
         .sort_values(by='all')
         [[var1 , var2]]
         .tail(n)
         .sort_values(var2)
         .plot.barh(stacked=True))

    plt.title(f'Proportion of {group1} vs {group2} for the {n} most common words')