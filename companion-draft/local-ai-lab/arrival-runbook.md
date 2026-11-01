# Machine-arrival runbook: from a plan to observed local AI

Before starting, verify the actual machine, memory, storage, operating system and selected runtime against its current official requirements. This is a proposed local-model trial procedure, not a measured performance result. Do not assume a machine configuration, purchase price or delivered device from a planning example.

The first useful outcome is small: use a locally loaded model to classify fictional maintenance notes, preserve unknown dates and negation, and save evidence that another person can inspect. Passing this task does not establish a general-purpose autonomous assistant.

## 1. Check what arrived

Compare the invoice/configuration with System Settings > General > About and Storage. Record chip, unified memory, SSD capacity, available storage and macOS version. Exclude serial numbers, account names and order identifiers from published evidence. Run `python3 companion-draft/local-ai-lab/preflight.py --out arrival-preflight.json` from the repository root if Python3 is installed. It reads selected hardware/software information and writes a new report; it does not install software, download models or change settings. If Python is absent, record that dependency and use Apple's UI for the inventory first.

A1TB SSD is persistent storage;256GB unified memory is working space shared by the system. Neither number is the space available solely to the model. Inspect free storage and leave an explicit reserve for the OS, applications, evidence and backups before downloading.

Record a storage budget with columns: artifact, planned bytes, observed bytes, location, reason to keep, removal rule. Allow for multiple quantizations, download caches, temporary conversions and backups. An external SSD is an option to test for the model library; do not assume its speed or continuous availability. No particular SSD purchase is required by this runbook.

**Gate:** hardware matches the intended order, storage reserve is chosen, and current observations are saved. A discrepancy goes back to the purchase record before performance testing.

## 2. Select one runtime and one modest model

Start with one supported runtime. The first proposed track uses native macOS Ollama from its [official download page](https://ollama.com/download/mac). MLX-LM is an optional later comparison via its [maintainer repository](https://github.com/ml-explore/mlx-lm). Do not install several overlapping servers to make the first task work. Record the download URL, installer version and macOS verification outcome. A signature or scan is one check, not proof of every model or plugin's safety.

Use `model-intake-template.json` before the model download. Prefer a repository reached from the model developer's official release or organization page. A community conversion needs an additional trail back to that release, its conversion description, format and license. Read the complete relevant license terms; a commercial deployment or redistribution may have different conditions. No model is preapproved merely because its name contains a familiar company or appears on Hugging Face.

Choose a small instruction-following candidate compatible with the selected runtime. Record the exact repository, revision or observed digest, format, quantization, download size and runtime requirement. Read the model card and any warnings. Begin without model-supplied custom executable code; do not enable remote-code execution simply to bypass an error. The [Hugging Face model-card guide](https://huggingface.co/docs/hub/model-cards), [file download guide](https://huggingface.co/docs/huggingface_hub/guides/download), and [security documentation](https://huggingface.co/docs/hub/security) explain available metadata and controls.

For the Ollama-library route, open the exact model's library page and copy its supported model identifier into your source receipt. After completing the intake, download it with the following command, replacing the placeholder rather than running it literally:

```sh
ollama pull 'REPLACE_WITH_REVIEWED_LIBRARY_MODEL_AND_TAG'
ollama list
```

This step uses the network and may transfer many gigabytes. Check the expected size before starting, save the actual command and download outcome, and record the resulting digest via `/api/tags` in the next stage. A tag can change over time; the recorded digest identifies the observed artifact. Do not run a `:cloud` candidate for this local track. For a Hugging Face/MLX candidate, follow the exact revision-based download procedure from its current official runtime documentation and record all files; do not assume Ollama's pull syntax accepts every Hub repository or format.

**Gate:** the source and license are understood, the chosen file fits the storage plan, and compatibility is documented. A hash records identity or detects a mismatch against a separately trusted value; it does not prove the publisher or model is benign. Keep an unresolved intake unresolved rather than guessing.

## 3. Separate downloads from the local test

Downloading the runtime and model requires network access. Once the candidate is present, test inference separately. For an Ollama command-line instance, first stop an existing Ollama application/server using its normal controls. Do not launch a second copy or kill an unidentified listener. In a terminal, the proposed foreground service command is:

```sh
OLLAMA_NO_CLOUD=1 OLLAMA_HOST=127.0.0.1:11434 ollama serve
```

Keep this terminal visible. Confirm its startup logs report cloud disabled; the exact setting and log behavior are documented in the [Ollama FAQ](https://docs.ollama.com/faq). These variables affect this launched process, not an already-running unrelated instance. If using the GUI instead, follow the documented application configuration and restart procedure; do not assume the shell command reconfigures it.

In a second terminal:

```sh
ollama --version
ollama list
curl --noproxy '*' --fail --silent --show-error http://127.0.0.1:11434/api/tags
```

Select the exact already-downloaded local model. Record its digest. A cloud-tagged model is not the local experiment. No web search, hosted embedding service, browser tool, MCP server or cloud fallback belongs in this first test. A local URL alone cannot establish where the whole application sends data.

After downloading, an optional disconnected test can examine whether this bounded text task works without a network connection. Disconnect only when it will not interrupt other work; restore connectivity deliberately afterward. Retain the observed result. An offline success for one task does not certify every feature or constitute a complete network audit.

**Gate:** runtime version, local model identity and server configuration observed; no unresolved provider fallback. No automatic login service, network exposure or memory-limit tuning at this stage.

## 4. Submit one case and preserve what happened

Read `cases.json` and predict the first answer before running it. `answer-key.json` is for review, not a prompt attachment. Create a unique evidence folder; never overwrite a failed attempt to make the record look cleaner.

Use `make_request.py` to build the exact JSON body for an already selected local model. Replace the quoted model identifier with the value observed in `ollama list`; the example is a placeholder and is not a download recommendation:

```sh
mkdir local-ai-arrival-run-01
python3 companion-draft/local-ai-lab/make_request.py --case L1 --model 'YOUR_RECORDED_LOCAL_MODEL' --out local-ai-arrival-run-01/request.json
curl --noproxy '*' --fail-with-body --silent --show-error --max-time 180 --header 'Content-Type: application/json' --data-binary @local-ai-arrival-run-01/request.json http://127.0.0.1:11434/api/generate > local-ai-arrival-run-01/response.json 2> local-ai-arrival-run-01/transport-error.txt
```

Record the command's exit code immediately with `echo $?`. A nonzero code is a failure to investigate, not permission to silently retry. `--fail-with-body` requires curl7.76 or later; check `curl --version`. A timeout may leave the server working; inspect the visible server/logs before a retry. The180-second limit is an initial experimental cap, not a performance prediction.

The request asks for nonstreaming output, limits generated tokens and explicitly sets a modest context. The [generate API reference](https://docs.ollama.com/api/generate) documents response and timing fields. Save the full raw JSON, including output-limit termination or errors. Do not judge only the answer shown in a UI.

Inspect `done`, `done_reason` when supplied, the response text and runtime metadata. Missing or limit-truncated output is not accepted as a completed answer. Then compare meaning against the separate key. Record pass/fail per criterion, original response and any correction. Temperature0 is a reproducibility aid, not a correctness or absolute-determinism guarantee.

Run L2–L4 separately, preserving every first result. For a repeatability check, run three recorded attempts per case with the same settings, without tuning between them. This small public set is exploratory coverage, not a statistical accuracy claim or an unseen test set. If you revise the prompt using these cases, acquire new cases before making a generalization.

**Gate:** all specified semantic checks pass for the intended bounded use, or that candidate remains a failed/limited candidate. A successful load or well-formed JSON alone does not pass the task.

## 5. Increase one dimension at a time

Keep the accepted small-model baseline. Try a larger candidate or another quantization, then separately test a longer context. Change concurrency only after measuring single-request behavior. Record cold-load and warm-run time separately, peak memory observations, memory pressure/swap, response token counts where available, output correctness and human correction effort. Do not convert the chip's advertised bandwidth into a measured token rate.

Measure electricity with a suitable meter if available; otherwise leave energy unmeasured or label an estimate and its assumptions. A power-supply maximum is not observed consumption. Use the cost worksheet for both full ownership allocation and marginal cost. Running a local model may avoid a provider's per-token inference charge while still consuming equipment life, power, storage and maintenance time.

Do not begin by changing macOS wired-memory limits. If a model fails to fit, reduce its size or context and preserve the failure. Any advanced system tuning needs a current supported procedure, recovery instructions and its own isolated experiment.

**Gate:** larger or more complex configurations earn adoption by meeting the same task criteria with acceptable measured effort. “Fits” and “useful” are separate findings.

## 6. Add personal knowledge, then optional actions

Only after the fictional text task works, add a small approved document set with known answers and conflicting/outdated examples. Keep source retrieval separate from answer generation. Verify that embeddings also run in the intended place. Personalization through a profile or retrieval is different from training/fine-tuning; do not promise that uploading documents permanently teaches the weights.

Connect Merlin or another agent only after the chosen model passes that application's current tool-call checks AND its task-delivery checks. The old Merlin notes are historical leads, not current acceptance evidence. Start with isolated fictional files, no external send/purchase tools and an explicit stop rule. Verify the selected backend cannot silently fall back to a metered or hosted provider before processing private data. Serving other devices, authentication, encryption, backups, access control and restoration are a later hosting stage; keep the initial server on loopback.

**Gate:** full workflow observed, with actual permissions, state changes and failure recovery. Never infer successful work from a tool-call-shaped string.

## 7. Compare the proposed architecture with the experience

Maintain `arrival-ledger.csv`: planned step, actual observation, evidence file, deviation, corrective action and unresolved dependency. Write the case study from these records. Keep the initial design even when experience changes it. Include abandoned candidates and unsuccessful runs.

The book may then say which configuration completed which tasks under which conditions. It must not turn one workstation into proof that every reader needs that hardware or that a local model replaces Claude universally. Present the affordable entry path alongside the larger workstation case.
