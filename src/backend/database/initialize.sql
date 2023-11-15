CREATE TABLE IF NOT EXISTS item (
    id INTEGER PRIMARY KEY,
    name TEXT,
    store_id INTEGER,
    unit TEXT,
    price INTEGER,
    url TEXT
);

CREATE TABLE IF NOT EXISTS taxomony (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY,
    name TEXT,
    url TEXT
);

CREATE TABLE IF NOT EXISTS item_taxonomy (
    item_id INT,
    taxonomy_id INT,
    PRIMARY KEY (item_id, taxonomy_id),
    FOREIGN KEY (item_id) REFERENCES item(id),
    FOREIGN KEY (taxonomy_id) REFERENCES taxonomy(id)
);

INSERT OR IGNORE INTO store VALUES (1, "AH", "https://www.ah.nl");
INSERT OR IGNORE INTO store VALUES (2, "Jumbo", "https://www.jumbo.com");