# define imports
import io

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import sys

txt = sys.argv[1]
min_char = int(sys.argv[2])

# open text file contraining string to analyze
text = open(txt).read()
# remove special characters and convert to lower case
text = re.sub(r"[^a-zA-Z0-9 ]", "", text).lower()
text_split = text.split()
wordfreq = [text_split.count(w) for w in text_split] # count instances of each word

# convert list into dataframe (take mean to remove duplicates for the final dataset)
list_freq = pd.DataFrame(list(zip(text_split, wordfreq)))
list_freq.columns =['word', 'frequency']
list_freq = list_freq[list_freq['word'].str.len() >= min_char]
list_freq = list_freq.groupby('word').mean()

# prepare datasets for both the top 5 and 15 groups
list_freq_top20 = list_freq.sort_values(by='frequency', ascending = False).head(15).reset_index()
list_freq_top5 = list_freq.sort_values(by='frequency', ascending = False).head(5).reset_index()
# covert top 5 into string to be used in call out for first text sentence in PDF
list_top5 = list(list_freq_top5['word'])
str_top5 = ', '.join(str(e) for e in list_top5)


# set up function for the styling of all text items
def add_text(text, style="Normal", fontsize=10):
    pdf_report.append(Spacer(1,12))
    ptext = "<font size={}>{}</font>".format(fontsize, text)
    pdf_report.append(Paragraph(ptext, styles[style]))
    
# utilize basic styles and define PDF attributes
styles=getSampleStyleSheet()
doc = SimpleDocTemplate("word_frequency.pdf",pagesize=letter,
                        rightMargin=inch/2,leftMargin=inch/2,
                        topMargin=38,bottomMargin=18)


# begin defining the PDF components
pdf_report=[]


# add title header
add_text("Word Frequency Report", style="Heading1", fontsize=18)
# add intro sentence with top 5 words
add_text('The 5 most common words to appear in the text were -- ' + str_top5)


# add title and plot for bar chart section
add_text("See below for the top 15 most common words, and the individual count per each.")
plt.figure(figsize=(10, 6.8))
plt.bar(list_freq_top20['word'], list_freq_top20['frequency'])
# plt.tight_layout()
plt.xlabel('Words')
plt.ylabel('Count of Occurences')
plt.xticks(rotation=45)
# create and save image to bar chart buffer
bar = io.BytesIO()
plt.savefig(bar, format='png', dpi=300)
bar.seek(0)
plt.close() # you'll want to close the figure once its saved to buffer
bar_img = Image(bar, 7*inch, 3.5*inch)
pdf_report.append(bar_img)


# add title and plot for pie chart section
add_text("See below for the % distribution per top 15 words.")
plt.figure(figsize=(9, 8))
        # explode = (.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)  # --> this needs to be implemented with a constraint on how many items are present in x axis
plt.pie(list_freq_top20['frequency'], labels=list_freq_top20['word'], autopct='%1.1f%%')
plt.tight_layout()
plt.legend(list_freq_top20['word'], loc="right")
# create and save image to pie chart buffer
pie = io.BytesIO()
plt.savefig(pie, format='png', dpi=300)
pie.seek(0)
plt.close()
pie_img = Image(pie, 6*inch, 5*inch)
pdf_report.append(pie_img)

# this will enable the build of the PDF
doc.build(pdf_report)

# close both buffers
bar.close()
pie.close()
