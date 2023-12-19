

import os
from openai import OpenAI


api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


# ## Prompt Generation

# In[3]:


def create_test_prompt(topic, num_questions, num_possible_answers, temperature):
    prompt = (
        f"Create a multiple choice quiz on the topic of {topic} consisting of {num_questions} questions."
        + f"Each question should have {num_possible_answers} options."
        + f"Also include the correct answer for each question using the starting string \n 'Correct Answer:' "
        + f"Set the temperature for generating responses to {temperature}."
    )
    return prompt


# ## Quiz Topic Selection
# #### Temperature in language generation adjusts the randomness of outputs
# Low temperature (close to 0) generates predictable text by favoring high-probability words.
# 
# Medium temperature (around 0.5 to 0.7) balances coherence and diversity in responses.
# 
# High temperature  (closer to 1 and above) fosters creativity but may yield less coherent outputs due to increased randomness.

# In[4]:


temperature_value = 0.9
prompt = create_test_prompt('Quantum Quest: Journey through the World of Quantum Computing',10,4, temperature_value)   #4,4 = 4 questions 4 options


# ### Using OpenAI's GPT-3.5-Turbo Model for Chatbot Responses.

# In[5]:


completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
)


# ### Quiz Generation along with the correct answers

# In[6]:


#print("Completion Details:")
#print(completion)
#print("\nMessage Content:")
content = completion.choices[0].message.content
print(content)


# ### Generating a student view based on the question paper

# In[7]:


def create_student_view(test,num_questions):
    student_view = {1:''}
    question_number = 1
    for line in test.split("\n"):
        if not line.startswith("Correct Answer:"):
            student_view[question_number] += line+ '\n'
        else:
            if question_number < num_questions:
                question_number +=1
                student_view[question_number]=''
    return student_view


# In[8]:


# Generate student view after the completion
student_view = create_student_view(content, 4)  # Assuming 4 questions as in the prompt


# ## Student View

# In[9]:


for key in student_view:
    print(student_view[key])


# ## Extracting the answers from the test

# In[10]:


def extract_answer(test,num_questions):
    answers = {1:''}
    question_number = 1
    for line in test.split("\n"):
        if line.startswith("Correct Answer:"):
            answers[question_number] += line+ '\n'
        
            if question_number < num_questions:
                question_number +=1
                answers[question_number]=''
    return answers


# In[11]:


extract_answer(completion.choices[0].message.content,4)


# In[12]:


student_view = create_student_view(completion.choices[0].message.content,10)


# In[13]:


answers = extract_answer(completion.choices[0].message.content,10)


# ## TAKING THE EXAM 

# In[14]:


def take(student_view):
    student_answers={}
    for question, question_view in student_view.items():
        print(question_view)
        answer = input("Enter your answer: ")
        student_answers[question] = answer
    return student_answers


# In[15]:


#student_view.items()


# In[16]:


student_answers = take(student_view)


# In[17]:


student_answers


# In[18]:


answers[2] #Sample


# ## Test Grading Function

# In[19]:


def grade(correct_answer_dict,student_answers):
    correct_answers = 0
    for question,answer in student_answers.items():
        print(question, answer)
        if answer.upper() == correct_answer_dict[question][16].upper():
            correct_answers +=1
    grade = 100*correct_answers / len(answers)
    
    if grade < 60:
        passed = "NO PASS"
    else:
        passed = "PASS!"
        
    return f"{correct_answers}/{len(answers)} correct! You got {grade} grade, {passed}"


# ## Presenting correct answers along with the total grade. 

# In[20]:


grade(answers, student_answers)


# In[ ]:




