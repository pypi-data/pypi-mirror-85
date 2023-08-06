# Sermos Tools

Tool Catalog for use in Sermos applications.

## Philosophy

There are countless tasks that take place in a typical 'data science enabled'
workflow and many of them are *common*. Sermos Tools are intended to provide
instant access to tooling that accomplishes those common tasks so you can move
quickly and with confidence. A Sermos Tool has been tested in production, comes
with specific python requirements and with a curated Docker environment to
ensure the tool runs in a containerized environment (without you fighting with
underlying system dependencies!).

## Building a Tool

## Tool Acceptance Criteria

## Contributing

## Testing

Testing is a critical part of the Sermos Tools ecosystem. Every tool that is
accepted into the production Tool Catalog must have appropriate tests with
reasonable test coverage and hygeine.

### Run Tests

To run the tests, ensure you've installed the `test` extras
(`pip install -e .[test]`). Sermos currently supports Python 3.7+.

Run tests for all tools:

    $ tox

To run tests for one or more select tests, provide a comma-separated list of
environment names, which match the name of the tools/{{dirname}}

    $ tox -e date_extractor,hasher
