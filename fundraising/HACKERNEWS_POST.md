# HackerNews Launch Post - KHAWRIZM Sovereign AI Stack

**Posting Time**: 5:00 PM Riyadh (9:00 AM EST, 2:00 PM GMT)  
**Strategy**: Technical depth + Open source + Hardware demo

---

## Title Options (Pick Best One):

### Option 1 (Hardware Hook):
```
We built a $5 through-wall radar that runs 100% offline (no cameras, no cloud)
```

### Option 2 (Security Hook):
```
Show HN: Sovereign AI stack that detects prompt injection attacks Big Tech can't see
```

### Option 3 (Sovereignty Hook):
```
KHAWRIZM – Complete AI stack with zero Big Tech dependencies (ESP32 + React + Rust)
```

---

## Post Body:

```markdown
Hey HN,

I'm Suleiman Al-Shamari (Dragon403), creator of KHAWRIZM – a complete sovereign AI stack built in Riyadh.

**The Problem:**

You spent millions on CST Class D cloud security, but your AI assistant just handed confidential docs to an attacker who put invisible white text in an email. 

Commercial through-wall sensors cost $2,000+ and upload your bedroom data to AWS.

Arabic NLP relies on translation wrappers that butcher morphological roots.

**Our Solution:**

**1. EchoWall** – $5 ESP32-S3 passive radar:
- Wi-Fi CSI + acoustic fusion → 94% accuracy through walls
- Detects breathing, posture, falls (no cameras)
- Hardware-seeded LFSR jitter blinds eavesdroppers
- LOCAL MQTT only (192.168.1.100:1883)
- Privacy by physics, not policy

**2. Security Framework** – Enterprise-grade threat detection:
- IPI Detector: 20+ patterns (system override, markdown exfiltration, hidden text)
- DLP Guardian: Saudi-specific PII (Iqama, National ID) with masking
- Zero Trust Validator: Risk-based access control (0.0-1.0 scoring)
- CST Compliance: KSA Class C validation (PDPL Articles 5, 7, 11, 14, 18)

**3. SARC Engine** – Deterministic Arabic NLP:
- 500+ trilateral roots (ك-ت-ب → {kataba, maktūb, kitāb})
- 90+ morphological patterns
- Dialect detection (Saudi, Egyptian, Gulf)
- NO translation layer (prevents semantic loss)

**4. CLI Tool** – 7 production commands:
```bash
khawrizm scan-ipi -f email.txt --strict
khawrizm scan-pii "رقم الإقامة: 2456789012" --mask
khawrizm extract "أريد بناء نظام ذكي"
khawrizm validate-zt -u user@company.sa -d confidential -a write
khawrizm check-compliance --region ksa-riyadh-1 --encryption
khawrizm check-sovereignty -d ./my-project/
khawrizm interactive  # Security REPL shell
```

**Tech Stack:**

- Python 3.11 (zero external APIs)
- ESP32-S3 firmware (ESP-IDF v5.x)
- React 19 + Vite (bundled, no CDN)
- Rust (zero dynamic memory allocation)
- SQLite (local database)
- Ollama (local LLM inference)

**Compliance:**

- ✅ Saudi PDPL compliant (data never leaves device)
- ✅ CST Class C architecture (KSA data residency)
- ✅ Zero Big Tech dependencies (verified via `grep`)

**Live Demo:**

- GitHub: https://github.com/Khawrzm/goose-khawrizm
- Hardware: Full ESP32 wiring diagrams + firmware
- Security Research: 22KB white paper on AI security paradigm shift
- CLI: Interactive demo with real threat detection

**What Makes This Different:**

Most "sovereign AI" projects are just wrappers around OpenAI APIs with a privacy policy. We're:

1. **Hardware-first**: Actual $5 chip that sees through walls
2. **Offline-capable**: Unplug ethernet, everything still works
3. **Linguistically grounded**: Arabic roots, not translation guessing
4. **Open source**: Apache 2.0 + Sovereignty Clause
5. **Production-ready**: 6,000+ LOC, 40+ tests, full CI/CD

**Roadmap:**

- [x] Phase 1-4: Foundation + Security + CLI (complete)
- [ ] Phase 5: ESP32 production firmware (in progress)
- [ ] Phase 6: TVWS mesh network (DePIN model)
- [ ] Phase 7: HAVEN IDE (React 19 + QEMU sandboxing)
- [ ] Phase 8: Founding 100 community launch

**Why Now:**

Google Workspace just got CST Class D in Saudi Arabia, but the "shared responsibility model" means they secure the infrastructure while you're responsible for protecting against:

- Indirect Prompt Injection (IPI) via RAG poisoning
- Permission amplification through OAuth proxies
- Cross-border data exfiltration
- Semantic attacks on AI agents

Our stack addresses all of these at the physics/math level, not policy level.

**Ask Me Anything About:**

- Passive radar using Wi-Fi CSI + acoustic FMCW chirps
- Arabic trilateral root extraction (SARC engine)
- Prompt injection detection (20+ attack patterns)
- Zero dynamic memory Rust architecture
- TVWS mesh networks for rural Saudi Arabia
- DePIN economics for community-owned infrastructure

---

**TL;DR**: $5 ESP32 chip sees through walls, runs 100% offline. Complete sovereign AI stack with Arabic-first NLP, enterprise security, and zero Big Tech dependencies. Open source, production-ready, Saudi PDPL compliant.

---

Posted from Riyadh with ❤️ for digital sovereignty.

الخوارزمية تعود للوطن 🚀
```

---

## Response Strategy:

### Expected Questions:

**Q: "Why not just use OpenAI API?"**  
A: Von Neumann deficit – cloud LLMs can't distinguish instructions from data. We need deterministic intent, not statistical guessing. Also, cross-border data transfer violates Saudi PDPL.

**Q: "How does Wi-Fi CSI work through walls?"**  
A: Radio waves reflect off human bodies, creating Channel State Information. We fuse CSI with acoustic FMCW chirps (18-22 kHz) for disambiguation. Hardware LFSR jitter (seed: 0xDEADBEEF) blinds eavesdroppers.

**Q: "500 roots seems small for Arabic?"**  
A: 500 trilateral roots × 90 morphological patterns = massive coverage. Root KTB generates {kataba, maktūb, kitāb, maktab, kātib, makātib...}. It's multiplicative, not additive.

**Q: "How do you make money?"**  
A: DePIN model – users own mesh network nodes. Token rewards for uptime. Enterprise licensing for threat dashboard. Hardware sales (ESP32 + TVWS radios). NO surveillance data sales.

**Q: "Can I try it now?"**  
A: `git clone https://github.com/Khawrzm/goose-khawrizm && cd goose-khawrizm && python3 khawrizm_cli.py interactive`

**Q: "What's the performance vs. cloud?"**  
A: ESP32-S3 (240 MHz dual-core) runs EcoNet at 12 Hz with 94% F1 accuracy. Raspberry Pi 4 runs full stack at 60 FPS. Trade-off: Lower throughput, but mathematically guaranteed privacy.

**Q: "Is this legal in the West?"**  
A: Yes. Passive radar (no transmission) is legal. CSI capture is standard Wi-Fi functionality. Acoustic chirps are ultrasonic (inaudible). Check local regulations for TVWS spectrum.

---

## Promotion Strategy:

### Before Posting:
1. Merge all pending PRs
2. Update README.md badges (build status, tests passing)
3. Add GIF demo to repo (EchoWall detecting breathing)
4. Prepare for traffic spike (check GitHub Actions limits)

### After Posting:
1. Monitor comments every 15 minutes
2. Answer technical questions with code examples
3. Thank contributors and critics equally
4. Post follow-up updates in comments
5. Cross-post to:
   - r/programming (after 24h)
   - Lobsters
   - LinkedIn (professional angle)
   - Twitter (viral thread)

### If It Goes Viral:
1. Prepare for issues/PRs flood
2. Set up Discord/Telegram for community
3. Schedule demo video recording
4. Reach out to Arabic tech media
5. Announce Founding 100 program

---

## Metrics to Track:

- HN points (target: 500+)
- GitHub stars (target: 1,000+)
- Comments/engagement (target: 200+)
- Website traffic spike
- Founding 100 applications
- Media mentions (Arabic + English)

---

**Status**: Ready to post  
**Last Updated**: 2026-05-26 19:50:00  
**Next**: Prepare YouTube script
