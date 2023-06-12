import os

for file in os.listdir("templates"):
    with open("templates/" + file, "r") as f:
        content = f.read()
    while "  " in content or "\n" in content:
        content = content.replace("  ", " ").replace("\n", "")
    with open("templates/" + file.split(".")[0] + "_min_min.html", "w") as f:
        f.write(content)


for file in os.listdir("static/css"):
    with open("static/css/" + file, "r") as f:
        content = f.read()
    while "  " in content or "\n" in content:
        content = content.replace("  ", " ").replace("\n", "")
    with open("static/css/" + file.split(".")[0] + "_min_min.css", "w") as f:
        f.write(content)
