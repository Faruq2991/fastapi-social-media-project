
-- Create the fastapi database
CREATE DATABASE fastapi;

-- Connect to the fastapi database
\c fastapi;

-- Create the posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    published BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
