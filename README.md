This project will focus on the design and development of a cryptographic application motivated from a practical use-case.

# Motivation
The average person has to manage multiple online accounts, each requiring unique login credentials. As the number of platforms grow exponentially, so does the challenge of safely managing these passwords. A report by Cybersecurity Ventures predicts that by 2025, cybercrime will cost the global economy over $10.5 trillion annually. A significant portion of these breaches was a result of weak or reused passwords.

Despite the importance of strong password practices, many people opt for convenience, using passwords that can be easily memorized (and hacked), or reusing the same password across multiple websites, because it is simply not possible for someone to remember multiple complex passwords.

This password manager bridges the gap between security and convenience. By implementing cryptographic practices in the backend, this project aims to provide a practical application of secure password management.

# Research

# Design

# Development
Frontend - React

Backend - Node

DB - 

Libraries:
1. 


# Setup

# User and Data Flow
1. Login Page
   1. Before accessing any features, the user is greeted with a login page
   2. The login page displays fields for inputting the master password, sign-up and forgot password links, and a login button
   3. For first-time users, a link redirects to a registration page where they can set up their master password
   4. If they have previously set a password, they need to input the master password to gain access
   5. On submitting the master password, a request is made to the Node backend to verify the provided credentials
   6. After three unsuccessful login attempts, the user sees a message stating that they have been locked out for 5 minutes
   7. If the vault has been tampered with, backend sends an appropriate response to the frontend which then logs the user out with a security warning

2. Vault Page
   1. Upon successful login, the user lands on the vault page which shows a list of saved websites
   2. The user can click on an entry to view more details (website, username, password)
   3. A "Show" button next to each entry allows users to toggle the visibility of passwords. By default, passwords are hidden, but clicking the button reveals them
   4. The user can also copy the password to their clipboard, but will be cleared from the clipboard after 10s to minimize unintentional exposure. 
   5. Action Buttons:
      1. Change Master Password: Opens a modal with a field to update the master password
      2. Add New: Opens a modal with fields to enter website details (URL, username, password)
      3. Edit: Allows the user to modify saved details
      4. Delete: Allows the user to remove saved details
      5. Password Generator: Opens a modal with a generated strong password
   6. Logout
      1. Clicking the Logout button clears any client-side data and session information, ensuring security. The user is then redirected to the login page
      2. The Node backend ensures that user sessions are managed securely, revoking access tokens or session IDs once a logout request is received