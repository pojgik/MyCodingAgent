Simple CLI coding assistant that uses Google's Gemini API to accept a coding task (user input) and a file or directory as input, at which point the LLM will choose from a list of the following tasks:
1. Scan the files in a directory
2. Read a file's contents.
3. Overwrite a file's contents.
4. Execute the python interpreter on a file.<br>
It then attempts to perform the task, repeatedly choosing from the above until it either completes the task or can no longer proceed.
