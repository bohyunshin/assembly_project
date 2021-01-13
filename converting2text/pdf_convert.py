import pdf2text

file = open("/Users/shinbo/contest_repository/assembly/data/2024990/2024990_행정안전위원회_위원회의결안.pdf", 'rb')
fileReader = pdf2text.PDF(file)

