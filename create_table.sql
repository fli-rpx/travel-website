-- Connect to the travel_website database
\c travel_website

-- Create the new table in the 'travel' schema
CREATE TABLE travel.travel_development_ideas (
    id SERIAL PRIMARY KEY,
    idea TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

-- Describe the new table to confirm its structure
\d travel.travel_development_ideas;
