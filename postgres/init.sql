-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE
);

-- Create sboms table
CREATE TABLE IF NOT EXISTS sboms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    content JSONB,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create scan_results table
CREATE TABLE IF NOT EXISTS scan_results (
    id SERIAL PRIMARY KEY,
    sbom_id INTEGER REFERENCES sboms(id),
    results JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create approvals table
CREATE TABLE IF NOT EXISTS approvals (
    id SERIAL PRIMARY KEY,
    sbom_id INTEGER REFERENCES sboms(id),
    approved_by INTEGER REFERENCES users(id),
    approved BOOLEAN,
    notes TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create tokens table
CREATE TABLE IF NOT EXISTS tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token TEXT,
    expires_at TIMESTAMP
);

CREATE TABLE scan_retries (
  id SERIAL PRIMARY KEY,
  sbom_id INTEGER NOT NULL REFERENCES sboms(id),
  requested_by TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);