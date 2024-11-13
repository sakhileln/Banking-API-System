from sqlite3 import connect


def create_database() -> None:
    """
    Create the banking API database with transactions and accounts.

    Parameters:
        None
    Return:
        None
    """
    # Initialize databbase connection
    connection = connect("database.db")
    # Get cursor to execute SQL commands
    cursor = connection.cursor()

    # Create the 'accounts' table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS accounts (
            account_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL, 
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    # Create the 'transactions' table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL,              -- Foreign Key: References 'accounts'
            amount DECIMAL(15, 2) NOT NULL,
            type TEXT CHECK(type IN ('deposit', 'withdraw')) NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE  -- Foreign key relationship
        );
        """
    )

    # Write changes to datavase
    connection.commit()

    # Close connection
    cursor.close()
    connection.close()
