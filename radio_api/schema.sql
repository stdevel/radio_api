DROP TABLE IF EXISTS stations;

CREATE TABLE stations(
    station_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_url TEXT NOT NULL
);

INSERT INTO stations VALUES(1, 'http://rbb-fritz-live.cast.addradio.de/rbb/fritz/live/mp3/128/stream.mp3');
