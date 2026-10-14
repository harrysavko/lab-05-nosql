
/* Step 2: Select the bookstore database */
db = db.getSiblingDB("bookstore");

// Step 3: Load authors.json
db.authors.drop();
db.authors.insertMany(
  JSON.parse(fs.readFileSync("authors.json", "utf8"))
);

// Step 4: Load books.json
db.books.drop();
db.books.insertMany(
  JSON.parse(fs.readFileSync("books.json", "utf8"))
);

// Step 5: List all authors and books
db.authors.find().forEach(printjson);
db.books.find().forEach(printjson);

// Step 6: Insert two new books
db.books.insertMany([
  {
    title: "Fahrenheit 451",
    published_year: 1953,
    author_ids: ["author_004"]
  },
  {
    title: "The Great Gatsby",
    published_year: 1925,
    author_ids: ["author_005"]
  }
]);

// Step 7: Add missing authors
db.authors.insertMany([
  {
    _id: "author_004",
    name: "Ray Bradbury",
    nationality: "American",
    bio: {
      short: "American science fiction author.",
      long: "Ray Bradbury was an American writer best known for Fahrenheit 451."
    }
  },
  {
    _id: "author_005",
    name: "F. Scott Fitzgerald",
    nationality: "American",
    bio: {
      short: "American novelist.",
      long: "F. Scott Fitzgerald was an American novelist best known for The Great Gatsby."
    }
  }
]);

// Step 8: Filter books by author IDs
db.books.find({
  author_ids: {
    $in: ["author_001", "author_004", "author_005"]
  }
}).forEach(printjson);
