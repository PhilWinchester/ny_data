CREATE TABLE test (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(30) NOT NULL,
    lastname VARCHAR(30) NOT NULL,
    email VARCHAR(50),
    datetime_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    datetime_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO test (firstname, lastname, email) VALUES ('test', 'test', 'test@example.com');
INSERT INTO test (firstname, lastname, email) VALUES ('test1', 'test1', 'test1@example.com');
INSERT INTO test (firstname, lastname, email) VALUES ('test2', 'test2', 'test2@example.com');
INSERT INTO test (firstname, lastname, email) VALUES ('test3', 'test3', 'test3@example.com');
INSERT INTO test (firstname, lastname, email) VALUES ('test4', 'test4', 'test4@example.com');
INSERT INTO test (firstname, lastname, email) VALUES ('test5', 'test5', 'test5@example.com');


