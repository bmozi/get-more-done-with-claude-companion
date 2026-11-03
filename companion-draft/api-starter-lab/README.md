# A first HTTP application you can inspect

Chapter 33 local teaching reference, October 18, 2026. AI-authored. Python 3.10+; standard library only. No installation, model, account, credentials, paid API, external message, or save operation is used. The server returns authored fixtures rather than interpreting language. This is a real local HTTP request/response exercise, **not a Claude API integration or Claude performance test**.

## Run it in two terminals

Start both terminals in the book repository root. Verify `python3 --version` reports 3.10 or later. In the first:

```sh
python3 companion-draft/api-starter-lab/fixture_server.py
```

Leave it running. In the second:

```sh
python3 companion-draft/api-starter-lab/app.py --endpoint http://127.0.0.1:8765/draft --case complete --note 'Replace the home air filter on 2026-10-20.'
```

Expected: `state` is `draft_for_review`, item is `home air filter`, date is `2026-10-20`, and evidence kind says `local_fixed_fixture_not_model_output`. No record is saved. The note must exactly match its authored fixture; arbitrary notes deliberately fail rather than impersonating a language model.

Try the missing-year case:

```sh
python3 companion-draft/api-starter-lab/app.py --endpoint http://127.0.0.1:8765/draft --case missing-year --note 'Replace the home air filter on October 20.'
```

Expected: draft for review with `due_date: null` and a clarification question. Then try a response with an extra action field:

```sh
python3 companion-draft/api-starter-lab/app.py --endpoint http://127.0.0.1:8765/draft --case extra-field --note 'Replace the home air filter on 2026-10-20.'
```

Expected: `rejected`, reason `expected only item, due_date, questions`, exit code 2. This is an intentionally failed case. A rejection is the expected protective behavior. There is no email tool to execute the unwanted field.

Stop the server with Control-C in the first terminal. Repeat the complete command in the second. Expected: transport failure, not a success using stale data. If port 8765 is occupied, start the server with `--port 8766` and change the client endpoint to match. Do not stop an unfamiliar process just to free a port.

## Follow the files

- `app.py`: input validation, one HTTP request, response decoding and validation, draft display.
- `fixture_server.py`: a loopback-only HTTP server that selects an authored response by case name. It is a teaching fixture server, not an Anthropic protocol emulator.
- `fixtures.json`: exact inputs, status codes and response bodies. Includes deliberately wrong outputs.
- `test_app.py`: checks the application boundaries and exposes one important limit.
- `capture_local_runs.py`: runs all ten case commands against an ephemeral loopback port and prints raw command/output evidence.

`request_draft` makes no automatic retry. The client disables proxies and redirects and rejects remote endpoints. The server is a short-lived local teaching program; do not deploy it publicly or treat it as a hardened service.

## Check the result, including the uncomfortable case

```sh
python3 -m unittest discover -s companion-draft/api-starter-lab -v
python3 companion-draft/api-starter-lab/capture_local_runs.py
```

Eleven test methods include seven rejection subcases, malformed HTTP and duplicate JSON fields. The ten captured CLI cases should accept only `complete` and `missing-year` as drafts. All eight other cases should exit 2. The timeout test injects a local exception; it does not measure a real provider outage. Local evidence is saved in `planning/reviews/adversarial-2026-10-18/api-starter-evidence/`.

The validator rejects an invented date by requiring a literal ISO date in the note. That narrow rule intentionally declines natural-language date conversion. It checks a real calendar date and a literal item span. It **does not understand the meaning of the note**. The negative sentence “Do not replace the filter on 2026-10-20” can still pass these literal checks if a proposed record includes `filter` and `2026-10-20`. A test preserves this limitation. Human review remains necessary; passing validation does not make a draft true or authorized.

## Change one condition

Predict what should happen when a correct-looking record arrives with `status: incomplete`. Run the case and explain why a valid date cannot repair unfinished processing. Then design a new fixture where the note contains two dates with different meanings. Record the intended interpretation before adding code. A date being present somewhere in a note does not show that it belongs to the action.

## The separate live integration

The local `/draft` protocol is ours. It is not the Anthropic endpoint, schema, authentication, or SDK. A live adapter must use the current official client or API, map its returned content and stop reason into the application contract, and preserve refusal, truncation, usage and errors. It must not pretend every HTTP 200 supplies an acceptable draft. Use the official quickstart for setup; record the installed SDK version and model available in the approved account. Disable or explicitly account for SDK retry behavior when recording attempts and costs.

Documentation consulted October 18, 2026:

- [Quickstart](https://platform.claude.com/docs/en/get-started): current Python client setup and message creation route.
- [Stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons): response completion is separate from HTTP success.
- [Errors](https://platform.claude.com/docs/en/api/errors): error categories, request identifiers and SDK retry behavior.

No live adapter, provider run, billed usage, host authentication, human learning trial, or production readiness is established by this package. Those are remaining integration gates. The local application closes the reproducible transport-and-validation lesson; it does not close the promise of a fully demonstrated Claude API application.
