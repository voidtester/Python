filename = "text.txt"
start_text = "-----BEGIN CERTIFICATE-----"
end_text = "-----END CERTIFICATE-----"

# read in the file
with open(filename, "r") as file:
    content = file.read()

# find the start and end indices of the paragraph
start_index = content.find(start_text)
end_index = content.find(end_text) + len(end_text)

# extract the paragraph and print it
paragraph = content[start_index:end_index]
print(paragraph)