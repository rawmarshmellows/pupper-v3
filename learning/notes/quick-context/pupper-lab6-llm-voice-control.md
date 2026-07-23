---
topic: Pupper Lab 6 — LLM Voice Control (Karel + OpenAI Realtime API)
created: 2026-03-10
---

# Pupper Lab 6 — LLM Voice Control (Karel + OpenAI Realtime API)

> **Related:** [[quick-context/pupper-v3-labs]] | [[quick-context/pupper-lab5-neural-controller]] | [[quick-context/pupper-lab7-vision-tracking]] | [[quick-context/ros2-architecture]]

> **TL;DR:** Students build a voice-controlled robot by wiring together two systems: a KarelPupper class that wraps ROS2 Twist commands into named actions (move_forward, dance, bob), and an OpenAI Realtime API WebSocket client that streams microphone audio to an LLM whose system prompt constrains its output to exactly those action names, closing the loop from spoken English to motor movement.

## The Core Problem

Telling a robot "go forward and then do a little dance" is trivially easy for a human to understand but involves a surprisingly deep pipeline to execute. The voice signal must be captured, streamed to a speech-understanding model, interpreted as a sequence of discrete robot commands, translated into velocity messages the locomotion controller accepts, and finally converted to joint torques by the neural policy running on the real-time control loop. Every layer operates at a different timescale: audio at 24 kHz, the LLM at hundreds of milliseconds, ROS2 topics at tens of Hz, and the motor loop at 1 kHz. Lab 6 asks students to build the top two layers of this stack and connect them to the bottom layers they already have from Labs 4-5.

The KarelPupper abstraction exists because LLMs produce text, not Twist messages. Rather than asking the LLM to output raw linear and angular velocities (which it would hallucinate constantly), students define a small vocabulary of named actions — `move_forward`, `turn_left`, `bob`, `dance` — each implemented as a method that publishes the correct Twist sequence to `/cmd_vel`. This reduces the LLM's job from "generate arbitrary floating-point velocity vectors" to "pick from a menu of action names," which is a dramatically easier task for a language model and produces reliable behavior.

The hardest part of the lab is prompt engineering. The system prompt fed to the OpenAI Realtime API must accomplish two competing goals: it must be flexible enough that the LLM understands varied natural-language requests ("go forward," "walk ahead," "move up"), yet constrained enough that every LLM response contains exactly one parseable action keyword. Students discover that vague prompts produce verbose, unparseable responses, while overly rigid prompts make the robot feel unresponsive to natural speech. Finding the balance is the core design challenge.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **KarelPupper** | Python class in `karel.py` that wraps ROS2 Twist publishing into named methods (`move_forward()`, `bob()`, `dance()`), giving the LLM a discrete action vocabulary instead of continuous velocity space |
| **Realtime API** | OpenAI's WebSocket-based voice interface that accepts streaming PCM16 audio and returns text/audio responses with server-side VAD — replaces the traditional Whisper + GPT + TTS three-step pipeline with a single persistent connection |
| **VAD (Voice Activity Detection)** | Server-side algorithm that detects when the user has stopped speaking, triggering the LLM to generate a response — eliminates the need for push-to-talk or client-side silence detection |
| **Twist message** | ROS2 `geometry_msgs/msg/Twist` containing `linear.x/y/z` and `angular.x/y/z` velocities — the universal interface between high-level commands and the locomotion controller on `/cmd_vel` |
| **System prompt** | The instruction text sent to the Realtime API that constrains the LLM's output format to parseable action commands — the critical bridge between natural language understanding and structured robot control |

<details>
<summary><strong>How It Works</strong> — Voice command pipeline</summary>

The full pipeline from spoken word to motor movement passes through seven stages, each at a different abstraction level:

```
VOICE-TO-ACTION PIPELINE
================================================================

  ┌─────────┐    ┌──────────┐    ┌──────────────┐
  │   Mic   │───>│  PCM16   │───>│  WebSocket   │
  │ capture │    │  24 kHz  │    │  (base64)    │
  └─────────┘    │  encode  │    │  to OpenAI   │
                 └──────────┘    └──────┬───────┘
                                        │
                              ┌─────────▼─────────┐
                              │   OpenAI Server    │
                              │  ┌──────────────┐  │
                              │  │  VAD: detect  │  │
                              │  │  speech end   │  │
                              │  └──────┬───────┘  │
                              │  ┌──────▼───────┐  │
                              │  │  LLM: parse   │  │
                              │  │  intent, emit │  │
                              │  │  action word  │  │
                              │  └──────┬───────┘  │
                              └─────────┼─────────┘
                                        │
                 ┌──────────┐    ┌──────▼───────┐
                 │  Karel   │<───│  Command     │
                 │  action  │    │  parser      │
                 │  method  │    │  (string     │
                 │          │    │   matching)  │
                 └────┬─────┘    └──────────────┘
                      │
               ┌──────▼───────┐    ┌────────────────┐
               │  ROS2 Twist  │───>│  Neural policy  │
               │  on /cmd_vel │    │  (Lab 5) or     │
               │              │    │  gait controller│
               └──────────────┘    └───────┬────────┘
                                           │
                                    ┌──────▼───────┐
                                    │  12 joint    │
                                    │  targets →   │
                                    │  CAN → motors│
                                    └──────────────┘
```

### Stage-by-stage breakdown

1. **Audio capture**: The microphone captures raw audio, which is encoded as 24 kHz, 16-bit PCM (PCM16) — the format the Realtime API expects. Each audio chunk is base64-encoded for transmission.

2. **WebSocket streaming**: Audio chunks are sent continuously over a persistent WebSocket connection to `wss://api.openai.com/v1/realtime`. Unlike the traditional REST API, this connection stays open for the entire session, eliminating per-request overhead.

3. **Server-side VAD**: OpenAI's server detects when the user has finished speaking (a pause in the audio stream). This triggers response generation without requiring explicit "I'm done talking" signals from the client.

4. **LLM response generation**: The model processes the transcribed speech against the system prompt, which instructs it to respond with exactly one action keyword (e.g., `move_forward`, `dance`). The response arrives as a `response.done` event on the WebSocket.

5. **Command parsing**: The client-side parser in `realtime_voice.py` extracts the action keyword from the LLM's text response using string matching. The parsed command is published to `/gpt4_response_topic` for logging and dispatched to the corresponding Karel method.

6. **Karel execution**: The matched method (e.g., `move_forward()`) publishes a Twist message to `/cmd_vel` with the appropriate linear and angular velocities, held for a duration (typically 1-2 seconds per movement step).

7. **Motor execution**: The neural controller (from Lab 5) or the classical gait controller (from Lab 4) reads `/cmd_vel` and converts the velocity command into 12 joint position targets at ~50 Hz, which are sent to the servos via [[quick-context/can-bus|CAN bus]].

### Audio muting for echo prevention

A critical implementation detail: the robot has a speaker for audio playback (the LLM can respond with voice). Without muting, the speaker output feeds back into the microphone, creating an echo loop where the LLM hears itself, responds to its own response, and spirals. The solution is auto-muting: when the system detects that audio playback is active (a `response.audio.delta` event is being received), the microphone input stream is suppressed until playback completes.

</details>

<details>
<summary><strong>The Key Tension</strong> — Natural language vs. structured commands</summary>

Lab 6 exposes a fundamental mismatch at the heart of LLM-controlled robotics: natural language is fluid, ambiguous, and context-dependent, while robot APIs demand precise, unambiguous, structured inputs.

**The problem in concrete terms:** A user might say "go forward," "walk ahead," "move up," "advance," or "head that way" — all meaning the same thing. The LLM understands all of these. But the command parser only recognizes `move_forward`. If the LLM responds with "Sure, I'll walk ahead now!" instead of "move_forward," the robot does nothing.

**The system prompt as a bridge:** Students must write a system prompt that threads the needle:

```
Too loose:
  "You control a robot. Output commands to move it."
  → LLM says: "Of course! I'd be happy to move forward for you."
  → Parser: ??? (no match, robot freezes)

Too rigid:
  "Output ONLY one of: move_forward, move_backward, turn_left, turn_right"
  → LLM says: "move_forward"
  → Works! But now the robot feels robotic — no personality,
    no acknowledgment, no conversational flow

The sweet spot:
  "You are a friendly robot dog. When asked to do something,
   respond conversationally BUT always include exactly one action
   keyword on its own line: move_forward | move_backward |
   turn_left | turn_right | bob | dance"
  → LLM says: "Ooh, I love dancing! Let me show you my moves!
    dance"
  → Parser finds "dance" on its own line → robot dances
```

This tension is not unique to this lab — it is the central unsolved problem in LLM-to-API systems everywhere. The industry is converging on two solutions: (1) structured output / function calling, where the LLM emits JSON or calls predefined functions rather than free text, and (2) constrained decoding, where the model's token probabilities are masked to only allow valid outputs. Both approaches sacrifice some natural-language flexibility for reliability. Students discover this tradeoff firsthand.

**Why not just use function calling?** The OpenAI Realtime API does support function calling, and Lab 7 uses it. Lab 6 intentionally uses text-based command parsing so students experience the prompt engineering challenge directly. Understanding why structured output exists requires first struggling with unstructured output.

</details>

<details>
<summary><strong>Concrete Example</strong> — "Dance for me" end to end</summary>

Here is the complete trace of what happens when a student says "Dance for me" to the Pupper running the Lab 6 system:

**T=0ms — Audio capture**
The [[quick-context/usb-peripheral-hardware|USB]] microphone captures the phrase at 24 kHz, 16-bit PCM. "Dance for me" is roughly 600ms of audio = ~28,800 samples = ~57,600 bytes of raw PCM16 data.

**T=0-600ms — Streaming to OpenAI**
Audio chunks are base64-encoded and sent as `input_audio_buffer.append` events over the WebSocket. The chunks stream in real time — there is no "record then send" step.

**T=600-900ms — VAD triggers**
OpenAI's server-side VAD detects ~300ms of silence after "me" and determines the user has finished speaking. It emits a `input_audio_buffer.speech_stopped` event and begins processing.

**T=900-1400ms — LLM generates response**
The model sees the transcribed "Dance for me" and the system prompt, which includes something like:

```
You are a playful robot dog named Pupper. When the user asks you
to do something, respond briefly and include one action keyword
on its own line. Available actions:
move_forward, move_backward, move_left, move_right,
turn_left, turn_right, bob, dance
```

The LLM generates: "Time to bust a move!\ndance"

**T=1400ms — Command parsing**
The `response.done` WebSocket event arrives. The parser in `realtime_voice.py` scans the response text line by line, finds "dance" matching a known action keyword, and calls `karel.dance()`.

**T=1400-8000ms — Karel dance() execution**
The `dance()` method is a choreographed sequence of Karel primitives. A typical implementation:

```python
def dance(self):
    self.turn_left()    # spin left  — publishes Twist(angular.z=+1.0) for 1s
    self.turn_right()   # spin right — publishes Twist(angular.z=-1.0) for 1s
    self.bob()          # bob up/down with sound
    self.move_left()    # strafe left  — publishes Twist(linear.y=+0.5) for 1s
    self.move_right()   # strafe right — publishes Twist(linear.y=-0.5) for 1s
    self.bob()          # finish with another bob
```

Each method call publishes a Twist to `/cmd_vel` and sleeps for the movement duration before the next step.

**T=1400-8000ms (in parallel) — Neural controller executes**
While `dance()` sequences through its moves, the Lab 5 neural policy continuously reads `/cmd_vel` at ~50 Hz. For each Twist command, it generates 12 joint position targets that make the robot physically spin, strafe, and bob. The CAN bus carries these targets to the servo motors at 1 kHz.

**T=1400-2000ms (in parallel) — Audio playback**
The Realtime API also returns an audio version of "Time to bust a move!" as `response.audio.delta` events. The client decodes these and plays them through the speaker. During playback, the microphone input is muted to prevent echo.

**Net result:** ~1.4 seconds from the end of speech to the robot starting to dance, with the LLM's voice response playing simultaneously. The user perceives near-instant responsiveness.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/pupper-v3-labs]]** — The full 7-lab progression. Lab 6 sits between the neural controller (Lab 5) and vision tracking (Lab 7), adding the voice-to-command layer.
- **[[quick-context/pupper-brain]]** — The hardware architecture underneath: the Raspberry Pi runs the Python voice client and Karel class, while the [[micro-context/stm32-microcontroller|STM32]] microcontrollers handle the real-time motor loop.
- **WebSocket protocol** — Lab 6 uses a persistent WebSocket (`wss://`) rather than REST API calls. WebSockets provide full-duplex communication: audio streams up while responses stream down simultaneously, which is essential for real-time voice interaction. REST would require "record, send, wait, receive" — far too slow for conversational feel.
- **PCM16 audio format** — Pulse-Code Modulation at 16-bit depth. Each sample is a signed 16-bit integer (-32768 to +32767) representing the instantaneous amplitude. At 24 kHz, this produces 48,000 bytes/second of raw audio. No compression (unlike MP3/Opus), which means low latency but high bandwidth.
- **Echo cancellation** — In production voice systems, acoustic echo cancellation (AEC) algorithms subtract the known speaker output from the microphone input in real time. Lab 6 uses a simpler approach (mute during playback) because full AEC requires DSP expertise beyond the lab's scope. The tradeoff: the robot cannot hear new commands while it is speaking.
- **OpenAI function calling** — A more robust alternative to text-based command parsing where the LLM emits structured JSON matching a predefined schema. Lab 7 upgrades to this approach. Function calling eliminates the parsing ambiguity problem but removes the instructive struggle of prompt engineering.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does the KarelPupper class exist as an abstraction layer rather than having the LLM directly output Twist messages with specific linear and angular velocity values?

<details>
<summary>Answer</summary>

Three reasons: (1) **LLMs are unreliable with numbers.** Asking a language model to output `Twist(linear.x=0.5, angular.z=0.0)` would frequently produce hallucinated values — wrong magnitudes, swapped axes, or invalid formats. Named actions reduce the output space from infinite continuous values to a handful of discrete keywords. (2) **Temporal sequencing.** A Twist message is instantaneous, but actions like `bob()` and `dance()` require timed sequences of multiple Twist messages with sleeps in between. The LLM cannot manage real-time timing. (3) **Safety.** Karel methods can enforce velocity limits and duration caps, preventing the LLM from accidentally commanding dangerous speeds.
</details>

**Q2:** The Realtime API uses server-side VAD rather than client-side silence detection. What advantage does this provide, and what is the tradeoff?

<details>
<summary>Answer</summary>

**Advantage:** Server-side VAD is tuned by OpenAI and can use the LLM's language understanding to better detect utterance boundaries — it knows when a sentence is semantically complete, not just when audio amplitude drops. It also reduces client-side complexity (no need to implement and tune silence thresholds). **Tradeoff:** The server controls when to trigger a response, and the client cannot override this timing. If the VAD triggers too early (mid-sentence), the LLM responds to an incomplete command. If it triggers too late, the user perceives lag. Client-side VAD gives developers fine-grained control over these thresholds at the cost of more implementation work.
</details>

**Q3:** During audio playback, the system mutes the microphone to prevent echo loops. Why would an echo loop occur, and why is it particularly problematic with an LLM in the pipeline?

<details>
<summary>Answer</summary>

The speaker plays the LLM's audio response. The microphone picks up this audio. The system streams it to OpenAI as if it were new user speech. The LLM processes its own words as a new command and generates another response, which plays through the speaker, which gets picked up again — an infinite feedback loop. This is worse than a traditional audio echo because the LLM actively interprets and responds to the echoed content, potentially triggering robot actions nobody requested. Each loop iteration also incurs API costs. The simple mute approach works but means the robot is temporarily deaf while speaking — a limitation that production systems solve with proper acoustic echo cancellation (AEC) algorithms.
</details>

</details>
