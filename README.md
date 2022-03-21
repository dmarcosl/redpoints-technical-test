## Redpoints Technical Test

This is my solution to the [technical test of Redpoints](https://confluence.rdpnts.com/display/IKB/Python+developer+technical+task).

I used two external libraries to ease the test:

- `requests`: to perform the GET requests.
- `lxml`: to parse XML and extract the data.

### How-to

In [input.json](input.json) is the input data to perform the search.

The program reads it and performs the search using a random proxy (if provided).

The HTML is parsed to XML and the repository list is iterated. For each repository is extracted the `url` and `owner`.

Then perform a request for each repository asynchronously to extract the remaining data, the language info.

After all repositories are requested, the results are gathered and writen into the `output.json` file.

### Efficiency

I didn't use redundant variables and reused as much code as possible. Also I used lightweight and powerful libraries like `requests` and `lxml`, and make the optional part asynchronous with  and `asyncio` to make it faster.