-- Flyway migration for items table
CREATE TABLE IF NOT EXISTS items (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster name lookups (stretch goal)
CREATE INDEX IF NOT EXISTS idx_items_name ON items(name);

-- Optional: Seed some data for testing
INSERT INTO items (name, description) VALUES 
    ('Test Item 1', 'This is a test item'),
    ('Test Item 2', 'This is another test item')
ON CONFLICT DO NOTHING;