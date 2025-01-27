# UAS-SAR
Unmanned Aerial System - Search and Rescue
# UAS Search and Rescue Image Analysis

## Project Overview
This project enhances UAS-based search and rescue operations by leveraging advanced computer vision and path planning techniques. It processes aerial images of fire-affected areas, detecting and classifying houses based on their surroundings and computing a dynamic rescue priority. An optimized rescue route is generated using a nearest neighbor heuristic, ensuring efficient resource allocation in disaster-stricken regions.

## Key Features
- **Advanced House Detection**: Utilizes HSV-based segmentation to identify houses based on red and blue color characteristics.
- **Environmental Classification**: Differentiates between burnt (brown) and safe (green) regions using color segmentation.
- **Rescue Priority Computation**: Dynamically calculates priority scores based on house type and location.
- **Intelligent Route Planning**: Implements a nearest neighbor heuristic to determine the most efficient rescue path.
- **Graphical Visualization**: Overlays detected elements and routes on images for comprehensive analysis.

## Technical Implementation
### 1. Image Processing
- Converts UAV images to HSV format for precise color segmentation.
- Generates masks to isolate red (critical houses), blue (non-critical houses), green (safe zones), and brown (burnt regions).
- Applies Gaussian blur for noise reduction and overlays colors for clarity.

### 2. House Detection & Classification
- Extracts contours and approximates triangular shapes to detect houses.
- Computes centroid coordinates for accurate location mapping.
- Cross-references house positions with burnt and green regions.

### 3. Rescue Priority Calculation
- Assigns priority weights:
  - **Red Houses**: Priority = 1 (high-risk structures)
  - **Blue Houses**: Priority = 2 (lower-risk structures)
- Computes cumulative priority scores:
  - **Green Region Priority (Pg) = (Red Houses × 1) + (Blue Houses × 2)**
  - **Burnt Region Priority (Pb) = (Red Houses × 1) + (Blue Houses × 2)**
- Derives the **Rescue Ratio (Pr)**: `Pr = Pb / Pg` to establish urgency rankings.

### 4. Optimized Path Planning
- Uses the nearest neighbor heuristic to formulate an efficient rescue sequence.
- Draws the computed route directly on the analyzed image.
- Ensures minimal travel distance for rescue teams.

### 5. Experimental Results
- Analyzed 11 UAV images, classifying houses based on environmental risk.
- Computed rescue ratios to prioritize images for intervention.
- **Top-ranked Image (Most Urgent Rescue)**: Image 5 (Rescue Ratio = 2.25)
- **Lowest Priority Image**: Image 7 (Rescue Ratio = 0.3)

## Installation & Execution
1. **Install Dependencies**:
   ```bash
   pip install opencv-python numpy
   ```
2. **Run the Analysis Script**:
   ```bash
   python main.py
   ```
3. **View Results**:
   - Processed images with detected houses and optimized paths are displayed.
   - Ranked rescue priorities are outputted for mission planning.

## Future Enhancements
- Integrate deep learning for enhanced house detection.
- Implement real-time path optimization using reinforcement learning.
- Develop an interactive dashboard for emergency response teams.
- Enable UAV live feed analysis for on-the-fly decision-making.

## Conclusion
This project presents a sophisticated approach to UAV-based search and rescue operations, leveraging computer vision and algorithmic path optimization. By automating house detection, risk assessment, and rescue route planning, it offers a powerful tool for disaster management teams, enhancing response efficiency and life-saving capabilities.

