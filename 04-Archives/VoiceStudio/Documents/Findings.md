# Test-clip findings: 2026-10-26

Target: `aap kaise ho, this is a test of ElevenLabs alternative.`
(Hindi first 3 words, English rest. Engine: OmniVoice on CPU, language=Auto.)

| take | spelling | voice | ASR heard (faster-whisper-small) | notes |
|---|---|---|---|---|
| 1 | romanized `aap kaise ho` | female, young adult | "At Case Ho, this is a test of 11 Labs Alternative." | English half perfect; Hindi approximated |
| 2 | romanized | male, middle-aged | "App Case Ho. This is a test of 11 Labs alternative." | best of the romanized: "App" = aap; "Case" = kaise |
| 3 | Devanagari `आप कैसे हो` | female, young adult | "Apke se ho, this is a test of 11 labs alternative." | recognisably Hindi-ish, still imperfect |
| 4 | Devanagari | male, middle-aged | "Up case a hoe, this is a test of 11 labs alternative." | roughest Hindi rendering |

## Interpretation

- **English part is clean in all 4 takes.** "11 Labs" is literally how
  "ElevenLabs" is pronounced - correct, the ASR just writes digits.
- **Hindi opening is approximate in all takes.** Caveat: faster-whisper-small
  is weak on Hindi-for-Hindi transcription, so its text is a noisy proxy.
  The ear verdict (owner) still decides; ASR is a sanity check.
- take1 vs take2 same duration, different audio (hashes 2549A917 /
  B5E6629C) - genuinely different takes.

## If the Hindi part sounds wrong, candidate fixes (in order of likely gain)

1. Pin `language=hi` in the generate call with the Devanagari text
2. Inline phoneme respelling on the romanized text
   (`[[...]]` pronunciation overrides)
3. Bigger ASR model (medium/large-turbo) for a fairer transcription verdict

Files: `output/take{1..4}_*.wav` | engine 0.5.6 cpu | raw ASR JSON in
`%TEMP%\opencode\asr_take*.json`
