CREATE TABLE IF NOT EXISTS travel_development_idea (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idea TEXT NOT NULL,
    status TEXT NOT NULL
);

INSERT INTO travel_development_idea (idea, status) VALUES ('Fix carousel CSS: remove all the broken css rules, and dynamically calculate slide width', 'pending');
INSERT INTO travel_development_idea (idea, status) VALUES ('Fix carousel JavaScript: replace the static script with a dynamic one that correctly handles slide navigation and updates the UI', 'pending');
