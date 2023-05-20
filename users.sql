CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    role VARCHAR(255)
);

INSERT INTO users (id, name, email, role) VALUES
    (1, 'John Doe', 'johndoe@example.com', 'Admin'),
    (2, 'Jane Smith', 'janesmith@example.com', 'User'),
    (3, 'Bob Johnson', 'bobjohnson@example.com', 'User');
