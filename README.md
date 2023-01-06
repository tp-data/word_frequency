# Word Frequency Report
>This repository contains a python script to output a PDF report around frequency of words in a text exerpt. This will take a user's text file and return a report on the most common words, including a summary and visualizations for a handful of the most common words.

## Usage
1. Clone the repository to your local machine.
2. Update the text present in the _text.txt_ file so that the output is a more personalized report. See the sample text exerpt provided:
    When Prince Peter became the ruler of Russia in the 1600s, he realized that his country had fallen behind others. Countries to the west had increased their knowledge and technology. They had advanced, but Russia had not. Peter decided that he had to push his nation forward. To do this, he knew that he would have to change himself first. So Peter took a trip through Europe. People there thought he was very strange. Even though he was a monarch, he did not behave like one. Instead of going to parties, Peter spent his time learning. For example, he enjoyed spending time at the docks learning how to build ships.
3. Open terminal and move to the directory with the repository (using _cd path/to/repository_).
4. Run the python file _word_frequency.py_.
    python word_frequency.py
5. Check the directory for the PDF output.

## Dependencies
* pandas
* numpy
* matplotlib
* reportlab
