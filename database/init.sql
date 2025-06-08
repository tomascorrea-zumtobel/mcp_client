-- Database initialization script for German Learning MCP project
-- This script creates the translations table with all required fields

-- Create the translations table
CREATE TABLE IF NOT EXISTS translations (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    german TEXT NOT NULL,
    english TEXT,
    spanish TEXT
);


-- Insert some sample data for testing
INSERT INTO translations (german, english, spanish) VALUES
    ('Hallo', 'Hello', 'Hola'),
    ('Danke', 'Thank you', 'Gracias'),
    ('Auf Wiedersehen', 'Goodbye', 'Adiós')
ON CONFLICT DO NOTHING;

-- Show the table structure
\d translations;
