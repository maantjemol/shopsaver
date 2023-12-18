# Shopsaver

A fullstack webapp to unearth the Best Grocery Deals!

Video: https://www.youtube.com/watch?v=fsJYcPDZ2us

## Installation

Clone the project

```bash
git clone https://github.com/maantjemol/shopsaver.git
cd shopsaver
```

Install the `requirements.txt`

```bash
pip3 install -r requirements.txt
```

Make sure npm and node is [installed](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) and run te following commands to install the frontend:

```bash
cd src/frontend
npm install
```

## Usage

### Backend

We included the already build database to get up and running as fast as possible. We describe below how you can build this database yourself

Open a new terminal window and go into the `API` folder

```bash
cd src/backend/API
```

Start the server

```bash
python3 server.py
```

### Frontend

Open a new terminal window and go into the `frontend` folder.

```bash
cd src/frontend
```

Run the webserver:

```bash
npm run dev
```

## Building the database

This part of the process is a bit flacky because we get the data from the websites of the supermarkets. These websites change, so it could be possible that the current setup doesn't work anymore. This happened multiple times during development. We cached the response from the APIs in a JSON file to make it easier to build the database, be it with outdated data.

### Building from cache

Go into the backend folder

```bash
cd src/backend
```

Run the `main.py` file to build the database from cache

```bash
python3 main.py
```

This should take about 5-10 minutes

### Building from API (NOT RECOMMENDED)

Go into the backend folder

```bash
cd src/backend
```

Execute the `build_cache.py`

```bash
python3 build_cache.py
```

This will probably fail. You can cancel it if it keeps hanging

Run the `main.py` file to build the database from cache

```bash
python3 main.py
```

## Running Tests

To run tests, run the following commands

```bash
  cd src/backend
  python3 -m unittest discover -v -s . -p "*test*.py
```
