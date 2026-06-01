# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd
from pylatex import Document, Package, Enumerate, Command
from pylatex.utils import NoEscape
from pylatex.basic import NewPage, LineBreak, NewLine
import os


def read_data(excel_file, subject_name):
    df = pd.read_excel(Path(excel_file).absolute(), sheet_name=subject_name,
                       header=[0, 1, 2],
                       index_col=0)
    df = df.astype(str)
    return df        


class TEX_writer:
    def __init__(self, subject_longname, author):
        # qp doc
        qp_document_options = ["a4paper", "12pt"]
        qp_geometry_options = {"left": "1.7cm", "right": "1.7cm",
                                "top": "1.7cm", "bottom": "1.7cm"}
        self.qp_doc = Document(documentclass='book',
                               document_options=qp_document_options,
                               fontenc='T1', # times new roman
                                geometry_options=qp_geometry_options
                               )
        # packages
        self.qp_doc.packages.append(Package('mathptmx'))
        self.qp_doc.packages.append(Package('enumitem'))
        self.qp_doc.packages.append(Package('graphicx')) # load one-page pdf
        self.qp_doc.packages.append(Package('fancyhdr')) # head and foot
        self.qp_doc.packages.append(Package('xcolor', options='svgnames'))
        self.qp_doc.append(NoEscape(r'\newcommand*{\plogo}{\fbox{$\mathcal{M}$}}'))
        self.qp_doc.packages.append(Package('PTSerif'))
        self.qp_doc.packages.append(Package('adjustbox', options='export'))
        self.qp_doc.packages.add(Package('grffile', options=['encoding', 'filenameencoding=utf8']))
        # title page
        self.qp_doc.append(NoEscape(r'\begin{titlepage}'))
        self.qp_doc.append(NoEscape(r'\raggedleft'))
        self.qp_doc.append(NoEscape(r'\vspace*{\baselineskip}'))
        self.qp_doc.append(NoEscape(r'\includegraphics[width=6cm,right]{logo}')) # logo
        # self.qp_doc.append(NoEscape(r'{\Large Cambridge International AS \& A Level Mathematics}')) # no logo
        self.qp_doc.append(NoEscape(r'\vspace*{0.167\textheight}'))
        self.qp_doc.append(NoEscape(r'\newline'))
        # self.qp_doc.append(NoEscape(r'\textbf{\LARGE The Questions by Topic for}\\[\baselineskip]'))
        # self.qp_doc.append(NoEscape(r'\textbf{\LARGE Selected Past Paper Questions by Topic for}\\[\baselineskip]')) # holiday HW
        self.qp_doc.append(NoEscape(r'\textbf{\LARGE Selected Calculus Questions for}\\[\baselineskip]')) # holiday HW P3
        self.qp_doc.append(NoEscape(r'{\textcolor{Red}{\Huge %s}}\\[\baselineskip]' % subject_longname))
        # self.qp_doc.append(NoEscape(r'{\Large \textit{An exercise book}}'))
        self.qp_doc.append(NoEscape(r'{\Large \textit{A holiday homework booklet}}')) # holiday HW
        self.qp_doc.append(NoEscape(r'\vfill'))
        self.qp_doc.append(NoEscape(r'{\large Mathematics~~\plogo}'))
        self.qp_doc.append(NoEscape(r'\vspace*{3\baselineskip}'))
        self.qp_doc.append(NoEscape(r'\end{titlepage}'))
        # contents
        self.qp_doc.append(NoEscape(r'\tableofcontents'))
        # header and footer
        self.qp_doc.append(NoEscape(r'\pagestyle{fancy}'))
        self.qp_doc.append(NoEscape(r'\fancyhead{}'))
        self.qp_doc.append(NoEscape(r'\fancyhead[RE, LO]{\leftmark}'))
        self.qp_doc.append(NoEscape(r'\fancyhead[LE, RO]{\thepage}'))
        self.qp_doc.append(NoEscape(r'\fancyfoot{}'))
        
        # ms doc
        if subject_longname == 'IGCSE Additional Mathematics 0606':
            ms_document_options = ["a4paper", "12pt"] # for 0606
        else:
            ms_document_options = ["a4paper", "landscape", "12pt"]
        ms_geometry_options = {"left": "2.1cm", "right": "2.1cm",
                               "top": "1cm", "bottom": "1.7cm",
                               "headsep": "8pt"}
        self.ms_doc = Document(documentclass='book',
                               document_options=ms_document_options,
                               fontenc='T1', # times new roman
                               geometry_options=ms_geometry_options)
        self.ms_doc.packages.append(Package('mathptmx'))
        self.ms_doc.packages.append(Package('enumitem'))
        self.ms_doc.packages.append(Package('pdfpages')) # load multi-page pdf
        self.ms_doc.packages.append(Package('etoolbox'))
        self.ms_doc.packages.append(Package('fancyhdr')) # head and foot
        # self.ms_doc.packages.append(Package('xcolor', options='svgnames'))
        self.ms_doc.append(NoEscape(r'\newcommand*{\plogo}{\fbox{$\mathcal{M}$}}'))
        self.ms_doc.packages.append(Package('PTSerif'))
        self.ms_doc.packages.append(Package('adjustbox', options='export'))
        self.ms_doc.packages.add(Package('grffile', options=['encoding', 'filenameencoding=utf8']))
        # define some commands for loading pdf
        self.ms_doc.append(NoEscape(r'\makeatletter'))
        self.ms_doc.append(NoEscape(r'\pretocmd{\includepdf}{\def\victor@dynpage{\victor@firstpage\global\let\victor@dynpage\relax}}'))
        self.ms_doc.append(NoEscape(r'\newcommand*\dynpage[1]{\def\victor@firstpage{#1}\victor@dynpage}'))
        self.ms_doc.append(NoEscape(r'\makeatother'))
        # title page
        self.ms_doc.append(NoEscape(r'\begin{titlepage}'))
        self.ms_doc.append(NoEscape(r'\raggedleft'))
        self.ms_doc.append(NoEscape(r'\vspace*{\baselineskip}'))
        self.ms_doc.append(NoEscape(r'\includegraphics[width=6cm,right]{logo}')) # logo
        # self.ms_doc.append(NoEscape(r'\Large Cambridge International AS \& A Level Mathematics')) # no logo
        self.ms_doc.append(NoEscape(r'\vspace*{0.167\textheight}'))
        self.ms_doc.append(NoEscape(r'\newline'))
        # self.ms_doc.append(NoEscape(r'\textbf{\LARGE The Questions by Topic for}\\[\baselineskip]'))
        # self.ms_doc.append(NoEscape(r'\textbf{\LARGE Selected Past Paper Questions by Topic for}\\[\baselineskip]')) # holiday HW
        self.ms_doc.append(NoEscape(r'\textbf{\LARGE Selected Calculus Questions for}\\[\baselineskip]')) # holiday HW P3
        # self.ms_doc.append(NoEscape(r'{\textcolor{Red}{\Huge %s}}\\[\baselineskip]' % subject_longname))
        self.ms_doc.append(NoEscape(r'{\Huge %s}\\[\baselineskip]' % subject_longname))
        self.ms_doc.append(NoEscape(r'{\Large \textit{Mark schemes}}'))
        self.ms_doc.append(NoEscape(r'\vfill'))
        self.ms_doc.append(NoEscape(r'{\large Mathematics~~\plogo}'))
        self.ms_doc.append(NoEscape(r'\vspace*{3\baselineskip}'))
        self.ms_doc.append(NoEscape(r'\end{titlepage}'))        
        # contents
        self.ms_doc.append(NoEscape(r'\tableofcontents'))
        # header and footer
        self.ms_doc.append(NoEscape(r'\pagestyle{fancy}'))
        self.ms_doc.append(NoEscape(r'\fancyhead{}'))
        self.ms_doc.append(NoEscape(r'\fancyhead[RE, LO]{\leftmark}'))
        self.ms_doc.append(NoEscape(r'\fancyhead[LE, RO]{\thepage}'))
        self.ms_doc.append(NoEscape(r'\fancyfoot{}'))
        
    def create_chapter(self, chapter_title):
        self.qp_doc.append(NoEscape(r'\chapter{%s}' % chapter_title))
        self.ms_doc.append(NoEscape(r'\chapter{%s}' % chapter_title))
        
    def create_enum(self):
        qp_enumerate_options = ["leftmargin=0.8cm", "rightmargin=0cm",
                                "itemindent=0cm", "listparindent=0cm",
                                "labelsep=0.1cm", "labelwidth=0.7cm",
                                "align=left",
                                "parsep=1em",
                                NoEscape(r"label=\textbf{\arabic*}")]
        ms_enumerate_options = ["leftmargin=0cm", "rightmargin=0cm",
                                "itemindent=0cm", "listparindent=0cm",
                                "labelsep=0.1cm", "labelwidth=0.7cm",
                                "align=left",
                                "parsep=1em",
                                NoEscape(r"label=\textbf{\arabic*}")]
        with self.qp_doc.create(Enumerate(options=qp_enumerate_options)) as qp_enum:
            with self.ms_doc.create(Enumerate(options=ms_enumerate_options)) as ms_enum:
                return qp_enum, ms_enum
        
    def add_one_question(self, enum, question_source, qp_path):
        enum.append(NewPage())
        enum.add_item(NoEscape(question_source)) # use question source
        # enum.add_item(NoEscape(r'Question:')) # do not use question source
        enum.append(LineBreak())
        enum.append(NewLine())
        enum.append(Command('includegraphics',
                            options=NoEscape(r'width=\linewidth'),
                            arguments=NoEscape(qp_path)))
        qp_continue_path = r'%s_continue' % (qp_path)
        if os.path.isfile(qp_continue_path + '.pdf'):
            enum.append(NewPage())
            # enum.append(LineBreak()) # Linebreak和Newline都不能加，否则会编码错误
            # enum.append(NewLine())
            enum.append(Command('includegraphics',
                                options=NoEscape(r'width=\linewidth'),
                                arguments=NoEscape(qp_continue_path)))
        
    def add_one_answer(self, enum, question_source, ms_path):
        ms_options = [NoEscape(r'pages=-'),
                      NoEscape(r'pagecommand=\dynpage{\item %s}' % question_source)]
        enum.append(Command('includepdf',
                            options=ms_options,
                            arguments=NoEscape(ms_path)))
        
    def save_tex(self, filepath):
        self.qp_doc.generate_tex(filepath=filepath)
        self.ms_doc.generate_tex(filepath=filepath+' ms')
        
    def save_pdf(self, filepath):
        self.qp_doc.generate_pdf(filepath=filepath, clean_tex=True)
        self.ms_doc.generate_pdf(filepath=filepath+' ms', clean_tex=True)


def get_information_for_tex(subject_name, year, season, paper_number, question_number):
    # get subject code
    if subject_name in ['P1', 'P3', 'M1', 'S1']:
        subject_code = '9709'
    elif subject_name in ['FP1', 'FP2']:
        subject_code = '9231'
        if year <= 2019: subject_name = 'FP'
    elif subject_name in ['FM', 'FS']:
        if year <= 2019: subject_name = 'FX'
        if str(paper_number)[0] == '5': # M2
            subject_code = '9709'
            subject_name = 'M2'
        else:
            subject_code = '9231'
    elif subject_name in ['IG0606']:
        subject_code = '0606'
    else:
        subject_code = 'xxxx'
    
    # [9231/s21/31/q1.b]
    question_source = r'{[%s/%s%s/%s/q%s]}' % \
        (subject_code, season, str(year)[-2:], paper_number, question_number)
    # 9231_s21_qp_31_q1
    qp_file = r'%s_%s%s_qp_%s_q%s' % \
        (subject_code, season, str(year)[-2:], paper_number, question_number.split('.')[0])
    # 9231_s21_ms_31_q1
    ms_file = r'%s_%s%s_ms_%s_q%s' % \
        (subject_code, season, str(year)[-2:], paper_number, question_number.split('.')[0])
    # FM/2021/s/9231_s21_qp_31_q1
    qp_path = r'%s/%s/%s/%s' % (subject_name, year, season, qp_file)
    # FM/2021/s/9231_s21_ms_31_q1
    ms_path = r'%s/%s/%s/%s' % (subject_name, year, season, ms_file)
    return question_source, qp_path, ms_path


if __name__ == "__main__":
    """
    pastpaper information:
        subject_code: 9231, 9709, 0606
        subject_name: FP1, FP2, FM, FS, P1, P3, M1, S1, M2, IG0606
        year: 2022(22), 2021(21), 2020(20), ...
        season: m, s, w
        paper_number: 31, 32, 33, ...
        question_number: 1, 2, ...
        
        resource_type: qp, ms
    """
    ##########################################################################
    # what do you want?
    subject_name = r'P3'
    start_year = 2021
    end_year = 2015
    # subset = False
    subset = True
    ##########################################################################
    
    # get more
    if subset:
        excel_file = r'Questions by topic subset.xlsx'
    else:
        excel_file = r'Questions by topic.xlsx'
    
    subject_longname = {'P1': 'Pure Mathematics 1',
                        'P3': 'Pure Mathematics 3',
                        'M1': 'Mechanics',
                        'S1': 'Probability and Statistics 1',
                        'FP1': 'Further Pure Mathematics 1',
                        'FP2': 'Further Pure Mathematics 2',
                        'FM': 'Further Mechanics',
                        'FS': 'Further Probability and Statistics',
                        'IG0606': 'IGCSE Additional Mathematics 0606'}
    
    author = r'Mathematics Department'
    
    # read data from excel
    df = read_data(excel_file, subject_name)
    # create tex doc. get qp_doc and ms_doc
    tex = TEX_writer(subject_longname[subject_name], author)
    
    # read one question's information from data:
    # chapter, year, season, paper_number, question_number
    for chapter in df.index:
        print('Chapter:', chapter)
        tex.create_chapter(chapter)
        qp_enum, ms_enum = tex.create_enum()
        for column in df.loc[[chapter]].columns:
            (year, season, paper_number) = column # 2021, s, 31
            if year > start_year:
                continue
            if year < end_year:
                continue
            question_numbers = df.loc[chapter][column] # 1, 3.b, 7.2, 11a
            if question_numbers == 'nan':
                continue
            question_numbers = [x.strip() for x in question_numbers.split(',')] # list
            for question_number in question_numbers:
                if question_number.split('.')[-1] == '0': # 5.0
                    question_number = question_number.split('.')[0]
                # transfer it to tex information: question_source, qp_path, ms_path
                question_source, qp_path, ms_path = get_information_for_tex(
                    subject_name, year, season, paper_number, question_number)
                # add one question and one answer
                tex.add_one_question(qp_enum, question_source, qp_path)
                tex.add_one_answer(ms_enum, question_source, ms_path)
    
    # save tex or pdf
    # if subset: subject_name += ' subset'
    
    # tex.save_tex(subject_name)
    # print('Save tex successfully.')
    tex.save_pdf(subject_name)
    print('Save pdf successfully.')

