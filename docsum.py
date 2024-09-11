def split_document_into_chunks(text):
    r'''
    Split the input text into smaller chunks so that an LLM can process those chunks individually.

    >>> split_document_into_chunks('This is a sentence.\n\nThis is another paragraph.')
    ['This is a sentence.', 'This is another paragraph.']
    >>> split_document_into_chunks('This is a sentence.\n\nThis is another paragraph.\n\nThis is a third paragraph.')
    ['This is a sentence.', 'This is another paragraph.', 'This is a third paragraph.']
    >>> split_document_into_chunks('This is a sentence.')
    ['This is a sentence.']
    >>> split_document_into_chunks('')
    []
    >>> split_document_into_chunks('This is a sentence.\n')
    ['This is a sentence.']
    >>> split_document_into_chunks('This is a sentence.\n\nThis is another paragraph.\n\n')
    ['This is a sentence.', 'This is another paragraph.']
    >>> split_document_into_chunks('   This is a sentence.   \n\nThis is another paragraph.')
    ['   This is a sentence.   ', 'This is another paragraph.']
    >>> split_document_into_chunks('Sentence one.\nSentence two.')
    ['Sentence one.\nSentence two.']
    '''
    if text == "":
        return []
    if "\n" in text and "\n\n" not in text:
        return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    return [chunk for chunk in text.split("\n\n") if chunk]

if __name__ == '__main__':
    import doctest
    import os
    from groq import Groq

    # parse command line args
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    with open(args.filename) as f:
        text = f.read()

import time
from groq import Groq

def summarizer(text):
    r'''
    Summarizes text passed to it
    '''
    retries = 5
    for attempt in range(retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        'role': 'system',
                        'content': 'Summarize the input text below. Limit the summary to 1 paragraph and use a 1st grade reading level.',
                    },
                    {
                        "role": "user",
                        "content": text,
                    }
                ],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:  # Catch all exceptions if specific ones are not defined
            if attempt < retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Error occurred: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Failed after {retries} attempts")
                raise e

smalldoc = ""
for paragraph in split_document_into_chunks(text):
    sumpara = summarizer(paragraph)
    smalldoc += sumpara
    smalldoc +="\n"

print(summarizer(smalldoc))