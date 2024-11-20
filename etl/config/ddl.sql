CREATE TABLE steam_game (
    appid BIGINT PRIMARY KEY,
    name VARCHAR(255),
    developer VARCHAR(255),
    publisher VARCHAR(255),
    score_rank INT,                    -- Kolom score_rank yang sebelumnya hilang
    positive INT,
    negative INT,
    userscore DECIMAL(5, 2),           -- Asumsi tipe data untuk score
    owners VARCHAR(255),               -- Menggunakan VARCHAR untuk menyimpan data seperti '100K-200K'
    average_forever DECIMAL(10, 2),
    average_2weeks DECIMAL(10, 2),
    median_forever DECIMAL(10, 2),
    median_2weeks DECIMAL(10, 2),
    price DECIMAL(10, 2),              -- Harga dalam format desimal
    initialprice DECIMAL(10, 2),       -- Harga awal dalam format desimal
    discount INT,
    ccu INT,                           -- Asumsi tipe data untuk ccu
    link TEXT,                          -- Link terkait
    title VARCHAR(255),                -- Judul game
    release_date DATE                  -- Tanggal rilis
);


CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,         -- ID unik untuk genre
    appid BIGINT REFERENCES steam_game(appid) ON DELETE CASCADE,   -- Hubungan dengan tabel games
    genre VARCHAR(255) NOT NULL,
    UNIQUE (appid,genre)
);

CREATE TABLE languages (
    language_id SERIAL PRIMARY KEY,      -- ID unik untuk bahasa
    appid BIGINT REFERENCES steam_game(appid) ON DELETE CASCADE,  -- Hubungan dengan tabel games
    language VARCHAR(255) NOT NULL,
    UNIQUE (language,appid)
);



CREATE TABLE player_chart (
    month DATE NOT NULL,          -- Represents the month
    appId BIGINT NOT NULL,        -- Foreign key referencing the game table
    average_players DECIMAL(10, 2), -- Average number of players
    gain DECIMAL(10, 2),          -- Gain in player count
    percentage_gain DECIMAL(6, 4), -- Percentage gain as a decimal
    peak_players INT,             -- Peak number of players
    PRIMARY KEY (month, appId),   -- Composite primary key
    FOREIGN KEY (appId) REFERENCES steam_game(appId) ON DELETE CASCADE,
    UNIQUE (month,appId)
);