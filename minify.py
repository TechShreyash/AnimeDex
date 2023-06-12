import os

for file in os.listdir("templates"):
    if 'min' in file:
        os.remove("templates/" + file)
        continue

    with open("templates/" + file, "r") as f:
        content = f.read()
    while "  " in content or "\n" in content:
        content = content.replace("  ", " ").replace("\n", "")
    with open("templates/" + file.split(".")[0] + "_min.html", "w") as f:
        f.write(content)


for file in os.listdir("static/css"):
    if 'min' in file:
        os.remove("static/css/" + file)
        continue
    
    with open("static/css/" + file, "r") as f:
        content = f.read()
    while "  " in content or "\n" in content:
        content = content.replace("  ", " ").replace("\n", "")
    with open("static/css/" + file.split(".")[0] + "_min.css", "w") as f:
        f.write(content)
