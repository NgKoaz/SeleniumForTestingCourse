import openpyxl

# path = "C:\\Users\\HP\\OneDrive\\Desktop\\test.xlsx"
# workbook = openpyxl.load_workbook(path)
# sheet = workbook.active
# sheet.title = "Changed"
#
# sheet["A5"] = "KHOA"
#
# workbook.save(path)

workbook = openpyxl.load_workbook("data\\quiz.xlsx")
sheet = workbook["Data"]
print(sheet.)



