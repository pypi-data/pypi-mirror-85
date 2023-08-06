# -*- coding: utf-8 -*-
'''
Created on 2020-11-11

@author: zhys513(254851907@qq.com)
''' 
# pip3 install camelot-py[cv]
# pip3 install xlsxwriter
import camelot
import pandas as pd

def extract_pdf_table(input_file, output_file):
    """
    只支持text-based 的pdf table
    :param input_file: 输入pdf文件
    :param output_file: 保存每个table，输出到excel文件
    :return:
    """
    #提取pdf的table
    tables = camelot.read_pdf(input_file,flavor='stream')
    table_number = tables.n
    print(f"pdf文件 {input_file} 共包含text-based类型表格 {table_number} 个")

    #准备保存每个table
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    for num in range(table_number):
        table = tables[num]
        # 打印每个table
        print(table.df)
        # 保存到sheet
        table.df.to_excel(writer, sheet_name='page{}_num{}'.format(table.page, num), encoding="utf-8")
    #保存excel
    writer.save()

if __name__ == '__main__':
    filename = '开工报告1'
    file = f"test/{filename}.pdf"
    outfile = f"out/{filename}.xlsx"
    extract_pdf_table(input_file=file, output_file=outfile)