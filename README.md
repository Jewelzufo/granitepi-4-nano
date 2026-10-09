# GranitePi-4-Nano

Run Granite 4.0 H 350M locally on a Raspberry Pi 5 using Ollama.

A small-model project for learning, local inference and edge-device experiments. It includes setup guidance, Python examples and a shell timing script. Model output can be wrong, biased or unsafe; review it before using it in decisions or executing generated code.

**Documentation updated: October 9, 2026.** This README was rewritten to correct installation paths, distinguish the new installer from the existing repository, and replace unsupported privacy and performance guarantees with testable limits.

Designed by Julian A. Gonzalez. Co-contributor: Thomas Mertens.

## Current status

> [!IMPORTANT]
> The consent-first Python installer v1.0.0 was supplied separately. At the repository revision reviewed below, `install_granitepi.py`, `test_install_granitepi.py` and `INSTALLER_GUIDE.txt` are **not committed to this repository**. Cloning alone will not provide them. Obtain those files from the maintainer before following the Python installation steps.

- Reviewed `main` tree: `ff9feebebac632de5b20a360679127d969161f7c`.
- Existing repository installer: [`setup/setup.sh`](setup/setup.sh), not a root-level `setup.sh`.
- New deployment option: a consent-first, standard-library Python installer with a read-only default and a user-owned Ollama service.
- Validation level: production-oriented, **not production-certified**. The supplied installer has reported offline test coverage; a real Raspberry Pi acceptance run is still required.
- No published benchmark is treated here as a verified result for the new installer.

## Requirements for the Python installer

| Requirement | Details |
| --- | --- |
| Hardware | Raspberry Pi 5; other boards are rejected by this installer |
| Architecture | ARM64 Linux (`aarch64` or `arm64`); not a 32-bit OS |
| OS | Raspberry Pi OS / Debian 12 (Bookworm) or newer; accepted OS IDs are `debian` and `raspbian` |
| RAM | Physical 4 GB minimum, with a warning; 8 GB recommended |
| Free storage | At least **12 GiB on the home filesystem**, including archive, extraction and model headroom |
| Cooling and power | Active cooling and a suitable Pi 5 power supply; preflight stops at 75 C or above and on detected current undervoltage/throttling |
| Python | Python 3.10+; run apply mode from a virtual environment |
| Services | An active systemd user session |
| Decompression | `zstd`; the installer offers a separate approval if it is missing |
| Network | Required for runtime/model downloads and any approved OS-package installation |

Windows, macOS, other Pi generations and general-purpose ARM devices are outside this installer's support scope. A successful resource check is not proof of sustained performance or model quality.

## Quick start: consent-first installation

### 1. Obtain and review the files

Get these separately supplied files from the maintainer:

```text
install_granitepi.py
test_install_granitepi.py
INSTALLER_GUIDE.txt
```

Keep the source and tests in the same directory. If delivered as `.txt` attachments, remove `.txt` and any delivery-added hash suffix so the Python filenames match exactly. Read the source and guide before applying changes.

You can also clone the repository for its examples and older documentation:

```bash
git clone https://github.com/Jewelzufo/granitepi-4-nano.git
cd granitepi-4-nano
```

Place the separately supplied installer files in your chosen working directory. Do not assume they arrived with the clone.

### 2. Create a virtual environment

On the Pi, from the directory containing `install_granitepi.py`:

```bash
python3 -m venv .installer-venv
```

If this fails because `python3-venv` is missing, review these system-package changes before running them manually:

```bash
sudo apt-get update
sudo apt-get install python3-venv
```

Then repeat virtual-environment creation. These commands change OS package state; they are not part of the read-only check.

### 3. Run the read-only preflight

```bash
.installer-venv/bin/python install_granitepi.py
```

The installer checks its supported platform, RAM, home-filesystem space and available hardware health signals. It downloads nothing, creates no installer files and does not change services. Creating the virtual environment in the previous step does create local files.

An unsupported host returns an error rather than simulating an installation. This preflight does not establish that every later download or service operation will succeed.

### 4. Apply, with separate approvals

Run as your normal Pi user, **not with `sudo`**:

```bash
.installer-venv/bin/python install_granitepi.py --apply --smoke-test
```

At each prompt, type the full word `yes` to approve that step. `y`, blank input or EOF stops the workflow. There is no blanket `--yes` option. Earlier approved steps may remain if you decline or a later step fails.

Optional boot and logout persistence:

```bash
.installer-venv/bin/python install_granitepi.py --apply --boot --smoke-test
```

`--boot` separately asks to enable user linger. Linger affects all enabled services for that user, not only Ollama. Without this approval, the installer enables login startup but does not enable linger itself.

### 5. Chat using the installed binary

The installer does not edit `PATH`. Use its full binary path:

```bash
unset OLLAMA_HOST
~/.local/share/granitepi/ollama-0.33.3/bin/ollama run jewelzufo/unsloth_granite-4.0-h-350m-GGUF:latest
```

`unset OLLAMA_HOST` clears a possible CLI endpoint override in the current shell. The dedicated service listens on `127.0.0.1:11434`.

For a bounded CPU setting in an interactive Ollama chat:

```text
/set parameter num_thread 2
/set parameter num_ctx 2048
```

These are starting settings, not measured optimal settings for every workload.

## What the installer changes

Each of these has its own permission prompt when applicable:

1. Create or reuse `~/.cache/granitepi-installer.lock` to prevent concurrent apply runs.
2. If needed, refresh apt package lists and install `zstd` with `sudo`. Apt may install dependencies and requests its own package confirmation.
3. Download and verify pinned Ollama ARM64 files, then create the user-local runtime, model directory and integrity receipt.
4. Write or reuse the dedicated systemd user unit, reload user systemd, enable login startup and start Ollama.
5. With `--boot`, enable linger for the current user.
6. Pull the chosen model if its exact tag is absent locally.
7. With `--smoke-test`, load the model and generate a short answer using CPU/RAM.

The installer does **not** run a remote shell installer, perform a full OS upgrade, edit swap, install into `/usr`, create system users/groups, install GPU drivers, edit shell profiles or firewall rules, clone this repository, install its Python examples, or change GitHub.

It refuses conflicting external Ollama binaries, an unmanaged port-11434 server, conflicting service files and unmanaged or modified runtime installations. Existing system Ollama is not automatically migrated or adopted.

### Locations and defaults

| Item | Value |
| --- | --- |
| Runtime | `~/.local/share/granitepi/ollama-0.33.3/` |
| Model data | `~/.local/share/granitepi/ollama-0.33.3/models/` |
| Integrity receipt | `~/.local/share/granitepi/ollama-0.33.3/INSTALL_RECEIPT.json` |
| User unit | `~/.config/systemd/user/granitepi-ollama.service` |
| Local API | `http://127.0.0.1:11434` |
| Cloud setting | `OLLAMA_NO_CLOUD=1` |
| Default context | 2,048 tokens |
| Concurrency | One parallel request and one loaded model |
| Model retention | 5 minutes |

The service uses `UMask=0077` and `NoNewPrivileges=true`. API options can override runtime defaults. The optional smoke test uses two threads, a 2,048-token context, at most 32 generated tokens and `keep_alive: 0` to unload afterward. It is not an accuracy test or a benchmark.

### Download integrity

The supplied installer pins **Ollama v0.33.3**, not an automatically changing latest release:

- [ARM64 release archive](https://github.com/ollama/ollama/releases/download/v0.33.3/ollama-linux-arm64.tar.zst)
- Archive size: **1,554,076,220 bytes**, about **1.55 GB** in decimal units.
- SHA-256:

```text
4425a112af999ae6572c1ce211fbabeaca7bab23ed5860972acdfc0cc2358420
```

The size and digest match GitHub's [release asset metadata](https://api.github.com/repos/ollama/ollama/releases/tags/v0.33.3) checked on the documentation date. The installer checks both before extraction and execution. Its extraction code rejects unsafe archive paths and entries and caps unpacked size at 8 GiB; reruns compare the installed binary/library inventory against the receipt.

A checksum is integrity evidence, not a signature or a security audit. The user-owned receipt is not a tamper-proof boundary against that same user. Check upstream security advisories before deployment. Updating the pinned runtime requires reviewing and updating the URL, size and checksum and rerunning tests; do not change a checksum merely to accept an unexplained mismatch.

## Model selection

The default is:

```text
jewelzufo/unsloth_granite-4.0-h-350m-GGUF:latest
```

This is a community-published GGUF of the Granite 4.0 H 350M model family. IBM's [upstream model card](https://huggingface.co/ibm-granite/granite-4.0-h-350m) describes an instruction-tuned model and lists 12 supported languages: English, German, Spanish, French, Japanese, Portuguese, Arabic, Czech, Italian, Korean, Dutch and Chinese. Capabilities described by a model card are not project-specific acceptance results.

Registry sizes observed on October 9, 2026:

| Registry tag | Listed model size | Status |
| --- | --- | --- |
| `latest` | 223 MB | Installer default; mutable tag |
| `Q4_K_M` | 223 MB | Explicit quantization option |
| `Q4_K_XL` | 225 MB | Listed registry option |
| `Q5_K_XL` | 253 MB | Listed registry option |
| `Q8_K_XL` | 461 MB | Listed registry option |

These are model download sizes, not peak RAM or total installation sizes. The old blanket estimate of approximately 366 MB does not describe the current default; the registry lists that size for `Base-Q8_0`, a different tag. RAM depends on context, quantization and workload. The runtime archive is a separate, much larger download.

To choose an explicit quantization during installation:

```bash
.installer-venv/bin/python install_granitepi.py --apply --model jewelzufo/unsloth_granite-4.0-h-350m-GGUF:Q4_K_M --smoke-test
```

The older [`docs/TUTORIAL.md`](docs/TUTORIAL.md) refers to `ibm/granite4:350m-h`; that is **not the model ID used by this installer**. Use the exact model you installed in CLI and API requests.

Tags, including quantization tags, may change. The installer reuses an already-present exact tag rather than refreshing it. Ollama handles blob checks during pull; this installer does not independently authenticate model authorship or certify its weights, training data, license compliance, accuracy or safety. Record the installed model digest from `/api/tags` for deployment records.

## Local API and Python usage

Applications connect to the loopback API:

```text
Application -> http://127.0.0.1:11434 -> user-owned Ollama -> local model files
```

A bounded, standard-library example is shown below. Run it with your virtual-environment Python after the service and chosen model are available. Change `model` if you selected a different tag.

```python
import json
import urllib.request

payload = {
    "model": "jewelzufo/unsloth_granite-4.0-h-350m-GGUF:latest",
    "prompt": "Explain quantization in two short sentences.",
    "stream": False,
    "keep_alive": "5m",
    "options": {"num_ctx": 2048, "num_thread": 2, "num_predict": 128},
}
request = urllib.request.Request(
    "http://127.0.0.1:11434/api/generate",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)
# Do not send this local request through environment-configured proxies.
client = urllib.request.build_opener(urllib.request.ProxyHandler({}))
with client.open(request, timeout=300) as response:
    result = json.load(response)
if result.get("done") is not True:
    raise RuntimeError("Generation did not finish")
print(result["response"])
```

Handle connection, timeout and response errors in applications. This example has been syntax-checked, not run against a real Pi or Ollama server.

### Existing repository examples

The repository contains `basic_query.py`, `chat_loop.py`, `doc_chat.py` and `sentiment_analysis.py` under [`examples/`](examples). Their tests are under `examples/tests/`. These are separate from the new installer tests.

The basic example uses the third-party `requests` package. To try it after reviewing the code, from the repository root:

```bash
python3 -m venv .examples-venv
.examples-venv/bin/python -m pip install requests
.examples-venv/bin/python examples/basic_query.py
```

Installing `requests` downloads a Python dependency into that virtual environment. Review dependencies and endpoint/model settings in each example before running it. The installer does not install these examples or their dependencies; they have not been validated here against the new runtime.

## Privacy and security boundaries

- The new service is configured for loopback-only access and disables Ollama cloud features. These are configuration choices, not a blanket guarantee that all device data stays private.
- Runtime/model downloads and approved package operations require network access. Offline inference with already-downloaded local models is intended, but must be verified on the target device after disconnecting the network.
- Loopback is **not authentication**. Other local users or programs may reach the API. Do not expose port 11434 through a LAN bind, proxy or tunnel without access control.
- Your OS, other applications, proxies, logs, backups and any integrations you add have their own data-handling behavior. Review that environment before processing sensitive material.
- No telemetry audit, penetration test or proof of zero data egress is claimed here. Do not treat the earlier README's "100% private" and "no tracking" statements as verified assurances.
- Use models only for authorized, ethical purposes. Review answers and generated code; this project does not make medical, legal or other high-stakes decisions safe.

## Service checks and troubleshooting

These commands apply to the **new user service**, not an existing system-wide `ollama.service`:

```bash
systemctl --user status granitepi-ollama.service
journalctl --user -u granitepi-ollama.service -n 100 --no-pager
```

| Problem | What to check |
| --- | --- |
| Unsupported platform | Confirm Pi 5, ARM64 and accepted Debian/Raspberry Pi OS version; do not bypass the checks |
| Insufficient disk | Free at least 12 GiB on the filesystem containing your home, not merely in the current directory |
| Hot, slow or unstable | Check active cooling, power, temperature and `vcgencmd get_throttled` if available; reduce workload/context before assuming a software fix |
| User bus unavailable | Use a normal user login with an active systemd user session; do not rerun as root |
| Existing Ollama or port conflict | Inspect the existing install/service; resolve it deliberately before retrying. The installer will not overwrite or migrate it |
| Download checksum mismatch | Stop and investigate the source, release metadata and downloaded bytes; do not bypass verification |
| Model absent or pull failed | Check the exact tag, connectivity, disk space and service logs; partial blobs may remain |
| CLI reaches the wrong endpoint | Clear `OLLAMA_HOST` in that shell and use the full installed binary path |
| Requests time out | Inspect logs and hardware health; cold loading and generation time vary. A timeout is not proof that the model is unsupported |

The new installer does not configure swap, and this README does not prescribe a swap change. Review OS-specific guidance if you decide one is needed.

## Recovery, reruns and removal

Approved steps are incremental. A later failure or declined prompt does not undo earlier changes. The runtime, service, packages or partial model data may remain. Do not assume completion unless the installer prints its final success result.

A matching receipt and identical service can be reused by rerunning apply mode. Modified/conflicting files stop the workflow. There is no automatic upgrade, migration or destructive rollback. Hard power loss can leave staging directories; inspect them before deleting anything.

To stop the service and disable its login startup:

```bash
systemctl --user disable --now granitepi-ollama.service
```

For removal, stop/disable the service first, back up model data if needed, then review and delete only the named user unit and installer-owned runtime directory. Reload user systemd after removing the unit. Do not delete another Ollama installation or unrelated models.

If you approved linger, review its effect on your other user services before disabling it with `loginctl disable-linger` for your user. Removing this installer does not automatically uninstall `zstd` or other apt dependencies.

See the separately supplied `INSTALLER_GUIDE.txt` for the full recovery and acceptance checklist.

## Testing and production acceptance

### Offline installer checks

With the separately supplied source and tests in the same directory:

```bash
.installer-venv/bin/python -m py_compile install_granitepi.py test_install_granitepi.py
.installer-venv/bin/python -W error::ResourceWarning -m unittest -v test_install_granitepi
```

The installer delivery report records **59 passing unittest tests** on Python 3.10.12/Linux in a virtual environment with network denied. Network, API and system-command boundaries were mocked. Compilation, help/version, invalid-input exit codes and generated-unit verification with an inert fixture executable were also reported as passing.

Those results belong to the supplied installer, not the older repository's test suite. They were not rerun as part of this README update. The attached installer source was checked against its reported SHA-256:

```text
239fbf7d8860194b7e0f22e8c82f060938fe2d987002a07c00187b5daf2874b2
```

**Not verified:** a real Pi/ARM64 install, real release-archive extraction, package installation, real model pull or inference, actual systemd startup/logout/reboot, peak RAM, thermals, accuracy or throughput. Offline mocks do not prove these.

### Acceptance checklist before production use

- [ ] Read-only preflight leaves installer files and service state unchanged.
- [ ] Declining each prompt prevents all later, unapproved steps.
- [ ] Full installation and bounded generation succeed on a supported spare Pi.
- [ ] Runtime/model permissions, loopback listener and cloud-disabled startup are checked on the actual device.
- [ ] Local inference works after a controlled network disconnect following downloads.
- [ ] Rerun, logout/login and optional approved boot persistence behave as intended.
- [ ] Failure cases are exercised: insufficient disk, thermal/power warnings, interrupted download/pull and existing-install conflicts.
- [ ] Model quality, RAM, latency and throughput meet the intended workload's requirements.

### Performance reporting

The earlier README's load-time, response-time, 30-50 tokens/second, temperature and RAM numbers are **not retained as established benchmarks**. No reproducible measurements for this deployment were supplied.

[`setup/benchmark.sh`](setup/benchmark.sh) is a legacy single-query wall-clock script. It also pulls the model and expects `ollama` on `PATH`, so it is neither read-only nor directly suited to this user-local installation. Do not treat its elapsed time as generation tokens/second.

For a reproducible report, record Pi/RAM, OS, cooling, power, runtime version, model tag and digest, context, thread count, prompt, output tokens and cold versus warm runs. Ollama's generate API returns `eval_count` and `eval_duration` in nanoseconds; generation throughput is `eval_count / (eval_duration / 1e9)` when duration is nonzero. Report load and total latency separately and repeat trials.

## Repository map and older documentation

```text
granitepi-4-nano/
├── README.md
├── LICENSE
├── assets/images/
│   ├── architecture-pi.jpg
│   └── granitepi4.jpg
├── setup/
│   ├── setup.sh
│   └── benchmark.sh
├── docs/
│   ├── INDEX.md
│   ├── QUICK_REFERENCE.md
│   ├── TUTORIAL.md
│   └── models.md
└── examples/
    ├── basic_query.py
    ├── chat_loop.py
    ├── doc_chat.py
    ├── sentiment_analysis.py
    └── tests/
```

The new installer files are supplied separately and are intentionally not shown as tracked files above.

The legacy `setup/setup.sh` refreshes package lists, changes swap configuration, executes an upstream remote shell installer when Ollama is absent, writes system-service overrides and pulls a model. It does not provide the new per-step consent behavior. Review it before any use; it is not the recommended route described in this README.

Older docs may retain different model IDs, disk assumptions, privacy claims and system-wide service commands. This README does not modify those files. In particular:

- The shell installer is under `setup/`, not the repository root.
- The clone command above is plain shell syntax; Markdown link syntax does not belong inside a command.
- Architecture image files are under `assets/images/`, not the repository root. The text API flow above avoids presenting an older image as the new installer's deployment layout.
- The new installer uses five-minute retention rather than the legacy 24-hour override and leaves swap unchanged.

## Contributing

Open an issue with the OS, Pi model/RAM, runtime and model versions, exact command and relevant error output. Remove secrets and private prompts/documents from logs before sharing.

For changes, include tests and explain any new system effects or permission prompts. Hardware benchmarks should include the reproducibility details listed above. Updating only this README does not add the separate installer to the repository; include its source, tests and guide in a reviewed contribution when ready.

## License and upstream resources

Repository code and documentation use [Apache License 2.0](LICENSE). IBM's upstream Granite 4.0 H 350M model card also lists Apache 2.0. Ollama and any distributed model artifacts have their own license terms; check the exact versions and artifacts you use rather than treating the repository license as blanket permission.

- [Project repository](https://github.com/Jewelzufo/granitepi-4-nano)
- [Community GGUF model and tags](https://ollama.com/jewelzufo/unsloth_granite-4.0-h-350m-GGUF)
- [IBM upstream model card](https://huggingface.co/ibm-granite/granite-4.0-h-350m)
- [Ollama v0.33.3 release](https://github.com/ollama/ollama/releases/tag/v0.33.3)
- [Ollama configuration and privacy FAQ](https://docs.ollama.com/faq)
- [Ollama generate API](https://docs.ollama.com/api/generate)
- [Repository quantization notes](docs/models.md)

External release and registry values were checked on the documentation date and can change. This README is installation guidance, not a security certification or a performance guarantee.
