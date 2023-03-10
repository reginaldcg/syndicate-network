# DEVLOG.md
*Just the bits, pieces and bullshit for organizational purposes.*

## Heatmap
	Cardano Blockchain
	|-- OpenAI
		|-- Gamified Experience
		|-- No Data Collection
		|-- Modern UI Design

## Tech Stack
	Chrome Extension
	|-- Content Creation and Distribution
	|-- Task Reward
	|-- Paper Money

---

## Niche Collection
Take inspiration from the below niches, ya´ bithc.

### ⚓ Transaction Analyzer
> A Cardano transaction history analyzer that uses OpenAI's NLP to categorize transactions into specific groups (such as income, expenses, etc.) and displays them in a modern UI.

### ⚓ Blockchain Explorer
> A Cardano blockchain explorer that provides real-time analysis and visualization of transactions on the Cardano network. OpenAI's natural language processing could be used to provide meaningful insights into the data.

### ⚓ Newsfeed Aggregator
> A Cardano news aggregator that uses OpenAI's API to summarize news articles in real-time, so users can quickly digest the most important information and rewarding users with tokens for engaging with the content.

### ⚓ Automated Trading
> An extension that integrates with OpenAI's API to generate custom, automated trading algorithms for the Cardano market based on user risk tolerance and market conditions.

### ⚓ Personalized News
> An extension that aggregates the latest news and updates on the Cardano blockchain from multiple sources, using OpenAI's language processing capabilities to curate high-quality content.

### ⚓ Crowdfunding Platform
> A Cardano-based crowdfunding platform that leverages OpenAI's natural language processing to match users with compatible projects and facilitate funding.

### ⚓ Lending Platform
> A Cardano-based decentralized lending platform that uses OpenAI's predictive modeling to determine borrower eligibility and provide automated loan underwriting and decision-making.

### ⚓ Content Creation and Distribution
> A Cardano-based content creation and distribution platform that utilizes OpenAI's language processing to help users generate and curate high-quality content.

### ⚓ Voting System
> A Cardano-based platform for online voting and decision-making that leverages OpenAI's predictive modeling to provide users with real-time feedback and insights.

### ⚓ Task Reward
> An extension that rewards users for completing tasks related to Cardano, such as participating in community discussions or spreading the word about the project on social media.

### ⚓ Paper Money
> An extension that presents users with a simulated trading environment, where they can buy and sell ADA using play money, with the goal of achieving the highest returns.

### ⚓ Social Discovery Network
> A Cardano social network that gamifies the process of discovering new projects and connecting with other users, rewarding users who contribute valuable insights or content with points or other rewards.

### ⚓ NFT Explorer
> "Cardano NFT Explorer" - An extension that helps users explore and discover NFTs (non-fungible tokens) on the Cardano blockchain, leveraging the Cardano NFT Metadata API.

### ⚓ Prediction Market
> A browser extension that gamifies the prediction market process by allowing users to make predictions about the future of the Cardano blockchain and rewarding them with tokens for accurate predictions.

---

## Tech Stack (continued...)

- React for the UI
- Redux for state management
- TypeScript for type checking
- Web3.js for interacting with the Cardano blockchain
- OpenAI API for language processing
- Firebase for data storage and authentication
- Material-UI for UI components

Setting up Firebase Authentication
```ts
import firebase from 'firebase/app';
import 'firebase/auth';

const firebaseConfig = {
  // Your Firebase configuration here
};

firebase.initializeApp(firebaseConfig);

// Sign in with Google
const provider = new firebase.auth.GoogleAuthProvider();
export const signInWithGoogle = () => {
  firebase.auth().signInWithPopup(provider);
};

// Sign out
export const signOut = () => {
  firebase.auth().signOut();
};
```

Retrieving Cardano wallet balance using Web3.js
```ts
import Web3 from 'web3';
import { CARDANO_NETWORK, BLOCKFROST_API_KEY } from '../constants';

const web3 = new Web3(new Web3.providers.HttpProvider(CARDANO_NETWORK));

export const getBalance = async (address: string) => {
  const balanceInLovelace = await web3.eth.getBalance(address);
  const balanceInADA = web3.utils.fromWei(balanceInLovelace, 'ether');
  return balanceInADA;
};
```

Using OpenAI API to generate content
```ts
import OpenAI from 'openai-api';

const openai = new OpenAI(process.env.OPENAI_API_KEY);

export const generateText = async (prompt: string) => {
  const response = await openai.complete({
    engine: 'text-davinci-002',
    prompt,
    maxTokens: 1024,
    n: 1,
    stop: '\n',
  });
  return response.choices[0].text.trim();
};
```

Creating a simulated trading environment
```ts
import { ADA_PRICE } from '../constants';

const startingBalance = 1000000; // Amount of play money to start with
let balance = startingBalance;

const buyADA = (quantity: number) => {
  const cost = ADA_PRICE * quantity;
  if (cost > balance) {
    throw new Error('Insufficient funds');
  }
  balance -= cost;
  // Add ADA to user's simulated wallet
};

const sellADA = (quantity: number) => {
  const salePrice = ADA_PRICE * quantity;
  balance += salePrice;
  // Remove ADA from user's simulated wallet
};
```

**!** Constants defined in a separate file. **!**
> `CARDANO_NETWORK`
>
> `BLOCKFROST_API_KEY`
>
> `ADA_PRICE`
