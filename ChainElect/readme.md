# 🗳️ ChainElect
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)  
![Issues](https://img.shields.io/github/issues/knightlesssword/flet)  
![Python Version](https://img.shields.io/badge/Python-3.12+-blue.svg)  
![Repo Size](https://img.shields.io/github/repo-size/knightlesssword/flet)  
![Last Commit](https://img.shields.io/github/last-commit/knightlesssword/flet)  
![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange)  
![License](https://img.shields.io/badge/License-CC%20BY--NC--4.0-blue)  

![Forks](https://img.shields.io/github/forks/knightlesssword/flet?style=social)  ![Stars](https://img.shields.io/github/stars/knightlesssword/flet?style=social)
## Blockchain Voting System

A **secure, decentralized voting system** built using **Flet** and **Python**, leveraging blockchain technology to ensure trust and transparency in elections. ChainElect stores each vote in a block, making it immutable and traceable, while featuring administrative functions like vote validation and ledger export. **Fernet encryption** further enhances the confidentiality of voter data by encrypting sensitive information.

## 🚀 Features
- 🔗 Blockchain-Powered Voting:
Store each vote securely in a block linked to the previous one, ensuring immutability and transparency throughout the voting process.

- 🛡️ Data Encryption with Fernet:
Keep votes and sensitive data confidential with Fernet symmetric encryption, providing high-level security.

- 📱 QR Code Generation:
Generate a QR code for the blockchain ledger, making sharing or verification quick and easy.

- 📤 Export Blockchain Ledger:
Save the entire blockchain as a JSON file to back up data or share it with others effortlessly.

- ✅ Vote Validation:
Ensure the integrity of the blockchain by validating the hashes and maintaining seamless continuity between blocks.

- 🌙 Dark Mode Toggle:
Switch between light and dark themes for a user-friendly and accessible experience.

- 🛠️ Admin Panel:
Manage elections with ease—view election details, reset voting data, or adjust settings as needed.

## 🛠️ Tech Stack
- **Frontend**: Flet (Python-based UI library)
- **Blockchain Backend**: A custom in-memory blockchain implemented in Python
- **Encryption**: cryptography library (Fernet for symmetric encryption)
- **QR Code Generation**: qrcode library from PyPI
- **Data Export/Import**: JSON handling for saving and restoring blockchain data

---

## 📋 Installation Instructions

1. **Clone the Repository**  
   Use `git clone` followed by the repository URL to clone the project locally.
    ```bash
   git clone https://github.com/knightlesssword/flet/

2. **Navigate into the Project Directory**  
   Use `cd` to change into the cloned project directory.
    ```bash
   cd ChainElect

3. **Install Required Dependencies**  
   Install all dependencies listed in the `requirements.txt`.
   ```bash
   pip install requirements.txt

4. **Configure environment variable(s)**  
   Create a `.env` file in the project directory.
   ```bash
   ADMIN_PASSWORD = '<some-value>'

5. **Run the Application**  
   Execute the `main` Python script to start the application.
   ```bash
   python main.py

---

## 🧩 Dive in code

### 🧱 `Block` Class  
The `Block` class represents an individual **block** in the blockchain, the fundamental unit that holds encrypted data and links to other blocks.  

Each block stores:  
- 🔢 **Index**: Position of the block within the chain.  
- ⏰ **Timestamp**: When the block was created.  
- 🔐 **Data**: The encrypted content, such as a vote, secured with **Fernet encryption** for privacy.  
- 🔗 **Previous Hash**: The hash of the preceding block, ensuring continuity between blocks.  
- 🧩 **Hash**: The current block’s unique identifier, generated using **SHA-256** to maintain integrity.  

✨ **Encryption**: Data in every block is encrypted using **Fernet** to ensure confidentiality, making it impossible for unauthorized users to tamper with or read the contents.  

---

### 🔗 `Blockchain` Class  
The `Blockchain` class manages the entire **chain of blocks** and provides essential functionalities to maintain its structure and security.  

Key features include:  
- 🧬 **Genesis Block Creation**: Initializes the chain with the **first block**, called the genesis block, which serves as the starting point of the blockchain.  
- ➕ **Add Block**: Appends a new block by **encrypting the data** and linking it to the **previous block**.  
- 🕵️‍♂️ **Get Latest Block**: Retrieves the most **recent block** in the blockchain, ensuring new blocks can be correctly appended.  
- 🛡️ **Blockchain Validation**: Maintains blockchain **integrity** by verifying the consistency of **hashes** and the continuity of the block sequence. If any block is tampered with, the chain becomes invalid.  

🔒 **Security Mechanism**: The blockchain is **immutable**—once a block is added, it cannot be altered without breaking the chain, ensuring **transparency** and **trust**.

---

## 🛡️ Security Features
- **Encryption**: All votes are encrypted using Fernet symmetric encryption, providing an additional layer of security.
- **Blockchain Integrity**: Hashes are used to link blocks and ensure immutability.
- **Validation Mechanism**: Built-in validation function verifies the consistency and correctness of the blockchain.

---

## 📂 How to Export Data
- **Export**: The blockchain can be exported as a JSON file to create backups or share the ledger using `Export Ledger` button.
- `View Ledger as QR` - allows you to share the current ledger in a JSON format via QR code.

---

## 🔧 Admin Capabilities
- 🗳️ **Reset Election**: Admins can reset all voting data to start a new election.
- 🔢 **View vote count**: A quick look at vote count with candidate details for analytics.

---

## 🌗 User Experience
- **Dark/Light Mode**: Users can toggle between dark and light themes based on preference.
- **Intuitive UI**: The interface, built using Flet, provides a simple and user-friendly experience for voters and administrators.

---

## 📈 Future Improvements
- **Multi-user Authentication**: Implement user accounts with varying access levels.
- **Smart Contract Integration**: Use smart contracts for automated processes like voter registration.
- **Distributed Storage**: Store the blockchain across multiple nodes for enhanced reliability.

---

## 🤝 Contribution

Open source community is built on contribution. Feel free to contribute to this project by forking and creating pull requests.


## ⚖️ License  
This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. 
For more information, visit [this link](https://creativecommons.org/licenses/by-nc/4.0/).

## 👩🏻‍💻 Author
[Abu Bakr](https://github.com/knightlesssword)
