# Section 10 – Full-Text Search

## 10.1 Full-Text Search Concepts

Full-text search enables searching through large amounts of text data efficiently.

### Full-Text Search Features:
- **Text Processing**: Normalization, stemming, stop words
- **Indexing**: GIN indexes for fast searching
- **Ranking**: Relevance scoring for search results
- **Highlighting**: Highlighting matching terms
- **Multi-language**: Support for different languages

### Real-World Analogy:
Full-text search is like a smart librarian:
- **Text Processing** = Organizing books by content
- **Indexing** = Creating a searchable catalog
- **Ranking** = Recommending most relevant books
- **Highlighting** = Marking relevant passages
- **Multi-language** = Supporting books in different languages

### SQL Example - Full-Text Search Basics:
```sql
-- Create table with text content
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    author VARCHAR(100),
    published_date DATE
);

INSERT INTO articles (title, content, author, published_date) VALUES
    ('PostgreSQL Basics', 'PostgreSQL is a powerful open-source database system with advanced features.', 'John Doe', '2024-01-15'),
    ('Advanced SQL Queries', 'Learn about window functions, CTEs, and recursive queries in PostgreSQL.', 'Alice Smith', '2024-01-16'),
    ('Database Performance', 'Optimizing database performance requires understanding indexes and query plans.', 'Bob Wilson', '2024-01-17'),
    ('PostgreSQL Extensions', 'PostgreSQL supports many extensions like PostGIS for geospatial data.', 'Carol Brown', '2024-01-18');

-- Basic full-text search
SELECT 
    title,
    content,
    author
FROM articles
WHERE to_tsvector('english', title || ' ' || content) @@ to_tsquery('english', 'PostgreSQL');

-- Search with ranking
SELECT 
    title,
    content,
    ts_rank(to_tsvector('english', title || ' ' || content), to_tsquery('english', 'PostgreSQL')) as rank
FROM articles
WHERE to_tsvector('english', title || ' ' || content) @@ to_tsquery('english', 'PostgreSQL')
ORDER BY rank DESC;
```

## 10.2 Text Search Vectors (tsvector)

tsvector represents normalized text for efficient searching.

### tsvector Features:
- **Normalization**: Converts text to normalized form
- **Stemming**: Reduces words to root forms
- **Stop Words**: Removes common words
- **Position Information**: Tracks word positions
- **Weight Classes**: Assigns weights to words

### Real-World Analogy:
tsvector is like a searchable index:
- **Normalization** = Standardizing text format
- **Stemming** = Reducing words to root forms
- **Stop Words** = Removing common words
- **Position Information** = Tracking word locations
- **Weight Classes** = Assigning importance levels

### SQL Example - tsvector Operations:
```sql
-- Create tsvector column
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- Update search vector
UPDATE articles 
SET search_vector = to_tsvector('english', title || ' ' || content);

-- Create GIN index on tsvector
CREATE INDEX idx_articles_search ON articles USING GIN (search_vector);

-- Basic tsvector operations
SELECT 
    title,
    search_vector,
    array_length(search_vector, 1) as word_count
FROM articles
WHERE search_vector @@ to_tsquery('english', 'database');

-- tsvector functions
SELECT 
    title,
    search_vector,
    tsvector_to_array(search_vector) as words,
    tsvector_length(search_vector) as length
FROM articles
ORDER BY tsvector_length(search_vector) DESC;

-- Weighted tsvector
UPDATE articles 
SET search_vector = setweight(to_tsvector('english', title), 'A') || 
                   setweight(to_tsvector('english', content), 'B');

-- Query with weights
SELECT 
    title,
    search_vector,
    ts_rank(search_vector, to_tsquery('english', 'PostgreSQL')) as rank
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL')
ORDER BY rank DESC;
```

## 10.3 Text Search Queries (tsquery)

tsquery represents search queries with operators and modifiers.

### tsquery Features:
- **Operators**: AND (&), OR (|), NOT (!)
- **Phrases**: Exact phrase matching
- **Prefix Matching**: Wildcard searches
- **Distance Operators**: Proximity searches
- **Weight Filtering**: Search by weight classes

### Real-World Analogy:
tsquery is like a search request:
- **Operators** = Combining search terms
- **Phrases** = Searching for exact phrases
- **Prefix Matching** = Searching for word beginnings
- **Distance Operators** = Finding nearby words
- **Weight Filtering** = Searching in specific sections

### SQL Example - tsquery Operations:
```sql
-- Basic tsquery operations
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL & database');

-- OR operator
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL | SQL');

-- NOT operator
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL & !performance');

-- Phrase search
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ phraseto_tsquery('english', 'database system');

-- Prefix matching
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ to_tsquery('english', 'Postgre:*');

-- Distance operators
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL <-> database');

-- Weight filtering
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL:A');

-- Complex queries
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ to_tsquery('english', '(PostgreSQL | SQL) & (database | performance)');
```

## 10.4 Full-Text Search Functions

PostgreSQL provides comprehensive functions for full-text search operations.

### Search Functions:
- **to_tsvector()**: Convert text to tsvector
- **to_tsquery()**: Convert text to tsquery
- **plainto_tsquery()**: Simple text to tsquery
- **phraseto_tsquery()**: Phrase text to tsquery
- **websearch_to_tsquery()**: Web search to tsquery

### Real-World Analogy:
Search functions are like different search tools:
- **to_tsvector()** = Text processing tool
- **to_tsquery()** = Advanced search tool
- **plainto_tsquery()** = Simple search tool
- **phraseto_tsquery()** = Phrase search tool
- **websearch_to_tsquery()** = Web search tool

### SQL Example - Full-Text Search Functions:
```sql
-- to_tsvector function
SELECT 
    title,
    to_tsvector('english', title) as title_vector,
    to_tsvector('english', content) as content_vector
FROM articles
LIMIT 3;

-- to_tsquery function
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL & database');

-- plainto_tsquery function
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ plainto_tsquery('english', 'PostgreSQL database');

-- phraseto_tsquery function
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ phraseto_tsquery('english', 'database system');

-- websearch_to_tsquery function
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ websearch_to_tsquery('english', 'PostgreSQL "database system"');

-- Function comparison
SELECT 
    'to_tsquery' as function_name,
    to_tsquery('english', 'PostgreSQL & database') as result
UNION ALL
SELECT 
    'plainto_tsquery',
    plainto_tsquery('english', 'PostgreSQL & database')
UNION ALL
SELECT 
    'phraseto_tsquery',
    phraseto_tsquery('english', 'PostgreSQL & database')
UNION ALL
SELECT 
    'websearch_to_tsquery',
    websearch_to_tsquery('english', 'PostgreSQL & database');
```

## 10.5 Text Search Configuration

Text search configuration controls how text is processed and searched.

### Configuration Components:
- **Parser**: Breaks text into tokens
- **Dictionary**: Normalizes and stems tokens
- **Stop Words**: Words to ignore
- **Synonyms**: Word mappings
- **Rules**: Processing rules

### Real-World Analogy:
Text search configuration is like a language processing system:
- **Parser** = Breaking text into words
- **Dictionary** = Understanding word meanings
- **Stop Words** = Ignoring common words
- **Synonyms** = Mapping related words
- **Rules** = Processing guidelines

### SQL Example - Text Search Configuration:
```sql
-- Check available configurations
SELECT 
    cfgname,
    cfgowner,
    cfgparser
FROM pg_ts_config
ORDER BY cfgname;

-- Check configuration details
SELECT 
    cfgname,
    cfgowner,
    cfgparser,
    prsname,
    prsstart,
    prstoken,
    prsend,
    prsheadline,
    prslextype
FROM pg_ts_config c
JOIN pg_ts_parser p ON c.cfgparser = p.oid
WHERE cfgname = 'english';

-- Check dictionaries
SELECT 
    dictname,
    dicttemplate,
    dictinitoption
FROM pg_ts_dict
ORDER BY dictname;

-- Check stop words
SELECT 
    dictname,
    dicttemplate,
    dictinitoption
FROM pg_ts_dict
WHERE dictname LIKE '%stop%';

-- Create custom configuration
CREATE TEXT SEARCH CONFIGURATION custom_config (COPY = english);

-- Add custom dictionary
CREATE TEXT SEARCH DICTIONARY custom_dict (
    TEMPLATE = simple,
    STOPWORDS = custom_stop
);

-- Use custom configuration
SELECT 
    title,
    content
FROM articles
WHERE to_tsvector('custom_config', title || ' ' || content) @@ 
      to_tsquery('custom_config', 'PostgreSQL');

-- Check configuration usage
SELECT 
    cfgname,
    cfgowner,
    cfgparser
FROM pg_ts_config
WHERE cfgname = 'custom_config';
```

## 10.6 GIN Indexes for Full-Text Search

GIN indexes provide efficient indexing for full-text search operations.

### GIN Index Features:
- **Inverted Index**: Maps terms to documents
- **Fast Lookups**: O(log n) search performance
- **Compression**: Efficient storage
- **Maintenance**: Automatic updates
- **Statistics**: Query optimization

### Real-World Analogy:
GIN indexes are like a comprehensive book index:
- **Inverted Index** = Terms pointing to pages
- **Fast Lookups** = Quick page finding
- **Compression** = Efficient storage
- **Maintenance** = Keeping index current
- **Statistics** = Usage tracking

### SQL Example - GIN Indexes:
```sql
-- Create GIN index on tsvector
CREATE INDEX idx_articles_search_gin ON articles USING GIN (search_vector);

-- Check index usage
EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL');

-- Check index statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE indexname = 'idx_articles_search_gin';

-- Check index size
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size
FROM pg_indexes
WHERE indexname = 'idx_articles_search_gin';

-- Partial GIN index
CREATE INDEX idx_articles_search_partial ON articles USING GIN (search_vector)
WHERE published_date >= '2024-01-01';

-- Check partial index usage
EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL')
AND published_date >= '2024-01-01';
```

## 10.7 Ranking and Highlighting

PostgreSQL provides functions for ranking search results and highlighting matches.

### Ranking Functions:
- **ts_rank()**: Basic ranking algorithm
- **ts_rank_cd()**: Cover density ranking
- **ts_rank_cd()**: Cover density with normalization
- **ts_rank()**: With normalization

### Highlighting Functions:
- **ts_headline()**: Highlight matching terms
- **ts_headline()**: With custom options
- **ts_headline()**: With custom configuration

### Real-World Analogy:
Ranking and highlighting are like search result presentation:
- **Ranking Functions** = Sorting results by relevance
- **Highlighting Functions** = Marking matching terms
- **Custom Options** = Customizing presentation
- **Configuration** = Language-specific settings

### SQL Example - Ranking and Highlighting:
```sql
-- Basic ranking
SELECT 
    title,
    content,
    ts_rank(search_vector, to_tsquery('english', 'PostgreSQL')) as rank
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL')
ORDER BY rank DESC;

-- Cover density ranking
SELECT 
    title,
    content,
    ts_rank_cd(search_vector, to_tsquery('english', 'PostgreSQL')) as rank
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL')
ORDER BY rank DESC;

-- Ranking with normalization
SELECT 
    title,
    content,
    ts_rank(search_vector, to_tsquery('english', 'PostgreSQL'), 1) as rank
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL')
ORDER BY rank DESC;

-- Basic highlighting
SELECT 
    title,
    ts_headline('english', content, to_tsquery('english', 'PostgreSQL')) as headline
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL');

-- Highlighting with options
SELECT 
    title,
    ts_headline('english', content, to_tsquery('english', 'PostgreSQL'), 
                'MaxWords=10, MinWords=5, StartSel=<b>, StopSel=</b>') as headline
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL');

-- Highlighting with custom configuration
SELECT 
    title,
    ts_headline('english', content, to_tsquery('english', 'PostgreSQL'),
                'MaxWords=15, MinWords=8, StartSel=<mark>, StopSel=</mark>') as headline
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL');

-- Combined ranking and highlighting
SELECT 
    title,
    ts_rank(search_vector, to_tsquery('english', 'PostgreSQL')) as rank,
    ts_headline('english', content, to_tsquery('english', 'PostgreSQL')) as headline
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL')
ORDER BY rank DESC;
```

## 10.8 Multi-language Support

PostgreSQL supports full-text search in multiple languages.

### Language Features:
- **Built-in Languages**: English, French, German, Spanish, etc.
- **Custom Languages**: User-defined language configurations
- **Language Detection**: Automatic language detection
- **Mixed Content**: Handling multiple languages
- **Localization**: Language-specific processing

### Real-World Analogy:
Multi-language support is like having multilingual librarians:
- **Built-in Languages** = Librarians who speak common languages
- **Custom Languages** = Specialized language experts
- **Language Detection** = Automatic language recognition
- **Mixed Content** = Handling multilingual documents
- **Localization** = Language-specific processing

### SQL Example - Multi-language Support:
```sql
-- Check available languages
SELECT 
    cfgname,
    cfgowner,
    cfgparser
FROM pg_ts_config
WHERE cfgname IN ('english', 'french', 'german', 'spanish')
ORDER BY cfgname;

-- Create multilingual content
CREATE TABLE multilingual_articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    language VARCHAR(10),
    search_vector tsvector
);

INSERT INTO multilingual_articles (title, content, language, search_vector) VALUES
    ('PostgreSQL Basics', 'PostgreSQL is a powerful database system', 'en', 
     to_tsvector('english', 'PostgreSQL is a powerful database system')),
    ('Les Bases de PostgreSQL', 'PostgreSQL est un système de base de données puissant', 'fr',
     to_tsvector('french', 'PostgreSQL est un système de base de données puissant')),
    ('PostgreSQL Grundlagen', 'PostgreSQL ist ein leistungsstarkes Datenbanksystem', 'de',
     to_tsvector('german', 'PostgreSQL ist ein leistungsstarkes Datenbanksystem'));

-- Search in specific language
SELECT 
    title,
    content,
    language
FROM multilingual_articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL');

-- Search in French
SELECT 
    title,
    content,
    language
FROM multilingual_articles
WHERE search_vector @@ to_tsquery('french', 'PostgreSQL');

-- Search in German
SELECT 
    title,
    content,
    language
FROM multilingual_articles
WHERE search_vector @@ to_tsquery('german', 'PostgreSQL');

-- Mixed language search
SELECT 
    title,
    content,
    language,
    ts_rank(search_vector, to_tsquery('english', 'PostgreSQL')) as rank
FROM multilingual_articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL')
   OR search_vector @@ to_tsquery('french', 'PostgreSQL')
   OR search_vector @@ to_tsquery('german', 'PostgreSQL')
ORDER BY rank DESC;

-- Language-specific highlighting
SELECT 
    title,
    content,
    language,
    ts_headline(language, content, to_tsquery(language, 'PostgreSQL')) as headline
FROM multilingual_articles
WHERE search_vector @@ to_tsquery(language, 'PostgreSQL');
```

## 10.9 Search Optimization

Optimizing full-text search involves tuning configuration and queries.

### Optimization Techniques:
- **Index Tuning**: Optimizing GIN indexes
- **Query Rewriting**: Simplifying complex queries
- **Configuration Tuning**: Adjusting language settings
- **Statistics**: Using query statistics
- **Caching**: Result caching strategies

### Real-World Analogy:
Search optimization is like tuning a search engine:
- **Index Tuning** = Optimizing the search index
- **Query Rewriting** = Simplifying search requests
- **Configuration Tuning** = Adjusting search settings
- **Statistics** = Using usage data
- **Caching** = Storing frequent results

### SQL Example - Search Optimization:
```sql
-- Check search performance
EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    title,
    content,
    ts_rank(search_vector, to_tsquery('english', 'PostgreSQL')) as rank
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL')
ORDER BY rank DESC;

-- Optimize with index hints
SET enable_seqscan = off;
EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    title,
    content
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL');

-- Reset settings
RESET enable_seqscan;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE indexname = 'idx_articles_search_gin';

-- Optimize query with statistics
SELECT 
    title,
    content,
    ts_rank(search_vector, to_tsquery('english', 'PostgreSQL')) as rank
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL')
AND published_date >= '2024-01-01'
ORDER BY rank DESC
LIMIT 10;

-- Check query statistics
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
WHERE query LIKE '%ts_rank%'
ORDER BY total_time DESC;
```

## 10.10 Advanced Search Features

PostgreSQL provides advanced features for complex search scenarios.

### Advanced Features:
- **Fuzzy Search**: Approximate string matching
- **Synonym Support**: Word relationship mapping
- **Custom Dictionaries**: User-defined word processing
- **Search Suggestions**: Query completion
- **Faceted Search**: Multi-dimensional search

### Real-World Analogy:
Advanced search features are like having a smart search assistant:
- **Fuzzy Search** = Finding similar words
- **Synonym Support** = Understanding word relationships
- **Custom Dictionaries** = Learning specialized terms
- **Search Suggestions** = Helping with queries
- **Faceted Search** = Multi-dimensional filtering

### SQL Example - Advanced Search Features:
```sql
-- Fuzzy search using similarity
CREATE EXTENSION IF NOT EXISTS pg_trgm;

SELECT 
    title,
    content,
    similarity(title, 'PostgreSQL') as sim
FROM articles
WHERE similarity(title, 'PostgreSQL') > 0.3
ORDER BY sim DESC;

-- Search suggestions
SELECT 
    title,
    content,
    similarity(title, 'PostgreSQL') as sim
FROM articles
WHERE similarity(title, 'PostgreSQL') > 0.5
ORDER BY sim DESC
LIMIT 5;

-- Faceted search
SELECT 
    author,
    COUNT(*) as article_count,
    AVG(ts_rank(search_vector, to_tsquery('english', 'PostgreSQL'))) as avg_rank
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL')
GROUP BY author
ORDER BY avg_rank DESC;

-- Custom dictionary example
CREATE TEXT SEARCH DICTIONARY custom_dict (
    TEMPLATE = simple,
    STOPWORDS = custom_stop
);

-- Search with custom dictionary
SELECT 
    title,
    content
FROM articles
WHERE to_tsvector('english', title || ' ' || content) @@ 
      to_tsquery('english', 'PostgreSQL');

-- Advanced ranking with weights
SELECT 
    title,
    content,
    ts_rank(
        setweight(to_tsvector('english', title), 'A') || 
        setweight(to_tsvector('english', content), 'B'),
        to_tsquery('english', 'PostgreSQL')
    ) as rank
FROM articles
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL')
ORDER BY rank DESC;
```