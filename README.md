# Borrow books task

### Book Model

The `Book` model is designed to represent information about books in the system.

#### Fields:

- `title`: CharField - the title of the book.
- `authors`: CharField - the authors of the book.
- `category`: CharField - the category of the book.
- `availability`: BooleanField - indicates whether the book is currently available.

### BorrowRecord Model

The `BorrowRecord` model is designed to track borrowings, including borrower details, borrow dates, and return dates.

#### Fields:

- `borrow_date`: DateField - the date the book was borrowed (auto-generated on borrowing).
- `return_date`: DateField - the date the book was returned.
- `borrower`: ForeignKey to User - the user who borrowed the book.
- `book`: ForeignKey to Book - the book that was borrowed.

## Borrowing and Returning

The system allows for the borrowing and returning of available books with the following logic:

### Borrowing:

- The user requests to borrow a book by providing the book ID and their user ID.
- If the book is available, a `BorrowRecord` is created, and the book's availability status is updated to "unavailable."

### Returning:

- The user returns a borrowed book by providing the `BorrowRecord` ID.
- The book's availability status is updated to "available," and the return date is recorded in the `BorrowRecord`.

## Borrow Records Management

Endpoints have been created to manage and filter borrow records:

- `GET /borrowrecords/`: List all borrow records.
- `GET /borrowrecords/<pk>/`: Retrieve details of a specific borrow record.
- `POST /borrowrecords/`: Create a new borrow record.
- `PUT /borrowrecords/<pk>/`: Update details of a specific borrow record.
- `DELETE /borrowrecords/<pk>/`: Delete a specific borrow record.
- `GET /borrowrecords/filter/`: Filter borrow records based on `borrower_id` or `book_id`.

## Security Measures

The API includes security measures focusing on authentication and authorization:

- Token-based authentication is implemented using the `/api-token-auth/` endpoint.
- Endpoints related to book and borrow record management require user authentication.
- Permissions are set to control access to specific views based on user roles.
- Token-based authentication is implemented using the `/api-token-auth/` endpoint.
- Endpoints related to book and borrow record management require user authentication.
- Permissions are set to control access to specific views based on user roles.
