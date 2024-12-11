# Diploma-verification-and-validation-system

# Blockchain Academic Validation System

## Description
This project implements a blockchain-based system for validating and authenticating academic credentials. It addresses the challenges of traditional methods by providing a secure, transparent, and decentralized solution. Universities can generate, record, and verify academic diplomas through the Ethereum blockchain, ensuring authenticity and resistance to fraud.

## Features
- **Secure and Immutable Records**: Diplomas are stored on a decentralized ledger.
- **Digital Signature**: Ensures the authenticity of the documents.
- **IPFS Integration**: Decentralized file storage using InterPlanetary File System.
- **Smart Contracts**: Automated validation and recording of data.
- **User-Friendly Interface**: Simplified access for universities and verifiers.

## Technologies used
- **Blockchain platform**: Ethereum
- **Programming language**: Solidity, Python
- **Storage system**: IPFS (via Pinata)
- **Frontend**: Streamlit, HTML, CSS, JavaScript
- **Backend**: Node.js
- **Storage**: IPFS with Pinata as client (to store diplomas in pdf format in a decentralized way)

## Installation

### Prerequisites
- Node.js and npm installed
- Access to an Ethereum node (e.g., Infura)
- Pinata account for IPFS management

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/username/Blockchain-Diplomas.git
   cd Blockchain-Diplomas
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Configure environment variables:
   - Create a `.env` file and add the following:
     ```plaintext
     INFURA_API_KEY=your_infura_key
     PINATA_API_KEY=your_pinata_api_key
     PINATA_SECRET_API_KEY=your_pinata_secret
     ```
4. Deploy the smart contract:
   ```bash
   node scripts/deploy.js
   ```
5. Start the server:
   ```bash
   npm start
   ```
6. Access the application at `http://localhost:3000`.

## Usage
1. **University**:
   - Upload diploma details.
   - Generate a signed PDF and store it on IPFS.
   - Record transaction on the blockchain.
2. **Verifier**:
   - Enter the diploma ID or upload the diploma file.
   - Verify its authenticity by matching the hash.

## System Architecture
- **Frontend**: Provides user interfaces for universities and verifiers.
- **Backend**: Manages interactions with IPFS and the Ethereum blockchain.
- **Smart Contract**: Handles secure and immutable storage of diploma data.

![System Architecture Diagram](link_to_diagram.png)

## Testing
- **Usability Evaluation**: Conducted using the System Usability Scale (SUS).
- **Performance Analysis**:
  - Average confirmation time: ~10 seconds
  - Transaction cost: ~0.0001415 ETH ($0.51 USD)

## Future Improvements
- Optimization of transaction costs.
- Integration with existing educational management systems.
- Support for additional credential types (e.g., certificates of participation).
- Large-scale validations with multiple institutions.

## License
This project is licensed under the [MIT License](LICENSE).

## Contributing
We welcome contributions! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for details.

## Contact
- **Author**: [Your Name](mailto:your.email@example.com)
- **GitHub**: [Your GitHub Profile](https://github.com/username)
