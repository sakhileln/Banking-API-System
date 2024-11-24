// Function to create a new account via the API
function createAccount() {
    let firstName = document.getElementById('first_name').value;
    let lastName = document.getElementById('last_name').value;
    let email = document.getElementById('email').value;
    let balance = parseFloat(document.getElementById('balance').value);

    fetch('/accounts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            first_name: firstName,
            last_name: lastName,
            email: email,
            balance: balance
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById('message').textContent = data.message;
            document.getElementById('message').classList.add('success');
        }
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Error: ' + error;
        document.getElementById('message').classList.add('error');
    });
}

// Function to fetch account details via the API
function viewAccount(accountId) {
    fetch(`/accounts/${accountId}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('message').textContent = data.error;
            document.getElementById('message').classList.add('error');
        } else {
            // Display account details
            document.getElementById('account_details').innerHTML = `
                <h3>Account Details:</h3>
                <p><strong>Account ID:</strong> ${data.account_id}</p>
                <p><strong>Name:</strong> ${data.first_name} ${data.last_name}</p>
                <p><strong>Email:</strong> ${data.email}</p>
                <p><strong>Balance:</strong> $${data.balance}</p>
            `;
        }
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Error: ' + error;
        document.getElementById('message').classList.add('error');
    });
}

// Function to make a transaction (deposit or withdraw) based on user selection
function makeTransaction() {
    const email = document.getElementById('transaction-email').value;
    const transactionType = document.getElementById('transaction-type').value;
    const amount = parseFloat(document.getElementById('transaction-amount').value);

    // Validate input
    if (email === "" || amount <= 0) {
        document.getElementById('transaction-message').innerHTML = "<p class='error'>Please provide valid email and amount.</p>";
        return;
    }

    // Fetch user account using email (this would be an API call or a backend query)
    const account = getAccountByEmail(email);  // This is a placeholder function

    if (!account) {
        document.getElementById('transaction-message').innerHTML = "<p class='error'>Account not found.</p>";
        return;
    }

    // Perform deposit or withdraw based on transaction type
    if (transactionType === "deposit") {
        account.balance += amount;  // Increase balance by the deposit amount
        document.getElementById('transaction-message').innerHTML = `<p class='success'>Deposited $${amount}. New Balance: $${account.balance}</p>`;
    } else if (transactionType === "withdraw") {
        if (account.balance >= amount) {
            account.balance -= amount;  // Decrease balance by the withdrawal amount
            document.getElementById('transaction-message').innerHTML = `<p class='success'>Withdrew $${amount}. New Balance: $${account.balance}</p>`;
        } else {
            document.getElementById('transaction-message').innerHTML = "<p class='error'>Insufficient balance for withdrawal.</p>";
        }
    }
}

// Mock account database (replace with actual backend call)
const accounts = [
    { email: "user@example.com", name: "John Doe", balance: 1000 },
    { email: "jane.doe@example.com", name: "Jane Doe", balance: 500 }
];

function getAccountByEmail(email) {
    return accounts.find(account => account.email === email);
}

// Function to hide all sections
function hideSections() {
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.classList.add('hidden');
    });
}

// Function to show the selected section
function showSection(sectionId) {
    hideSections(); // Hide all sections first
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.remove('hidden'); // Show the selected section
    }
}

// Initially show the create-account section
document.addEventListener('DOMContentLoaded', function () {
    showSection('create-account');
});

// Function to navigate to the respective section
function navigateToSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => section.classList.remove('active'));

    // Show the section corresponding to the clicked link
    const sectionToShow = document.getElementById(sectionId);
    sectionToShow.classList.add('active');
}
