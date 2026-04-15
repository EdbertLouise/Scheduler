import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage 

from googlecalendar import extractPresent

from extraction import extract

load_dotenv()

groq_key = os.getenv("GROQ_KEY")
# print("Loaded key?", groq_key is not None)
# print("Key prefix:", groq_key[:8] if groq_key else None)

##############################################################################################

llm = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    temperature=0,
    openai_api_key=groq_key,
    openai_api_base="https://api.groq.com/openai/v1"
)

def returnJSON(files, userInput):

    #print("THIS", files, userInput)
    
    full_text = f"""

    {userInput}

    content:
    {extract(files)}"""

    prompt = f"""
    You are extracting scheduling information from a PDF.

    Return ONLY valid JSON.
    Do not include markdown.
    Do not include explanations.
    Do not include extra text before or after the JSON.

    Always return a JSON array. Do not return a single object. Even if there is only one item, it must be inside a list.

    Each item must follow this format:
    {{
    "title": "string",
    "type": "event" or "deadline",
    "category": "College" or "Church" or "Personal" or "Work"
    "day": "string or null",
    "startDate": "YYYY-MM-DD or null",
    "endDate": "YYYY-MM-DD or null",
    "startTime": "HH:MM or null",
    "endTime": "HH:MM or null",
    "recurring": true or false,
    "recurringType": Weekly, Biweekly, Monthly, Yearly
    "recurrence_days": ["MO", "TU", "WE", "TH", "FR", "SA", "SU"] or [],
    "until": "YYYYMMDD or null (if recurring is false)"
    "notes": "string"
    }}


    Rules:
    1. Make sure to be very specific about its title. Include its most unique properties. Don't include code
    2. Set "category" to either "College", "Church", "Work", or "Personal" according to the topic of the user input. Example: If the task is about homework, then set "category" to College.
       If user input specifies a hangout with friends or a practice session of skills, set "category" to "Personal"
    3. Today is {extractPresent()}. Adjust the date according to what the user wants. Example. If today is 4 April 2025 and the user specifies that they have an event tomorrow then set the endDate to 5 April 2025.
    4. If no exact time is given, set both "startTime" and "endTime" to null.
    5. If no exact date is given and rule 2 isn't applied, set "startDate" and "endDate" to null.
    6. Set "day" according to the "date" given unless "date" is null
    7. If no timezone is given, assume "startTime"/"endTime", "startDate"/"endDate", and "day" follow the Asia/Taipei timezone. Otherwise, convert to follow the Asia/Taipei timezone
    8. If the item is a task or homework, treat it as an all-day event. Set "type" to "deadline", set the "endDate" first before setting "startDate" to the "endDate", and set "startTime" to null.
    9. If time range exceeds over 7 days. set "startDate" to "endDate".
    10. If it is a scheduled activity/class/meeting, set "type" to "event".
    11. If it does not repeat, set "recurring" to false and "recurrence_days" to []. Otherwise set to True.
    12. Ensure that the recurrence_days list includes the weekday corresponding to startDate.
    13. Set "until" according to the date the user specifies. "until" is not the same as "endDate".
    14. "until" cannot be null if "recurring" is true. if "until" is null and "recurring" is true, set "until" to endDate.
    15. Convert weekdays to Google Calendar style:
    Monday = MO
    Tuesday = TU
    Wednesday = WE
    Thursday = TH
    Friday = FR
    Saturday = SA
    Sunday = SU
    16. "notes" should briefly describe the extracted item.
    

    PDF content:
    {full_text}
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content 



