# SVD Visual Audit Manifest

## Teaching Overview: Singular Value Decomposition (SVD)
**Presenter:** Luis Serrano
**Core Theme:** Geometric transformation (Rotation -> Stretching -> Rotation) and Low-rank approximation.
**Analogy:** The "Puzzle" of transforming a circle into a tilted ellipse.

---

## Frame-by-Frame Audit

| Frame | Visual Description | Mathematical Notations | Teaching Point |
|:---|:---|:---|:---|
| 0001 | Title Slide: "Singular Value Decomposition" by Luis Serrano. | None | Introduction. |
| 0002 | Overview: Heart shape reconstructed from SVD components; code snippet shown. | Python/NumPy code | Practical application in imaging/compression. |
| 0003 | Book Promotion: "Grokking Machine Learning". | None | Source material reference. |
| 0004 | Transformation: Dachshund silhouette stretched horizontally. | "Stretch (or compress) horizontally" | Definition of linear transformation. |
| 0005 | Transition: "A puzzle" on black. | None | Introducing the core analogy. |
| 0006 | Puzzle (Easy): Grey circle -> Tilted ellipse. | "Puzzle (easy)" | Identifying a transformation from start to finish. |
| 0007 | Puzzle (Easy): Horizontal ellipse -> Tilted ellipse. | "Puzzle (easy)" | Transformation between different shapes. |
| 0008 | Puzzle (Hard): Circle split into Blue (Top) and Red (Bottom). | "Puzzle (hard)" | Adding "orientation" data to the transformation. |
| 0009 | Puzzle (Hard): Tilted bi-color ellipse. | None | Visualizing rotation and stretching simultaneously. |
| 0010 | Solution: Original split circle and final ellipse side-by-side. | "Solution" | The "Puzzle" is solved by breaking it down. |
| 0011-0012 | Solution: Rotating the ellipse to align with axes. | None | Decomposition step: Inverse rotation. |
| 0013 | Transition: Matrix introduction. | $A = \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix}$ | Connecting geometry to algebra. |
| 0014 | Mapping: Highlighting rows/columns and the transformation rule. | $(p, q) \to (3p+0q, 4p+5q)$ | Understanding matrix-vector multiplication. |
| 0015 | Point Mapping: Point (1,0) in blue mapped to (3,4). | $(1,0) \to (3,4)$ | Visualizing specific vector transformations. |
| 0016 | Multi-point Mapping: Red point (0,1) -> (0,5); Green point (-1,0) -> (-3,-4). | Multiple $(p,q)$ pairs | Showing how a basis transforms. |
| 0017 | Circle Mapping: A ring of colored points maps to an elliptical ring. | None | Mapping the unit circle to an ellipse. |
| 0018 | Rotation Matrix: Overlapping Dachshund with rotation formula. | $\begin{bmatrix} \cos(\theta) & -\sin(\theta) \\ \sin(\theta) & \cos(\theta) \end{bmatrix}$ | Defining the $V^T$ and $U$ components. |
| 0019 | Stretching Matrix: Unit circle with blue axis arrows $\sigma_1, \sigma_2$. | $\begin{bmatrix} \sigma_1 & 0 \\ 0 & \sigma_2 \end{bmatrix}$ | Defining the $\Sigma$ component. |
| 0020 | Stretching: Ellipse formed by $\sigma_1 \approx 5, \sigma_2 \approx 2$. | $\sigma_1, \sigma_2$ labels | Singular values as axis lengths. |
| 0021-0022 | Rotation/Stretch combined: Ellipse with R, G, B, O points. | None | The composite effect of $A$. |
| 0023 | SVD Formula: $A$ as product of three matrices. | $[A] = [\text{rot } \theta][\text{stretch } \sigma_1, \sigma_2][\text{rot } \phi]$ | Conceptual SVD. |
| 0024-0026 | SVD Formula: Standard notation. | $A = U \Sigma V^T$ | Mathematical definition. |
| 0027 | Numerical SVD: Values for $A = [3, 0; 4, 5]$. | $U, \Sigma, V^T$ with decimals | Real-world example. |
| 0028 | $V^T$ Highlight: Rotation of $-45^\circ$. | $\theta = -45^\circ$ | Understanding the first rotation. |
| 0029 | Rotation Visual: Coordinate system tilt. | "Rotation" | Geometry of $V^T$. |
| 0030 | Stretch Highlight: Vertical scaling by $\sqrt{5}$. | Vertical scaling by $\sqrt{5}$ | Geometry of $\Sigma$. |
| 0031 | $U$ Highlight: Rotation of $71.72^\circ$. | $\theta = \arctan(3) = 71.72^\circ$ | Understanding the final rotation. |
| 0032 | 4-Quadrant Map: Full transformation cycle. | $V^T, \Sigma, U$ labels | The SVD "Grand Map". |
| 0033 | 4-Quadrant Map: Adding icons (curved arrows for rot, double for stretch). | $A = U \Sigma V^T$ | Complete visual summary. |
| 0034-0036 | New Example: $A = [1.8, 1.2; 4.4, 4.6]$. | Matrix values | Demonstrating consistency across examples. |
| 0037-0038 | Sensitivity: Highlighting the small singular value (0.44). | $\sigma_2 = 0.44$ | Introduction to rank and noise. |
| 0039-0040 | Rank-1 Case: Ellipse collapses to a line. | $\sigma_2 = 0$ | Definition of rank-deficiency. |
| 0041-0043 | Transition: Rank 2 vs Rank 1 matrices. | "Rank 2", "Rank 1" | Visual difference in output space. |
| 0044 | Rank 1 Matrix: $4 \times 4$ grid of numbers. | None | Scaling the concept to higher dimensions. |
| 0045-0048 | Outer Product: Matrix split into Blue col and Green row. | Col x Row | $A$ as a single outer product. |
| 0049-0052 | Higher Rank: $4 \times 4$ matrix with '?' vectors. | "Higher rank matrices" | Building complex matrices from simple ones. |
| 0053 | Color Blocks: $U$ (Blue), $\Sigma$ (Red), $V^T$ (Green). | $A = U \Sigma V^T$ | **Primary Color Coding Scheme**. |
| 0054 | Component Expansion: $u_i, \sigma_i, v_i$ columns/rows. | $u_1 \dots u_4, \sigma_1 \dots \sigma_4, v_1 \dots v_4$ | Detailed matrix structure. |
| 0055 | Summation: $A$ as sum of $\sigma_i u_i v_i^T$. | $A = \sum \sigma_i u_i v_i^T$ | The core of low-rank approximation. |
| 0056-0059 | Weighting: Labeling $\sigma_i$ as "Large", "Medium", "Small", "Tiny". | Large, Medium, Small, Tiny | Importance of singular values. |
| 0060-0063 | Reconstruction: Progressively adding rank-1 matrices to build $A$. | Numerical grids | Summing components to reach full rank. |
| 0064-0069 | Rank Visuals: Comparing Rank 1, 2, 3, 4 structures. | "Rank of a matrix" | Dimensionality as the count of components. |
| 0070-0072 | Rectangular Matrices: SVD for $4 \times 6$ matrix. | "No square matrix? No problem!" | Generality of SVD. |
| 0073-0074 | Image Example: Heart shape binary matrix. | 0s and 1s grid | SVD in digital images. |
| 0075-0080 | Image SVD: Reconstructing heart from components. | Matrix numerical lists | Convergence to the original image. |
| 0081-0083 | Convergence: Showing error decrease as rank increases. | 4.74, 1.41, 0.73, 0.0... | Numerical proof of approximation. |
| 0084 | Movie-User Matrix: Users (Rows) vs Movies (M1-M5). | Ratings 1-5 | Recommendation systems application. |
| 0085 | PCA/Factorization: 3D point cloud projected to 2D plane. | "Principal Component Analysis" | Connection to dimensionality reduction. |
| 0086 | Outro: Book promotion. | Discount code: serranoyt | Conclusion. |
| 0087 | Final: "Thank you!" and social media links. | youtube.com/c/LuisSerrano | Call to action. |

---

## Technical Visual Specifications

### 1. Colors Used for SVD Components
*   **U (Blue):** Cyan/Sky Blue (#00AEEF style) - used for columns $u_i$.
*   **Sigma (Yellow/Red):** Note: In diagrams, $\Sigma$ blocks are often **Red** (Deep Salmon), but the user requested **Yellow**. Ratings in the Movie matrix use Yellow for middle-range values.
*   **V (Red/Green):** $V^T$ rows are primarily **Lime Green**. $V$ vectors in the "Puzzle" solution often use **Red** for contrast (Bottom half of circle).

### 2. The "Puzzle" Analogy Steps
1.  **Preparation:** Split a unit circle into two hemispheres (Blue top, Red bottom).
2.  **Rotation ($V^T$):** Tilt the circle (e.g., -45 degrees).
3.  **Scaling ($\Sigma$):** Stretch along the X and Y axes (different $\sigma$ values).
4.  **Final Rotation ($U$):** Tilt the resulting ellipse to the final orientation.

### 3. Movie-User Matrix Details
*   **Dimensions:** 4 Users x 5 Movies (M1 to M5).
*   **Heatmap Colors:** 
    *   **Blue:** High (5)
    *   **Green:** Above Average (4)
    *   **Yellow:** Average (2-3)
    *   **Red:** Low (1)

### 4. Geometric Core (Minimalist Reconstruction)
*   **Basis:** Use a $14 \times 14$ grid for all coordinate systems.
*   **Points:** Circles of radius 0.1 for R, G, B, O mapping points.
*   **Ellipses:** Pure geometric paths without fill (thin black strokes).
*   **Dachshund:** Simple black silhouette for transformation context.
