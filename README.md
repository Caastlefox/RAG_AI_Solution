# How to run
To run this project ensure all project files are in the same directory that is:
<ol>
<li>main.py</li>
<li>functions.py</li>
</ol>

Create .env file with following parameters
<ol>
<li>OPEN_AI_API_KEY - your open ai api key</li>
<li>FILENAME - file you want to parse to vector database</li>  
</ol>

Ensure that the following python packages are installed in your environment
<ol>
<li>python-dotenv</li>
<li>openai</li>
<li>chromadb</li>
<li>striprtf</li>
</ol>

After these steps you can run project by executing script main.py.
Project was tested with Python 3.13 (64-bit)