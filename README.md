This project will focus on the design and development of a cryptographic application motivated from a practical use-case.

# Motivation
The average person has to manage multiple online accounts, each requiring unique login credentials. As the number of platforms grow exponentially, so does the challenge of safely managing these passwords. A report by Cybersecurity Ventures predicts that by 2025, cybercrime will cost the global economy over $10.5 trillion annually. A significant portion of these breaches was a result of weak or reused passwords.

Despite the importance of strong password practices, many people opt for convenience, using passwords that can be easily memorized (and hacked), or reusing the same password across multiple websites, because it is simply not possible for someone to remember multiple complex passwords.

This password manager bridges the gap between security and convenience. By implementing cryptographic practices in the backend, this project aims to provide a practical application of secure password management.

# Research
## Authenticating HTTP Requests
- When a user signs up or logs in, they're provided with a JWT
- When a user hits an endpoint, they need to send this token in the request headers along with their request
- The backend then verifies this token
- Once the token is verified, the user's data is extracted from it (the data was stored in the token when it was created)

## Password Hashing
The choice of a password hashing library is crucial in ensuring that even if data breaches occur, the actual passwords remain secure and indecipherable.

The password hashing algorithm must be slow ([250ms]([https://security.stackexchange.com/questions/3959/recommended-of-iterations-when-using-pbkdf2-sha256)), and the library used must be well-documented (easy to understand), and open source and widely used (will have been vetted by security experts).

`bcrypt` is suitable for this. 

## Password Generation
To ensure the generation of cryptographically secure and random passwords, let's use the `crypto` module in Node.js.

How it works:

1. Predefine the ASCII ranges for lowercase letters, uppercase letters, numbers, and symbols. These ranges are used to assemble arrays of character codes representing potential characters for password generation
2. Based on user preferences, dynamically construct a master array of character codes. For example, if a user opts for both uppercase letters and numbers, the character code array will contain codes for both uppercase letters and digits
3. For each position in the desired password length, randomly select a character code from the master array using `crypto.randomInt()`. This code is then converted to its corresponding character. This process is repeated until we've achieved the desired password length.
   1. `crypto.randomInt()` provides cryptographically secure random integers, ensuring each character in the generated password is randomly and securely chosen
4. Finally, the assembled array of characters is joined together to form the final password string, ready for use

By combining user preferences with cryptographically secure random number generation, this implementation ensures the both customizable and secure passwords.

# Design

# Development
Frontend - React

Backend - Express

DB - Mongo

Main Libraries:

1. `jsonwebtoken` (to secure/authenticate HTTP requests)
2. `bcryptjs` (to hash passwords)
2. `crypto` (to generate secure passwords)

# Setup

# User and Data Flow
1. Login Page
   1. Before accessing any features, the user is greeted with a login page
   2. The login page displays fields for inputting email, master password, and sign-up and login buttons
   3. For first-time users, they will be redirected to a registration page where they can set up their master password
   4. Otherwise, on login, a request (with the JWT) is sent to the backend

2. Vault Page
   1. Upon successful login, the user lands on the vault page which shows a list of saved websites and their credentials
   2. The user can click on an entry to view more details (website, username, password). By default, passwords are hidden, but clicking the button reveals them
   3. The user can also copy the password to their clipboard
   4. Action Buttons:
      1. Add Item: Opens a modal with fields to enter website details (URL, username, password)
      2. Edit: Allows the user to modify saved details
      3. Delete: Allows the user to remove saved details
      4. Generator: Redirects the user to a page with a generated strong password
   5. Logout
      1. Clicking the Logout button clears any client-side data and session information, ensuring security. The user is then redirected to the login page
      2. The backend ensures that user sessions are managed securely, revoking access tokens or session IDs once a logout request is received

3. Generator Page
   1. The user can customize length using a slider, with a maximum of 128 characters
   2. The user can choose what to include in the password, including lowercase letters, uppercase letters, numbers, and symbols
   3. The user can regenerate the password if they are not satisfied with it, or copy it to their clipboard