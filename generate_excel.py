import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "Posts"

# Header row
sheet.append(["title", "content", "author_id"])

# Dummy 20 posts
for i in range(1, 21):
    sheet.append([f"Post Title {i}", f"This is the content of post {i}.", 1])

wb.save("posts_data.xlsx")  # Excel file create hogi project root me
print(" Excel file created!")
