
# Build an Interactive PDF Reader using LangChain and Streamlit



# Task 0: Introduction
In this project, you’ll create an interactive PDF reader using LangChain and Streamlit. When a file is uploaded, the PDF reader will extract chunks of text from it and generate embeddings for each chunk. It will then create a searchable database.

Users can interact with the PDF reader with a chatbot. When a question is presented to the chatbot, the reader generates an embedding for the question and searches the database for answers. The most relevant chunk and the chat history are then used as context to generate an answer in natural language using a large language model (LLM). This response is shown to the user and appended to the chat history.

Navigate through the code files provided to you. You’ll be making changes to the /usercode/app.py file.

Note: Every task in the project has an associated comment in the app.py file to indicate where the code should be written for that task.

To view the website properly, click the button in the URL bar of the on-platform browser to open the web page in a new browser tab.

Note: You can terminate the application at any time using the “Control + C” keys.

Use the following command in a new terminal to re-execute the web application:

## streamlit run app.py

# Task 1: Import the Libraries
In this task, you’ll import the libraries and modules that will be used to build the application. To complete this task, import the following libraries:

streamlit: This library will be used to create the frontend of the application.
load_dotenv: This library will be used to import the API keys from the .env file.
HuggingFaceEmbeddings and OpenAIEmbeddings: These methods are from the langchain.embeddings module and will be used to create embeddings for the text.
ChatOpenAI: This method is from the langchain.chat_models module and will be used to initialize the LLM chat model.
ConversationalRetrievalChain: This is a method from the langchain.chains module and will be used to create prompt chains.
Chroma: This is a method from the langchain.vectorstores module and creates the database that you’ll be using to store your PDF embeddings.
PyPDFLoader: This is a method in the langchain.document_loaders module and will be used to load the PDF.
PdfReader and PdfWriter: These are methods in the PyPDF2 library and will be used to extract sections of the PDF files.
NamedTemporaryFile: This is a method in the tempfile library and will be used to create a temporary PDF file.
base64: This method is used for encoding binary files as text for displaying them on web pages.


# Task 2: Set Up the API Keys
You’ll use the HuggingFace models to generate word embeddings of the text in the PDFs. These search results will then be used to generate responses to the questions asked using the GPT-3 LLM by OpenAI.

In this task, you’ll provide the following API keys in the /usercode/.env file:

HuggingFace: Use this Answer to get the access token for HuggingFace.
OpenAI: Use this Answer to get an API key for GPT-3.




# Task 3: Create the Web Page Layout
In this task, you’ll create the basic layout for your web application. The web page will render the UI for the PDF reader you will build. It will enable users to upload a PDF file. It will also have a text box in which the users will write their questions, a chat box that will display the chat, and an iframe that will display the relevant pages of the PDF file.


The final web application

The final web application
In this task, perform the following operations in the /usercode/app.py file:
Load the API keys using the load_dotenv() method.
Configure the page layout, choose the page title, and the page icon.
Initialize the following variables in the st.session_state if they are not present:
The conversation chain that will use prompt engineering for querying the LLM.
The history of the conversation that comprises questions and answers in the current session.
The page number of the PDF page that is referenced when answering a question.
You’ll have two columns on your web page. The second column will display the PDF file, and the first will contain all the other components of the page. Create these two columns on the page.
Set the page title in the first column.
Provide a text box in the first column and save the input question to a variable.
Create a scrollable area for displaying your chat in the first column. Apply the CSS to set up the chat box.


# Task 4: Define a Function to Process the Input File
You will now create a process_file() function that will take a PDF document as input, process it using a provided model for creating embeddings, and return an initialized conversational retrieval chain object. This initialized chain object will query the document in later tasks.

To complete this task, perform the following operations in the /usercode/app.py file:

Create the embeddings object using the HuggingFaceEmbeddings() method from the langchain.embeddings module. This method requires the following inputs:
model_name: This is the name of the model from HuggingFace that you want to use for creating embeddings.
model_kwargs: This is a dictionary containing the device key-value pair, specifying the device on which the model will create the embeddings.
encode_kwargs: This is a dictionary containing the normalize_embeddings key-value pair, indicating whether the embeddings should be normalized (a boolean value).
Create a vector store for the PDF document using Chroma by passing the PDF document and the embeddings object as parameters.
Create and return a conversation chain using the ConversationalRetrievalChain.from_llm() method from the langchain.chains module. This method accepts the following parameters:
llm: This is the LLM API ChatOpenAI for language generation and accepts the temperature value as a parameter that influences the diversity and creativity of the generated text.
retriever: This is the vector store retriever that searches the database using a search configuration. It accepts the search_kwargs dictionary, which includes a k key-value pair to specify the number of neighbors to return.
return_source_documents: This is a boolean that specifies whether the source document should be returned as well.


You can choose any model from the Massive Text Embedding Benchmark (MTEB) for creating the embeddings, or use the thenlper/gte-small model for simplicity. Set this as a value to the model_name parameter.
Use cpu as the value for the device parameter when creating embeddings. Other values you can choose in other contexts are cuda for Nvidia GPUs and mps for Apple silicon.
Configure the model to ensure that embeddings are not normalized by setting the encode_kwargs parameter to False.
Configure the LLM with a temperature of 0.3.
Use the Chroma.from_documents() method to create a searchable database for the PDF document.
Configure the vector store to return 2 neighbors.



# Task 5: Get and Process the File
In this task, you’ll add the components for uploading the PDF file on the web page and process it using the process_file() method from Task 4. The user will see a spinner while the file is being processed. Once the PDF has been processed, it can then be queried for answers to the user’s questions.

To complete this task, perform the following operations in the /usercode/app.py file:

Create a subheader in the first column with the text “Your Documents.”
Create a file uploader with the “Upload a PDF and click ‘Process’” label. Save the uploaded file in the session_state variable. Create a button labeled “Process” and perform the following steps when it is pressed:
Display that the file is being processed by displaying a spinner with “Processing” as the label.
Invoke the process_file() method on the uploaded file, saving the returned chain in the initialized session variable for this purpose.
Print a message to notify the user when processing has finished.


# Task 6: Set Up the Chatbot
In this task, you’ll write code for the handle_userinput() method, which will be run when the user asks a question. This function will generate a response for the user query using the initialized conversational chain, update the chat history, and update the chat transcript on the web page.

To complete this task, perform the following operations in the /usercode/app.py file:

Use the conversation chain object saved in the session_state to get a response from the API. The callable conversation chain object takes a dictionary containing the following key-value pairs as input:
question: This is the query from the user.
chat_history: This is the chat transcript from the session_state variable.
Append the query and the received response to the saved chat history in the session.
Retrieve the page number in the response and save it to the session_state variable. This is the page that was referenced when generating the response.
Update the chat in the expander component created for this purpose using the chat transcript saved in the chat history.


# Task 7: Respond to User Queries
In this task, you’ll write code to handle the user questions using the handle_userinput() method defined in Task 6. You will then display the referenced portion of the book in an iframe. To add context, you’ll add two pages before and after the referenced page in the extracted PDF.

To extract and display the PDF, perform the following operations in the /usercode/app.py file:

Determine the starting and ending page numbers of the PDF to be extracted.
Initialize a PDF writer object using the PdfWriter() method, and use the PDF.add_page() method to add pages to it.
Display the resulting file in an iframe component in the second column.

![Screenshot 2024-06-28 at 2 12 42 PM](https://github.com/ChaitanyaKarnati/Build-an-Interactive-PDF-Reader-using-LangChain-and-Streamlit/assets/126136362/c7f49d75-1bad-4ca7-a7c0-e1633aee6890)





