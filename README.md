# About the project

There are lots of questions from past papers we can find on websites. However, it is inconvenient to look for all the questions related to some topic we want. This project is created to solve this problem.

### Structure

The project has been uploaded in `UK 24-25 Mathematics Cohort/Files/questions_by_topic_CIE`.

All the directories are listed below.

| Directories | Papers contained              | PDF Files contained  |
| ----------- | ----------------------------- | -------------------- |
| P1          | P1 from 2022 to 2015          | P1 chapter files     |
| P3          | P3 from 2022 to 2015          | P3 chapter files     |
| M1          | M1 from 2022 to 2015          | M1 chapter files     |
| S1          | S1 from 2022 to 2015          | S1 chapter files     |
| FP1         | FP1 from 2022 to 2020         | FP1 chapter files    |
| FP2         | FP2 from 2022 to 2020         | FP2 chapter files    |
| FP          | FP1 and FP2 from 2019 to 2015 |                      |
| FM          | FM from 2022 to 2020          | FM chapter files     |
| M2          | FM from 2019 to 2015          |                      |
| FS          | FS from 2022 to 2020          | FS chapter files     |
| FX          | FM and FS from 2019 to 2015   |                      |
| IG0606      | IG0606 from 2024 to 2019      | IG0606 chapter files |
| books       |                               | All the book files   |

In addition, there are five files in this project.

- `Questions by topic.xlsx` 

  All the information about how the questions are sorted is recorded in this file.

- `Questions by topic subset.xlsx` 

  Just as the file name shows, if you think there are too many questions for each topic, then you can freely select the *important questions you think* in this file.

- `questions_by_topic_book.py` 

  The function of this python file is to generate the PDF file containing all the questions sorted by topics. You can change the parameter to generate which paper you want.

- `questions_by_topic_chapters.py` 

  The function of this python file is to generate some PDF files, each of which contains all the questions for just one chapter. You can change the parameter to generate which paper you want.

- `README.pdf` 

  This is the file you are reading.

### Environment prerequisites

In order to generate correct files, latex and python software are needed.

- Click [here](https://www.tug.org/texlive/) to download **TeX Live**, the best LaTeX software.
- Click [here](https://www.anaconda.com/download/success) to download **Anaconda**, a popular distribution of the Python language.

# Usage

### Record question information

The information is recorded in `Questions by topic.xlsx` or `Questions by topic subset.xlsx`, where

- several questions related to the same topic should be divided by a comma, such as `1, 3, 6`.
- if a particular part of one question is recorded, a dot should be used, such as `3.b, 7.2`.
- for FP and FX papers from 2019 to 2015, the last question contains two sub questions, so `a` and `b` are used to represent the first or the second question, such as `11a, 11b`.

### Generate PDF files

##### Step 1: Set parameters

Set parameters in python file `questions_by_topic_book.py` or `questions_by_topic_chapters.py`.

Find these four lines in the python file:

```python
# what do you want?
subject_name = r'S1'
start_year = 2021
end_year = 2015
subset = False
```

There are four parameters.

- `subject_name` 
  - `P1`: Pure Mathematics 1
  - `P3`: Pure Mathematics 3
  - `M1`: Mechanics
  - `S1`: Probability and Statistics 1
  - `FP1`: Further Pure Mathematics 1
  - `FP2`: Further Pure Mathematics 2
  - `FM`: Further Mechanics
  - `FS`: Further Probability and Statistics
  - `IG0606`: IGCSE Additional Mathematics 0606
- `start_year` 
  - The past papers are from `start_year` to `end_year`.
  - Now, `start_year` is recommended to be 2021, in order to using past papers from 2024 to 2022 as mock tests.
- `end_year` 
  - The past papers are from `start_year` to `end_year`.
  - Now, `end_year` should be not smaller than 2015.
- `subset` 
  - `True` means using information in `Questions by topic.xlsx`.
  - `False` means using information in `Questions by topic subset.xlsx`.

##### Step 2: Run python file

Run python file in python IDE.

In another way, run python file in terminal by typing

```shell
python questions_by_topic_book.py
```

or

```shell
python questions_by_topic_chapters.py
```

