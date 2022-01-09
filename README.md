# LZBooru 1.0

from the [Wiktionary definition:](https://en.wiktionary.org/wiki/booru)

> **Booru**
> 
> *noun*
> 
> (Internet) A form of imageboard where images are categorized with tags. 

A basic image aggregator backend, with basic reverse image search.

This was created using Flask RESTful, based on [this tutorial](https://ericbernier.com/flask-restful-api).

Other tutorials I followed:
[Flask SQLAlchemy database models](https://hackersandslackers.com/flask-sqlalchemy-database-models/)
[Flask API key implementation](https://github.com/ericsopa/flask-api-key/blob/master/goaway.py)
[Multiprocessing Logging](https://fanchenbao.medium.com/python3-logging-with-multiprocessing-f51f460b8778)

## Get Started

To get started, clone this repo and install the required modules in a virtual environment using `pip install -r requirements.txt`. 

Ensure the configuration is complete by replacing the placeholder values in `.env-template` and renaming it to `.env`.

To run each component, run the following commands:
- **Booru**: `flask run --no-debugger --no-reload`
- **Greg**: `python -m greg -u`
- **Parsa**: `python -m parsa -u`
- **Coco**: `python -m coco -u`

Logging will show in standard output and standard error by default. `supervisord` can be used to redirect those outputs to files.

## Overview

LZBooru is currently split into four main components: Booru, Greg, Parsa, and Coco.

### Booru

The **board** component for LZBooru, nicknamed **Booru**. This is the Flask RESTful based component that interacts with a database to add, update, delete, and query tables defined by models. The models are as follows:

- **Subreddit**
    - `name`: The name (20 char max) of the subreddit as it appears on reddit.
    - `created`: The timestamp (in seconds) of the subreddit creation date.
    - `updated`: The timestamp (in seconds) of the last submission posted on the subreddit.

- **Submission**
    - `id`: The given ID of the submission (able to be visited as `https://redd.it/<id>`)
    - `title`: The title (300 char max) of the submission as it appears on reddit.
    - `author`: The username (20 char max) of the submission author as it appears on reddit.
    - `subreddit`: The name (20 char max) or the subreddit the submission was posted in (must already exist in **Subreddit**)
    - `created`: The timestamp (in seconds) of the submission creation date.
    - `flair`: The submission flair text (64 char max), if any.
    - `nsfw`: Indicates if the submission is marked as Not Safe For Work (18+).

- **Link**
    - `id`: The given ID of the submission containing this link (must already exist in **Submission**).
    - `url`: The url representing this link.
    - `created`: The timestamp (in seconds) of the submission creation date.
    - `type`: specialized category for parsing optimization purposes (any one of `imgur`, `reddit`, `generic`, or None)
    - `last_visited`: The timestamp (in seconds) recorded when the link was last visited by a link parser if the link could not be parsed.
    - `priority`: The priority, or equivalently number of tries, set by a link parser if the link could not be parsed.

- **Image**
    - `id`: A unique integer.
    - `url`: The url representing a direct link to an image.
    - `submission_id`: The reddit submission ID associated with this image (must already exist in **Submission**).

- **Histogram**
    - `id`: The ID of the associated image (must already exist in **Image**).
    - `red`: An array of integers representing bins of a red channel histogram.
    - `green`: An array of integers representing bins of a green channel histogram.
    - `blue`: An array of integers representing bins of a blue channel histogram.

- **Dhash**
    - `id`: The ID of the associated image (must already exist in **Image**).
    - `red`: A string of bits representing a red channel difference hash.
    - `green`: A string of bits representing a green channel difference hash.
    - `blue`: A string of bits representing a blue channel difference hash.

Each model has an associated endpoint in Flask, organized by Flask-RESTful as resources. Conversion of model data to JSON responses and vice-versa is handled by Marshmallow schemas. Resources can only be accessed using a defined API key. Additionally, a resource exists to handle image similarity requests, querying both **Histogram** and **Dhash** models.

The database itself is handled using SQLAlchemy and PostgreSQL. Originally, SQLite3 was used until the implementation of image similarity, which required more features such as `ARRAY` and `BIT` types as well as SQL function creation.

### Greg

The **aggregator** component for LZBooru, nicknamed **Greg**. This component continuously aggregates submissions made to assigned subreddits through chapters. Currently, for both current posts and archived posts, the Pushshift API is used via PMAW. Each chapter executes the following procedure:

1. Obtain the registered subreddits from **Booru**.
2. Query the Pushshift API and obtain all submissions made after the `last_updated` date. If the subreddit was just initialized, obtain all submissions made after the `created` date.
3. Format the submission and link data into JSON format for **Booru** to receive.
4. Post the formatted submission and link data to the respective endpoints of **Booru**.
5. Sleep for 60 seconds, then go back to step 1.

### Parsa

The **image parser** component for LZBooru, nicknamed **Parsa**. This component continuously parses links associated with submissions in chapters, converting them into direct image links. Note that there are optimized procedures if a link is from a particular site or a link is of a particular form:

- `reddit.com/gallery` : The submission data is obtained using the reddit API via PRAW, where gallery data can be read and individual image links can be extracted.
- `imgur.com` : Single images, albums, and galleries can be read into direct image links using the Imgur API. This process is necessarily slow due to the Imgur API rate limiting.

Processed links will be deleted from the database. Parsa does not necessarily check if a link is valid, but if it cannot access a link to extract images from, it will report its failure to **Booru** using the `last_visited` and `priority` attributes of **Link**. By default, it will retry failed Links in one hour since the `last_visited` timestamp. If three failures are recorded for a Link, it will be deleted from the database.

Several processes for each `type` of Link can be run simultaneously. Each chapter executes the following procedure:

1. Obtain links of a particular `type` from **Booru**.
2. Parse links into Image JSON format and record succeeded links and failed links.
3. Post the formatted image data to the corresponding endpoint of **Booru**.
4. Delete processed links sent to the corresponding endpoint of **Booru**.
5. Put failed links sent to the corresponding endpoint of **Booru**.
6. Sleep for 60 seconds, then go back to step 1.

### Coco

The **image encoder** component for LZBooru, nicknamed **Coco**. This component continuously downloads, resizes, and encodes images through chapters. Currently, images are resized to 512 × 512 resolution and can be encoded as:

- **RGB histogram**: By default, four bin histograms are computed for each color channel using `cv2.calcHist`.
- **Difference hash**: Computed for each color channel using `imagehash.dhash`.

Each chapter executes the following procedure:

1. Obtain images that have not been encoded yet from **Booru**.
2. Attempt to download received images by visiting the link. If a valid image is downloaded, process and resize it using `PIL.Image`. Record succeeded and failed images.
3. Encode Image objects.
4. Post the encoded image data to the respective endpoints of **Booru**.
5. Delete failed images sent to the corresponding endpoint of **Booru**.
6. Sleep for 60 seconds, then go back to step 1.

## Image Similarity Methods

Currently, the following methods are implemented:

- **Absolute norm**: The histogram data is compared using the lower [absolute value norm](https://en.wikipedia.org/wiki/Norm_(mathematics)#Absolute-value_norm) of the difference as vectors.
- **Euclidean norm**: The histogram data is compared using the lower [euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance) of the difference as vectors.
- **Difference hash norm**: The difference hash data is compared by performing bitwise XOR and summing up the number of set bits.

## Limitations

Due to Flask's basic structure, I had the pleasure and pain of self-learning and coding trivial functions like API authentication. In the end, the program is more fragile than I'd like, does not handle errors very well, and might not scale very well. Incoming results from the APIs used are subject to stability issues. Some results may be missing. Several computations could be handled better but due to time issues I cannot address them right now. Multiprocessing lead to a few issues but was still able to be implemented in the end.

I do plan to try other tech stacks (Django or even Node) upon revisiting this project.

## Final Thoughts

I had hoped to make a complete stack for LZBooru by the end of my holiday, but I ran out of time, as usual. :P

This was a very fun project to take on during the month, and one I hope will lead to a more complete, concrete, and scalable solution for reddit. I was inspired by some of the courses I took in university (namely intros to software engineering and machine learning) as well as the conclusion of [RedditBooru](https://github.com/redditbooru/reddit-booru).

My goal ultimately is to construct a solution similar to, if not the same as RedditBooru. For now, the name will stay LZBooru until its scalability is deserving of an equivalent title.
