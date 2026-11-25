# M3 Internal Assessment — Eigenvalues & Eigenvectors (Animation Video)

> **GitHub Submission Repo Name:** `M3_AnimationVideo_Eigenvectors_E25B070773`  
> **Student:** Shlok Sharma (`E25B070773`)  
> **Concept:** Eigenvalues & Eigenvectors of a 2×2 Matrix (Geometric Intuition + Algebraic Derivation)  
> **Learning Objective:** By the end of this video, the viewer can explain what an eigenvector is geometrically and compute the eigenvalues and eigenvectors of a 2×2 matrix.

---

## Repository Structure

```text
M3_AnimationVideo_Eigenvectors_E25B070773/
├── Shlok_Sharma_Video.mp4        # Final 1080p (1920x1080) 16:9 MP4 (~5:08) with Opening & Closing Frames
├── README.md                     # Concept summary, run instructions & references
└── Code/
    ├── main.py                   # 6 Scene classes (Scene1_Hook ... Scene6_Summary) + FullVideo
    └── helpers.py                # Shared colors, NumberPlane pair, labelled vectors, matrix builders
```

---

## Concept Summary & Worked Example

When a $2 \times 2$ matrix $A$ acts as a linear transformation on $\mathbb{R}^2$, most vectors are rotated off their starting direction. **Eigenvectors** ($\mathbf{v} \neq \mathbf{0}$) are the special directions that remain on their own span line, scaled only by their **eigenvalue** ($\lambda$):

$$A\mathbf{v} = \lambda\mathbf{v} \iff (A - \lambda I)\mathbf{v} = \mathbf{0}$$

For a nonzero vector $\mathbf{v}$ to exist, $A - \lambda I$ must be singular, yielding the characteristic equation $\det(A - \lambda I) = 0$.

### Worked Example Used in the Video
$$A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$$

1. **Characteristic Equation:**
   $$\det(A - \lambda I) = (2-\lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = (\lambda - 3)(\lambda - 1) = 0$$
   $$\implies \lambda_1 = 3, \quad \lambda_2 = 1$$

2. **Eigenvectors & Verification by Substitution:**
   - For $\lambda_1 = 3$: $(A - 3I)\mathbf{v}_1 = \mathbf{0} \implies -x + y = 0 \implies \mathbf{v}_1 = \begin{bmatrix}1 \\ 1\end{bmatrix}$.  
     Check: $A\begin{bmatrix}1 \\ 1\end{bmatrix} = \begin{bmatrix}3 \\ 3\end{bmatrix} = 3\begin{bmatrix}1 \\ 1\end{bmatrix}$.
   - For $\lambda_2 = 1$: $(A - I)\mathbf{v}_2 = \mathbf{0} \implies x + y = 0 \implies \mathbf{v}_2 = \begin{bmatrix}1 \\ -1\end{bmatrix}$.  
     Check: $A\begin{bmatrix}1 \\ -1\end{bmatrix} = \begin{bmatrix}1 \\ -1\end{bmatrix} = 1\begin{bmatrix}1 \\ -1\end{bmatrix}$.

---

## How to Run & Render

1. Create a Python virtual environment and install Manim Community Edition (`v0.18+`), FFmpeg, and a LaTeX distribution:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install manim
   ```
2. Render the full 1080p 16:9 video (`Shlok Sharma` / `E25B070773` are already embedded in Scene 1 & Scene 6):
3. Render the full 1080p 16:9 video:
   ```bash
   manim -qh --resolution 1920,1080 Code/main.py FullVideo
   ```
4. Or render any individual scene for quick testing:
   ```bash
   manim -pql Code/main.py Scene3_VisualIntuition
   ```

---

## References

1. Gilbert Strang, *Introduction to Linear Algebra* (5th ed.), Wellesley-Cambridge Press — Chapter 6: Eigenvalues and Eigenvectors.
2. Grant Sanderson (3Blue1Brown), *Essence of Linear Algebra*, Chapter 14: "Eigenvectors and Eigenvalues."
3. M3 Course Lecture Notes — Linear Algebra & Calculus.
4. Manim Community Developers, *Manim Community Edition Documentation (v0.18+)* — `https://docs.manim.community`.
