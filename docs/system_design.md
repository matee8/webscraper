# System Design

The goal is to create a robust, scalable and user-friendly web scraping
application; in a single, unified system that can handle a variety of web
sources through a simple, declarative configuration file.

## Technologies

- Scraping Framework: `scrapy`
- JavaScript rendering: `playwright` (via `scrapy-playwright` plugin)
- HTML extraction: `trafilatura`
- PDF extraction (direct): `PyMuPDF` (or something similar)
- PDF extraction (OCR): `tesseract`
- Academic Metadata: Node.JS microservice running `zotero-translation-server`

## Components

### Main entry point

A simple Python CLI which initiates the crawling. It does the following steps:

1. Reads the configuration file.
2. Iterates through the defined `tasks`.
3. Launches an instance of `ConfigurableSpider` for each task.

### Configuration file

A TOML (or something similar) file defining the list of scraping tasks. Each
task is an object with the following keys:

| Key           | Type    | Required?  | Description                         |
| ------------- | ------- | ---------- | ----------------------------------- |
| `name`        | string  | No         | A user-friendly name for the task.  |
| `mode`        | string  | Yes        | The primary extraction method.      |
| `start_urls`  | list    | Yes        | A list of URLs to crape.            |
| `javascript`  | boolean | No         | Enable `playwright`.                |
| `crawl`       | boolean | No         | Enable link-following.              |
| `handle_pdfs` | boolean | No         | Download and process linked PDFs.   |
| `domain`      | string  | If `crawl` | The domain to constrain the spider. |
| `crawl_rules` | object  | If `crawl` | `allow` and `deny` regex patterns.  |

### `ConfigurableSpider`

A single, poweful spider inheriting from `CrawlSpider`. Configurable based on
the parsed configuration file. Its responsibilities are as follows:

- Dynamically building `CrawlSpider` rules if `crawl` is set to true.
- Adding playwright metadata to requests if `javascript` is set to true.
- Dispatching the correct extraction logic (`trafilatura`, `zotero`).
- Discovering PDF links and handling them if `handle_pdfs` is set to true.

### Pipelines

- PDF extraction:

    - First attempts to extract text. This works for digitally-created PDFs.
    - If the direct method fails, a OCR process is started.

- Data validation
- Provenance: enriches each item with metadata like `crawl_timestamp`.
- Storage: writes the structured data to an output.

### Zotero microservice

A decoupled Node.JS application that exposes a few simple HTTP endpoints.
Utilizes the `zotero-translation-server` library. See more in Roland's
documentation.

## Data schema

All data procudes will conform to the following schema:

| Field              | Type      | Description                     |
| -----------------  | --------- | ------------------------------- |
| `source_url`       | string    | The exact URL.                  |
| `source_domain`    | string    | The domain.                     |
| `crawl_timestamp`  | timestamp | UTC timestamp of crawling.      |
| `extractor`        | string    | The extractor used.             |
| `language`         | string    | The language of the content.    |
| `content`          | object    | An object for the primary data. |
| `content.text`     | string    | The main extracted text.        |
| `content.metadata` | object    | Additional metadata.            |

## Policies

These rules are enforced:

- `robots.txt` compliance.
- Rate limiting will be applied to avoid overwhelming servers.
- A rotating User-Agent list will be implemented to avoid blocking.
- A mandatory ToS review is required before a site is added to the tasks.
- The system will not attempt to solve CAPTCHAs.
