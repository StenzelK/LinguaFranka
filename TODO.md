# Project Development Plan

## Functionalities

### To Implement

1. **Settings Panel**
   - **Difficulty: 1/5**
   - Design and implement a user-friendly settings interface that allows users to customize their preferences.

2. **OpenAI API Integration**
   - **Difficulty: 4/5**
   - Integrate the application with OpenAI's API to enhance interaction capabilities using advanced artificial intelligence features.
   - **DONE**


3. **Implement GPT Placeholders**
   - **Difficulty: 3/5**
   - Transition from placeholder functions to actual API calls to the OpenAI service for dynamic responses.
   - **DONE**

4. **Chat Functionality**
   - **Difficulty: 5/5**
   - Develop a real-time chat interface to facilitate interactive communication between users and the AI bot.
   - **DONE**

5. **Chat Selection**
   - **Difficulty: 2/5**
   - Implement storage and selection for past chat instances

6. **AI bots generation**
   - **Difficulty:3/5**
   - Implement a system for generating bot personalities based on practice language and user interest-
   - **50% DONE**

6. **Bot selection**
   - **Difficulty: 2/5**
   -Implement storage and selection of bots based on practice language

5. **User Prompt Commentary**
   - **Difficulty: 3/5**
   - Implement a feature where the AI uses OpenAI's API to provide commentary on texts submitted by users.

6. **Bot Response Explanation**
   - **Difficulty: 3/5**
   - Use OpenAI's API to generate detailed explanations of the AI bot's responses to enhance user understanding.

7. **UX Design**
   - **Difficulty: 4/5**
   - Craft an intuitive, engaging, and accessible user experience design for a wide range of users.

8. **One Click Installer**
   - **Difficulty: 2/5**
   - Develop a straightforward installation process that simplifies setup to a single-click action for users.

9. **End-User Evaluation**
   - **Difficulty: 1/5**
   - Distribute the application to a select group of beta users to procure valuable insights and feedback.

10. **Rebuild auto-translate**
   - **Difficulty: 2/5**
   - Googletrans and openai modules conflict in httpx version, rewrite auto-translate using GCP 

11. **Add new texts to the auto-translate json file**
   - **Difficulty: 1/5**
   - Move the fixed demo text to auto-translate once it's fixed

12. **Gemini API integration**
   - **Difficulty: 4/5**
   - Implement requiered functionalities for Gemini


13. **LLaMa2 API integration**
   - **Difficulty: 4/5**
   - Implement requiered functionalities for LLaMa2


14. **AI interface overhaul**
   - **Difficulty: 5/5**
   - Rewrite backend logic to be model agnostic and support seemless model change via single parameter

## Bugs

### To Fix

1. **Fatal Error If Translation Files Don't Match**
   - **Priority: CRITICAL**
   - Resolve the critical issue where mismatched translation files cause the application to crash, ensuring consistent stability across various locales.
   - **FIX - nonexistent files default to English, mismatch to be detected in testing**

2. **No Translation on User Profile**
   - **Priority: Evaluate**
   - Assess the need and potential benefits of translating user profile content, based on user feedback and usage analytics.
   - **Irrelevant - no tangible benefit to the user**

3. **No Sanitization on User Profile Input**
   - **Priority: Medium**
   - Implement validation for user profile inputs to prevent issues arising from malformed or malicious data entries.
   - **FIX - implemented js based sanitizer to all forms**

4. **Examples in profile submit form ot displaying correctly**
   - **Priority: Low**
   - Fix improper default texts in user profile submition form
   - **FIX - corrected jinja formatting**

5. **Language explanation chooses a random language when both practice and user language are the same**
   - **Priority: Low**
   - Fringe scenario that will likely never happen in actual use

6. **Form data appears to get trunkated in some edge cases**
   - **Priority: Medium**
   - User observed incomplete translation during a conversation in Italian, log inspection confirmed only partof the text was parsed, potential culprit is the character "
   - Suggestion: Introduce escape characters during the initial parsing

## Considerations

### Potential Changes

1. **Remove `user_lang` from Config**
   - **Consideration: Redundancy?**
   - Evaluate the redundancy of `user_lang` in the config, considering the possibility of using `native_language` from user profiles instead.
   - **CLOSED - variables made codepentent, kept user_lang for ease of access**

2. **Refactor GPT_Tools**
   - **Consideration: Potential name conflicts**
   - Consts in GPT_tools.py are global and may cause namespace issues. Refactor to OOP?
   - **CLOSED - renamed consts to minimize conflict opportunities**
   
### Additional features

1. **Implement a tutorial for new users**
	- **Consideration: Nessesary?**
	- To be determined based on tester feedback