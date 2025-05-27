# AromaWay: Scent-Based Traffic Light Guidance for the Visually Impaired

AromaWay is a wearable assistive system that enables visually impaired individuals to safely cross roads using real-time sensory feedback. The system integrates traffic light recognition with scent-based and haptic signals.

---

## 🧠 Core Concept

Smellight detects red and green lights and communicates them through two primary channels:
- **Scent**: Unique perfume capsules emit brief scents to indicate red or green light.
- **Vibration**: Gentle vibrations notify the user of state transitions and approaching traffic islands.

---

## 🧰 System Components

### Hardware (Wearable Glasses)
- **Dual Cameras**: For visual recognition and depth estimation.
- **Odor Dispensers**: Emits different scents via detachable capsules.
- **Vibrators**: Physical feedback on both sides of the glasses.
- **Wireless Receiver**: Connects to real-time C-V2X traffic data.

---

## 🧪 Software & Model

### Files Included
- `ColorBlockDetection.py`: Color block detection script for red/green light classification.
- `main.py`: Main application integrating camera input, C-V2X input, and actuator outputs.
- `report.json`: Training logs and metrics of the color classification model (YOLO-style), trained to distinguish red and green lights with image input of shape `[224, 224, 3]`.

### Model Summary
- **Input Shape**: (224, 224, 3)
- **Output**: Multiscale detection (28×28, 14×14, 7×7) with 21 channels each
- **Total Parameters**: 7,025,023
- **Validation Accuracy**: ~18.2% (room for improvement)
- **Classes**: `["red", "green"]`

---

## 🔁 Workflow

```mermaid
graph TD;
    A[Start: Camera + C-V2X Input] --> B{Is there a traffic island?}
    B -- Yes --> C[Vibrate twice]
    B -- No --> D{Is the light red?}
    D -- Yes --> E[Emit red scent]
    D -- No --> F[Emit green scent]
    E --> G[End after 3 sec]
    F --> G
    G --> H{Is the light counting down?}
    H -- Yes --> I[Vibrate once]
    H -- No --> J[Wait]
