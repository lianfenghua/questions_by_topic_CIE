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
    def __init__(self, subject_longname, chapter_name, show_question_source):
        # qp doc
        qp_document_options = ["a4paper", "12pt"]
        # qp_geometry_options = {"left": "1.7cm", "right": "1.7cm",
        #                        "top": "1.7cm", "bottom": "1.7cm"}
        qp_geometry_options = {"left": "1.7cm", "right": "1.7cm",
                                "top": "1.5cm", "bottom": "1.7cm"}
        self.qp_doc = Document(documentclass='article',
                               document_options=qp_document_options,
                               fontenc='T1', # times new roman
                                geometry_options=qp_geometry_options
                               )
        # packages
        self.qp_doc.packages.append(Package('mathptmx'))
        self.qp_doc.packages.append(Package('enumitem'))
        self.qp_doc.packages.append(Package('graphicx')) # load one-page pdf (9709, 9231, 0580 paper2)
        self.qp_doc.packages.append(Package('pdfpages')) # load multi-page pdf (0606, 0580 paper4)
        self.qp_doc.packages.append(Package('etoolbox'))
        # define some commands for loading pdf
        self.qp_doc.append(NoEscape(r'\makeatletter'))
        self.qp_doc.append(NoEscape(r'\pretocmd{\includepdf}{\def\victor@dynpage{\victor@firstpage\global\let\victor@dynpage\relax}}'))
        self.qp_doc.append(NoEscape(r'\newcommand*\dynpage[1]{\def\victor@firstpage{#1}\victor@dynpage}'))
        self.qp_doc.append(NoEscape(r'\makeatother'))
        
        # ms doc
        if subject_longname in ['IGCSE Additional Mathematics 0606', 'IGCSE Mathematics 0580']:
            ms_document_options = ["a4paper", "12pt"] # for 0606 and 0580
        else:
            ms_document_options = ["a4paper", "landscape", "12pt"]
        ms_geometry_options = {"left": "2.1cm", "right": "2.1cm",
                               "top": "0.8cm", "bottom": "1.2cm"}
        self.ms_doc = Document(documentclass='article',
                               document_options=ms_document_options,
                               fontenc='T1', # times new roman
                               geometry_options=ms_geometry_options)
        self.ms_doc.packages.append(Package('mathptmx'))
        self.ms_doc.packages.append(Package('enumitem'))
        self.ms_doc.packages.append(Package('graphicx')) # load one-page pdf (0580)
        self.ms_doc.packages.append(Package('pdfpages')) # load multi-page pdf (9709, 9231, 0606)
        self.ms_doc.packages.append(Package('etoolbox'))
        # define some commands for loading pdf
        self.ms_doc.append(NoEscape(r'\makeatletter'))
        self.ms_doc.append(NoEscape(r'\pretocmd{\includepdf}{\def\victor@dynpage{\victor@firstpage\global\let\victor@dynpage\relax}}'))
        self.ms_doc.append(NoEscape(r'\newcommand*\dynpage[1]{\def\victor@firstpage{#1}\victor@dynpage}'))
        self.ms_doc.append(NoEscape(r'\makeatother'))

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
        
    def add_one_question(self, enum, question_source, qp_path, show_question_source):
        enum.append(NewPage())
        # if not (question_source[2:6] == '0580' and question_source[11] == '2'):
        #     enum.append(NewPage())
        if show_question_source:
            enum.add_item(NoEscape(question_source))
        else:
            enum.add_item(NoEscape(r'\textcolor{lightgray}{%s}' % question_source))
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

    def add_one_question_wholepages(self, enum, question_source, qp_path, show_question_source):
        if show_question_source:
            qp_options = [NoEscape(r'pages=-'),
                          NoEscape(r'pagecommand=\dynpage{\item %s}' % question_source)]
        else:
            qp_options = [NoEscape(r'pages=-'),
                          NoEscape(r'pagecommand=\dynpage{\item \textcolor{lightgray}{%s}}' % question_source)]
        enum.append(Command('includepdf',
                            options=qp_options,
                            arguments=NoEscape(qp_path)))

    def add_one_answer(self, enum, question_source, ms_path, show_question_source):
        if not (question_source[2:6] == '0580'):
            enum.append(NewPage())
        if show_question_source:
            enum.add_item(NoEscape(question_source))
        else:
            enum.add_item(NoEscape(r'\textcolor{lightgray}{%s}' % question_source))
        enum.append(LineBreak())
        # enum.append(NewLine())
        enum.append(Command('includegraphics',
                            options=NoEscape(r'width=\linewidth'),
                            arguments=NoEscape(ms_path)))
        ms_continue_path = r'%s_continue' % (ms_path)
        if os.path.isfile(ms_continue_path + '.pdf'):
            enum.append(NewPage())
            # enum.append(LineBreak()) # Linebreak和Newline都不能加，否则会编码错误
            # enum.append(NewLine())
            enum.append(Command('includegraphics',
                                options=NoEscape(r'width=\linewidth'),
                                arguments=NoEscape(ms_continue_path)))

    def add_one_answer_wholepages(self, enum, question_source, ms_path, show_question_source):
        if show_question_source:
            ms_options = [NoEscape(r'pages=-'),
                          NoEscape(r'pagecommand=\dynpage{\item %s}' % question_source)]
        else:
            # ms_options = [NoEscape(r'pages=-'),
            #               NoEscape(r'pagecommand=\dynpage{\item \hspace{0pt}}')]
            ms_options = [NoEscape(r'pages=-'),
                          NoEscape(r'pagecommand=\dynpage{\item \textcolor{lightgray}{%s}}' % question_source)]
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
    elif subject_name in ['IG0580']:
        subject_code = '0580'
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
        subject_code: 9231, 9709, 0606, 0580
        subject_name: FP1, FP2, FM, FS, P1, P3, M1, S1, M2, IG0606, IG0580
        year: 2022(22), 2021(21), 2020(20), ...
        season: m, s, w
        paper_number: 31, 32, 33, ...
        question_number: 1, 2, ...
        
        resource_type: qp, ms
    """
    ##########################################################################
    # what do you want?
    subject_name = r'P1'
    start_year = 2025
    end_year = 2015
    subset = True
    # subset = False
    # show_question_source = True
    show_question_source = False
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
                        'IG0606': 'IGCSE Additional Mathematics 0606',
                        'IG0580': 'IGCSE Mathematics 0580'}
    
    # read data from excel
    df = read_data(excel_file, subject_name)
    
    # read one question's information from data:
    # chapter, year, season, paper_number, question_number
    for chapter in df.index:
        print('Chapter:', chapter)
        # create tex doc. get qp_doc and ms_doc
        tex = TEX_writer(subject_longname[subject_name], chapter, show_question_source)
        
        qp_enum, ms_enum = tex.create_enum()
        number_of_questions = 0
        for column in df.loc[[chapter]].columns:
            (year, season, paper_number) = column # 2021, s, 31
            if year > start_year:
                continue
            if year < end_year:
                continue
            question_numbers = df.loc[chapter][column] # 1, 3.b, 7.2, 11a
            if question_numbers == 'nan':
                # print('There are no question(s) on this paper:', column)
                continue
            question_numbers = [x.strip() for x in question_numbers.split(',')] # list
            for question_number in question_numbers:
                if question_number.split('.')[-1] == '0': # 5.0
                    question_number = question_number.split('.')[0]
                # transfer it to tex information: question_source, qp_path, ms_path
                question_source, qp_path, ms_path = get_information_for_tex(
                    subject_name, year, season, paper_number, question_number)
                # add one question and one answer
                if (subject_name in ['IG0606']) or (subject_name in ['IG0580'] and str(paper_number)[0] == '4'):
                    tex.add_one_question_wholepages(qp_enum, question_source, qp_path, show_question_source)
                else:
                    tex.add_one_question(qp_enum, question_source, qp_path, show_question_source)
                if subject_name in ['IG0580']:
                    tex.add_one_answer(ms_enum, question_source, ms_path, show_question_source)
                else:
                    tex.add_one_answer_wholepages(ms_enum, question_source, ms_path, show_question_source)
                number_of_questions += 1
    
        # save tex or pdf
        if number_of_questions == 0:
            print('There are no question(s) for this Chapter:', chapter)
            continue
        # tex.save_tex(chapter)
        # print('Save tex successfully.')
        tex.save_pdf(chapter)
        print('Save pdf successfully.')

