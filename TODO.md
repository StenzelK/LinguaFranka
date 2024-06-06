# Project Development Plan

## Functionalities

### To Implement

1. **Settings Panel**
   - **Difficulty: 1/5**
   - Design and implement a user-friendly settings interface that allows users to customize their preferences.

2. **OpenAI API Integration**
   - **Difficulty: 4/5**
   - Integrate the application with OpenAI's API to enhance interaction capabilities using advanced artificial intelligence features.

3. **Implement GPT Placeholders**
   - **Difficulty: 3/5**
   - Transition from placeholder functions to actual API calls to the OpenAI service for dynamic responses.

4. **Chat Functionality**
   - **Difficulty: 5/5**
   - Develop a real-time chat interface to facilitate interactive communication between users and the AI bot.

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

## Bugs

### To Fix

1. **Fatal Error If Translation Files Don't Match**
   - **Priority: CRITICAL**
   - Resolve the critical issue where mismatched translation files cause the application to crash, ensuring consistent stability across various locales.

2. **No Translation on User Profile**
   - **Priority: Evaluate**
   - Assess the need and potential benefits of translating user profile content, based on user feedback and usage analytics.

3. **No Sanitization on User Profile Input**
   - **Priority: Medium**
   - Implement validation for user profile inputs to prevent issues arising from malformed or malicious data entries.

## Considerations

### Potential Changes

1. **Remove `user_lang` from Config**
   - **Consideration: Redundancy?**
   - Evaluate the redundancy of `user_lang` in the config, considering the possibility of using `native_language` from user profiles instead.
   
### Additional features

1. **Implement a tutorial for new users**
	- **Consideration: Nessesary?**
	- To be determined based on tester feedback