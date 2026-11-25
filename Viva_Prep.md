# Viva / Q&A Preparation — 10 Likely Evaluator Questions & Model Answers

Use this sheet to explain both the **mathematics** and the **Manim code** independently without relying on the video.

---

### 1. Why must we solve $\det(A - \lambda I) = 0$ to find eigenvalues?
**Model Answer:**  
Starting from $A\mathbf{v} = \lambda\mathbf{v}$, we rewrite $\lambda\mathbf{v}$ as $\lambda I \mathbf{v}$ so both sides are matrix-vector products, giving $(A - \lambda I)\mathbf{v} = \mathbf{0}$. By definition, an eigenvector must be nonzero ($\mathbf{v} \neq \mathbf{0}$). If $(A - \lambda I)$ were invertible, multiplying both sides by $(A - \lambda I)^{-1}$ would force $\mathbf{v} = \mathbf{0}$. Therefore, $(A - \lambda I)$ must be singular (non-invertible), which is equivalent to $\det(A - \lambda I) = 0$.

---

### 2. Why can't $\mathbf{v} = \mathbf{0}$ be an eigenvector?
**Model Answer:**  
For *every* matrix $A$ and *every* scalar $\lambda$, $A\mathbf{0} = \mathbf{0} = \lambda\mathbf{0}$. If $\mathbf{0}$ were allowed, every real or complex number would trivially be an eigenvalue, making the concept meaningless—plus the zero vector has no direction to remain invariant.

---

### 3. Why did we rewrite $\lambda\mathbf{v}$ as $\lambda I \mathbf{v}$ before factoring?
**Model Answer:**  
You cannot subtract a scalar $\lambda$ directly from a $2\times 2$ matrix $A$ ($A - \lambda$ is undefined by matrix dimensions). Multiplying by the identity matrix $I$ turns $\lambda$ into $\lambda I = \begin{bmatrix}\lambda & 0 \\ 0 & \lambda\end{bmatrix}$, which has the same $2\times 2$ dimensions as $A$ and satisfies $(\lambda I)\mathbf{v} = \lambda(I\mathbf{v}) = \lambda\mathbf{v}$.

---

### 4. What does $\lambda = 0$ mean geometrically and algebraically?
**Model Answer:**  
If $\lambda = 0$ with eigenvector $\mathbf{v} \neq \mathbf{0}$, then $A\mathbf{v} = 0\mathbf{v} = \mathbf{0}$. Geometrically, $A$ collapses the entire line spanned by $\mathbf{v}$ onto the origin, reducing the dimension of the image. Algebraically, $\mathbf{v}$ lies in the kernel (nullspace) of $A$, which immediately implies $\det(A) = 0$ ($A$ is singular/non-invertible).

---

### 5. What does a negative eigenvalue ($\lambda < 0$) mean geometrically?
**Model Answer:**  
The vector $\mathbf{v}$ still stays on the exact same line (its 1D span), so it is still an eigenvector—but it reverses orientation by $180^\circ$ (flips to the opposite direction) and scales in length by $|\lambda|$. For example, $\lambda = -2$ flips $\mathbf{v}$ and doubles its length.

---

### 6. Why did our matrix $A = \begin{bmatrix}2 & 1 \\ 1 & 2\end{bmatrix}$ produce perpendicular eigenvectors $(1,1)$ and $(1,-1)$?
**Model Answer:**  
Notice that $A^T = A$, so $A$ is a **real symmetric matrix**. By the Spectral Theorem, eigenvectors of a real symmetric matrix corresponding to distinct eigenvalues are always orthogonal. Indeed, $\mathbf{v}_1 \cdot \mathbf{v}_2 = (1)(1) + (1)(-1) = 0$.

---

### 7. Are $(1,1)$ and $(1,-1)$ the *only* eigenvectors of $A = \begin{bmatrix}2 & 1 \\ 1 & 2\end{bmatrix}$?
**Model Answer:**  
No—any nonzero scalar multiple $c\mathbf{v}$ of an eigenvector is also an eigenvector for the same eigenvalue, because $A(c\mathbf{v}) = c(A\mathbf{v}) = c(\lambda\mathbf{v}) = \lambda(c\mathbf{v})$. So the entire eigenspaces are $\text{span}\{(1,1)\} \setminus \{\mathbf{0}\}$ (the line $y=x$) and $\text{span}\{(1,-1)\} \setminus \{\mathbf{0}\}$ (the line $y=-x$). We pick $(1,1)$ and $(1,-1)$ as clean basis representatives.

---

### 8. How do $\det(A)$ and $\operatorname{tr}(A)$ serve as a quick sanity check for our eigenvalues?
**Model Answer:**  
For any $2\times 2$ matrix, the sum of the eigenvalues equals the trace ($\lambda_1 + \lambda_2 = \operatorname{tr}(A)$) and the product equals the determinant ($\lambda_1 \lambda_2 = \det(A)$). For $A = \begin{bmatrix}2 & 1 \\ 1 & 2\end{bmatrix}$: $\operatorname{tr}(A) = 2 + 2 = 4 = 3 + 1$, and $\det(A) = 2\cdot 2 - 1\cdot 1 = 3 = 3 \times 1$. Both match!

---

### 9. In your Manim code, what does `ApplyMatrix` do, and why did you pair a `ghost_plane` with an `active_plane`?
**Model Answer:**  
`ApplyMatrix(A_MATRIX, active_plane, about_point=plane_center)` applies the $2\times 2$ linear map $A$ to every point of `active_plane` relative to `plane_center`, smoothly interpolating the grid deformation over `run_time`. We separate `ghost_plane` (which stays static with upright tick numbers) from `active_plane` (which has no text numbers) so the grid lines shear and stretch cleanly without squashing or skewing the coordinate axis numbers.

---

### 10. How does your `ValueTracker` animation work in Scene 3, and why use `base_grid.copy()` inside the updater?
**Model Answer:**  
`t_tracker = ValueTracker(0.0)` stores a scalar parameter $t \in [0, 1]$. On every frame, the updater computes $M(t) = (1 - t)I + tA$ (`interpolated_matrix(t)`), resets the active plane to `base_grid.copy()`, and applies $M(t)$ around `plane_center`. Resetting from an immutable `base_grid` each frame prevents cumulative distortion and lets us animate smoothly both forward ($0 \to 1$) and backward ($1 \to 0$) while `always_redraw` recalculates the vector positions and $\Delta\theta$ readouts in real time.
