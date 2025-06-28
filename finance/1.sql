CREATE TABLE tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price INTEGER NOT NULL,
    purchase_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE UNIQUE INDEX unique_tracking ON tracking(id);
CREATE INDEX index_tracking ON tracking(user_id, symbol);
