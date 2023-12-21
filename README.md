# Space Searcher (Rough Draft)
This **Space Searcher** code is from my Fall 2023 NASA internship: Expanding Diversity in the NASA Astrophysics Panel and is an extension 
of [Mallory's code](https://github.com/MalloryHelfenbein/NASA_Internship/blob/main/README.md) 

## What it does

The Space Searcher searches a csv file and can filter what ouput is displayed based on how much information the user provides. All text entry boxes do not need to be filled out 
in order to receive results. In each user input box, there is a placeholder that provides the user with the correct formatting. When the years are searched, extra "cushion" room 
is given just in case that article was not published in that exact year but instead, within that time frame. The user can then save this filtered csv file directly to their computer.

The code will allow the user to search for the following criteria:
- Author
- Institution
- Bibcode
- Start year
- End year

## What is required

### API
A personal API token will be needed. In the 5th cell, it states where to insert this. A user can obtain a token through 
[Mallory's github link](https://github.com/MalloryHelfenbein/NASA_Internship/blob/main/README.md)

### Imports (I need to update these)
- requests
- urllib.parse
  - urlencode
  - quote_plus
- numpy
- sys
- nltk
- csv
- pandas (1.5.3 or later)
- tkinter 
- tkinter.messagebox
- For the custom tkinter version:
  - 

### Files needed (need updates):
- textAnalysis file
- ADSsearcher file

Place these files within the same directory, as the path will be necessary in order for the code to function correctly.

## How to use it

When the Space Searcher initially opens up, directions are given to the user to be as detailed as possible witht their user input.
The more information provided, the more refined the search is. There are four user input boxes (author, institution, start year, and end year).
Placeholders are provided in the user input boxes so the user can have the correct formatting. If the user were to delete the data they have in
that user input textbox, the placeholder retuens and it does not affect the outcome of the search. Once the necessary information is provided, 
the user can press `search`, leading to a dataframe being displayed within the window. Depending on if there are a lot of results, the user can
use the scrollbar omn the left to search througout the dataframe. In the end, the user can press the `Save CSV` button, and this will cause a 
popup window to show, asking the user what they want to name the file and the specific destinantion they have for the file to be saved.
